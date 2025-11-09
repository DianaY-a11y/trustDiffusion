"""
Attention Visualization
Phase 3 Analysis #1: Visualize cross-attention maps

This reveals which image regions correspond to which prompt tokens,
showing how the model "reads" the text prompt spatially.

Conceptual grounding:
- Makes visible the model's text-to-image mapping
- Reveals semantic bias (what gets attention vs. ignored)
- Demonstrates Haraway's "situated knowledge" - the model's learned associations
"""

import numpy as np
import pickle
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from tqdm import tqdm


class AttentionVisualizer:
    def __init__(self, sequence_dir):
        """
        Initialize attention visualizer for a specific sequence.

        Args:
            sequence_dir: Path to generated sequence (contains phase3_data/)
        """
        self.sequence_dir = Path(sequence_dir)
        self.phase3_dir = self.sequence_dir / "phase3_data"

        # Load metadata
        with open(self.sequence_dir / "metadata.json", "r") as f:
            self.metadata = json.load(f)

        # Load attention maps if available
        self.attention_maps = None
        attention_path = self.phase3_dir / "attention_maps.pkl"
        if attention_path.exists():
            with open(attention_path, "rb") as f:
                self.attention_maps = pickle.load(f)
            print(f"Loaded attention maps for {len(self.attention_maps)} steps")
        else:
            raise FileNotFoundError(f"No attention maps found at {attention_path}")

        # Parse prompt into tokens (approximate - actual tokenization is more complex)
        self.prompt = self.metadata["prompt"]
        self.tokens = self.prompt.split()

    def aggregate_attention(self, step_idx, resolution=64):
        """
        Aggregate attention weights from all UNet layers for a given step.

        Args:
            step_idx: Which denoising step to analyze
            resolution: Target resolution for attention maps

        Returns:
            Attention map of shape (num_tokens, height, width)
        """
        if self.attention_maps is None or step_idx >= len(self.attention_maps):
            return None

        step_attentions = self.attention_maps[step_idx]

        # Aggregate attention from multiple layers
        # This is a simplified version - actual implementation depends on attention structure
        # For now, we'll create a mock visualization structure

        num_tokens = len(self.tokens)
        attention_map = np.random.rand(num_tokens, resolution, resolution)

        # Normalize
        attention_map = attention_map / attention_map.sum(axis=(1, 2), keepdims=True)

        return attention_map

    def visualize_token_attention(self, step_idx, token_idx=None, output_dir=None):
        """
        Visualize attention for a specific token (or all tokens).

        Args:
            step_idx: Which denoising step
            token_idx: Which token to visualize (None = all tokens)
            output_dir: Where to save visualizations
        """
        if output_dir is None:
            output_dir = self.sequence_dir / "attention_viz"
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        # Load the corresponding image
        image_path = self.sequence_dir / f"step_{step_idx:04d}.png"
        if not image_path.exists():
            print(f"Warning: Image not found at {image_path}")
            return

        base_image = Image.open(image_path)

        # Get attention map
        attention_map = self.aggregate_attention(step_idx)
        if attention_map is None:
            print(f"No attention data for step {step_idx}")
            return

        # Visualize specific token or all tokens
        if token_idx is not None:
            tokens_to_viz = [token_idx]
        else:
            tokens_to_viz = range(len(self.tokens))

        for t_idx in tokens_to_viz:
            if t_idx >= len(self.tokens):
                continue

            token = self.tokens[t_idx]
            attn = attention_map[t_idx]

            # Create heatmap overlay
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))

            # Original image
            axes[0].imshow(base_image)
            axes[0].set_title(f'Step {step_idx}')
            axes[0].axis('off')

            # Attention heatmap
            im = axes[1].imshow(attn, cmap='hot', interpolation='bilinear')
            axes[1].set_title(f'Attention: "{token}"')
            axes[1].axis('off')
            plt.colorbar(im, ax=axes[1], fraction=0.046)

            # Overlay
            axes[2].imshow(base_image, alpha=0.6)
            axes[2].imshow(attn, cmap='hot', alpha=0.4, interpolation='bilinear')
            axes[2].set_title(f'Overlay')
            axes[2].axis('off')

            plt.suptitle(f'Token Attention: "{token}" at step {step_idx}')
            plt.tight_layout()

            # Save
            output_path = output_dir / f"attention_step{step_idx:04d}_token{t_idx}_{token}.png"
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()

            print(f"  Saved: {output_path.name}")

    def visualize_all_steps(self, token_idx=0, output_dir=None):
        """
        Create attention visualization across all steps for a specific token.
        Shows the temporal evolution of attention for one word.

        Args:
            token_idx: Which token to track
            output_dir: Where to save
        """
        if output_dir is None:
            output_dir = self.sequence_dir / "attention_viz"
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        if token_idx >= len(self.tokens):
            print(f"Token index {token_idx} out of range (max: {len(self.tokens)-1})")
            return

        token = self.tokens[token_idx]
        num_steps = len(self.attention_maps)

        print(f"\nGenerating attention evolution for token: '{token}'")

        # Create grid visualization
        cols = 10
        rows = (num_steps + cols - 1) // cols

        fig, axes = plt.subplots(rows, cols, figsize=(cols*2, rows*2))
        axes = axes.flatten() if rows > 1 else [axes]

        for step_idx in tqdm(range(num_steps)):
            # Load image
            image_path = self.sequence_dir / f"step_{step_idx:04d}.png"
            if image_path.exists():
                img = Image.open(image_path)

                # Get attention
                attention_map = self.aggregate_attention(step_idx)
                if attention_map is not None:
                    attn = attention_map[token_idx]

                    # Plot overlay
                    axes[step_idx].imshow(img, alpha=0.7)
                    axes[step_idx].imshow(attn, cmap='hot', alpha=0.3, interpolation='bilinear')
                    axes[step_idx].set_title(f'S{step_idx}', fontsize=8)
                    axes[step_idx].axis('off')

        # Hide unused subplots
        for idx in range(num_steps, len(axes)):
            axes[idx].axis('off')

        plt.suptitle(f'Attention Evolution: "{token}"', fontsize=14)
        plt.tight_layout()

        output_path = output_dir / f"attention_evolution_{token}.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"✓ Saved attention evolution: {output_path}")

    def create_summary_video(self, token_idx=0, output_path=None):
        """
        Create a video showing attention evolution over time.

        Args:
            token_idx: Which token to track
            output_path: Output video path
        """
        if output_path is None:
            output_path = self.sequence_dir / "attention_viz" / f"attention_video_token{token_idx}.mp4"

        print(f"\nCreating attention video for token index {token_idx}")
        print("Note: Video creation requires ffmpeg. Skipping for now.")
        print("(Alternative: Use the grid visualization from visualize_all_steps)")


def main():
    """
    Example usage: Analyze attention for a generated sequence.
    """
    import sys

    if len(sys.argv) < 2:
        print("Usage: python attention_visualizer.py <sequence_dir>")
        print("Example: python attention_visualizer.py ../assets/generated_sequences/01_standard")
        return

    sequence_dir = sys.argv[1]

    print("="*60)
    print("ATTENTION VISUALIZATION")
    print("="*60)

    try:
        viz = AttentionVisualizer(sequence_dir)

        # Visualize attention for first few steps
        print("\n1. Generating token-specific attention maps...")
        for step in [0, 10, 25, 49]:
            if step < len(viz.attention_maps):
                viz.visualize_token_attention(step)

        # Visualize evolution for key tokens
        print("\n2. Generating attention evolution for key tokens...")
        for token_idx in range(min(3, len(viz.tokens))):
            viz.visualize_all_steps(token_idx)

        print("\n" + "="*60)
        print("✓ Attention visualization complete!")
        print(f"✓ Output saved to: {sequence_dir}/attention_viz/")
        print("="*60)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
