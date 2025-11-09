# Usage Guide

How to use the Diffusion Visualization Installation for creating and displaying AI generation sequences.

---

## Phase 1: Generating Sequences

### Basic Usage

**Run the default experiments:**
```bash
cd phase1_generation
python diffusion_step_generator.py
```

This generates 4 pre-configured sequences demonstrating different "failure modes."

---

### Custom Prompts

**Edit `diffusion_step_generator.py`** or create your own script:

```python
from diffusion_step_generator import DiffusionStepCapture
from pathlib import Path

# Initialize
generator = DiffusionStepCapture(device="mps")  # or "cuda" or "cpu"
base_output = Path("../assets/generated_sequences")

# Generate custom sequence
generator.generate_sequence(
    prompt="your prompt here",
    output_dir=base_output / "my_sequence",
    num_inference_steps=50,
    guidance_scale=7.5,
    seed=42
)
```

---

### Key Parameters Explained

#### `prompt` (string)
The text description of what to generate.

**Tips:**
- Be specific but not overly detailed
- Use artistic qualifiers: "dreamlike," "cinematic," "ethereal"
- Combine concepts: "a library made of light, surreal architecture"

**Examples:**
```python
"a protest march at sunset, hope and struggle"
"impossible architecture, MC Escher style"
"a face half-formed from static and noise"
```

---

#### `num_inference_steps` (int, default: 50)
How many denoising iterations to perform.

**Effects:**
- **10-20 steps**: Incomplete, dreamlike, abstract
- **30-50 steps**: Balanced (standard)
- **100+ steps**: Diminishing returns, slightly sharper

**For installation art:**
- Use **fewer steps (15-25)** to emphasize the "arrested development" aesthetic
- More steps = smoother animation but less visible "struggle"

**Example:**
```python
# Deliberately incomplete
generator.generate_sequence(
    prompt="a city dissolving into light",
    num_inference_steps=15,  # Stop early
    ...
)
```

---

#### `guidance_scale` (float, default: 7.5)
How strongly to follow the text prompt.

**Effects:**
- **1-5**: Weak guidance, more random/abstract
- **7-10**: Balanced (standard)
- **15-25**: Strong guidance, oversaturated, "melted" look
- **30+**: Extreme, often artifacts

**For installation art:**
- **High values (15-20)** create surreal over-interpretation
- **Low values (3-5)** create ambiguity

**Example:**
```python
# Force over-interpretation
generator.generate_sequence(
    prompt="a crowd of people",
    guidance_scale=20.0,  # Over-commit
    ...
)
```

---

#### `seed` (int or None)
Random seed for reproducibility.

**Effects:**
- **Same seed** = same result (given same prompt/settings)
- **Different seed** = different interpretation
- **None** = random seed each time

**For installation art:**
- Use **fixed seed** to compare across parameters
- Use **None** for variety

**Example:**
```python
# Generate variations
for i in range(5):
    generator.generate_sequence(
        prompt="a memory fading",
        seed=i,  # Different each time
        output_dir=base_output / f"variation_{i}"
    )
```

---

#### `negative_prompt` (string, default: "")
What to avoid in the generation.

**Common negative prompts:**
```python
negative_prompt="blurry, low quality, distorted"  # Standard
negative_prompt="text, watermark, signature"       # Remove artifacts
negative_prompt=""                                  # Allow anything (for art)
```

**For installation art:**
- **Leave empty** or minimal — "mistakes" are interesting
- You *want* blurriness, distortion, etc.

---

#### `height` and `width` (int, default: 512)
Image dimensions in pixels.

**Options:**
- **256x256**: Fast, low-res (good for testing)
- **512x512**: Standard (balanced)
- **768x768**: High-res (slower, needs more VRAM)

**Note:** Must be multiples of 8 (model requirement)

**For installation/projection:**
- Start with 512x512 for testing
- Use 768x768 or 1024x1024 for final exhibition (if GPU allows)

---

### Designing "Failure Mode" Experiments

The most interesting sequences come from deliberately pushing the model's limits.

#### 1. **Arrested Development** (Low Steps)
```python
generator.generate_sequence(
    prompt="a face emerging from fog",
    num_inference_steps=12,  # Very low
    guidance_scale=7.5,
    output_dir=base_output / "arrested"
)
```
**Effect:** Half-formed imagery, like a thought interrupted

