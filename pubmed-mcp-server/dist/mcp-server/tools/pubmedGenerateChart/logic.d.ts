import { z } from "zod";
import { RequestContext } from "../../../utils/index.js";
export declare const PubMedGenerateChartInputSchema: z.ZodObject<{
    chartType: z.ZodEnum<["bar", "line", "scatter", "pie", "doughnut", "bubble", "radar", "polarArea"]>;
    title: z.ZodOptional<z.ZodString>;
    width: z.ZodDefault<z.ZodOptional<z.ZodNumber>>;
    height: z.ZodDefault<z.ZodOptional<z.ZodNumber>>;
    dataValues: z.ZodArray<z.ZodRecord<z.ZodString, z.ZodAny>, "many">;
    outputFormat: z.ZodDefault<z.ZodEnum<["png"]>>;
    xField: z.ZodString;
    yField: z.ZodString;
    seriesField: z.ZodOptional<z.ZodString>;
    sizeField: z.ZodOptional<z.ZodString>;
}, "strip", z.ZodTypeAny, {
    width: number;
    height: number;
    outputFormat: "png";
    chartType: "bar" | "line" | "scatter" | "pie" | "doughnut" | "bubble" | "radar" | "polarArea";
    dataValues: Record<string, any>[];
    xField: string;
    yField: string;
    title?: string | undefined;
    seriesField?: string | undefined;
    sizeField?: string | undefined;
}, {
    chartType: "bar" | "line" | "scatter" | "pie" | "doughnut" | "bubble" | "radar" | "polarArea";
    dataValues: Record<string, any>[];
    xField: string;
    yField: string;
    title?: string | undefined;
    width?: number | undefined;
    height?: number | undefined;
    outputFormat?: "png" | undefined;
    seriesField?: string | undefined;
    sizeField?: string | undefined;
}>;
export type PubMedGenerateChartInput = z.infer<typeof PubMedGenerateChartInputSchema>;
export type PubMedGenerateChartOutput = {
    base64Data: string;
    chartType: string;
    dataPoints: number;
};
export declare function pubmedGenerateChartLogic(input: PubMedGenerateChartInput, parentRequestContext: RequestContext): Promise<PubMedGenerateChartOutput>;
//# sourceMappingURL=logic.d.ts.map