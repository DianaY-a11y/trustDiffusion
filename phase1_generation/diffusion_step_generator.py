"""
Diffusion Step Generator
Phase 1: Generate and save all intermediate steps from a diffusion model

This script captures the "invisible" process of diffusion models,
saving each denoising step to visualize the model's "thinking."
"""

import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import json
import os
from datetime import datetime
from pathlib import Path
import numpy as np


class DiffusionStepCapture:
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5", device="mps"):
        """
        Initialize the diffusion model with step-by-step capture capabilities.

        Args:
            model_id: HuggingFace model identifier
            device: "cuda", "mps" (for Mac M1/M2), or "cpu"
        """
        print(f"Loading model: {model_id}")
        self.device = device

        # Load the pipeline
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            safety_checker=None  # Disable for artistic freedom
        )
        self.pipe = self.pipe.to(device)

        # Storage for intermediate steps
        self.intermediate_images = []
        self.metadata = []

    def step_callback(self, step, timestep, latents):
        """
        Callback function that captures each denoising step.
        This is where the "invisible" becomes visible.
        """
        # Decode latents to image
        with torch.no_grad():
            # Scale and decode
            latents_scaled = 1 / 0.18215 * latents
            image = self.pipe.vae.decode(latents_scaled).sample

            # Convert to PIL Image
            image = (image / 2 + 0.5).clamp(0, 1)
            image = image.cpu().permute(0, 2, 3, 1).numpy()
            image = (image * 255).round().astype("uint8")
            pil_image = Image.fromarray(image[0])

        # Store the image and metadata
        self.intermediate_images.append(pil_image)

        # Calculate noise variance (approximation)
        noise_variance = float(latents.std().cpu().numpy())

        self.metadata.append({
            "step": step,
            "timestep": int(timestep),
            "noise_variance": noise_variance,
            "timestamp": datetime.now().isoformat()
        })

        print(f"  Step {step}: timestep={timestep}, noise_var={noise_variance:.4f}")

        return latents  # Return latents for pipeline to continue

    def generate_sequence(
        self,
        prompt,
        output_dir,
        num_inference_steps=50,
        guidance_scale=7.5,
        seed=None,
        negative_prompt="",
        height=512,
        width=512
    ):
        """
        Generate a complete diffusion sequence with all intermediate steps saved.

        Args:
            prompt: Text prompt for generation
            output_dir: Directory to save sequence
            num_inference_steps: Number of denoising steps (more = slower but smoother)
            guidance_scale: How closely to follow prompt (higher = more literal, can cause oversaturation)
            seed: Random seed for reproducibility
            negative_prompt: What to avoid in the image
        """
        # Reset storage
        self.intermediate_images = []
        self.metadata = []

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Set seed for reproducibility
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)
        else:
            generator = None
            seed = torch.randint(0, 2**32, (1,)).item()

        print(f"\nGenerating: '{prompt}'")
        print(f"Steps: {num_inference_steps}, Guidance: {guidance_scale}, Seed: {seed}")

        # Generate with callback
        # Note: callback is called during denoising loop
        output = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator,
            height=height,
            width=width,
            callback=self.step_callback,
            callback_steps=1  # Capture every step
        )

        # Save all intermediate images
        print(f"\nSaving {len(self.intermediate_images)} intermediate frames...")
        for i, img in enumerate(self.intermediate_images):
            img.save(output_path / f"step_{i:04d}.png")

        # Save final image
        final_image = output.images[0]
        final_image.save(output_path / "final.png")

        # Save metadata
        full_metadata = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "seed": seed,
            "height": height,
            "width": width,
            "generated_at": datetime.now().isoformat(),
            "steps": self.metadata
        }

        with open(output_path / "metadata.json", "w") as f:
            json.dump(full_metadata, f, indent=2)

        print(f"✓ Sequence saved to: {output_path}")

        return final_image, self.intermediate_images, full_metadata


def main():
    """
    Example usage: Generate sequences with different "failure modes"
    to reveal the model's interpretive process.
    """

    # Initialize generator
    # Use "mps" for Mac M1/M2, "cuda" for NVIDIA GPU, "cpu" for CPU
    generator = DiffusionStepCapture(device="mps")

    # Base output directory
    base_output = Path("../assets/generated_sequences")

    # Experiment 1: Normal generation
    print("\n" + "="*60)
    print("EXPERIMENT 1: Standard generation")
    print("="*60)
    generator.generate_sequence(
        prompt="a protest in a city square, dreamlike lighting, chaos and hope",
        output_dir=base_output / "01_standard",
        num_inference_steps=50,
        guidance_scale=7.5,
        seed=42
    )

    # Experiment 2: Low steps (incomplete formation)
    print("\n" + "="*60)
    print("EXPERIMENT 2: Low steps - Arrested development")
    print("="*60)
    generator.generate_sequence(
        prompt="a protest in a city square, dreamlike lighting, chaos and hope",
        output_dir=base_output / "02_low_steps",
        num_inference_steps=15,  # Much fewer steps
        guidance_scale=7.5,
        seed=42
    )

    # Experiment 3: High guidance (oversaturated interpretation)
    print("\n" + "="*60)
    print("EXPERIMENT 3: High guidance - Over-interpretation")
    print("="*60)
    generator.generate_sequence(
        prompt="a protest in a city square, dreamlike lighting, chaos and hope",
        output_dir=base_output / "03_high_guidance",
        num_inference_steps=50,
        guidance_scale=20.0,  # Very high guidance
        seed=42
    )

    # Experiment 4: Paradoxical prompt (confusion)
    print("\n" + "="*60)
    print("EXPERIMENT 4: Paradoxical prompt - Model confusion")
    print("="*60)
    generator.generate_sequence(
        prompt="transparent concrete building, frozen fire, liquid architecture",
        output_dir=base_output / "04_paradox",
        num_inference_steps=50,
        guidance_scale=7.5,
        seed=42
    )

    print("\n" + "="*60)
    print("All experiments complete!")
    print("="*60)


if __name__ == "__main__":
    main()