---

#### 2. **Over-Interpretation** (High Guidance)
```python
generator.generate_sequence(
    prompt="fire and ice colliding",
    num_inference_steps=50,
    guidance_scale=22.0,  # Very high
    output_dir=base_output / "oversaturated"
)
```
**Effect:** Forced clarity, oversaturated colors, "melted" look

---

#### 3. **Paradoxical Prompts** (Semantic Conflict)
```python
generator.generate_sequence(
    prompt="transparent concrete, frozen fire, solid smoke",
    num_inference_steps=50,
    guidance_scale=7.5,
    output_dir=base_output / "paradox"
)
```
**Effect:** Model averages impossibilities → surreal hybrids

---

#### 4. **Iterative Corruption** (Feedback Loop)
```python
# Generate once
output1, images1, meta1 = generator.generate_sequence(
    prompt="a quiet room",
    output_dir=base_output / "iteration_1"
)

# Use output as new input (re-encode → re-generate)
# This creates a "telephone game" effect
# (Requires additional code to re-encode image as latent)
```
**Effect:** Progressive loss of coherence, "xerox of a xerox"

---

#### 5. **Extreme Resolution Mismatch**
```python
# Generate low-res, upscale naively
generator.generate_sequence(
    prompt="a detailed cityscape",
    height=128, width=128,  # Very low
    num_inference_steps=50,
    output_dir=base_output / "low_res"
)
# Then upscale with basic interpolation (not AI upscaling)
```
**Effect:** Pixelation, compression artifacts, texture noise

---

### Batch Generation Script

To generate multiple sequences systematically:

```python
experiments = [
    {
        "name": "dream_standard",
        "prompt": "a dream of flying",
        "steps": 50,
        "guidance": 7.5
    },
    {
        "name": "dream_arrested",
        "prompt": "a dream of flying",
        "steps": 15,
        "guidance": 7.5
    },
    {
        "name": "dream_intense",
        "prompt": "a dream of flying",
        "steps": 50,
        "guidance": 18.0
    }
]

for exp in experiments:
    generator.generate_sequence(
        prompt=exp["prompt"],
        num_inference_steps=exp["steps"],
        guidance_scale=exp["guidance"],
        output_dir=base_output / exp["name"],
        seed=42  # Same seed for comparison
    )
```

---

## Phase 2: Interactive Viewer

### Basic Controls

**Launch viewer:**
```bash
cd phase2_viewer
python -m http.server 8000
```
Open: `http://localhost:8000`

---

### Interface Elements

#### **Sequence Selector** (dropdown)
Choose which generated sequence to view:
- `01_standard`: Normal generation
- `02_low_steps`: Arrested development
- `03_high_guidance`: Over-interpretation
- `04_paradox`: Paradoxical prompt

**Action:** Changes entire loaded sequence

---

#### **Step Slider**
Scrub through individual frames (step 0 → final step)

**Interaction:**
- Drag slider: Jump to specific step
- Click on track: Jump to position
- Keyboard arrows: Move one step at a time

**What you see:**
- Each position shows the image at that denoising step
- Metadata updates in real-time

---

#### **Play/Pause Button**
Animate through steps automatically

**Playback:**
- Plays at ~30fps (adjustable with speed slider)
- Loops back to start when reaching end
- Keyboard shortcut: `Space`

---

#### **Speed Slider**
Control playback speed (0.1x to 3.0x)

**Use cases:**
- **0.1x - 0.5x**: Slow-motion (see subtle changes)
- **1.0x**: Normal (smooth animation)
- **2.0x - 3.0x**: Fast (overview of process)

---

#### **Overlay Toggles** (checkboxes)

**Show Metadata:**
Displays on-canvas overlay with:
- Current step / total steps
- Timestep value
- Noise variance
- Guidance scale

**Show Difference Map:**
*(Phase 3 feature - not yet implemented)*
Highlights pixels that changed between current and previous step

**Show Prompt:**
Displays the generation prompt at bottom of canvas

---

### Keyboard Shortcuts

