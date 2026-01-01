#!/usr/bin/env node

/**
 * Carousel Slide Renderer using Puppeteer
 *
 * Usage:
 *   node render.js --input slides.json --output ./output
 *   node render.js --slide '{"type":"hook","data":{...}}' --output slide.png
 *
 * The script expects either:
 * - A JSON file with an array of slides
 * - A single slide JSON object via --slide argument
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const RENDERER_DIR = path.resolve(__dirname, '..');
const DEFAULT_OUTPUT_DIR = path.join(RENDERER_DIR, 'output');
const DEV_SERVER_PORT = 3001;
const DEV_SERVER_HOST = '127.0.0.1';
const BUILD_DIR = path.join(RENDERER_DIR, 'build');

// Start Vite dev server
function startDevServer() {
  return new Promise((resolve, reject) => {
    console.log('Starting Vite dev server...');

    const vite = spawn('npm', ['run', 'dev', '--', '--host', DEV_SERVER_HOST, '--port', DEV_SERVER_PORT.toString()], {
      cwd: RENDERER_DIR,
      stdio: ['pipe', 'pipe', 'pipe'],
      shell: true
    });

    let serverReady = false;

    vite.stdout.on('data', (data) => {
      const output = data.toString();
      if ((output.includes('Local:') || output.includes('http://')) && !serverReady) {
        serverReady = true;
        console.log('Vite dev server ready');
        resolve(vite);
      }
    });

    vite.stderr.on('data', (data) => {
      // Vite outputs to stderr sometimes
      const output = data.toString();
      if ((output.includes('Local:') || output.includes('http://')) && !serverReady) {
        serverReady = true;
        console.log('Vite dev server ready');
        resolve(vite);
      }
    });

    vite.on('error', (err) => {
      reject(new Error(`Failed to start Vite: ${err.message}`));
    });

    // Timeout after 30 seconds
    setTimeout(() => {
      if (!serverReady) {
        vite.kill();
        reject(new Error('Vite dev server startup timeout'));
      }
    }, 30000);
  });
}

function buildStaticSite() {
  return new Promise((resolve, reject) => {
    console.log('Building static renderer...');
    const build = spawn('npm', ['run', 'build'], {
      cwd: RENDERER_DIR,
      stdio: ['pipe', 'pipe', 'pipe'],
      shell: true
    });

    build.on('error', (err) => {
      reject(new Error(`Failed to run build: ${err.message}`));
    });

    build.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`Build failed with exit code ${code}`));
      }
    });
  });
}

async function resolveRenderTarget() {
  try {
    const viteProcess = await startDevServer();
    return {
      renderUrl: `http://${DEV_SERVER_HOST}:${DEV_SERVER_PORT}?mode=render`,
      viteProcess
    };
  } catch (err) {
    console.warn(`Dev server failed (${err.message}). Falling back to static build...`);
    const indexPath = path.join(BUILD_DIR, 'index.html');
    if (!fs.existsSync(indexPath)) {
      await buildStaticSite();
    }
    return {
      renderUrl: `file://${indexPath}?mode=render`,
      viteProcess: null
    };
  }
}

// Helper to wait
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Render a single slide with retry logic
async function renderSlide(page, renderUrl, slideData, outputPath, retries = 3) {
  let lastError;

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      if (attempt > 1) {
        console.log(`Retry attempt ${attempt}/${retries} for ${slideData.type} slide...`);
        await delay(1000 * attempt); // Exponential backoff
      } else {
        console.log(`Rendering ${slideData.type} slide to ${outputPath}...`);
      }

      // Set slide data in localStorage before navigating
      await page.evaluateOnNewDocument((data) => {
        localStorage.setItem('slideData', JSON.stringify(data));
      }, slideData);

      // Navigate to render mode
      await page.goto(renderUrl, {
        waitUntil: 'networkidle0',
        timeout: 30000
      });

      // Also try setting via window function
      await page.evaluate((data) => {
        if (window.setSlideData) {
          window.setSlideData(data);
        }
      }, slideData);

      // Wait for the slide to render
      await page.waitForSelector('#slide-container', { timeout: 15000 });
      await delay(800); // Extra time for React to re-render and images to load

      // Get the slide element
      const slideElement = await page.$('#slide-container');
      if (!slideElement) {
        throw new Error('Slide container not found');
      }

      // Take screenshot
      await slideElement.screenshot({
        path: outputPath,
        type: 'png'
      });

      // Verify the file was created and has content
      if (!fs.existsSync(outputPath)) {
        throw new Error(`Output file not created: ${outputPath}`);
      }

      const stats = fs.statSync(outputPath);
      if (stats.size < 1024) {
        throw new Error(`Output file too small (${stats.size} bytes)`);
      }

      console.log(`Saved: ${outputPath} (${(stats.size / 1024).toFixed(1)}KB)`);
      return; // Success!

    } catch (error) {
      lastError = error;
      console.error(`Attempt ${attempt} failed: ${error.message}`);

      if (attempt === retries) {
        throw new Error(`Failed after ${retries} attempts: ${lastError.message}`);
      }
    }
  }
}

// Main function
async function main() {
  const args = process.argv.slice(2);

  // Parse arguments
  let inputFile = null;
  let singleSlide = null;
  let outputDir = DEFAULT_OUTPUT_DIR;
  let outputFile = null;
  let width = 1080;
  let height = 1080;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--input' && args[i + 1]) {
      inputFile = args[++i];
    } else if (args[i] === '--slide' && args[i + 1]) {
      singleSlide = JSON.parse(args[++i]);
    } else if (args[i] === '--output' && args[i + 1]) {
      const out = args[++i];
      if (out.endsWith('.png')) {
        outputFile = out;
      } else {
        outputDir = out;
      }
    } else if (args[i] === '--width' && args[i + 1]) {
      width = parseInt(args[++i], 10);
    } else if (args[i] === '--height' && args[i + 1]) {
      height = parseInt(args[++i], 10);
    } else if (args[i] === '--help') {
      console.log(`
Carousel Slide Renderer

Usage:
  node render.js --input slides.json --output ./output
  node render.js --slide '{"type":"hook","data":{...}}' --output slide.png

Options:
  --input    Path to JSON file with array of slides
  --slide    Single slide JSON object
  --output   Output directory (for multiple slides) or file path (for single slide)
  --width    Output width (default 1080)
  --height   Output height (default 1080)
  --help     Show this help message

Slide Types:
  hook   - Hook/intro slide
  myth   - Myth vs Truth slide
  stat   - Statistics slide
  tips   - Tips/list slide
  cta    - Call-to-action slide
`);
      process.exit(0);
    }
  }

  // Load slides
  let slides = [];
  if (singleSlide) {
    slides = [singleSlide];
  } else if (inputFile) {
    const content = fs.readFileSync(inputFile, 'utf-8');
    slides = JSON.parse(content);
    if (!Array.isArray(slides)) {
      slides = [slides];
    }
  } else {
    console.error('Error: Please provide --input or --slide argument');
    process.exit(1);
  }

  // Create output directory
  if (!outputFile) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Start dev server
  const { renderUrl, viteProcess } = await resolveRenderTarget();

  // Launch browser
  const userDataDir = path.join(RENDERER_DIR, '.puppeteer-profile');
  fs.mkdirSync(userDataDir, { recursive: true });

  const browser = await puppeteer.launch({
    headless: 'new',
    userDataDir,
    ignoreDefaultArgs: ['--enable-crashpad'],
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-crashpad',
      '--disable-breakpad',
      `--user-data-dir=${userDataDir}`
    ],
    env: {
      ...process.env,
      HOME: userDataDir,
      XDG_CACHE_HOME: userDataDir,
      XDG_CONFIG_HOME: userDataDir,
      XDG_DATA_HOME: userDataDir
    }
  });

  try {
    const page = await browser.newPage();

    // Set viewport to match slide dimensions
    await page.setViewport({
      width,
      height,
      deviceScaleFactor: 2 // Retina quality
    });

    // Render each slide with timing
    const timings = [];
    for (let i = 0; i < slides.length; i++) {
      const slide = slides[i];
      const filename = outputFile || path.join(outputDir, `slide_${String(i + 1).padStart(2, '0')}.png`);

      const startTime = Date.now();
      await renderSlide(page, renderUrl, slide, filename);
      const renderTime = Date.now() - startTime;

      timings.push({
        slide: i + 1,
        type: slide.type,
        time_ms: renderTime
      });
    }

    // Performance report
    const totalTime = timings.reduce((sum, t) => sum + t.time_ms, 0);
    const avgTime = totalTime / timings.length;

    console.log(`\n✅ Rendered ${slides.length} slide(s) successfully!`);
    console.log(`📊 Performance:`);
    console.log(`   Total: ${(totalTime / 1000).toFixed(1)}s`);
    console.log(`   Average: ${(avgTime / 1000).toFixed(2)}s per slide`);
    console.log(`   Fastest: ${(Math.min(...timings.map(t => t.time_ms)) / 1000).toFixed(2)}s`);
    console.log(`   Slowest: ${(Math.max(...timings.map(t => t.time_ms)) / 1000).toFixed(2)}s`);

  } finally {
    await browser.close();
    if (viteProcess) {
      viteProcess.kill();
    }
  }
}

// Run if called directly
if (require.main === module) {
  main().catch((err) => {
    console.error('Error:', err.message);
    process.exit(1);
  });
}

module.exports = { renderSlide, startDevServer };
