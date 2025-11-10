/**
 * Diffusion Process Visualizer
 * Interactive viewer for exploring the invisible computation of diffusion models
 */

let currentSequence = '01_standard';
let metadata = null;
let images = [];
let currentStep = 0;
let isPlaying = false;
let playbackSpeed = 1.0;
let lastFrameTime = 0;

// UI state
let showDiff = false;
let showPrompt = false;

// Previous image for diff calculation
let previousImage = null;

// Comparison mode
let comparisonMode = false;
let compareSequence = '02_low_steps';
let compareMetadata = null;
let compareImages = [];

// Intensity graph
let showIntensityGraph = false;
let intensityData = [];

// Difference map intensity
let diffIntensity = 2.0;

// Theme + Mode selection
let currentTheme = 'truth_vs_lies';
let currentMode = 'standard';
let showThemeSelector = false;

// Phase 3 Interpretability overlays
let showLatentOverlay = false;
let latentVectors = null;
let latentChangeData = [];
let latentOverlayIntensity = 2.0;

// Loading state
let loadingProgress = 0;
let totalImagesToLoad = 0;
let isLoading = false;

function preload() {
    // Load the default theme + mode sequence
    loadThemeModeSequence();
}

function setup() {
    // Create responsive canvas
    let container = select('#canvas-container');
    let w = container.width;
    let h = container.height;
    let size = min(w, h) - 40; // Leave some padding

    let canvas = createCanvas(size, size);
    canvas.parent('canvas-container');

    // Set up UI event listeners
    setupUIControls();

    console.log('Visualizer initialized');
    console.log('Canvas size:', size);
    console.log('Loading theme:', currentTheme, 'mode:', currentMode);
}

function draw() {
    background(20);

    // Auto-play logic
    if (isPlaying && millis() - lastFrameTime > (1000 / (30 * playbackSpeed))) {
        currentStep = (currentStep + 1) % images.length;
        updateStep(currentStep);
        lastFrameTime = millis();
    }

    if (comparisonMode) {
        // Comparison mode: side-by-side view
        drawComparisonView();
    } else {
        // Single view mode
        // Draw current image
        if (images[currentStep]) {
            image(images[currentStep], 0, 0, width, height);
        } else {
            // Placeholder when no images loaded
            drawPlaceholder();
        }

        // Draw difference map overlay if enabled
        if (showDiff && images[currentStep] && previousImage) {
            drawDifferenceMap();
        }

        // Draw latent change overlay if enabled (Phase 3)
        if (showLatentOverlay && latentChangeData.length > 0 && currentStep > 0) {
            drawLatentOverlay();
        }

        // Draw intensity graph
        if (showIntensityGraph && intensityData.length > 0) {
            drawIntensityGraph();
        }

        // Draw theme selector overlay (bottom-right)
        drawThemeSelector();
    }

    // Update prompt display (DOM element) - works for both modes
    drawPromptOverlay();
}

function drawPlaceholder() {
    // Placeholder is not shown during loading
}

function drawDifferenceMap() {
    if (!images[currentStep] || !images[currentStep - 1]) return;

    let current = images[currentStep];
    let previous = images[currentStep - 1];

    // Create difference visualization
    push();

    // Load pixels from both images
    current.loadPixels();
    previous.loadPixels();

    // Calculate pixel differences and find max
    let maxDiff = 0;
    let w = current.width;
    let h = current.height;

    // First pass: find max difference
    for (let i = 0; i < current.pixels.length; i += 4) {
        let dr = abs(current.pixels[i] - previous.pixels[i]);
        let dg = abs(current.pixels[i + 1] - previous.pixels[i + 1]);
        let db = abs(current.pixels[i + 2] - previous.pixels[i + 2]);
        let diff = (dr + dg + db) / 3;
        maxDiff = max(maxDiff, diff);
    }

    // Draw difference map using direct pixel plotting
    blendMode(ADD);
    noStroke();

    // Scale factors to map image pixels to canvas size
    let scaleX = width / w;
    let scaleY = height / h;

    // Second pass: draw colored rectangles for each pixel
    for (let y = 0; y < h; y++) {
        for (let x = 0; x < w; x++) {
            let index = (y * w + x) * 4;

            // Calculate RGB difference
            let dr = abs(current.pixels[index] - previous.pixels[index]);
            let dg = abs(current.pixels[index + 1] - previous.pixels[index + 1]);
            let db = abs(current.pixels[index + 2] - previous.pixels[index + 2]);

            // Average difference for this pixel
            let diff = (dr + dg + db) / 3;
            let normalized = maxDiff > 0 ? diff / maxDiff : 0;

            // Amplify small differences to make them more visible
            normalized = pow(normalized, 1.0 / diffIntensity);

            // Skip pixels with no change
            if (normalized < 0.01) continue;

            // Create heatmap color
            let r, g, b;
            if (normalized < 0.25) {
                let t = normalized / 0.25;
                r = 0;
                g = 0;
                b = t * 255;
            } else if (normalized < 0.5) {
                let t = (normalized - 0.25) / 0.25;
                r = 0;
                g = t * 255;
                b = 255;
            } else if (normalized < 0.75) {
                let t = (normalized - 0.5) / 0.25;
                r = t * 255;
                g = 255;
                b = (1 - t) * 255;
            } else {
                let t = (normalized - 0.75) / 0.25;
                r = 255;
                g = (1 - t) * 255;
                b = 0;
            }

            // Draw pixel as scaled rectangle
            fill(r, g, b, normalized * 180);
            rect(x * scaleX, y * scaleY, scaleX, scaleY);
        }
    }

    blendMode(BLEND);

    // Draw legend
    drawDiffLegend(maxDiff);

    pop();
}