| Key             | Action                    |
| --------------- | ------------------------- |
| `Space`         | Play / Pause              |
| `←` (Left)      | Previous step             |
| `→` (Right)     | Next step                 |
| `M`             | Toggle metadata overlay   |
| `D`             | Toggle difference map     |
| `P`             | Toggle prompt overlay     |
| `R`             | Reset to step 0           |

---

### Metadata Panel

Located bottom-right, shows:
- **Prompt**: Full text prompt used
- **Step**: Current / Total steps
- **Timestep**: Scheduler's internal counter
- **Noise Variance**: How noisy the latent is (1.0 = noise, 0.1 = clear)
- **Guidance Scale**: Prompt following strength
- **Seed**: Random seed used

**Why this matters:**
Understanding these values helps interpret what the model is "doing" at each step.

---

### Curatorial Tips for Exhibition

#### **Single-screen Setup**
- Display one sequence on loop
- Set speed to 0.5x (slow enough to see changes)
- Enable metadata and prompt overlays
- Let it loop continuously

#### **Multi-screen Comparison**
- Show 2-4 sequences side-by-side
- Use same prompt but different parameters
- Synchronize playback (requires custom code)
- Example: Standard vs. Low Steps vs. High Guidance

#### **Interactive Kiosk**
- Touchscreen or tablet
- Let visitors scrub through steps
- Include brief instructions on wall text
- Hide technical metadata (too distracting for general audience)

---

## Advanced Usage

### Creating Smooth Video Exports

Use Python/ffmpeg to convert image sequences to video:

```bash
# Install ffmpeg (if not already)
brew install ffmpeg  # macOS
# or: sudo apt install ffmpeg  # Linux

# Convert sequence to MP4
cd assets/generated_sequences/01_standard
ffmpeg -framerate 30 -i step_%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4
```

**Parameters:**
- `-framerate 30`: 30 fps (adjust for speed)
- `step_%04d.png`: Input pattern (step_0000.png, step_0001.png, ...)
- `-c:v libx264`: H.264 codec (compatible)
- `output.mp4`: Output filename

---

### Adding Custom Metadata Overlays

Edit `sketch.js`, function `drawMetadataOverlay()`:

```javascript
function drawMetadataOverlay() {
    let stepData = metadata.steps[currentStep];

    // Customize appearance
    fill(0, 255, 136);  // Cyan color
    textSize(16);
    text(`Clarity: ${(1 - stepData.noise_variance).toFixed(2)}`, 20, 40);

    // Add your own metrics
    let progress = currentStep / metadata.num_inference_steps;
    text(`Progress: ${(progress * 100).toFixed(0)}%`, 20, 60);
}
```

---

### Connecting Multiple Sequences

To compare sequences side-by-side (requires code modification):

1. **Load multiple sequences simultaneously**
2. **Display in grid layout**
3. **Synchronize step scrubbing**

*(Future documentation will include multi-sequence viewer template)*

---

## Interpreting the Visuals

### What You're Seeing

**Step 0-10 (High noise):**
- Mostly chaos, random color blobs
- Vague shapes might appear (pareidolia)
- Noise variance: ~0.8-1.0

**Step 10-30 (Structure emerges):**
- Large-scale composition forms
- Colors start to cohere
- "Subject" becomes recognizable (face, building, etc.)
- Noise variance: ~0.3-0.7

**Step 30-50 (Refinement):**
- Details sharpen
- Textures appear
- Final colors settle
- Noise variance: ~0.1-0.3

**Final step:**
- Closest to "intended" image
- Often *less* interesting than intermediate steps

---

### What Makes a "Good" Installation Sequence

**Not**: Clean, perfect final images
**Yes**: Visible process, surprising intermediates

**Look for:**
- Steps where something unexpected happens
- Moments of ambiguity (what *is* that?)
- Beautiful "mistakes" (oversaturation, blending, impossible geometry)

**Curatorial strategy:**
Focus on **steps 10-35** — where form is emerging but incomplete.
This is where the model's "thinking" is most visible.

---

## Next Steps

- Experiment with different prompts
- Generate sequences specifically for your conceptual framework
- Customize viewer for your installation context
- Move to Phase 3: Interpretability layers (heatmaps, comparisons)

---

**Remember:** The goal isn't perfect images — it's revealing the *process* of algorithmic interpretation.
