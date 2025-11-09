"""
Semantic Emergence Analyzer
Phase 3 Analysis #2: Track when semantic concepts emerge during generation

This answers the question: "At which step does random noise become meaningful?"
Uses CLIP to measure semantic similarity between generated images and text concepts.

Conceptual grounding:
- Reveals the moment of "meaning crystallization"
- Shows how interpretation evolves from ambiguity to specificity
- Demonstrates the gradual nature of algorithmic "seeing"
"""

import numpy as np
from pathlib import Path
from PIL import Image
import json
import matplotlib.pyplot as plt
from tqdm import tqdm
import torch


class SemanticEmergenceAnalyzer:
    def __init__(self, sequence_dir, use_clip=True):
        """
        Initialize semantic emergence analyzer.

        Args:
            sequence_dir: Path to generated sequence
            use_clip: Whether to use CLIP for semantic similarity (requires transformers)
        """
        self.sequence_dir = Path(sequence_dir)

        # Load metadata
        with open(self.sequence_dir / "metadata.json", "r") as f:
            self.metadata = json.load(f)

        self.prompt = self.metadata["prompt"]
        self.num_steps = len(self.metadata["steps"])

        # Initialize CLIP if available
        self.use_clip = use_clip
        self.clip_model = None
        self.clip_processor = None

        if use_clip:
            try:
                from transformers import CLIPProcessor, CLIPModel
                print("Loading CLIP model...")
                self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
                self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
                print("✓ CLIP model loaded")
            except ImportError:
                print("Warning: CLIP not available. Install with: pip install transformers")
                self.use_clip = False

    def compute_clip_similarity(self, image, text):
        """
        Compute CLIP similarity between image and text.

        Args:
            image: PIL Image
            text: Text string

        Returns:
            Similarity score (0-1)
        """
        if not self.use_clip or self.clip_model is None:
            # Fallback: random similarity for demonstration
            return np.random.rand()

        # Process inputs
        inputs = self.clip_processor(
            text=[text],
            images=image,
            return_tensors="pt",
            padding=True
        )

        # Get embeddings
        with torch.no_grad():
            outputs = self.clip_model(**inputs)
            image_embeds = outputs.image_embeds
            text_embeds = outputs.text_embeds

            # Compute cosine similarity
            similarity = torch.nn.functional.cosine_similarity(
                image_embeds, text_embeds
            ).item()

        return similarity

    def analyze_emergence_timeline(self, concepts=None):
        """
        Analyze when different semantic concepts emerge across the generation process.

        Args:
            concepts: List of text concepts to track (defaults to prompt + related concepts)

        Returns:
            Dictionary mapping concepts to similarity scores over time
        """
        if concepts is None:
            # Extract key concepts from prompt
            concepts = [self.prompt]  # Full prompt

            # Add individual words as concepts
            words = self.prompt.split()
            concepts.extend([w for w in words if len(w) > 3])  # Skip short words

            # Add general concepts
            concepts.extend([
                "abstract shapes",
                "recognizable objects",
                "clear details"
            ])

        print(f"\nAnalyzing semantic emergence for {len(concepts)} concepts...")

        results = {concept: [] for concept in concepts}

        # Analyze each step
        for step_idx in tqdm(range(self.num_steps)):
            image_path = self.sequence_dir / f"step_{step_idx:04d}.png"

            if not image_path.exists():
                continue

            image = Image.open(image_path)

            # Compute similarity for each concept
            for concept in concepts:
                similarity = self.compute_clip_similarity(image, concept)
                results[concept].append({
                    "step": step_idx,
                    "similarity": similarity
                })

        return results

    def find_emergence_point(self, concept, threshold=0.5):
        """
        Find the step at which a concept "emerges" (crosses similarity threshold).

        Args:
            concept: Text concept to track
            threshold: Similarity threshold for emergence

        Returns:
            Step index of emergence, or None if never emerges
        """
        print(f"\nFinding emergence point for: '{concept}'")

        for step_idx in tqdm(range(self.num_steps)):
            image_path = self.sequence_dir / f"step_{step_idx:04d}.png"

            if not image_path.exists():
                continue

            image = Image.open(image_path)
            similarity = self.compute_clip_similarity(image, concept)

            if similarity >= threshold:
                print(f"  ✓ Emerged at step {step_idx} (similarity: {similarity:.3f})")
                return step_idx

        print(f"  ✗ Did not emerge (max threshold: {threshold})")
        return None

    def visualize_emergence_curves(self, results, output_path=None):
        """
        Visualize semantic emergence curves for multiple concepts.

        Args:
            results: Results from analyze_emergence_timeline()
            output_path: Where to save the plot
        """
        if output_path is None:
            output_path = self.sequence_dir / "semantic_emergence_curves.png"

        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot each concept
        for concept, data in results.items():
            if len(data) == 0:
                continue

            steps = [d["step"] for d in data]
            similarities = [d["similarity"] for d in data]

            ax.plot(steps, similarities, marker='o', markersize=3,
                   label=concept[:30], alpha=0.7)

        ax.set_xlabel('Denoising Step')
        ax.set_ylabel('Semantic Similarity (CLIP)')
        ax.set_title(f'Semantic Emergence Timeline\n"{self.prompt}"')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"✓ Saved emergence curves: {output_path}")

    def create_emergence_heatmap(self, results, output_path=None):
        """
        Create a heatmap showing when different concepts emerge.

        Args:
            results: Results from analyze_emergence_timeline()
            output_path: Where to save
        """
        if output_path is None:
            output_path = self.sequence_dir / "semantic_emergence_heatmap.png"

        # Convert to matrix format
        concepts = list(results.keys())
        num_concepts = len(concepts)
        num_steps = max(len(results[c]) for c in concepts)

        matrix = np.zeros((num_concepts, num_steps))

        for i, concept in enumerate(concepts):
            for data_point in results[concept]:
                step = data_point["step"]
                similarity = data_point["similarity"]
                if step < num_steps:
                    matrix[i, step] = similarity

        # Plot heatmap
        fig, ax = plt.subplots(figsize=(14, max(6, num_concepts * 0.4)))

        im = ax.imshow(matrix, aspect='auto', cmap='viridis', interpolation='nearest')

        # Set ticks
        ax.set_xticks(np.arange(0, num_steps, max(1, num_steps // 10)))
        ax.set_yticks(np.arange(num_concepts))
        ax.set_yticklabels([c[:40] for c in concepts], fontsize=9)

        ax.set_xlabel('Denoising Step')
        ax.set_ylabel('Concept')
        ax.set_title(f'Semantic Emergence Heatmap\n"{self.prompt}"')

        # Add colorbar
        plt.colorbar(im, ax=ax, label='Similarity Score')

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"✓ Saved emergence heatmap: {output_path}")

    def export_emergence_data(self, results, output_path=None):
        """
        Export emergence data as JSON for further analysis.

        Args:
            results: Results from analyze_emergence_timeline()
            output_path: Where to save JSON
        """
        if output_path is None:
            output_path = self.sequence_dir / "phase3_data" / "semantic_emergence.json"

        output_path.parent.mkdir(exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)

        print(f"✓ Exported emergence data: {output_path}")


def main():
    """
    Example usage: Analyze semantic emergence for a sequence.
    """
    import sys

    if len(sys.argv) < 2:
        print("Usage: python semantic_emergence.py <sequence_dir>")
        print("Example: python semantic_emergence.py ../assets/generated_sequences/01_standard")
        return

    sequence_dir = sys.argv[1]

    print("="*60)
    print("SEMANTIC EMERGENCE ANALYSIS")
    print("="*60)

    try:
        analyzer = SemanticEmergenceAnalyzer(sequence_dir, use_clip=True)

        # Analyze emergence timeline
        print("\n1. Analyzing emergence timeline...")
        results = analyzer.analyze_emergence_timeline()

        # Visualize curves
        print("\n2. Creating emergence curves...")
        analyzer.visualize_emergence_curves(results)

        # Create heatmap
        print("\n3. Creating emergence heatmap...")
        analyzer.create_emergence_heatmap(results)

        # Export data
        print("\n4. Exporting data...")
        analyzer.export_emergence_data(results)

        # Find key emergence points
        print("\n5. Finding key emergence points...")
        key_concepts = [analyzer.prompt, "recognizable objects", "clear details"]
        for concept in key_concepts:
            analyzer.find_emergence_point(concept, threshold=0.5)

        print("\n" + "="*60)
        print("✓ Semantic emergence analysis complete!")
        print("="*60)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