function drawDiffLegend(maxDiff) {
    push();
    noStroke();

    // Background for legend
    fill(0, 200);
    rect(width - 170, 10, 160, 100);

    // Title
    fill(255);
    textAlign(LEFT, TOP);
    textSize(11);
    textFont('Courier New');
    text('DIFFERENCE MAP', width - 165, 20);

    // Gradient bar
    let barWidth = 140;
    let barHeight = 20;
    let barX = width - 165;
    let barY = 45;

    for (let i = 0; i < barWidth; i++) {
        let t = i / barWidth;
        let r, g, b;

        // Match the enhanced heatmap colors (black -> blue -> cyan -> yellow -> red)
        if (t < 0.25) {
            // Black to blue
            let tt = t / 0.25;
            r = 0;
            g = 0;
            b = tt * 255;
        } else if (t < 0.5) {
            // Blue to cyan
            let tt = (t - 0.25) / 0.25;
            r = 0;
            g = tt * 255;
            b = 255;
        } else if (t < 0.75) {
            // Cyan to yellow
            let tt = (t - 0.5) / 0.25;
            r = tt * 255;
            g = 255;
            b = (1 - tt) * 255;
        } else {
            // Yellow to red
            let tt = (t - 0.75) / 0.25;
            r = 255;
            g = (1 - tt) * 255;
            b = 0;
        }

        stroke(r, g, b);
        line(barX + i, barY, barX + i, barY + barHeight);
    }

    // Labels
    noStroke();
    fill(255);
    textSize(9);
    text('No Change', barX, barY + barHeight + 5);
    textAlign(RIGHT);
    text('Max Change', barX + barWidth, barY + barHeight + 5);

    textAlign(LEFT);
    text(`Max diff: ${maxDiff.toFixed(1)}`, barX, barY + barHeight + 18);

    pop();
}

function drawLatentOverlay() {
    /**
     * Phase 3: Latent Space Change Overlay
     * Visualizes changes in latent space (deeper than pixel differences)
     * Shows where the model is "thinking" hardest
     */

    if (currentStep === 0 || !latentChangeData[currentStep]) return;

    push();
    blendMode(ADD);
    noStroke();

    let changeMap = latentChangeData[currentStep];
    let maxChange = changeMap.max;

    // Resolution of latent space (typically 64x64)
    let resolution = changeMap.resolution;
    let scaleX = width / resolution;
    let scaleY = height / resolution;

    // Draw heatmap rectangles
    for (let y = 0; y < resolution; y++) {
        for (let x = 0; x < resolution; x++) {
            let idx = y * resolution + x;
            let change = changeMap.data[idx];

            if (change < 0.01) continue; // Skip near-zero changes

            // Normalize and amplify
            let normalized = (change / maxChange);
            normalized = pow(normalized, 1.0 / latentOverlayIntensity);

            // Create heatmap color (purple → cyan → yellow)
            let r, g, b;
            if (normalized < 0.33) {
                // Purple to blue
                let t = normalized / 0.33;
                r = 128 * (1 - t);
                g = 0;
                b = 128 + 127 * t;
            } else if (normalized < 0.66) {
                // Blue to cyan
                let t = (normalized - 0.33) / 0.33;
                r = 0;
                g = 255 * t;
                b = 255;
            } else {
                // Cyan to yellow
                let t = (normalized - 0.66) / 0.34;
                r = 255 * t;
                g = 255;
                b = 255 * (1 - t);
            }

            fill(r, g, b, normalized * 160);
            rect(x * scaleX, y * scaleY, scaleX, scaleY);
        }
    }

    blendMode(BLEND);

    // Draw legend
    drawLatentLegend(maxChange);

    pop();
}

