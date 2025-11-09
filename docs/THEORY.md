# Theoretical Framework

**Conceptual grounding for the Diffusion Visualization Installation**

---

## Core Premise

Most AI-generated images are presented as *finished products* — clean outputs that conceal the computational process that created them. This installation inverts that relationship: **the process becomes the subject.**

By capturing and displaying every intermediate step of diffusion-based image generation, we make visible:
1. **The algorithm's interpretive labor** (how it "reads" text prompts)
2. **The aesthetics of incompleteness** (beauty in partial formation)
3. **The situatedness of machine vision** (no view is objective or final)

---

## Theoretical Foundations

### 1. Walter Benjamin: Mechanical Reproduction and Aura

**From:** *The Work of Art in the Age of Mechanical Reproduction* (1935)

**Key argument:**
Mechanical reproduction (photography, film) removes the "aura" of artworks — their unique presence in time and space.

**Relevance to this project:**
AI image generation is the latest form of mechanical reproduction. But by revealing its *process*, we restore a kind of aura:
- Each diffusion sequence is temporally unique (unfolding over steps)
- Each intermediate image is fleeting, imperfect, singular
- The "mistakes" are unreproducible (change parameters → different mistakes)

**Where Benjamin saw loss, we find recovery:**
> The revealed process becomes the new site of aura — not in the final image, but in the *becoming* of the image.

---

### 2. Vilém Flusser: The Apparatus and Technical Images

**From:** *Towards a Philosophy of Photography* (1983)

**Key argument:**
Photographs are not direct representations of reality — they are outputs of an apparatus (camera). To understand images, we must understand the apparatus that produces them.

**Flusser's challenge:**
> "The task is to make the apparatus visible."

**Relevance to this project:**
Diffusion models are black-box apparatuses. Users input text, receive images, but never see the computation.

**This installation makes the apparatus visible by:**
- Exposing intermediate states (what the model "sees" at each step)
- Displaying metadata (timesteps, noise levels, guidance strength)
- Comparing "failure modes" (how different settings alter interpretation)

**We literalize Flusser's imperative:**
The diffusion process is no longer hidden — it becomes the exhibition itself.

---

### 3. Donna Haraway: Situated Knowledges

**From:** *Situated Knowledges: The Science Question in Feminism and the Privilege of Partial Perspective* (1988)

**Key argument:**
All vision is partial, embodied, and situated. There is no "view from nowhere." Even scientific or technological vision is positioned within specific contexts.

**Relevance to this project:**
AI-generated images are often presented as neutral or objective ("the AI saw this"). But:
- The model was trained on specific datasets (bias)
- Prompts are interpreted through learned associations (culture)
- Generation parameters shape outputs (choices, not inevitabilities)

**Haraway's concept of "situated knowledges" applies to machines:**
> What does a diffusion model "know"? Only what its training corpus taught it.
> What does it "see" in a prompt? Only associations it has learned.

**This installation situates the model's vision:**
- By showing its hesitations (low-step incompleteness)
- By revealing its over-commitments (high-guidance oversaturation)
- By exposing its confusions (paradoxical prompts)

**The model's "view" is not objective — it is situated within:**
- Its training data (billions of image-text pairs)
- Its algorithmic constraints (denoising U-Net, CLIP text encoder)
- Our curatorial choices (which prompts, which parameters)

---

## Conceptual Threads

### A. The Aesthetics of Computation

**Traditional AI art:** Final outputs (clean, polished)
**This project:** Computational traces (messy, revealing)

We shift focus from *product* to *process* — similar to:
- **Process art** (1960s-70s): Hans Haacke, Robert Morris
- **Generative art**: Casey Reas, Marius Watz
- **Glitch aesthetics**: Rosa Menkman, Kim Asendorf

**But unique in:**
Diffusion models' process is invisible by default. We excavate it.

---

### B. Error as Insight

**In conventional use:**
- Errors = failures (to be fixed or discarded)
- "Good" output = high fidelity, prompt-following

**In this project:**
- Errors = windows into the model's interpretive process
- "Good" output = revelatory incompleteness

**Inspiration from:**
- **Glitch art**: Intentional corruption as aesthetic/critical strategy
- **Phenomenology of mistakes**: What do errors reveal about systems?
- **"Abraded" images** (Georges Didi-Huberman): Wear and damage as historical traces

