#!/usr/bin/env python3
"""Round 2 imagery — Katapult design + natural materials + lifestyle warmth.
Byron Bay sensibility. Save to images_v2/."""

import base64
import json
import os
import sys
import time
import urllib.request

# Run: GOOGLE_AI_STUDIO_API_KEY=AIza... python3 generate_images_v2.py
API_KEY = os.environ.get("GOOGLE_AI_STUDIO_API_KEY", "")
if not API_KEY:
    print("ERROR: Set GOOGLE_AI_STUDIO_API_KEY in your environment before running.", file=sys.stderr)
    sys.exit(1)
MODEL = "imagen-4.0-generate-001"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:predict?key={API_KEY}"

STYLE_BASE = (
    "Editorial magazine photograph in the tradition of Wallpaper, Cereal, Kinfolk, and Apartamento — "
    "premium design meets lifestyle warmth. Byron Bay coastal-design sensibility. "
    "Composition with abundant negative space and natural light streaming in from a side window. "
    "Restrained palette: warm off-white (#F2EFE9), aged timber tones, deep ink-black (#171717), "
    "with a single muted sage-green accent (#79a949) where appropriate. "
    "Natural materials throughout — raw timber, linen, ceramic, paper, stone. "
    "Hint of plant life — a small leaf, a branch in soft focus, an indoor plant just out of focus. "
    "Shot on a medium-format camera with shallow depth of field. "
    "Considered, slightly mysterious, but warm and inhabited — not sterile. "
    "ABSOLUTELY NO TEXT: no words, letters, numbers, labels, captions, titles, headlines, or typography of any kind anywhere in the image. "
    "The image must be purely visual."
)

