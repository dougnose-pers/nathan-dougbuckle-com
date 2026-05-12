#!/usr/bin/env python3
"""Generate magazine imagery for the Five Explorations reader."""

import base64
import json
import os
import sys
import time
import urllib.request

# Run: GOOGLE_AI_STUDIO_API_KEY=AIza... python3 generate_images.py
API_KEY = os.environ.get("GOOGLE_AI_STUDIO_API_KEY", "")
if not API_KEY:
    print("ERROR: Set GOOGLE_AI_STUDIO_API_KEY in your environment before running.", file=sys.stderr)
    sys.exit(1)
MODEL = "imagen-4.0-generate-001"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:predict?key={API_KEY}"

# Universal style language layered into every prompt
STYLE_BASE = (
    "Editorial magazine photograph in the tradition of Wallpaper, Monocle, and Apartamento. "
    "Cinematic composition with generous negative space. Soft directional natural light. "
    "Restrained palette of ink-black (#171717), warm off-white paper, and a single touch of azure blue (#0099FF) where appropriate. "
    "Premium, considered, slightly mysterious. Shot on a medium-format camera with a shallow depth of field. "
    "ABSOLUTELY NO TEXT: no words, letters, numbers, labels, captions, titles, headlines, or typography of any kind anywhere in the image. "
    "The image must be purely visual."
)

PROMPTS = [
    {
        "name": "01_hero_intro",
        "ratio": "16:9",
        "prompt": (
            "A single dark ink-coloured monolithic sculptural form floating in mid-air against an off-white paper background. "
            "The form is geometric — angular, architectural — suggestive of an idea taking shape. "
            "Soft warm light from the upper right casts a long delicate shadow across the textured paper. "
            "Composition is centred-left, with abundant negative space to the right. "
            "Atmospheric, contemplative, the visual equivalent of a held breath before speaking. "
            + STYLE_BASE
        ),
    },
    {
        "name": "02_contents_constellation",
        "ratio": "16:9",
        "prompt": (
            "Five small dark abstract sculptural objects arranged in a loose constellation on an off-white textured paper surface, "
            "shot from directly overhead. Each object is distinct — one angular, one curved, one layered, one looped, one fractured. "
            "They are spaced like punctuation marks across a page. Subtle warm overhead light. "
            "Reads as a curated grouping, like specimens or chess pieces. "
            "Quiet, considered, inviting closer inspection. "
            + STYLE_BASE
        ),
    },
    {
        "name": "03_slingshot_hero",
        "ratio": "16:9",
        "prompt": (
            "Two angular geometric forms — one large and dark, one smaller and the same dark colour — caught in the moment of separation, "
            "as if mid-launch, against an off-white textured paper background. A faint suggestion of motion blur on the smaller form. "
            "The composition implies trajectory and propulsion without being literal. "
            "Soft warm light from upper right. The image evokes a partnership where the smaller form is being launched by the larger one. "
            + STYLE_BASE
        ),
    },
    {
        "name": "04_slingshot_detail",
        "ratio": "4:3",
        "prompt": (
            "Close-up still life of a clean modernist desk surface with a few precisely arranged objects: a small dark notebook, "
            "a single black pen at a slight angle, a printed page with abstract geometric markings partially visible. "
            "Off-white paper textures dominate. Shot from a low three-quarter angle. "
            "Implies focused work, a venture taking shape. "
            + STYLE_BASE
        ),
    },
    {
        "name": "05_moat_hero",
        "ratio": "16:9",
        "prompt": (
            "A single hand-crafted physical object photographed in raking light against a deep shadow background fading to pure ink-black. "
            "The object is abstract but feels weighty, considered, expensive to replicate — perhaps a small dark stone form, or a hand-turned wooden vessel. "
            "Light reveals every facet of its surface. Composition is centre-right, with deep negative space to the left. "
            "Evokes craft, permanence, the kind of thing that took years to make right. "
            + STYLE_BASE
        ),
    },
    {
        "name": "06_moat_linkedin_visuals",
        "ratio": "16:9",
        "prompt": (
            "Four small dark abstract objects arranged in a neat 2x2 grid on an off-white textured paper background, shot from directly overhead. "
            "Each object is distinct but related — a family of forms. Slight shadows give depth. "
            "Reads like a typology or a series of essays laid out for inspection. "
            "Quiet, archival, editorial. "
            + STYLE_BASE
        ),
    },
    {
        "name": "07_validation_parked",
        "ratio": "4:3",
        "prompt": (
            "A still life: a closed dark notebook on an off-white textured paper surface, with a small dark stone resting on top as a paperweight. "
            "Soft window light from the left. Shot from a slight angle, three-quarter view. "
            "Reads as something deliberately set aside, kept but not active. "
            "The image carries the quietness of a considered decision. "
            + STYLE_BASE
        ),
    },
    {
        "name": "08_toolkit_modular",
        "ratio": "16:9",
        "prompt": (
            "Eight small dark geometric forms — like a precise set of artisan tools or modular components — arranged in a neat row on an off-white paper surface, shot from directly overhead. "
            "Each form is distinct in shape but unified in colour and finish. Equal spacing, like a typeset specimen sheet. "
            "Suggests a complete kit, a well-considered set. "
            + STYLE_BASE
        ),
    },
    {
        "name": "09_workshop_hero",
        "ratio": "16:9",
        "prompt": (
            "Interior of a quiet design studio in golden afternoon light. A wide workbench at centre with a few sketches, a small dark sculptural prototype, and a single hand visible at the edge of the frame holding a pencil. "
            "Soft warm light streams across the bench from a window out of frame. The workshop feels well-used but not cluttered. "
            "Shot at a slight three-quarter angle. Reads as the place where craft and thought meet. "
            + STYLE_BASE
        ),
    },
    {
        "name": "10_workshop_detail",
        "ratio": "4:3",
        "prompt": (
            "Close-up of a senior craftsperson's hands holding a pencil over a sketch, mid-thought. The sketch is partially visible — abstract geometric forms, no text. "
            "Soft warm light from the upper left. The hands are weathered, experienced — suggest decades of practice. "
            "Background is softly blurred — a hint of workshop materials. "
            "Reads as the moment of judgement: the pause before a decision is made. "
            + STYLE_BASE
        ),
    },
    {
        "name": "11_outro",
        "ratio": "16:9",
        "prompt": (
            "A wide quiet horizon: a single dark mountainous form silhouetted against an off-white misty sky, with a thin band of warm light along the ridgeline. "
            "The image is mostly empty space — atmospheric, peaceful, slightly aspirational. "
            "Reads as the end of a long thoughtful walk: still space to think. "
            + STYLE_BASE
        ),
    },
]