function drawLatentLegend(maxChange) {
    push();
    noStroke();

    // Background
    fill(0, 200);
    rect(width - 170, height - 120, 160, 110);

    // Title
    fill(255);
    textAlign(LEFT, TOP);
    textSize(11);
    textFont('Courier New');
    text('LATENT CHANGE', width - 165, height - 110);

    // Gradient bar
    let barWidth = 140;
    let barHeight = 20;
    let barX = width - 165;
    let barY = height - 85;

    for (let i = 0; i < barWidth; i++) {
        let t = i / barWidth;
        let r, g, b;

        if (t < 0.33) {
            let tt = t / 0.33;
            r = 128 * (1 - tt);
            g = 0;
            b = 128 + 127 * tt;
        } else if (t < 0.66) {
            let tt = (t - 0.33) / 0.33;
            r = 0;
            g = 255 * tt;
            b = 255;
        } else {
            let tt = (t - 0.66) / 0.34;
            r = 255 * tt;
            g = 255;
            b = 255 * (1 - tt);
        }

        stroke(r, g, b);
        line(barX + i, barY, barX + i, barY + barHeight);
    }

    // Labels
    noStroke();
    fill(255);
    textSize(9);
    text('Low', barX, barY + barHeight + 5);
    textAlign(RIGHT);
    text('High', barX + barWidth, barY + barHeight + 5);

    textAlign(LEFT);
    textSize(8);
    fill(150);
    text('Phase 3: Deep change', barX, barY + barHeight + 18);
    text(`Latent space activity`, barX, barY + barHeight + 28);

    pop();
}

function drawMetadataOverlay() {
    if (!metadata || !metadata.steps || !metadata.steps[currentStep]) return;

    let stepData = metadata.steps[currentStep];

    push();
    fill(0, 200);
    noStroke();
    rect(10, 10, 250, 100);

    fill(0, 255, 136);
    textAlign(LEFT, TOP);
    textSize(12);
    textFont('Courier New');

    let y = 20;
    text(`Step: ${stepData.step}/${metadata.num_inference_steps}`, 20, y);
    y += 20;
    text(`Timestep: ${stepData.timestep}`, 20, y);
    y += 20;
    text(`Noise: ${stepData.noise_variance.toFixed(4)}`, 20, y);
    y += 20;
    text(`Guidance: ${metadata.guidance_scale}`, 20, y);
    pop();
}

function drawPromptOverlay() {
    // Update DOM element instead of drawing on canvas
    if (!metadata || !metadata.prompt) {
        select('#prompt-display').style('display', 'none');
        return;
    }

    if (showPrompt) {
        select('#prompt-display').style('display', 'block');
        select('#prompt-text').html(`"${metadata.prompt}"`);
    } else {
        select('#prompt-display').style('display', 'none');
    }
}

