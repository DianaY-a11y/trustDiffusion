"""
Noise Decomposition Analysis
Phase 3 Analysis #3: Analyze predicted noise vs. actual denoising

This reveals the model's prediction accuracy at each step,
showing where the model is "confident" vs. "uncertain" in its interpretation.

Conceptual grounding:
- Visualizes the model's internal reasoning (what it thinks needs to change)
- Shows prediction accuracy over time (early steps = high uncertainty, late = refinement)
- Demonstrates the iterative nature of algorithmic interpretation
"""

import numpy as np
from pathlib import Path
from PIL import Image
import json
import matplotlib.pyplot as plt
from tqdm import tqdm


class NoiseDecompositionAnalyzer:
    def __init__(self, sequence_dir):
        """
        Initialize noise decomposition analyzer.

        Args:
            sequence_dir: Path to generated sequence
        """
        self.sequence_dir = Path(sequence_dir)
        self.phase3_dir = self.sequence_dir / "phase3_data"

        # Load metadata
        with open(self.sequence_dir / "metadata.json", "r") as f:
            self.metadata = json.load(f)

        # Load latent vectors
        latents_path = self.phase3_dir / "latent_vectors.npy"
        if latents_path.exists():
            self.latent_vectors = np.load(latents_path)
            print(f"Loaded latent vectors: {self.latent_vectors.shape}")
        else:
            raise FileNotFoundError(f"No latent vectors found at {latents_path}")

    def compute_step_changes(self):
        """
        Compute the magnitude of change at each denoising step.
        This shows how much the latent representation changes.

        Returns:
            Array of change magnitudes for each step
        """
        changes = []

        for i in range(1, len(self.latent_vectors)):
            prev_latent = self.latent_vectors[i-1]
            curr_latent = self.latent_vectors[i]

            # Compute L2 distance
            change = np.linalg.norm(curr_latent - prev_latent)
            changes.append(change)

        return np.array(changes)

    def compute_noise_variance_trajectory(self):
        """
        Extract noise variance over time from metadata.

        Returns:
            Array of noise variance values
        """
        return np.array([step["noise_variance"] for step in self.metadata["steps"]])

    def visualize_denoising_trajectory(self, output_path=None):
        """
        Visualize the denoising trajectory showing noise reduction over time.

        Args:
            output_path: Where to save the plot
        """
        if output_path is None:
            output_path = self.sequence_dir / "noise_decomposition_trajectory.png"

        # Get data
        noise_variance = self.compute_noise_variance_trajectory()
        step_changes = self.compute_step_changes()

        # Create plot
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

        # Plot 1: Noise variance over time
        steps = range(len(noise_variance))
        ax1.plot(steps, noise_variance, 'b-', linewidth=2, marker='o', markersize=3)
        ax1.set_xlabel('Denoising Step')
        ax1.set_ylabel('Noise Variance')
        ax1.set_title('Noise Variance Trajectory')
        ax1.grid(True, alpha=0.3)

        # Plot 2: Step-wise changes
        ax2.plot(range(len(step_changes)), step_changes, 'r-', linewidth=2, marker='o', markersize=3)
        ax2.set_xlabel('Denoising Step')
        ax2.set_ylabel('Change Magnitude')
        ax2.set_title('Magnitude of Latent Changes Between Steps')
        ax2.grid(True, alpha=0.3)

        # Plot 3: Combined view
        ax3_twin = ax3.twinx()

        ax3.plot(steps, noise_variance, 'b-', linewidth=2, label='Noise Variance', alpha=0.7)
        ax3_twin.plot(range(len(step_changes)), step_changes, 'r-', linewidth=2, label='Change Magnitude', alpha=0.7)

        ax3.set_xlabel('Denoising Step')
        ax3.set_ylabel('Noise Variance', color='b')
        ax3_twin.set_ylabel('Change Magnitude', color='r')
        ax3.set_title('Combined: Noise Reduction vs. Latent Changes')
        ax3.grid(True, alpha=0.3)

        # Add legends
        lines1, labels1 = ax3.get_legend_handles_labels()
        lines2, labels2 = ax3_twin.get_legend_handles_labels()
        ax3.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

        plt.suptitle(f'Noise Decomposition Analysis\n"{self.metadata["prompt"]}"', fontsize=12)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"✓ Saved denoising trajectory: {output_path}")

    def identify_critical_steps(self, threshold_percentile=75):
        """
        Identify steps where the most significant changes occur.

        Args:
            threshold_percentile: Percentile threshold for "significant" changes

        Returns:
            List of step indices with significant changes
        """
        step_changes = self.compute_step_changes()
        threshold = np.percentile(step_changes, threshold_percentile)

        critical_steps = np.where(step_changes > threshold)[0]

        print(f"\nCritical steps (>{threshold_percentile}th percentile):")
        for step in critical_steps:
            print(f"  Step {step}: change magnitude = {step_changes[step]:.4f}")

        return critical_steps

    def visualize_latent_space_evolution(self, output_path=None, sample_steps=10):
        """
        Visualize how the latent space evolves using PCA projection.

        Args:
            output_path: Where to save
            sample_steps: Number of steps to sample for visualization
        """
        if output_path is None:
            output_path = self.sequence_dir / "latent_space_evolution.png"

        # Sample steps
        total_steps = len(self.latent_vectors)
        step_indices = np.linspace(0, total_steps-1, sample_steps, dtype=int)

        # Flatten latents for PCA
        latents_flat = [self.latent_vectors[i].flatten() for i in step_indices]
        latents_matrix = np.array(latents_flat)

        # Simple 2D projection using first two principal components (manual PCA)
        # Center the data
        mean = latents_matrix.mean(axis=0)
        centered = latents_matrix - mean

        # Compute covariance and eigenvectors
        cov = np.cov(centered.T)
        eigenvalues, eigenvectors = np.linalg.eig(cov)

        # Sort by eigenvalues
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # Project onto first 2 components
        projection = centered @ eigenvectors[:, :2]

        # Plot
        fig, ax = plt.subplots(figsize=(10, 8))

        # Plot trajectory
        ax.plot(projection[:, 0], projection[:, 1], 'b-', alpha=0.3, linewidth=2)

        # Plot points with color gradient (early = blue, late = red)
        colors = plt.cm.viridis(np.linspace(0, 1, len(projection)))

        for i, (x, y) in enumerate(projection):
            ax.scatter(x, y, c=[colors[i]], s=100, edgecolors='black', linewidths=1.5)
            ax.text(x, y, f'{step_indices[i]}', fontsize=8, ha='center', va='center')

        ax.set_xlabel('First Principal Component')
        ax.set_ylabel('Second Principal Component')
        ax.set_title(f'Latent Space Evolution (PCA Projection)\n"{self.metadata["prompt"][:60]}..."')
        ax.grid(True, alpha=0.3)

        # Add colorbar
        sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=0, vmax=total_steps))
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax)
        cbar.set_label('Denoising Step')

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"✓ Saved latent space evolution: {output_path}")

    def export_analysis_data(self, output_path=None):
        """
        Export analysis data as JSON.

        Args:
            output_path: Where to save
        """
        if output_path is None:
            output_path = self.phase3_dir / "noise_decomposition.json"

        step_changes = self.compute_step_changes()
        noise_variance = self.compute_noise_variance_trajectory()

        data = {
            "prompt": self.metadata["prompt"],
            "num_steps": len(self.latent_vectors),
            "noise_variance": noise_variance.tolist(),
            "step_changes": step_changes.tolist(),
            "critical_steps": self.identify_critical_steps().tolist()
        }

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✓ Exported noise decomposition data: {output_path}")


def main():
    """
    Example usage: Analyze noise decomposition for a sequence.
    """
    import sys

    if len(sys.argv) < 2:
        print("Usage: python noise_decomposition.py <sequence_dir>")
        print("Example: python noise_decomposition.py ../assets/generated_sequences/01_standard")
        return

    sequence_dir = sys.argv[1]

    print("="*60)
    print("NOISE DECOMPOSITION ANALYSIS")
    print("="*60)

    try:
        analyzer = NoiseDecompositionAnalyzer(sequence_dir)

        # Visualize denoising trajectory
        print("\n1. Visualizing denoising trajectory...")
        analyzer.visualize_denoising_trajectory()

        # Identify critical steps
        print("\n2. Identifying critical steps...")
        critical_steps = analyzer.identify_critical_steps()

        # Visualize latent space evolution
        print("\n3. Visualizing latent space evolution...")
        analyzer.visualize_latent_space_evolution()

        # Export data
        print("\n4. Exporting analysis data...")
        analyzer.export_analysis_data()

        print("\n" + "="*60)
        print("✓ Noise decomposition analysis complete!")
        print("="*60)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