def generate_one(item, out_dir):
    """Generate a single image with retries."""
    out_path = os.path.join(out_dir, f"{item['name']}.png")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 50000:
        print(f"  [skip] {item['name']} already exists")
        return True

    body = json.dumps({
        "instances": [{"prompt": item["prompt"]}],
        "parameters": {"sampleCount": 1, "aspectRatio": item["ratio"]},
    }).encode("utf-8")

    for attempt in range(3):
        try:
            req = urllib.request.Request(
                ENDPOINT,
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            preds = data.get("predictions", [])
            if not preds:
                print(f"  [warn] {item['name']} no predictions: {json.dumps(data)[:200]}")
                continue

            b64 = preds[0].get("bytesBase64Encoded")
            if not b64:
                print(f"  [warn] {item['name']} no base64")
                continue

            with open(out_path, "wb") as f:
                f.write(base64.b64decode(b64))
            size_kb = os.path.getsize(out_path) // 1024
            print(f"  [ok]   {item['name']}.png  ({size_kb} KB)")
            return True

        except Exception as e:
            print(f"  [err]  {item['name']} attempt {attempt+1}: {e}")
            time.sleep(3)

    print(f"  [FAIL] {item['name']} after 3 attempts")
    return False


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__)) + "/images"
    os.makedirs(out_dir, exist_ok=True)
    print(f"Generating {len(PROMPTS)} images into {out_dir}")
    successes = 0
    for i, item in enumerate(PROMPTS, 1):
        print(f"[{i}/{len(PROMPTS)}] {item['name']}")
        if generate_one(item, out_dir):
            successes += 1
        time.sleep(2)  # gentle rate-limit
    print(f"\nDone: {successes}/{len(PROMPTS)} succeeded.")
    return 0 if successes == len(PROMPTS) else 1


if __name__ == "__main__":
    sys.exit(main())
