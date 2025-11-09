# Diffusion Visualization Installation

**Making the Invisible Visible: An Interactive Exploration of AI Image Generation**

This project transforms the hidden computational process of diffusion models into a visible, poetic experience. Instead of just showing final outputs, it reveals the model's "thinking" — the gradual emergence from noise to form, including its mistakes, misunderstandings, and unique interpretive path.

---

## 🎯 Concept

Diffusion models (like Stable Diffusion) generate images through an iterative denoising process — starting from pure static and gradually clarifying structure, color, and meaning over many steps. This process is typically hidden from view.

This installation:
- **Captures** every intermediate step of generation
- **Visualizes** the model's "thought process" as it interprets prompts
- **Reveals** the aesthetic richness of "failure modes" (incomplete generation, over-interpretation, confusion)
- **Enables** interactive exploration through scrubbing, playback, and comparative viewing

### Theoretical Framework
Inspired by:
- **Walter Benjamin**: Mechanical reproduction and the aura of images
- **Vilém Flusser**: Making the apparatus visible
- **Donna Haraway**: Situated knowledges and partial perspectives

---

## 📁 Project Structure

```
diffusion-visualization-installation/
│
├── phase1_generation/              # Python scripts for capturing diffusion steps
│   ├── diffusion_step_generator.py # Main generation script (enhanced for Phase 3)
│   └── requirements.txt            # Python dependencies
│
├── phase2_viewer/                  # Interactive web-based viewer
│   ├── index.html                  # Main HTML structure
│   ├── style.css                   # Styling
│   └── sketch.js                   # p5.js visualization logic
│
├── phase3_interpretability/        # ✨ NEW: Deep algorithmic analysis
│   ├── attention_visualizer.py    # Token-to-region mapping
│   ├── semantic_emergence.py      # When concepts become recognizable
│   ├── noise_decomposition.py     # Latent space evolution
│   ├── token_attribution.py       # Which words matter most
│   ├── analyze_all.py             # Run all analyses
│   ├── requirements.txt           # Additional dependencies
│   └── README.md                  # Phase 3 usage guide
│
├── assets/
│   ├── generated_sequences/        # Output from phase1 (image sequences + metadata)
│   └── metadata/                   # Additional metadata files
│
├── docs/                           # Documentation and research
│   ├── SETUP.md                    # Detailed setup instructions
│   ├── USAGE.md                    # How to use each component
│   └── THEORY.md                   # Conceptual framework
│
└── README.md                       # This file
```

---

## 🚀 Quick Start

### Phase 1: Generate Diffusion Sequences

**Prerequisites:**
- Python 3.9+
- GPU recommended (NVIDIA with CUDA, or Apple Silicon with MPS)
- ~10GB disk space for model + outputs

**Installation:**
```bash
cd phase1_generation
pip install -r requirements.txt
```

**First Run:**
```bash
python diffusion_step_generator.py
```

This will:
1. Download Stable Diffusion v1.5 (first run only, ~4GB)
2. Generate 4 experimental sequences with different "failure modes"
3. Save all intermediate steps + metadata to `assets/generated_sequences/`

**Expected output:**
```
assets/generated_sequences/
├── 01_standard/
│   ├── step_0000.png ... step_0049.png
│   ├── final.png
│   └── metadata.json
├── 02_low_steps/
├── 03_high_guidance/
└── 04_paradox/
```

---

### Phase 2: Interactive Viewer

**Prerequisites:**
- Modern web browser (Chrome, Firefox, Safari)
- Local web server (for loading images)

**Running the viewer:**

**Option A: Simple Python server**
```bash
cd phase2_viewer
python -m http.server 8000
```
Then open: `http://localhost:8000`

**Option B: VS Code Live Server**
- Install "Live Server" extension
- Right-click `index.html` → "Open with Live Server"