**We embrace:**
- Oversaturation (over-interpretation as excess meaning-making)
- Arrested development (stopping before "resolution")
- Paradox (forcing impossible syntheses)

---

### C. Machine "Seeing" as Interpretation

**Naive view:**
AI models "recognize" or "represent" reality.

**Critical view (this project's stance):**
AI models *interpret* based on learned statistical patterns. Their "seeing" is:
- **Associative** (not representational)
- **Probabilistic** (not deterministic)
- **Cultural** (not universal)

**Example:**
Prompt: "a protest"
- Model doesn't "see" actual protests
- It synthesizes from thousands of protest photos in training data
- Output reflects *what protests looked like in its dataset* (bias toward Western urban protests)

**By showing the diffusion process:**
We see the model "deciding" — step by step — what "a protest" should look like.
This is not neutral vision. It's culturally-situated algorithmic interpretation.

---

### D. Temporality and Emergence

**Still images:** Single moment, frozen
**Video:** Continuous motion
**Diffusion sequences:** Discrete emergence

**This project introduces a unique temporality:**
- Not time-as-duration (video)
- But time-as-iteration (computational steps)

**Each step is:**
- A hypothesis (model's current guess)
- A revision (correcting previous noise prediction)
- A trace (evidence of interpretive labor)

**Philosophical parallel:**
- **Heidegger**: Truth as *aletheia* (unconcealment) — gradual revealing
- **Bergson**: Duration as qualitative change, not just quantity

**The diffusion process is a kind of algorithmic *becoming*:**
> The image is not "there" from the start. It emerges through iterative refinement.

---

## Critical Questions the Installation Raises

### 1. What does it mean for a machine to "interpret" a text prompt?
- Is it understanding? Association? Statistical pattern-matching?
- Where does "meaning" reside — in the prompt, the model, or the output?

### 2. Are diffusion models "creative" or "generative"?
- They don't invent from nothing (trained on existing images)
- But they synthesize novel combinations
- Is recombination creativity?

### 3. What is lost when we only see final AI outputs?
- The labor of computation (invisible)
- The contingency of results (could have been different)
- The biases embedded in training data (hidden)

### 4. Can revealing the process change how we relate to AI images?
- From passive consumption → critical engagement
- From "magic" → demystified computation
- From trust → situated skepticism

---

## Artistic Precedents and Dialogues

### AI Art with Process Focus

**Memo Akten, *Learning to See* (2017)**
- Trains neural networks on specific image sets
- Shows how models "learn" to see (loss curves, training epochs)
- Similar: Making invisible learning visible

**Refik Anadol, *Machine Hallucinations* (2019)**
- Visualizes latent space of GANs
- Projects high-dimensional data as abstract flows
- Different: Focuses on training data, not generation process

**Anna Ridler, *Mosaic Virus* (2018-19)**
- Hand-labels tulip dataset, trains GAN
- Reveals human labor behind "autonomous" AI
- Similar: Situating the model's "knowledge"

---

### Glitch & Error Aesthetics

**Rosa Menkman, *The Glitch Moment(um)* (2011)**
- Theorizes glitch as critical rupture
- Compression artifacts as truth about media
- Similar: Our "failures" reveal algorithmic truth

**Kim Asendorf, *Pixel Sorting* series**
- Deliberate corruption of images
- Reveals underlying data structures
- Similar: Making invisible processes visible

---

### Apparatus Theory

**Harun Farocki, *Eye/Machine* trilogy (2001-03)**
- Shows computer vision systems at work
- Military, industrial, surveillance contexts
- Similar: Revealing how machines "see"

**Trevor Paglen, *Invisible Images* (2016)**
- Images made by/for machines, not humans
- Questions autonomy of machine vision
- Different: We make machine vision human-legible

---

## Philosophical Implications

### Epistemology: What can we know through AI?

If AI models only recombine training data:
- They don't "know" the world, they know their *dataset*
- Outputs are **statistically plausible**, not **factually true**
- This installation reveals that plausibility is gradual, iterative, uncertain

**Lesson:**
AI "knowledge" is not direct access to reality — it's a curated, biased, probabilistic assemblage.

---

### Ontology: What kind of "thing" is a diffusion image?

- Not a photograph (no referent in reality)
- Not a painting (no human hand)
- Not a hallucination (deterministic given seed/prompt)

**Proposal:**
A diffusion image is a **computed interpretation** — synthesized from learned patterns.

**This installation shows:**
The image is not an object but a *process* — it exists in time, through steps.

---

### Ethics: Who is responsible for AI outputs?

- The model developer? (OpenAI, Stability AI)
- The dataset curator? (LAION, etc.)
- The user? (who writes the prompt)
- The algorithm itself? (autonomous decision-making)

**This installation distributes responsibility:**
- We see the model's "choices" (what it emphasizes at each step)
- But also our choices (parameters, prompts)
- And the training data's influence (what associations exist)

**No single agent is fully responsible.**
Responsibility is networked, distributed, situated.

---

## Curatorial Framing for Exhibition

### Possible Artist Statements

**Version 1: Accessible**
> "This installation slows down AI image generation to reveal its hidden process. Instead of showing finished images, we see the model 'thinking' — its gradual emergence from noise to form, including its mistakes and misunderstandings. By making this invisible computation visible, we ask: What does it mean for a machine to see?"

**Version 2: Critical**
> "Diffusion models are often presented as neutral tools that 'generate' images from text. But what is concealed in that generation? This work exposes the algorithmic labor — the iterative refinement, the probabilistic guesses, the culturally-situated associations — that produce seemingly autonomous images. The process is the subject."

**Version 3: Poetic**
> "An image dreaming itself into existence. A machine hesitating, over-committing, misunderstanding. Fifty steps from chaos to clarity — but is clarity the goal? Here, the beauty lies in incompleteness, in the visible traces of computation, in the moment before resolution."

---

### Wall Text for Exhibition

**Title:** *Seeing Through the Algorithm: Diffusion Process as Visible Thought*

**Description:**
> Artificial intelligence image generators create pictures by starting with random noise and iteratively "denoising" — predicting and removing disorder — until a coherent image emerges. This process typically happens invisibly, in milliseconds, hidden from the user.
>
> This installation makes the invisible visible. Each sequence captures all intermediate steps of the diffusion model's generation, revealing how it interprets text prompts and synthesizes images. Rather than presenting polished outputs, the work focuses on moments of incompleteness, over-interpretation, and algorithmic confusion.
>
> By slowing down and exposing the computational process, we see the model as an *interpreter* — not a neutral tool, but a culturally-situated system making probabilistic guesses based on learned patterns. The "mistakes" and hesitations become windows into how machines "see."

**Visitor Instructions:**
> Use the slider to move through the diffusion steps. Watch as form emerges from noise, structures coalesce, and meanings take shape. Notice where the model hesitates, over-commits, or creates impossible syntheses. These are not errors to be fixed — they are traces of algorithmic interpretation.

---

## Further Research Directions

### Technical Extensions
- **Attention visualization**: Where in the image does the model focus?
- **Latent space interpolation**: Blend between prompts mid-generation
- **Cross-model comparison**: Stable Diffusion vs. DALL-E vs. Midjourney

### Conceptual Extensions
- **Cultural bias exploration**: Same prompt, different model versions (trained on different data)
- **Language experiments**: Translate prompts, compare interpretations
- **Iterative feedback loops**: Feed outputs back as new inputs (drift analysis)

### Exhibition Formats
- **Large-scale projection**: Immersive, architectural
- **Multi-channel synchronization**: Side-by-side comparisons
- **Generative sound**: Map noise variance to audio (sonification)
- **VR/AR**: Navigate through 3D latent space

---

## Conclusion

This installation is not about celebrating or condemning AI. It's about **making visible what is usually invisible** — the interpretive labor of computation.

By revealing the diffusion process, we:
- Demystify "AI magic"
- Situate algorithmic vision as partial, biased, contingent
- Find aesthetic value in incompleteness and error
- Invite critical engagement with how machines "see"

**Ultimately, the question is:**
> What changes when we see *how* an image was made, not just *what* was made?

This installation proposes: **Everything.**

---

**References for this document:**

- Benjamin, Walter. *The Work of Art in the Age of Mechanical Reproduction* (1935)
- Flusser, Vilém. *Towards a Philosophy of Photography* (1983)
- Haraway, Donna. *Situated Knowledges* (1988)
- Menkman, Rosa. *The Glitch Moment(um)* (2011)
- Paglen, Trevor. *Invisible Images (Your Pictures Are Looking at You)* (2016)
- Crawford, Kate & Paglen, Trevor. *Excavating AI* (2019)
- Rombach et al. *High-Resolution Image Synthesis with Latent Diffusion Models* (2022)