function drawComparisonView() {
    // Draw both sequences side by side
    let halfWidth = width / 2;

    // Draw left sequence (current)
    push();
    if (images[currentStep]) {
        image(images[currentStep], 0, 0, halfWidth, height);
    } else {
        fill(40);
        rect(0, 0, halfWidth, height);
        fill(100);
        textAlign(CENTER, CENTER);
        text('Loading...', halfWidth / 2, height / 2);
    }
    pop();

    // Draw right sequence (comparison)
    push();
    translate(halfWidth, 0);

    // Adjust step for comparison sequence (might have different length)
    let compareStep = currentStep;
    if (compareImages.length > 0) {
        compareStep = min(currentStep, compareImages.length - 1);
    }

    if (compareImages[compareStep]) {
        image(compareImages[compareStep], 0, 0, halfWidth, height);
    } else {
        fill(40);
        rect(0, 0, halfWidth, height);
        fill(100);
        textAlign(CENTER, CENTER);
        text('Loading...', halfWidth / 2, height / 2);
    }
    pop();

    // Draw divider line
    stroke(0, 255, 136);
    strokeWeight(2);
    line(halfWidth, 0, halfWidth, height);

    // Draw labels
    push();
    fill(0, 200);
    noStroke();

    // Left label
    rect(10, 10, 200, 30);
    fill(0, 255, 136);
    textAlign(LEFT, TOP);
    textSize(11);
    textFont('Courier New');
    text(getSequenceName(currentSequence), 15, 20);

    // Right label
    fill(0, 200);
    rect(halfWidth + 10, 10, 200, 30);
    fill(0, 255, 136);
    text(getSequenceName(compareSequence), halfWidth + 15, 20);
    pop();

    // Draw step info
    if (showMetadata) {
        push();
        fill(0, 200);
        rect(10, height - 60, width - 20, 50);
        fill(0, 255, 136);
        textAlign(LEFT, TOP);
        textSize(11);
        textFont('Courier New');
        text(`Step: ${currentStep} | Comparing generation methods`, 20, height - 50);

        if (metadata && metadata.steps && metadata.steps[currentStep]) {
            text(`Noise variance: ${metadata.steps[currentStep].noise_variance.toFixed(4)}`, 20, height - 35);
        }
        if (compareMetadata && compareMetadata.steps && compareMetadata.steps[compareStep]) {
            text(`vs ${compareMetadata.steps[compareStep].noise_variance.toFixed(4)}`, 250, height - 35);
        }
        pop();
    }
}

function getSequenceName(sequenceId) {
    const names = {
        '01_standard': 'Standard',
        '02_low_steps': 'Low Steps',
        '03_high_guidance': 'High Guidance',
        '04_paradox': 'Paradox',
        '05_truth_vs_lies': 'Truth vs Lies',
        '06_echo_chamber': 'Echo Chamber',
        '07_propaganda': 'Propaganda',
        '08_deepfake_paradox': 'Deepfake Paradox',
        '09_info_overload': 'Info Overload',
        '10_viral_spread': 'Viral Spread'
    };
    return names[sequenceId] || sequenceId;
}

function drawIntensityGraph() {
    push();

    // Graph dimensions
    let graphWidth = 300;
    let graphHeight = 150;
    let graphX = 20; // Left side
    let graphY = height - graphHeight - 20;

    // Background
    fill(0, 220);
    noStroke();
    rect(graphX, graphY, graphWidth, graphHeight);

    // Title
    fill(0, 255, 136);
    textAlign(LEFT, TOP);
    textSize(10);
    textFont('Courier New');
    text('CHANGE INTENSITY', graphX + 10, graphY + 5);

    // Draw graph
    if (intensityData.length > 1) {
        let maxIntensity = max(intensityData);
        let padding = 30;
        let plotWidth = graphWidth - padding * 2;
        let plotHeight = graphHeight - padding - 20;

        // Draw axes
        stroke(100);
        strokeWeight(1);
        line(graphX + padding, graphY + padding, graphX + padding, graphY + padding + plotHeight);
        line(graphX + padding, graphY + padding + plotHeight, graphX + padding + plotWidth, graphY + padding + plotHeight);

        // Draw intensity curve
        stroke(0, 255, 136);
        strokeWeight(2);
        noFill();
        beginShape();
        for (let i = 0; i < intensityData.length; i++) {
            let x = map(i, 0, intensityData.length - 1, graphX + padding, graphX + padding + plotWidth);
            let y = map(intensityData[i], 0, maxIntensity, graphY + padding + plotHeight, graphY + padding);
            vertex(x, y);
        }
        endShape();

        // Draw current position indicator
        if (currentStep < intensityData.length) {
            let x = map(currentStep, 0, intensityData.length - 1, graphX + padding, graphX + padding + plotWidth);
            stroke(255, 100, 100);
            strokeWeight(2);
            line(x, graphY + padding, x, graphY + padding + plotHeight);
        }

        // Labels
        noStroke();
        fill(150);
        textSize(8);
        textAlign(CENTER);
        text('Step', graphX + padding + plotWidth / 2, graphY + graphHeight - 8);
        textAlign(LEFT);
        push();
        translate(graphX + 5, graphY + padding + plotHeight / 2);
        rotate(-PI / 2);
        text('Change', 0, 0);
        pop();
    }

    pop();
}

