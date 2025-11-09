#!/usr/bin/env python3
"""
Phase 3 Interpretability: Main Analysis Orchestrator

Run all Phase 3 interpretability analyses on a generated sequence:
1. Attention Visualization - Token-to-region mapping
2. Semantic Emergence - When concepts become recognizable
3. Noise Decomposition - Denoising trajectory and latent evolution
4. Token Attribution - Which words matter most (optional, expensive)

Usage:
    python analyze_all.py <sequence_dir> [--skip-attribution] [--skip-semantic]

Example:
    python analyze_all.py ../assets/generated_sequences/01_standard
    python analyze_all.py ../assets/generated_sequences/01_standard --skip-attribution
"""

import sys
import argparse
from pathlib import Path
import time

# Import all analysis modules
from attention_visualizer import AttentionVisualizer
from semantic_emergence import SemanticEmergenceAnalyzer
from noise_decomposition import NoiseDecompositionAnalyzer
from token_attribution import TokenAttributionAnalyzer


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def analyze_sequence(sequence_dir, skip_attribution=False, skip_semantic=False, device="mps"):
    """
    Run all Phase 3 analyses on a sequence.

    Args:
        sequence_dir: Path to generated sequence
        skip_attribution: Skip token attribution (saves time)
        skip_semantic: Skip semantic emergence (requires CLIP)
        device: Device for token attribution generation
    """
    sequence_dir = Path(sequence_dir)

    if not sequence_dir.exists():
        print(f"Error: Sequence directory not found: {sequence_dir}")
        return False

    print_header("PHASE 3 INTERPRETABILITY ANALYSIS")
    print(f"Analyzing: {sequence_dir}")
    print(f"Skip attribution: {skip_attribution}")
    print(f"Skip semantic: {skip_semantic}")

    overall_start = time.time()
    results = {}

    # Analysis 1: Attention Visualization
    print_header("1/4: ATTENTION VISUALIZATION")
    try:
        start = time.time()
        viz = AttentionVisualizer(sequence_dir)

        # Visualize key steps
        print("Generating token-specific attention maps...")
        for step in [0, 10, 25, 49]:
            if step < len(viz.attention_maps):
                viz.visualize_token_attention(step)

        # Visualize evolution for key tokens
        print("Generating attention evolution...")
        for token_idx in range(min(3, len(viz.tokens))):
            viz.visualize_all_steps(token_idx)

        duration = time.time() - start
        results['attention'] = {'success': True, 'duration': duration}
        print(f"✓ Attention analysis complete ({duration:.1f}s)")

    except Exception as e:
        print(f"✗ Attention analysis failed: {e}")
        results['attention'] = {'success': False, 'error': str(e)}

    # Analysis 2: Semantic Emergence
    if not skip_semantic:
        print_header("2/4: SEMANTIC EMERGENCE ANALYSIS")
        try:
            start = time.time()
            analyzer = SemanticEmergenceAnalyzer(sequence_dir, use_clip=True)

            # Analyze timeline
            print("Analyzing semantic emergence timeline...")
            emergence_results = analyzer.analyze_emergence_timeline()

            # Visualizations
            print("Creating visualizations...")
            analyzer.visualize_emergence_curves(emergence_results)
            analyzer.create_emergence_heatmap(emergence_results)
            analyzer.export_emergence_data(emergence_results)

            # Find key emergence points
            print("Finding emergence points...")
            key_concepts = [analyzer.prompt, "recognizable objects", "clear details"]
            for concept in key_concepts:
                analyzer.find_emergence_point(concept, threshold=0.5)

            duration = time.time() - start
            results['semantic'] = {'success': True, 'duration': duration}
            print(f"✓ Semantic analysis complete ({duration:.1f}s)")

        except Exception as e:
            print(f"✗ Semantic analysis failed: {e}")
            print("  (If CLIP is not installed: pip install transformers)")
            results['semantic'] = {'success': False, 'error': str(e)}
    else:
        print_header("2/4: SEMANTIC EMERGENCE ANALYSIS (SKIPPED)")
        results['semantic'] = {'success': None, 'skipped': True}

    # Analysis 3: Noise Decomposition
    print_header("3/4: NOISE DECOMPOSITION ANALYSIS")
    try:
        start = time.time()
        analyzer = NoiseDecompositionAnalyzer(sequence_dir)

        # Visualizations
        print("Visualizing denoising trajectory...")
        analyzer.visualize_denoising_trajectory()

        print("Identifying critical steps...")
        critical_steps = analyzer.identify_critical_steps()

        print("Visualizing latent space evolution...")
        analyzer.visualize_latent_space_evolution()

        print("Exporting analysis data...")
        analyzer.export_analysis_data()

        duration = time.time() - start
        results['noise_decomposition'] = {'success': True, 'duration': duration}
        print(f"✓ Noise decomposition complete ({duration:.1f}s)")

    except Exception as e:
        print(f"✗ Noise decomposition failed: {e}")
        results['noise_decomposition'] = {'success': False, 'error': str(e)}

    # Analysis 4: Token Attribution
    if not skip_attribution:
        print_header("4/4: TOKEN ATTRIBUTION ANALYSIS")
        print("⚠️  WARNING: This will regenerate the sequence N times (once per token)")
        print("⚠️  This can take significant time and compute resources")

        try:
            start = time.time()
            analyzer = TokenAttributionAnalyzer(sequence_dir, device=device)

            # Run attribution study
            print("Running attribution study...")
            attribution_results = analyzer.run_attribution_study()

            # Visualizations
            print("Creating visualizations...")
            analyzer.visualize_attribution_scores(attribution_results)
            analyzer.create_comparison_grid(attribution_results)

            print("Exporting data...")
            analyzer.export_attribution_data(attribution_results)

            duration = time.time() - start
            results['token_attribution'] = {'success': True, 'duration': duration}
            print(f"✓ Token attribution complete ({duration:.1f}s)")

        except Exception as e:
            print(f"✗ Token attribution failed: {e}")
            results['token_attribution'] = {'success': False, 'error': str(e)}
    else:
        print_header("4/4: TOKEN ATTRIBUTION ANALYSIS (SKIPPED)")
        results['token_attribution'] = {'success': None, 'skipped': True}

    # Summary
    overall_duration = time.time() - overall_start
    print_header("ANALYSIS SUMMARY")

    success_count = sum(1 for r in results.values() if r.get('success') is True)
    total_count = len([r for r in results.values() if not r.get('skipped')])

    print(f"Completed: {success_count}/{total_count} analyses")
    print(f"Total time: {overall_duration:.1f}s ({overall_duration/60:.1f} min)")
    print()

    for name, result in results.items():
        status = "✓" if result.get('success') else ("⊘" if result.get('skipped') else "✗")
        duration_str = f"({result['duration']:.1f}s)" if 'duration' in result else ""
        print(f"  {status} {name.replace('_', ' ').title()} {duration_str}")

    print()
    print(f"Output directory: {sequence_dir}")

    return success_count == total_count


def main():
    parser = argparse.ArgumentParser(
        description="Run all Phase 3 interpretability analyses on a generated sequence"
    )
    parser.add_argument(
        "sequence_dir",
        help="Path to generated sequence directory"
    )
    parser.add_argument(
        "--skip-attribution",
        action="store_true",
        help="Skip token attribution analysis (saves time)"
    )
    parser.add_argument(
        "--skip-semantic",
        action="store_true",
        help="Skip semantic emergence analysis (requires CLIP)"
    )
    parser.add_argument(
        "--device",
        default="mps",
        choices=["cuda", "mps", "cpu"],
        help="Device for token attribution generation"
    )

    args = parser.parse_args()

    success = analyze_sequence(
        args.sequence_dir,
        skip_attribution=args.skip_attribution,
        skip_semantic=args.skip_semantic,
        device=args.device
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
