"""
Prompt Token Attribution
Phase 3 Analysis #4: Determine which prompt words have the most influence

This performs ablation studies to measure each word's contribution to the final image.
By systematically removing each word and comparing the result, we reveal semantic importance.

Conceptual grounding:
- Reveals the model's hierarchical interpretation of language
- Shows which concepts are central vs. peripheral
- Demonstrates how linguistic structure affects visual generation

WARNING: This is computationally expensive - requires N+1 generations per prompt.
"""

import numpy as np
from pathlib import Path
from PIL import Image
import json
import matplotlib.pyplot as plt
from tqdm import tqdm
import torch
import sys

# Add parent directory to path to import DiffusionStepCapture
sys.path.append(str(Path(__file__).parent.parent / "phase1_generation"))
from diffusion_step_generator import DiffusionStepCapture


class TokenAttributionAnalyzer:
    def __init__(self, original_sequence_dir, device="mps"):
        """
        Initialize token attribution analyzer.

        Args:
            original_sequence_dir: Path to the original generated sequence
            device: Device for generation ("cuda", "mps", or "cpu")
        """
        self.sequence_dir = Path(original_sequence_dir)
        self.device = device

        # Load metadata from original sequence
        with open(self.sequence_dir / "metadata.json", "r") as f:
            self.metadata = json.load(f)

        self.prompt = self.metadata["prompt"]
        self.tokens = self.prompt.split()
        self.seed = self.metadata["seed"]
        self.guidance_scale = self.metadata["guidance_scale"]
        self.num_inference_steps = self.metadata["num_inference_steps"]

        # Load original final image for comparison
        self.original_image = Image.open(self.sequence_dir / "final.png")

        print(f"Loaded original sequence: {self.sequence_dir}")
        print(f"Prompt: '{self.prompt}'")
        print(f"Tokens: {self.tokens}")

    def compute_image_similarity(self, img1, img2):
        """
        Compute similarity between two images using MSE.

        Args:
            img1, img2: PIL Images

        Returns:
            Similarity score (lower = more different)
        """
        # Convert to numpy arrays
        arr1 = np.array(img1, dtype=np.float32)
        arr2 = np.array(img2, dtype=np.float32)

        # Compute MSE
        mse = np.mean((arr1 - arr2) ** 2)

        return mse

    def generate_ablated_sequence(self, token_idx, output_dir=None):
        """
        Generate a sequence with one token removed from the prompt.

        Args:
            token_idx: Index of token to remove
            output_dir: Where to save (defaults to sequence_dir/ablation_study/)

        Returns:
            Final image, ablated prompt
        """
        if output_dir is None:
            output_dir = self.sequence_dir / "ablation_study"

        # Create ablated prompt
        ablated_tokens = [t for i, t in enumerate(self.tokens) if i != token_idx]
        ablated_prompt = " ".join(ablated_tokens)

        if not ablated_prompt.strip():
            ablated_prompt = "image"  # Fallback if prompt becomes empty

        print(f"\n  Generating without '{self.tokens[token_idx]}'...")
        print(f"  Ablated prompt: '{ablated_prompt}'")

        # Initialize generator
        generator = DiffusionStepCapture(device=self.device, capture_attention=False)

        # Generate with ablated prompt (using same seed for comparison)
        output_path = output_dir / f"ablation_token{token_idx}_{self.tokens[token_idx]}"

        final_image, _, _ = generator.generate_sequence(
            prompt=ablated_prompt,
            output_dir=output_path,
            num_inference_steps=self.num_inference_steps,
            guidance_scale=self.guidance_scale,
            seed=self.seed  # Use same seed for fair comparison
        )

        return final_image, ablated_prompt

    def run_attribution_study(self):
        """
        Run full attribution study: generate sequences with each token removed.

        Returns:
            Dictionary mapping token indices to divergence scores
        """
        print("\n" + "="*60)
        print("RUNNING TOKEN ATTRIBUTION STUDY")
        print(f"This will generate {len(self.tokens)} additional sequences")
        print("="*60)

        results = {}

        for token_idx in range(len(self.tokens)):
            print(f"\n[{token_idx+1}/{len(self.tokens)}] Ablating token: '{self.tokens[token_idx]}'")

            # Generate ablated sequence
            ablated_image, ablated_prompt = self.generate_ablated_sequence(token_idx)

            # Compute divergence from original
            divergence = self.compute_image_similarity(self.original_image, ablated_image)

            results[token_idx] = {
                "token": self.tokens[token_idx],
                "ablated_prompt": ablated_prompt,
                "divergence": divergence
            }

            print(f"  Divergence: {divergence:.2f}")

        return results

    def visualize_attribution_scores(self, results, output_path=None):
        """
        Visualize token importance as a bar chart.

        Args:
            results: Results from run_attribution_study()
            output_path: Where to save
        """
        if output_path is None:
            output_path = self.sequence_dir / "token_attribution_scores.png"

        # Extract data
        tokens = [results[i]["token"] for i in sorted(results.keys())]
        divergences = [results[i]["divergence"] for i in sorted(results.keys())]

        # Create bar chart
        fig, ax = plt.subplots(figsize=(12, 6))

        bars = ax.bar(range(len(tokens)), divergences, color='steelblue', alpha=0.7)

        # Highlight most important tokens
        max_div = max(divergences)
        for i, bar in enumerate(bars):
            if divergences[i] > max_div * 0.7:  # Top 30%
                bar.set_color('crimson')
                bar.set_alpha(0.8)

        ax.set_xlabel('Token')
        ax.set_ylabel('Divergence (Image Difference)')
        ax.set_title(f'Token Attribution: Which Words Matter Most?\n"{self.prompt}"')
        ax.set_xticks(range(len(tokens)))
        ax.set_xticklabels(tokens, rotation=45, ha='right')
        ax.grid(True, axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"\n✓ Saved attribution scores: {output_path}")

    def create_comparison_grid(self, results, output_path=None):
        """
        Create a visual grid comparing original vs. ablated images.

        Args:
            results: Results from run_attribution_study()
            output_path: Where to save
        """
        if output_path is None:
            output_path = self.sequence_dir / "token_attribution_grid.png"

        num_tokens = len(results)
        cols = 4
        rows = (num_tokens + cols) // cols  # +1 for original

        fig, axes = plt.subplots(rows, cols, figsize=(cols*3, rows*3))
        axes = axes.flatten() if rows > 1 else [axes]

        # Show original first
        axes[0].imshow(self.original_image)
        axes[0].set_title('ORIGINAL\n(full prompt)', fontsize=10, fontweight='bold')
        axes[0].axis('off')

        # Show ablations
        for i, token_idx in enumerate(sorted(results.keys())):
            token = results[token_idx]["token"]
            divergence = results[token_idx]["divergence"]

            # Load ablated image
            ablation_dir = self.sequence_dir / "ablation_study" / f"ablation_token{token_idx}_{token}"
            ablated_image_path = ablation_dir / "final.png"

            if ablated_image_path.exists():
                ablated_image = Image.open(ablated_image_path)
                axes[i+1].imshow(ablated_image)
                axes[i+1].set_title(f'WITHOUT "{token}"\nDiv: {divergence:.1f}', fontsize=9)
                axes[i+1].axis('off')

        # Hide unused subplots
        for idx in range(num_tokens + 1, len(axes)):
            axes[idx].axis('off')

        plt.suptitle(f'Token Attribution Grid\n"{self.prompt}"', fontsize=12)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"✓ Saved comparison grid: {output_path}")

    def export_attribution_data(self, results, output_path=None):
        """
        Export attribution results as JSON.

        Args:
            results: Results from run_attribution_study()
            output_path: Where to save
        """
        if output_path is None:
            output_path = self.sequence_dir / "phase3_data" / "token_attribution.json"

        output_path.parent.mkdir(exist_ok=True)

        # Prepare exportable data
        export_data = {
            "original_prompt": self.prompt,
            "tokens": self.tokens,
            "attribution_scores": results
        }

        with open(output_path, "w") as f:
            json.dump(export_data, f, indent=2)

        print(f"✓ Exported attribution data: {output_path}")


def main():
    """
    Example usage: Run token attribution analysis.
    """
    import sys

    if len(sys.argv) < 2:
        print("Usage: python token_attribution.py <sequence_dir> [device]")
        print("Example: python token_attribution.py ../assets/generated_sequences/01_standard mps")
        print("\nWARNING: This will regenerate the sequence N times (once per token).")
        print("This can take significant time and compute resources.")
        return

    sequence_dir = sys.argv[1]
    device = sys.argv[2] if len(sys.argv) > 2 else "mps"

    print("="*60)
    print("TOKEN ATTRIBUTION ANALYSIS")
    print("="*60)

    try:
        analyzer = TokenAttributionAnalyzer(sequence_dir, device=device)

        # Run attribution study
        print("\n1. Running attribution study (this will take a while)...")
        results = analyzer.run_attribution_study()

        # Visualize scores
        print("\n2. Visualizing attribution scores...")
        analyzer.visualize_attribution_scores(results)

        # Create comparison grid
        print("\n3. Creating comparison grid...")
        analyzer.create_comparison_grid(results)

        # Export data
        print("\n4. Exporting attribution data...")
        analyzer.export_attribution_data(results)

        print("\n" + "="*60)
        print("✓ Token attribution analysis complete!")
        print("="*60)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