function calculateIntensityData() {
    intensityData = [];

    if (images.length < 2) {
        return;
    }

    console.log('Calculating intensity data...');

    for (let i = 1; i < images.length; i++) {
        if (!images[i] || !images[i - 1]) continue;

        let current = images[i];
        let previous = images[i - 1];

        current.loadPixels();
        previous.loadPixels();

        let totalDiff = 0;
        let pixelCount = 0;

        for (let j = 0; j < current.pixels.length; j += 4) {
            let dr = abs(current.pixels[j] - previous.pixels[j]);
            let dg = abs(current.pixels[j + 1] - previous.pixels[j + 1]);
            let db = abs(current.pixels[j + 2] - previous.pixels[j + 2]);

            totalDiff += (dr + dg + db) / 3;
            pixelCount++;
        }

        let avgDiff = totalDiff / pixelCount;
        intensityData.push(avgDiff);
    }

    console.log(`Intensity data calculated: ${intensityData.length} points`);
}

async function loadLatentData(sequenceName) {
    /**
     * Phase 3: Load latent vectors from numpy file
     * Note: This is a simplified loader - in production, use a proper numpy parser
     * For now, we'll compute latent changes from image data as a proxy
     */
    console.log(`Loading Phase 3 latent data for: ${sequenceName}`);

    latentVectors = null;
    latentChangeData = [];

    // Check if phase3_data exists
    let phase3Path = `/assets/generated_sequences/${sequenceName}/phase3_data/latent_vectors.npy`;

    // For now, compute proxy latent changes from images
    // This creates similar visual effect while we wait for proper numpy loading
    if (images.length > 1) {
        computeLatentChangeProxy();
    }
}

function computeLatentChangeProxy() {
    /**
     * Compute latent-like change maps from images
     * This approximates latent space changes by analyzing image structure
     * at lower resolution (similar to latent space dimensionality)
     */
    console.log('Computing latent change data from images...');

    latentChangeData = [];
    let resolution = 64; // Latent space resolution

    for (let step = 1; step < images.length; step++) {
        if (!images[step] || !images[step - 1]) continue;

        let current = images[step];
        let previous = images[step - 1];

        current.loadPixels();
        previous.loadPixels();

        let changeMap = {
            resolution: resolution,
            data: new Array(resolution * resolution).fill(0),
            max: 0
        };

        // Sample images at lower resolution
        let imgW = current.width;
        let imgH = current.height;
        let cellW = imgW / resolution;
        let cellH = imgH / resolution;

        for (let y = 0; y < resolution; y++) {
            for (let x = 0; x < resolution; x++) {
                let totalChange = 0;
                let samples = 0;

                // Sample within this cell
                let startX = floor(x * cellW);
                let startY = floor(y * cellH);
                let endX = floor((x + 1) * cellW);
                let endY = floor((y + 1) * cellH);

                for (let py = startY; py < endY; py += 2) {
                    for (let px = startX; px < endX; px += 2) {
                        let idx = (py * imgW + px) * 4;
                        if (idx >= current.pixels.length) continue;

                        let dr = abs(current.pixels[idx] - previous.pixels[idx]);
                        let dg = abs(current.pixels[idx + 1] - previous.pixels[idx + 1]);
                        let db = abs(current.pixels[idx + 2] - previous.pixels[idx + 2]);

                        totalChange += (dr + dg + db) / 3;
                        samples++;
                    }
                }

                let avgChange = samples > 0 ? totalChange / samples : 0;
                let cellIdx = y * resolution + x;
                changeMap.data[cellIdx] = avgChange;
                changeMap.max = max(changeMap.max, avgChange);
            }
        }

        latentChangeData.push(changeMap);
    }

    console.log(`✓ Computed ${latentChangeData.length} latent change maps`);
}

