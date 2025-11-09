"""
Fake News Themed Generation Script - All Modes
Generates each theme in 4 different modes: standard, low steps, high guidance, paradox
"""

import sys
from pathlib import Path
from diffusion_step_generator import DiffusionStepCapture


# Define all fake news themes
THEMES = {
    "truth_vs_lies": {
        "name": "Truth vs Lies",
        "prompt": "newspaper headlines morphing into smoke, truth and lies intertwined, digital glitch aesthetic",
        "seed": 123
    },
    "echo_chamber": {
        "name": "Echo Chamber",
        "prompt": "infinite mirrors reflecting distorted news, echo chamber, fragmented reality, social media bubbles",
        "seed": 456
    },
    "propaganda": {
        "name": "Propaganda Machine",
        "prompt": "propaganda posters, megaphones, manipulated crowds, red and black colors, authoritarian aesthetic",
        "seed": 789
    },
    "deepfake": {
        "name": "Deepfake",
        "prompt": "real photograph that is completely fake, authentic deception, genuine artificiality",
        "seed": 101112
    },
    "info_overload": {
        "name": "Information Overload",
        "prompt": "thousands of screens showing conflicting information, overwhelming data streams, drowning in headlines",
        "seed": 131415
    },
    "viral_spread": {
        "name": "Viral Spread",
        "prompt": "misinformation spreading like a virus through networks, glowing pathways, infection map, exponential growth",
        "seed": 161718
    }
}

# Define generation modes
MODES = {
    "standard": {
        "steps": 50,
        "guidance": 7.5,
        "description": "Normal generation"
    },
    "low_steps": {
        "steps": 15,
        "guidance": 7.5,
        "description": "Arrested development (dreamlike)"
    },
    "high_guidance": {
        "steps": 50,
        "guidance": 15.0,
        "description": "Over-interpretation (oversaturated)"
    },
    "paradox": {
        "steps": 50,
        "guidance": 7.5,
        "description": "Paradoxical interpretation"
    }
}


def main():
    """
    Generate all combinations of themes × modes
    Total: 6 themes × 4 modes = 24 sequences
    """

    # Initialize generator
    generator = DiffusionStepCapture(device="mps")
    base_output = Path("../assets/generated_sequences")

    total_sequences = len(THEMES) * len(MODES)
    current = 0

    print("\n" + "="*70)
    print(f"GENERATING {total_sequences} FAKE NEWS SEQUENCES")
    print(f"{len(THEMES)} themes × {len(MODES)} modes")
    print("="*70)

    for theme_id, theme_data in THEMES.items():
        for mode_id, mode_data in MODES.items():
            current += 1

            # Create output directory name
            output_dir = base_output / f"fakenews_{theme_id}_{mode_id}"

            # Special handling for paradox mode - add contradictory terms
            prompt = theme_data["prompt"]
            if mode_id == "paradox":
                # Add paradoxical modifiers
                paradox_suffix = ", simultaneously existing and non-existing, visible invisibility"
                prompt = prompt + paradox_suffix

            print(f"\n[{current}/{total_sequences}] {theme_data['name']} - {mode_data['description']}")
            print("="*70)

            generator.generate_sequence(
                prompt=prompt,
                output_dir=output_dir,
                num_inference_steps=mode_data["steps"],
                guidance_scale=mode_data["guidance"],
                seed=theme_data["seed"]
            )

    print("\n" + "="*70)
    print("✓ ALL 24 SEQUENCES GENERATED")
    print("="*70)
    print("\nThemes generated:")
    for theme_id, theme_data in THEMES.items():
        print(f"  - {theme_data['name']}")
    print("\nModes for each theme:")
    for mode_id, mode_data in MODES.items():
        print(f"  - {mode_id}: {mode_data['description']}")
    print("\nRefresh your web viewer to see them!")


if __name__ == "__main__":
    main()