PROMPTS = [
    {
        "name": "01_hero_intro",
        "ratio": "16:9",
        "prompt": (
            "A single dark ink-coloured sculptural object resting on a long raw timber surface, photographed in warm afternoon "
            "light streaming through a window from the upper left. A single eucalyptus branch lies casually nearby. "
            "The object is geometric, considered, premium — like a high-end designer's reference piece. "
            "The window beyond is softly out of focus with a hint of green coastal foliage. "
            "Composition is centred-left with abundant negative space and visible timber grain. "
            "Reads as the moment before reading a beautifully made book. "
            + STYLE_BASE
        ),
    },
    {
        "name": "02_contents_constellation",
        "ratio": "16:9",
        "prompt": (
            "Five distinct small objects arranged loosely on a raw timber surface, shot from directly overhead in soft natural light. "
            "Each object made of a different natural material — one dark ceramic form, one pale stone, one piece of bleached driftwood, "
            "one folded linen, one small dark sculptural shape. They sit like specimens or chess pieces. "
            "A tiny eucalyptus sprig and a single pebble add lifestyle warmth. "
            "Subtle shadows from overhead window light. Quiet, considered, inviting closer inspection. "
            + STYLE_BASE
        ),
    },
    {
        "name": "03_slingshot_hero",
        "ratio": "16:9",
        "prompt": (
            "Two angular dark forms on a raw timber surface — one larger and resting, one smaller and tilted as if "
            "caught mid-launch — with a long shadow trailing across the wood grain. "
            "Soft warm light from a window beyond suggests Byron Bay coastal morning. "
            "A single delicate native Australian flower stem (banksia or wattle) rests beside the larger form. "
            "The composition implies trajectory and partnership without being literal. "
            + STYLE_BASE
        ),
    },
    {
        "name": "04_slingshot_detail",
        "ratio": "4:3",
        "prompt": (
            "Close-up of a designer's working desk — raw timber surface, a small dark sculptural prototype, an open notebook with abstract sketches, "
            "a single black pen, a steaming ceramic mug just visible at the frame edge. Soft window light from the left, "
            "with a hint of greenery and ocean-light tones beyond. A single sprig of native plant in a small vessel. "
            "Reads as focused work in a beloved space — not a sterile office, a considered studio. "
            + STYLE_BASE
        ),
    },
    {
        "name": "05_moat_hero",
        "ratio": "16:9",
        "prompt": (
            "A single hand-crafted physical object — a beautifully turned dark wooden vessel — photographed in raking afternoon light "
            "against a warm cream textured paper background. Light reveals every facet of its surface and the grain of the timber. "
            "Reads as craft, weight, permanence. A single eucalyptus leaf sits near the base. "
            "Composition centre-right with deep negative space to the left. "
            "Evokes something that took years to make right — patiently, by hand. "
            + STYLE_BASE
        ),
    },
    {
        "name": "06_moat_linkedin_visuals",
        "ratio": "16:9",
        "prompt": (
            "Four small distinct dark objects arranged in a neat 2x2 grid on a raw timber surface, shot from directly overhead. "
            "Each object is a different natural-material specimen — a dark ceramic, a small stone, a piece of polished timber, "
            "a folded piece of dark linen. A single dried botanical specimen rests next to one of them. "
            "Reads like a typology, a series of essays laid out for inspection. "
            + STYLE_BASE
        ),
    },
    {
        "name": "07_validation_parked",
        "ratio": "4:3",
        "prompt": (
            "A still life: a closed dark linen-bound notebook on a worn timber surface, with a small smooth stone resting on top as a paperweight. "
            "A single dried eucalyptus leaf rests beside it. Soft window light from the left casts gentle shadows. "
            "Reads as something deliberately set aside, kept but not active. "
            "Carries the quietness of a considered decision. "
            + STYLE_BASE
        ),
    },
    {
        "name": "08_toolkit_modular",
        "ratio": "16:9",
        "prompt": (
            "Eight small distinct dark objects — like a precise set of artisan tools — arranged in a neat row on a raw timber surface, "
            "shot from directly overhead in soft natural light. Each form distinct in shape but unified in colour and finish. "
            "Equal spacing, like a typeset specimen sheet. A single sprig of native plant in the corner adds warmth. "
            "Reads as a complete kit, a well-considered set. "
            + STYLE_BASE
        ),
    },
    {
        "name": "09_workshop_hero",
        "ratio": "16:9",
        "prompt": (
            "Interior of a beautiful Byron Bay-style design studio bathed in golden afternoon light. A wide raw timber workbench at centre with "
            "a few hand-drawn sketches, a small dark sculptural prototype, a ceramic mug, and a small indoor plant. "
            "Behind: large floor-to-ceiling windows revealing soft-focus coastal greenery and natural light. "
            "The space feels lived-in, considered, slightly bohemian — a place where craft and thought meet. "
            "No people visible. Shot at a slight three-quarter angle. "
            + STYLE_BASE
        ),
    },
    {
        "name": "10_workshop_detail",
        "ratio": "4:3",
        "prompt": (
            "Close-up of weathered experienced hands holding a graphite pencil over a partially-visible abstract sketch on cream paper. "
            "Soft warm light streams from the upper left. The hands belong to a senior designer — weathered, experienced, mid-thought. "
            "A small eucalyptus sprig and a wooden ruler sit nearby on the timber surface. "
            "Background is softly blurred — a hint of indoor plants and natural materials. "
            "Reads as the moment of judgement: the pause before a decision is made. "
            + STYLE_BASE
        ),
    },
    {
        "name": "11_outro",
        "ratio": "16:9",
        "prompt": (
            "A wide quiet horizon: a Byron Bay-style coastal landscape at golden hour — long grasses in the foreground softly blurred, "
            "a hint of ocean and dunes in the middle distance, soft misty sky above with warm directional light from low on the horizon. "
            "The image is mostly empty atmospheric space — peaceful, slightly aspirational. "
            "Reads as the end of a long thoughtful walk: still space to think. "
            + STYLE_BASE
        ),
    },
]


def generate_one(item, out_dir):
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
                ENDPOINT, data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            preds = data.get("predictions", [])
            if not preds:
                print(f"  [warn] {item['name']} no predictions")
                continue
            b64 = preds[0].get("bytesBase64Encoded")
            if not b64:
                continue
            with open(out_path, "wb") as f:
                f.write(base64.b64decode(b64))
            print(f"  [ok]   {item['name']}.png  ({os.path.getsize(out_path)//1024} KB)")
            return True
        except Exception as e:
            print(f"  [err]  {item['name']} attempt {attempt+1}: {e}")
            time.sleep(3)
    return False


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__)) + "/images_v2"
    os.makedirs(out_dir, exist_ok=True)
    print(f"Generating {len(PROMPTS)} v2 images into {out_dir}")
    s = 0
    for i, item in enumerate(PROMPTS, 1):
        print(f"[{i}/{len(PROMPTS)}] {item['name']}")
        if generate_one(item, out_dir):
            s += 1
        time.sleep(2)
    print(f"\nDone: {s}/{len(PROMPTS)} succeeded.")
    return 0 if s == len(PROMPTS) else 1


if __name__ == "__main__":
    sys.exit(main())