function drawThemeSelector() {
    push();

    // Position bottom-right
    let selectorWidth = 280;
    let selectorHeight = showThemeSelector ? 330 : 110;
    let selectorX = width - selectorWidth - 20;
    let selectorY = height - selectorHeight - 20;

    // Background
    fill(0, 230);
    stroke(0, 255, 136);
    strokeWeight(2);
    rect(selectorX, selectorY, selectorWidth, selectorHeight, 5);

    // Title
    fill(0, 255, 136);
    noStroke();
    textAlign(LEFT, TOP);
    textSize(12);
    textFont('Courier New');
    text('THEME + MODE', selectorX + 15, selectorY + 10);

    // Current selection display
    textSize(10);
    fill(255);
    let themeName = getThemeName(currentTheme);
    let modeName = getModeName(currentMode);
    text(`${themeName}`, selectorX + 15, selectorY + 35);
    fill(150);
    textSize(9);
    text(`Mode: ${modeName}`, selectorX + 15, selectorY + 50);

    // Expand/collapse button
    fill(0, 255, 136, 100);
    noStroke();
    let btnY = selectorY + 80;
    rect(selectorX + 15, btnY, selectorWidth - 30, 20, 3);
    fill(255);
    textAlign(CENTER, CENTER);
    textSize(10);
    text(showThemeSelector ? '▲ COLLAPSE' : '▼ EXPAND', selectorX + selectorWidth / 2, btnY + 10);

    // If expanded, show all options
    if (showThemeSelector) {
        textAlign(LEFT, TOP);
        let optY = btnY + 30;

        // Theme options
        fill(150);
        textSize(9);
        text('THEMES:', selectorX + 15, optY);
        optY += 15;

        let themes = ['truth_vs_lies', 'echo_chamber', 'propaganda', 'deepfake', 'info_overload', 'viral_spread'];
        for (let theme of themes) {
            if (theme === currentTheme) {
                fill(0, 255, 136);
            } else {
                fill(200);
            }
            textSize(9);
            text('→ ' + getThemeName(theme), selectorX + 20, optY);
            optY += 14;
        }

        optY += 10;
        // Mode options
        fill(150);
        textSize(9);
        text('MODES:', selectorX + 15, optY);
        optY += 15;

        let modes = ['standard', 'low_steps', 'high_guidance', 'paradox'];
        for (let mode of modes) {
            if (mode === currentMode) {
                fill(0, 255, 136);
            } else {
                fill(200);
            }
            textSize(9);
            text('→ ' + getModeName(mode), selectorX + 20, optY);
            optY += 14;
        }
    }

    pop();
}

function getThemeName(themeId) {
    const names = {
        'truth_vs_lies': 'Truth vs Lies',
        'echo_chamber': 'Echo Chamber',
        'propaganda': 'Propaganda',
        'deepfake': 'Deepfake',
        'info_overload': 'Info Overload',
        'viral_spread': 'Viral Spread'
    };
    return names[themeId] || themeId;
}

function getModeName(modeId) {
    const names = {
        'standard': 'Standard',
        'low_steps': 'Low Steps',
        'high_guidance': 'High Guidance',
        'paradox': 'Paradox'
    };
    return names[modeId] || modeId;
}

function mousePressed() {
    // Check if click is on theme selector
    let selectorWidth = 280;
    let selectorHeight = showThemeSelector ? 330 : 110;
    let selectorX = width - selectorWidth - 20;
    let selectorY = height - selectorHeight - 20;

    // Check expand/collapse button
    let btnY = selectorY + 80;
    if (mouseX > selectorX + 15 && mouseX < selectorX + selectorWidth - 15 &&
        mouseY > btnY && mouseY < btnY + 20) {
        showThemeSelector = !showThemeSelector;
        return;
    }

    if (showThemeSelector) {
        let optY = btnY + 45;

        // Check theme clicks
        let themes = ['truth_vs_lies', 'echo_chamber', 'propaganda', 'deepfake', 'info_overload', 'viral_spread'];
        for (let theme of themes) {
            if (mouseX > selectorX + 20 && mouseX < selectorX + selectorWidth - 20 &&
                mouseY > optY && mouseY < optY + 14) {
                currentTheme = theme;
                loadThemeModeSequence();
                return;
            }
            optY += 14;
        }

        optY += 25;

        // Check mode clicks
        let modes = ['standard', 'low_steps', 'high_guidance', 'paradox'];
        for (let mode of modes) {
            if (mouseX > selectorX + 20 && mouseX < selectorX + selectorWidth - 20 &&
                mouseY > optY && mouseY < optY + 14) {
                currentMode = mode;
                loadThemeModeSequence();
                return;
            }
            optY += 14;
        }
    }
}

function loadThemeModeSequence() {
    let sequenceName = `fakenews_${currentTheme}_${currentMode}`;
    console.log(`Loading sequence: ${sequenceName}`);

    // Reset current images
    images = [];
    currentStep = 0;
    intensityData = [];

    // Load the sequence
    loadSequenceMetadata(sequenceName);
}


