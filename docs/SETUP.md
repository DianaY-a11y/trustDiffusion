# Setup Guide

Complete installation instructions for the Diffusion Visualization Installation project.

---

## System Requirements

### Minimum Requirements
- **OS**: macOS 10.15+, Ubuntu 20.04+, or Windows 10+
- **RAM**: 8GB (16GB recommended)
- **Storage**: 15GB free space
- **GPU**: Optional but highly recommended
  - NVIDIA GPU with 6GB+ VRAM (CUDA support), OR
  - Apple Silicon M1/M2/M3 (MPS support), OR
  - CPU-only (much slower, 5-10 min per sequence)

### Recommended Setup
- **RAM**: 16GB+
- **GPU**: NVIDIA RTX 3060 or Apple M1 Pro
- **Storage**: SSD with 20GB+ free

---

## Phase 1: Python Environment Setup

### Step 1: Install Python

**Check if you have Python 3.9+:**
```bash
python --version
# or
python3 --version
```

If not installed, download from [python.org](https://www.python.org/downloads/) or use a package manager:

**macOS (Homebrew):**
```bash
brew install python@3.11
```

**Ubuntu:**
```bash
sudo apt update
sudo apt install python3.11 python3-pip
```

**Windows:**
Download from python.org or use Windows Store.

---

### Step 2: Create Virtual Environment (Recommended)

```bash
cd diffusion-visualization-installation/phase1_generation

# Create virtual environment
python3 -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

---

### Step 3: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**This will install:**
- `torch` - Deep learning framework
- `diffusers` - Hugging Face diffusion models library
- `transformers` - Text encoding for prompts
- `Pillow` - Image processing
- `numpy` - Numerical operations

**Expected installation time:** 5-15 minutes (depending on internet speed)

**Expected download size:** ~2GB for CPU, ~4GB for GPU (CUDA)

---

### Step 4: Verify Installation

```bash
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"
python -c "from diffusers import StableDiffusionPipeline; print('diffusers OK')"
```

**Check GPU availability:**
```bash
# For NVIDIA GPU:
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

# For Apple Silicon:
python -c "import torch; print(f'MPS available: {torch.backends.mps.is_available()}')"
```

---

### Step 5: First Generation Test

**Quick test (no model download yet):**
```bash
python -c "from diffusers import StableDiffusionPipeline; print('Ready to generate')"
```

**Full test run:**
```bash
python diffusion_step_generator.py
```

**What happens:**
1. First run: Downloads Stable Diffusion v1.5 (~4GB) from Hugging Face
   - Stored in: `~/.cache/huggingface/`
   - Only downloads once
2. Generates 4 sequences (15-30 min total on GPU, 2-4 hrs on CPU)
3. Saves to `../assets/generated_sequences/`

**If it works:** You'll see output like:
```
Loading model: runwayml/stable-diffusion-v1-5
======================================
EXPERIMENT 1: Standard generation
======================================
Generating: 'a protest in a city square...'
  Step 0: timestep=999, noise_var=0.9823
  Step 1: timestep=980, noise_var=0.9156
  ...
✓ Sequence saved to: ../assets/generated_sequences/01_standard
```

---

## Phase 2: Web Viewer Setup

### Step 1: Check Project Structure

Navigate to viewer directory:
```bash
cd ../phase2_viewer
ls
```

You should see:
- `index.html`
- `style.css`
- `sketch.js`

---

### Step 2: Start Local Web Server

**Why?** Browsers block loading local images without a server (CORS policy).

**Option A: Python (easiest)**
```bash
# Python 3:
python -m http.server 8000

# Python 2 (if you somehow have it):
python -m SimpleHTTPServer 8000
```

**Option B: Node.js**
```bash
# Install http-server globally (one time):
npm install -g http-server

# Run:
http-server -p 8000
```

**Option C: VS Code Live Server**
1. Install "Live Server" extension in VS Code
2. Right-click `index.html`
3. Click "Open with Live Server"

---

### Step 3: Open in Browser

Navigate to:
```
http://localhost:8000
```

**Expected result:**
- Black interface with controls on the right
- Main canvas area (showing "No images loaded" placeholder)
- Metadata panel at bottom right

---

### Step 4: Connect to Generated Sequences

**Currently:** The viewer is a scaffold (no images loaded yet)

**To connect real images:**

1. **Option A: Edit `sketch.js` to load images**

In `sketch.js`, find the `loadSequenceImages()` function and uncomment:

```javascript
function loadSequenceImages(sequenceName) {
    images = [];

    // Load actual images
    for (let i = 0; i < metadata.num_inference_steps; i++) {
        let imgPath = `../assets/generated_sequences/${sequenceName}/step_${nf(i, 4)}.png`;
        images.push(loadImage(imgPath));
    }
}
```

**Important:** Make sure your web server can access `../assets/`

2. **Option B: Copy sequences into viewer directory**

```bash
# From project root:
cp -r assets/generated_sequences phase2_viewer/sequences
```

Then update paths in `sketch.js`:
```javascript
let imgPath = `sequences/${sequenceName}/step_${nf(i, 4)}.png`;
```

---

## Troubleshooting

### Python Issues

**Error: "No module named 'torch'"**
- Solution: Make sure virtual environment is activated
- Run: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)

**Error: "CUDA out of memory"**
- Solution: Your GPU doesn't have enough VRAM
- Fix: Reduce image size in script:
  ```python
  generator.generate_sequence(
      ...,
      height=256,  # Instead of 512
      width=256
  )
  ```

**Error: "MPS backend out of memory"**
- Solution: Mac GPU memory issue
- Fix: Use CPU instead:
  ```python
  generator = DiffusionStepCapture(device="cpu")
  ```

**Generation is very slow (CPU mode)**
- Expected: 10-20 min per sequence on modern CPU
- Solution: Reduce steps:
  ```python
  num_inference_steps=25  # Instead of 50
  ```

---

### Web Viewer Issues

**Error: "Images not loading"**
- **Cause**: CORS policy or wrong file paths
- **Fix**:
  1. Make sure you're using a local server (not `file://`)
  2. Check browser console (F12) for specific error
  3. Verify image paths match your directory structure

**Viewer shows but controls don't work**
- **Cause**: JavaScript error
- **Fix**:
  1. Open browser console (F12)
  2. Look for red error messages
  3. Check that p5.js loaded: look for "p5.js" in network tab

**Metadata shows "Loading..."**
- **Cause**: `loadSequenceMetadata()` isn't loading real JSON
- **Fix**: Update function to fetch actual `metadata.json`:
  ```javascript
  function loadSequenceMetadata(sequenceName) {
      loadJSON(
          `../assets/generated_sequences/${sequenceName}/metadata.json`,
          (data) => {
              metadata = data;
              updateUIWithMetadata();
          }
      );
  }
  ```

---

## Hardware-Specific Setup

### Apple Silicon (M1/M2/M3)

**Use MPS (Metal Performance Shaders) for GPU acceleration:**

Already configured in the script:
```python
generator = DiffusionStepCapture(device="mps")
```

**If MPS fails:**
```python
generator = DiffusionStepCapture(device="cpu")
```

**Performance:**
- M1 Pro/Max: ~2 min per 50-step sequence
- M1 base: ~4 min per sequence
- CPU fallback: ~15 min per sequence

---

### NVIDIA GPU (CUDA)

**Change device in script:**
```python
generator = DiffusionStepCapture(device="cuda")
```

**Install CUDA-enabled PyTorch:**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

**Performance:**
- RTX 3060: ~1-2 min per sequence
- RTX 4090: ~30 sec per sequence

---

### CPU-Only

**Works on any system, but slow:**
```python
generator = DiffusionStepCapture(device="cpu")
```

**Optimization:**
- Reduce image size: `height=256, width=256`
- Reduce steps: `num_inference_steps=25`
- Generate overnight: Run script before bed

---

## Next Steps

Once setup is complete:
1. Read [`USAGE.md`](USAGE.md) for how to customize prompts and settings
2. Read [`THEORY.md`](THEORY.md) for conceptual background
3. Experiment with different prompts and parameters

---

## Getting Help

**Check logs:**
- Python errors: Read the full traceback
- Browser errors: Open Developer Tools (F12) → Console

**Common issues:**
- 90% are path/permission problems
- Check file paths are correct
- Make sure virtual environment is activated
- Verify files were actually created

**Still stuck?**
- Check GitHub issues (if this becomes a public repo)
- Review code comments (scripts are heavily documented)
