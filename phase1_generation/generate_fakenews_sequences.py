"""
Fake News Themed Generation Script
Explores how AI interprets concepts of truth, misinformation, and propaganda
"""

import sys
from pathlib import Path
from diffusion_step_generator import DiffusionStepCapture


def main():
    """
    Generate sequences exploring fake news, misinformation, and truth themes
    """

    # Initialize generator
    # Use "mps" for Mac M1/M2, "cuda" for NVIDIA GPU, "cpu" for CPU
    generator = DiffusionStepCapture(device="mps")

    # Base output directory
    base_output = Path("../assets/generated_sequences")

    # FAKE NEWS SEQUENCE 1: Truth vs Lies
    print("\n" + "="*60)
    print("FAKE NEWS 1: Truth dissolving into lies")
    print("="*60)
    generator.generate_sequence(
        prompt="newspaper headlines morphing into smoke, truth and lies intertwined, digital glitch aesthetic",
        output_dir=base_output / "05_truth_vs_lies",
        num_inference_steps=50,
        guidance_scale=7.5,
        seed=123
    )

    # FAKE NEWS SEQUENCE 2: Echo Chamber
    print("\n" + "="*60)
    print("FAKE NEWS 2: Echo chamber visualization")
    print("="*60)
    generator.generate_sequence(
        prompt="infinite mirrors reflecting distorted news, echo chamber, fragmented reality, social media bubbles",
        output_dir=base_output / "06_echo_chamber",
        num_inference_steps=50,
        guidance_scale=7.5,
        seed=456
    )

    # FAKE NEWS SEQUENCE 3: Propaganda Machine (High Guidance - forced interpretation)
    print("\n" + "="*60)
    print("FAKE NEWS 3: Propaganda machine - Over-saturated")
    print("="*60)
    generator.generate_sequence(
        prompt="propaganda posters, megaphones, manipulated crowds, red and black colors, authoritarian aesthetic",
        output_dir=base_output / "07_propaganda",
        num_inference_steps=50,
        guidance_scale=15.0,  # High guidance = forced interpretation
        seed=789
    )

    # FAKE NEWS SEQUENCE 4: Deepfake Paradox
    print("\n" + "="*60)
    print("FAKE NEWS 4: Deepfake paradox - Contradictory concepts")
    print("="*60)
    generator.generate_sequence(
        prompt="real photograph that is completely fake, authentic deception, genuine artificiality",
        output_dir=base_output / "08_deepfake_paradox",
        num_inference_steps=50,
        guidance_scale=7.5,
        seed=101112
    )

    # FAKE NEWS SEQUENCE 5: Information Overload (Arrested Development)
    print("\n" + "="*60)
    print("FAKE NEWS 5: Information overload - Incomplete formation")
    print("="*60)
    generator.generate_sequence(
        prompt="thousands of screens showing conflicting information, overwhelming data streams, drowning in headlines",
        output_dir=base_output / "09_info_overload",
        num_inference_steps=20,  # Low steps = dreamlike incompleteness
        guidance_scale=7.5,
        seed=131415
    )

    # FAKE NEWS SEQUENCE 6: Viral Spread
    print("\n" + "="*60)
    print("FAKE NEWS 6: Viral misinformation spreading")
    print("="*60)
    generator.generate_sequence(
        prompt="misinformation spreading like a virus through networks, glowing pathways, infection map, exponential growth",
        output_dir=base_output / "10_viral_spread",
        num_inference_steps=50,
        guidance_scale=7.5,
        seed=161718
    )

    print("\n" + "="*60)
    print("✓ ALL FAKE NEWS SEQUENCES GENERATED")
    print("="*60)
    print("\nYou now have 6 new sequences exploring:")
    print("  - Truth vs Lies")
    print("  - Echo Chambers")
    print("  - Propaganda (oversaturated)")
    print("  - Deepfake Paradox")
    print("  - Information Overload (incomplete)")
    print("  - Viral Spread")
    print("\nRefresh your web viewer to see them!")


if __name__ == "__main__":
    main()