function setupUIControls() {
    // Step slider
    select('#step-slider').input(() => {
        currentStep = int(select('#step-slider').value());
        updateStep(currentStep);
        isPlaying = false;
        select('#play-button').html('Play');
    });

    // Play button
    select('#play-button').mousePressed(() => {
        isPlaying = !isPlaying;
        select('#play-button').html(isPlaying ? 'Pause' : 'Play');
    });

    // Reset button
    select('#reset-button').mousePressed(() => {
        currentStep = 0;
        updateStep(0);
        isPlaying = false;
        select('#play-button').html('Play');
    });

    // Speed slider
    select('#speed-slider').input(() => {
        playbackSpeed = float(select('#speed-slider').value());
        select('#speed-display').html(playbackSpeed.toFixed(1));
    });

    // Checkboxes
    select('#show-diff').changed(() => {
        showDiff = select('#show-diff').checked();
        // Show/hide intensity controls
        if (showDiff) {
            select('#diff-intensity-controls').style('display', 'block');
        } else {
            select('#diff-intensity-controls').style('display', 'none');
        }
    });

    // Diff intensity slider
    select('#diff-intensity').input(() => {
        diffIntensity = float(select('#diff-intensity').value());
        select('#diff-intensity-display').html(diffIntensity.toFixed(1));
    });

    select('#show-prompt').changed(() => {
        showPrompt = select('#show-prompt').checked();
    });

    // Phase 3: Latent overlay
    select('#show-latent-overlay').changed(() => {
        showLatentOverlay = select('#show-latent-overlay').checked();
        // Compute latent data if enabled and not already done
        if (showLatentOverlay && latentChangeData.length === 0 && images.length > 1) {
            computeLatentChangeProxy();
        }
        // Show/hide latent intensity controls
        if (showLatentOverlay) {
            select('#latent-intensity-controls').style('display', 'block');
        } else {
            select('#latent-intensity-controls').style('display', 'none');
        }
    });

    // Latent intensity slider
    select('#latent-intensity').input(() => {
        latentOverlayIntensity = float(select('#latent-intensity').value());
        select('#latent-intensity-display').html(latentOverlayIntensity.toFixed(1));
    });

    // Comparison mode
    select('#comparison-mode').changed(() => {
        comparisonMode = select('#comparison-mode').checked();
        // Show/hide comparison controls
        if (comparisonMode) {
            select('#comparison-controls').style('display', 'block');
            // Load comparison sequence if not loaded
            if (compareImages.length === 0) {
                loadComparisonSequence(compareSequence);
            }
        } else {
            select('#comparison-controls').style('display', 'none');
        }
    });

    // Comparison sequence selector
    select('#compare-sequence-select').changed(() => {
        compareSequence = select('#compare-sequence-select').value();
        loadComparisonSequence(compareSequence);
    });

    // Intensity graph toggle
    select('#show-intensity-graph').changed(() => {
        showIntensityGraph = select('#show-intensity-graph').checked();
        // Calculate intensity data if not already done
        if (showIntensityGraph && intensityData.length === 0 && images.length > 1) {
            calculateIntensityData();
        }
    });
}

function updateStep(step) {
    currentStep = step;
    select('#step-slider').value(step);
    select('#step-display').html(step);

    // Update metadata panel
    if (metadata && metadata.steps && metadata.steps[step]) {
        let stepData = metadata.steps[step];
        select('#meta-step').html(stepData.step);
        select('#meta-total').html(metadata.num_inference_steps);
        select('#meta-timestep').html(stepData.timestep);
        select('#meta-noise').html(stepData.noise_variance.toFixed(4));
    }

    // Store previous image for diff
    if (images[step - 1]) {
        previousImage = images[step - 1];
    }
}

function loadSequenceMetadata(sequenceName) {
    console.log(`Loading sequence: ${sequenceName}`);

    // Load actual metadata from JSON file
    let metadataPath = `/assets/generated_sequences/${sequenceName}/metadata.json`;

    fetch(metadataPath)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to load metadata: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            metadata = data;
            console.log('Metadata loaded:', metadata);

            // Update UI with metadata
            select('#meta-theme').html(getThemeName(currentTheme));
            select('#meta-mode').html(getModeName(currentMode));
            select('#meta-prompt').html(metadata.prompt);
            select('#meta-guidance').html(metadata.guidance_scale);
            select('#meta-seed').html(metadata.seed);
            select('#step-slider').attribute('max', metadata.steps.length - 1);

            // Load actual images
            loadSequenceImages(sequenceName);
        })
        .catch(error => {
            console.error('Error loading metadata:', error);
            // Fallback to mock data
            metadata = {
                prompt: "Error loading metadata",
                negative_prompt: "",
                num_inference_steps: 50,
                guidance_scale: 7.5,
                seed: 42,
                steps: generateMockSteps(50)
            };
            select('#meta-prompt').html(metadata.prompt);
        });
}

