/**
 * @fileoverview Core logic for the pubmed_generate_chart tool.
 * Generates charts from parameterized input by creating Chart.js configurations
 * and rendering them on the server using chartjs-node-canvas.
 * @module src/mcp-server/tools/pubmedGenerateChart/logic
 */
import { ChartConfiguration } from "chart.js";
import { ChartJSNodeCanvas } from "chartjs-node-canvas";
import { z } from "zod";
import { BaseErrorCode, McpError } from "../../../types-global/errors.js";
import {
  logger,
  RequestContext,
  requestContextService,
  sanitizeInputForLogging,
} from "../../../utils/index.js";

export const PubMedGenerateChartInputSchema = z.object({
  chartType: z
    .enum([
      "bar",
      "line",
      "scatter",
      "pie",
      "doughnut",
      "bubble",
      "radar",
      "polarArea",
    ])
    .describe("Specifies the type of chart to generate."),
  title: z
    .string()
    .optional()
    .describe("The main title displayed above the chart."),
  width: z
    .number()
    .int()
    .positive()
    .optional()
    .default(800)
    .describe("The width of the chart canvas in pixels."),
  height: z
    .number()
    .int()
    .positive()
    .optional()
    .default(600)
    .describe("The height of the chart canvas in pixels."),
  dataValues: z
    .array(z.record(z.string(), z.any()))
    .min(1)
    .describe(
      "An array of data objects to plot the chart (e.g., [{ 'year': '2020', 'articles': 150 }]).",
    ),
  outputFormat: z
    .enum(["png"])
    .default("png")
    .describe("Specifies the output format for the chart."),
  xField: z
    .string()
    .describe("The field name from `dataValues` for the X-axis."),
  yField: z
    .string()
    .describe("The field name from `dataValues` for the Y-axis."),
  seriesField: z
    .string()
    .optional()
    .describe(
      "The field name for creating multiple data series on the same chart.",
    ),
  sizeField: z
    .string()
    .optional()
    .describe("For bubble charts, the field name for encoding bubble size."),
});

export type PubMedGenerateChartInput = z.infer<
  typeof PubMedGenerateChartInputSchema
>;

export type PubMedGenerateChartOutput = {
  base64Data: string;
  chartType: string;
  dataPoints: number;
};

// Helper to group data by a series field
function groupDataBySeries(
  data: Record<string, unknown>[],
  xField: string,
  yField: string,
  seriesField: string,
) {
  const series = new Map<string, { x: unknown; y: unknown }[]>();
  for (const item of data) {
    const seriesName = item[seriesField] as string;
    if (!series.has(seriesName)) {
      series.set(seriesName, []);
    }
    series.get(seriesName)!.push({ x: item[xField], y: item[yField] });
  }
  return series;
}

export async function pubmedGenerateChartLogic(
  input: PubMedGenerateChartInput,
  parentRequestContext: RequestContext,
): Promise<PubMedGenerateChartOutput> {
  const operationContext = requestContextService.createRequestContext({
    parentRequestId: parentRequestContext.requestId,
    operation: "pubmedGenerateChartLogicExecution",
    input: sanitizeInputForLogging(input),
  });

  logger.info(
    `Executing 'pubmed_generate_chart' with Chart.js. Chart type: ${input.chartType}`,
    operationContext,
  );

  const {
    width,
    height,
    chartType,
    dataValues,
    xField,
    yField,
    title,
    seriesField,
    sizeField,
  } = input;

  const chartJSNodeCanvas = new ChartJSNodeCanvas({
    width,
    height,
    chartCallback: (ChartJS) => {
      ChartJS.defaults.responsive = false;
      ChartJS.defaults.maintainAspectRatio = false;
    },
  });

  const labels = [
    ...new Set(dataValues.map((item) => item[xField])),
  ] as string[];
  let datasets: ChartConfiguration["data"]["datasets"];

  if (seriesField) {
    const groupedData = groupDataBySeries(
      dataValues,
      xField,
      yField,
      seriesField,
    );
    datasets = Array.from(groupedData.entries()).map(([seriesName, data]) => ({
      label: seriesName,
      data: labels.map((label) => {
        const point = data.find((p) => p.x === label);
        return point ? (point.y as number) : null;
      }),
    }));
  } else {
    datasets = [
      {
        label: yField,
        data: labels.map((label) => {
          const item = dataValues.find((d) => d[xField] === label);
          return item ? (item[yField] as number) : null;
        }),
      },
    ];
  }

  // For scatter and bubble charts, the data format is different
  if (chartType === "scatter" || chartType === "bubble") {
    if (seriesField) {
      const groupedData = groupDataBySeries(
        dataValues,
        xField,
        yField,
        seriesField,
      );
      datasets = Array.from(groupedData.entries()).map(
        ([seriesName, data]) => ({
          label: seriesName,
          data: data.map((point) => ({
            x: point.x as number,
            y: point.y as number,
            r:
              chartType === "bubble" && sizeField
                ? (dataValues.find((d) => d[xField] === point.x)![
                    sizeField
                  ] as number)
                : undefined,
          })),
        }),
      );
    } else {
      datasets = [
        {
          label: yField,
          data: dataValues.map((item) => ({
            x: item[xField] as number,
            y: item[yField] as number,
            r:
              chartType === "bubble" && sizeField
                ? (item[sizeField] as number)
                : undefined,
          })),
        },
      ];
    }
  }

  const configuration: ChartConfiguration = {
    type: chartType,
    data: {
      labels:
        chartType !== "scatter" && chartType !== "bubble" ? labels : undefined,
      datasets: datasets,
    },
    options: {
      plugins: {
        title: {
          display: !!title,
          text: title,
        },
      },
      scales:
        chartType === "pie" ||
        chartType === "doughnut" ||
        chartType === "polarArea"
          ? undefined
          : {
              x: {
                title: {
                  display: true,
                  text: xField,
                },
              },
              y: {
                title: {
                  display: true,
                  text: yField,
                },
              },
            },
    },
  };

  try {
    const imageBuffer = await chartJSNodeCanvas.renderToBuffer(configuration);
    const base64Data = imageBuffer.toString("base64");

    logger.notice("Successfully generated chart with Chart.js.", {
      ...operationContext,
      chartType: input.chartType,
      dataPoints: input.dataValues.length,
    });

    return {
      base64Data,
      chartType: input.chartType,
      dataPoints: input.dataValues.length,
    };
  } catch (error: unknown) {
    const err = error as Error;
    throw new McpError(
      BaseErrorCode.INTERNAL_ERROR,
      `Chart generation failed: ${err.message || "Internal server error during chart generation."}`,
      {
        ...operationContext,
        originalErrorName: err.name,
        originalErrorMessage: err.message,
      },
    );
  }
}
