# Quick Start Guide

**Get running in 3 steps:**

---

## Step 1: Install Dependencies (5-10 minutes)

```bash
cd diffusion-visualization-installation/phase1_generation

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install packages
pip install -r requirements.txt
```

**Expected time:** 5-10 minutes (downloads ~2-4GB)

---

## Step 2: Generate Your First Sequence (2-5 minutes on GPU)

```bash
# Still in phase1_generation directory, with venv activated
python diffusion_step_generator.py
```

**What happens:**
- First run: Downloads Stable Diffusion model (~4GB, one-time)
- Generates 4 experimental sequences
- Saves to `../assets/generated_sequences/`

**Expected time:**
- **GPU (NVIDIA/Apple Silicon):** 2-5 min per sequence (~15 min total)
- **CPU only:** 15-30 min per sequence (~2 hours total)

**Output:**
```
assets/generated_sequences/
├── 01_standard/          (50 images + metadata)
├── 02_low_steps/         (15 images + metadata)
├── 03_high_guidance/     (50 images + metadata)
└── 04_paradox/           (50 images + metadata)
```

---

## Step 3: View in Browser (30 seconds)

```bash
cd ../phase2_viewer
python -m http.server 8000
```

Open browser to: **http://localhost:8000**

**Expected result:**
- Interactive viewer interface
- Currently shows placeholder (no images loaded yet)

**To connect generated images:**
See full setup in [`docs/SETUP.md`](docs/SETUP.md) section "Phase 2: Step 4"

---

## Next Steps

**Customize prompts:**
Edit `phase1_generation/diffusion_step_generator.py` and change the prompt text

**Learn more:**
- [`README.md`](README.md) - Full project overview
- [`docs/USAGE.md`](docs/USAGE.md) - Detailed usage guide
- [`docs/THEORY.md`](docs/THEORY.md) - Conceptual framework

**Experiment:**
Try different parameters:
```python
generator.generate_sequence(
    prompt="your idea here",
    num_inference_steps=20,  # Lower = more incomplete
    guidance_scale=15.0,     # Higher = more intense
    seed=42
)
```

---

## Troubleshooting

**"No module named torch"**
→ Make sure virtual environment is activated: `source venv/bin/activate`

**"CUDA/MPS not available"**
→ Edit script, change to: `generator = DiffusionStepCapture(device="cpu")`

**Generation very slow**
→ Expected on CPU. Reduce steps: `num_inference_steps=25`

**Viewer shows "No images loaded"**
→ Normal! Images need to be connected (see docs/SETUP.md Phase 2)

---

## That's it!

You now have:
- ✅ Diffusion model installed
- ✅ 4 experimental sequences generated
- ✅ Interactive viewer running

**Happy experimenting!**