function loadSequenceImages(sequenceName) {
    images = [];
    console.log(`Loading images for: ${sequenceName}`);

    if (!metadata || !metadata.steps) {
        console.error('Cannot load images: metadata not loaded');
        return;
    }

    // Load all step images (step_0000.png through step_00XX.png)
    let numSteps = metadata.steps.length;
    let loadedCount = 0;

    for (let i = 0; i < numSteps; i++) {
        let imagePath = `/assets/generated_sequences/${sequenceName}/step_${nf(i, 4)}.png`;

        loadImage(
            imagePath,
            (img) => {
                images[i] = img;
                loadedCount++;
                console.log(`Loaded image ${i + 1}/${numSteps}`);

                // Update display when first image loads
                if (loadedCount === 1) {
                    updateStep(0);
                }

                // Calculate intensity data once all images are loaded
                if (loadedCount === numSteps && showIntensityGraph) {
                    setTimeout(() => calculateIntensityData(), 500);
                }
            },
            (error) => {
                console.error(`Failed to load image ${i}:`, error);
            }
        );
    }
}

function loadComparisonSequence(sequenceName) {
    console.log(`Loading comparison sequence: ${sequenceName}`);

    // Load metadata for comparison sequence
    let metadataPath = `/assets/generated_sequences/${sequenceName}/metadata.json`;

    fetch(metadataPath)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to load comparison metadata: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            compareMetadata = data;
            console.log('Comparison metadata loaded:', compareMetadata);

            // Load comparison images
            loadComparisonImages(sequenceName);
        })
        .catch(error => {
            console.error('Error loading comparison metadata:', error);
        });
}

function loadComparisonImages(sequenceName) {
    compareImages = [];
    console.log(`Loading comparison images for: ${sequenceName}`);

    if (!compareMetadata || !compareMetadata.steps) {
        console.error('Cannot load comparison images: metadata not loaded');
        return;
    }

    let numSteps = compareMetadata.steps.length;
    let loadedCount = 0;

    for (let i = 0; i < numSteps; i++) {
        let imagePath = `/assets/generated_sequences/${sequenceName}/step_${nf(i, 4)}.png`;

        loadImage(
            imagePath,
            (img) => {
                compareImages[i] = img;
                loadedCount++;
                console.log(`Loaded comparison image ${i + 1}/${numSteps}`);
            },
            (error) => {
                console.error(`Failed to load comparison image ${i}:`, error);
            }
        );
    }
}

function generateMockSteps(numSteps) {
    // Generate mock step data for scaffold
    let steps = [];
    for (let i = 0; i < numSteps; i++) {
        steps.push({
            step: i,
            timestep: 1000 - (i * (1000 / numSteps)),
            noise_variance: 1.0 - (i / numSteps),
            timestamp: new Date().toISOString()
        });
    }
    return steps;
}

// Keyboard shortcuts
function keyPressed() {
    if (key === ' ') {
        // Spacebar: play/pause
        isPlaying = !isPlaying;
        select('#play-button').html(isPlaying ? 'Pause' : 'Play');
    } else if (keyCode === LEFT_ARROW) {
        // Previous step
        currentStep = max(0, currentStep - 1);
        updateStep(currentStep);
    } else if (keyCode === RIGHT_ARROW) {
        // Next step
        currentStep = min(images.length - 1, currentStep + 1);
        updateStep(currentStep);
    } else if (key === 'm' || key === 'M') {
        // Toggle metadata
        showMetadata = !showMetadata;
        select('#show-metadata').checked(showMetadata);
    } else if (key === 'd' || key === 'D') {
        // Toggle diff
        showDiff = !showDiff;
        select('#show-diff').checked(showDiff);
    } else if (key === 'p' || key === 'P') {
        // Toggle prompt
        showPrompt = !showPrompt;
        select('#show-prompt').checked(showPrompt);
    }
}