**Features:**
- ⏯️ Play/pause animation through diffusion steps
- 🎚️ Scrub through individual frames
- 📊 View metadata (step #, noise variance, prompt details)
- 🔍 Compare different generation modes
- ⌨️ Keyboard shortcuts (space = play/pause, arrows = step)

---

### Phase 3: Deep Interpretability Analysis ✨ NEW

**Prerequisites:**
- Modern Python 3.9+
- Sequences generated with enhanced Phase 1 (captures additional data)

**Installation:**
```bash
cd phase3_interpretability
pip install -r requirements.txt
```

**Quick Run:**
```bash
# Run all analyses (skip expensive token attribution)
python analyze_all.py ../assets/generated_sequences/01_standard --skip-attribution
```

**What it analyzes:**
- 🎯 **Attention maps** - Which image regions correspond to which prompt words
- 📈 **Semantic emergence** - When concepts become recognizable (uses CLIP)
- 🌀 **Noise decomposition** - Latent space evolution and denoising trajectory
- 🔤 **Token attribution** - Which words have the most influence (optional, slow)

**Output:**
- Attention heatmaps and evolution visualizations
- Emergence curves and timing data
- Latent space trajectory plots
- Word importance rankings

**See `phase3_interpretability/README.md` for detailed usage**

---

## 🎨 The Four Experimental Modes

### 1. Standard Generation
**Normal diffusion process** — 50 steps, moderate guidance
Shows the "intended" behavior of the model

### 2. Low Steps (Arrested Development)
**Only 15 denoising steps** instead of 50
Reveals half-formed imagery, dreamlike incompleteness

### 3. High Guidance (Over-interpretation)
**Guidance scale = 20** (normal is 7.5)
Model over-commits to prompt → oversaturated, melted aesthetic

### 4. Paradoxical Prompt
**Contradictory concepts**: "transparent concrete," "frozen fire"
Forces model confusion → surreal hybrids, impossible objects

---

## 🛠️ Customization

### Generate Your Own Sequences

Edit `phase1_generation/diffusion_step_generator.py`:

```python
generator.generate_sequence(
    prompt="your prompt here",
    output_dir=base_output / "custom_sequence",
    num_inference_steps=50,      # Lower = more incomplete
    guidance_scale=7.5,           # Higher = more oversaturated
    seed=42                       # Change for variation
)
```

### Modify Viewer Appearance

Edit `phase2_viewer/style.css`:
- Change color scheme (currently dark with cyan accents)
- Adjust layout for different screen sizes
- Customize overlay opacity and positioning

---

## 📊 Understanding the Metadata

Each sequence includes a `metadata.json` file:

```json
{
  "prompt": "a protest in a city square...",
  "num_inference_steps": 50,
  "guidance_scale": 7.5,
  "seed": 42,
  "steps": [
    {
      "step": 0,
      "timestep": 1000,
      "noise_variance": 0.9823,  // High = noisy, Low = clear
      "timestamp": "2025-11-08T..."
    },
    ...
  ]
}
```

**Key metrics:**
- **Timestep**: Diffusion scheduler's internal counter (1000 → 0)
- **Noise variance**: Measure of how "noisy" the latent space is
  - Step 0: ~1.0 (pure noise)
  - Final step: ~0.1 (mostly clear)

---

## 🔮 Roadmap

### Phase 3: Interpretability Layers ✅ COMPLETE
- [x] **Attention visualization** - Token-to-region mapping showing which words activate which areas
- [x] **Semantic emergence** - Tracking when concepts become recognizable using CLIP
- [x] **Noise decomposition** - Latent space evolution and denoising trajectory analysis
- [x] **Token attribution** - Which words have the most influence via ablation studies
- [x] **Unified orchestrator** - Run all analyses with one command

**See `phase3_interpretability/README.md` for usage guide**

### Phase 4: Installation Features (Future)
- [ ] Multi-screen setup guide
- [ ] Motion sensor integration
- [ ] Generative sound (noise → tone mapping)
- [ ] TouchDesigner version (for larger installations)
- [ ] Phase 2 + Phase 3 integration (interactive interpretability viewer)

---

## 🧠 Technical Details

### How Diffusion Models Work (Simplified)

1. **Start**: Random noise tensor (latent space)
2. **Loop**: For N steps (e.g., 50):
   - Predict noise in current image
   - Subtract predicted noise
   - Slightly denoise
3. **End**: Decode latent → pixel image

**What we capture:**
After each denoising step, we decode the latent to pixels and save it. This is normally invisible — you only see the final output.

### Why "Failures" Are Interesting

- **Low steps**: Stops denoising early → structure emerges but details are missing
- **High guidance**: Over-applies text conditioning → model "forces" interpretation
- **Paradoxes**: Conflicting semantic vectors → model averages impossible concepts

These aren't bugs — they're **windows into the model's interpretive process**.

---

## 🎓 For Exhibition

### Recommended Setup

**Hardware:**
- Projector or large monitor (1920x1080 or higher)
- Computer with GPU (for generation) or just CPU (for viewer)
- Optional: touchscreen for interaction

**Space:**
- Darkened room for projection
- Seating/standing area for 5-10 minute engagement
- Optional: headphones for sound (future phase)

### Artist Statement Template

> This installation reveals the hidden computation of AI image generation. Unlike traditional displays of AI art that show only polished outputs, this work exposes the iterative process by which diffusion models "dream" images into existence — including their mistakes, hesitations, and misunderstandings.
>
> By slowing down and making visible each denoising step, the work asks: What does it mean for a machine to "see"? What is lost when we only view the final, perfected image?
>
> The interactive interface invites viewers to scrub through the model's thought process, comparing how different constraints (speed, intensity, paradox) shape the emergence of form from noise.

---

## 📚 References & Further Reading

### Image Theory
- Walter Benjamin, *The Work of Art in the Age of Mechanical Reproduction* (1935)
- Vilém Flusser, *Towards a Philosophy of Photography* (1983)
- Donna Haraway, *Situated Knowledges* (1988)

### AI Art & Interpretation
- Trevor Paglen, *Invisible Images (Your Pictures Are Looking at You)* (2016)
- Kate Crawford & Trevor Paglen, *Excavating AI* (2019)

---

## 🤝 Contributing

This is an open-ended artistic research project. Ideas for extension:

- Alternative visualization methods (3D, VR)
- Different model architectures (DALL-E, Midjourney via API)
- Comparative cultural prompts
- Integration with other media (poetry, sound)

---

## 📄 License

MIT License - Free to use, modify, and exhibit with attribution.

---

## 💬 Questions?

This project is designed to be pedagogical and accessible. If you're stuck:

1. Check `docs/SETUP.md` for detailed installation help
2. Check `docs/USAGE.md` for usage examples
3. Review code comments (heavily documented)

---

**Created as an exploration of algorithmic interpretation and the aesthetics of computation.**

*"To see a world in a grain of sand... and eternity in an hour of diffusion steps."*
