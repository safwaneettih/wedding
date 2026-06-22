#!/usr/bin/env python3
import requests, json, base64, os, time, sys

API_KEY = "03f8748ca465eb3d2fd37287bd6874271bff6654d5dda8d9f594435bd2313fe7"
BASE = "https://api.piapi.ai"
OUT = "/Users/safwane-personal/Desktop/wedding/v8-assets"
os.makedirs(OUT, exist_ok=True)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

ASSETS = [
    # === LANTERN ===
    ("lantern.png", "A traditional Moroccan lantern, ornate brass with intricate filigree cutout patterns, arched dome top, hanging from a thin chain, warm glow emanating from inside, isolated on pure black background for luminosity masking, photorealistic, golden metal with patina, vertical composition, cinematic lighting, the lantern is the only object, sharp detail on the metalwork arabesque patterns"),
    ("courtyard.png", "A dim Moroccan courtyard at night, two ornate horseshoe arches flanking a central doorway, Tunisian Andalusian architecture, stone walls with subtle zellige tilework at the base, faint blue moonlight barely illuminating the edges, the scene is mostly dark with architectural silhouettes emerging from shadows, photorealistic, mysterious atmosphere, vertical 9:16 composition, deep blue-black tones with hints of warm gold where light will hit"),
    ("flame.png", "A single warm candle flame, golden orange glow, photographed against pure black background, soft flickering shape, the flame is small and centered, realistic, no candle body just the flame itself, warm yellow core fading to orange edges, subtle smoke wisps rising, square 1:1 composition, high resolution for compositing inside a lantern"),
    ("light-burst.png", "A radial light burst, warm golden glow expanding from a single center point, the center is bright white-gold fading to warm amber then to transparent, soft volumetric light rays spreading outward, dust particles floating in the light beam, atmospheric, cinematic, isolated on pure black background for screen blending, square 1:1, the glow fills 80% of the frame"),

    # === CALLIGRAPHHY ===
    ("bismillah.png", "Arabic calligraphy of bismillah ar-rahman ar-raheem in classical Thuluth script, hand-drawn with a reed pen on cream parchment, the strokes are bold and flowing with visible ink texture, monochrome deep blue-black ink on warm cream background, traditional Islamic manuscript style, horizontal composition 3:1 ratio, the text is centered with generous margins, high contrast clean strokes, no decorative borders just the pure calligraphy"),
    ("names-calligraphy.png", "Arabic calligraphy of the names Safwane and Manel in Arabic letters صفوان و منال in an elegant interlocking Diwani script style, the two names connected by a stylized waw in the center, gold ink with subtle gradient from deep gold to pale champagne, on a transparent cream background, the names are large and centered, flowing organic strokes with traditional flourishes, horizontal composition 4:1 ratio, luxury wedding invitation aesthetic, the calligraphy should feel hand-written by a master calligrapher"),
    ("geometric-border.png", "An Islamic geometric border pattern, repeating 8-pointed star and hexagon tessellation, thin golden lines on cream background, horizontal strip composition 6:1 ratio, the pattern is symmetrical and continuous, clean precise lines no fill only outlines, Moroccan zellige inspired geometry, the border should be elegant and minimal not overpowering, gold linework at uniform stroke weight"),
    ("inkwell.png", "A traditional brass inkwell with an open lid, a reed pen qalam resting beside it on cream parchment, a small drop of dark ink near the pen nib, warm directional lighting from the left, photorealistic still life, shallow depth of field, the objects are small and centered at the bottom of the frame, cream and gold tones, vertical composition 3:4 ratio, vintage manuscript atmosphere"),
    ("parchment-texture.png", "A seamless cream parchment paper texture, warm ivory tone with subtle fiber patterns, very faint aging at the edges, no text or marks, flat lay top-down view, even soft lighting, the texture is uniform and tileable, cream color matching hex FAF8F5, minimal texture just enough to feel like real paper not plain white"),

    # === WAX SEAL ===
    ("wax-seal.png", "A circular gold wax seal, deep gold color with a glossy surface texture, an embossed monogram letter S intertwined with M at the center, the seal is photographed top-down, centered on a cream envelope, photorealistic, soft shadow beneath the seal, the wax has natural irregular edges and surface imperfections, square 1:1 composition, the seal fills about 40% of the frame, warm golden tones with darker gold shadows in the crevices"),
    ("wax-seal-cracked.png", "A gold wax seal cracked cleanly down the middle into two halves, the crack reveals the darker interior of the wax, both halves are slightly separated, the monogram S and M is still visible but split by the crack, photorealistic, top-down view, cream envelope background, the crack has a jagged organic edge, warm gold tones, square 1:1 composition"),
    ("envelope-closed.png", "A luxury cream wedding envelope, rectangular with a triangular flap closure, subtle paper texture, photographed at a slight 3D angle from above, soft directional lighting casting a gentle shadow, the envelope is centered with generous margins, no text or decoration on the envelope body itself, cream color matching FAF8F5, photorealistic, portrait composition 3:4 ratio, the envelope has a faint gold border along the edges"),
    ("envelope-flap-open.png", "A cream envelope flap triangular shape, opened upward at 180 degrees, photographed flat with soft shadow, the inside of the flap has a slightly different cream tone, no text, isolated on white background for compositing, subtle gold border along the edges, photorealistic paper texture, the flap is a clean triangle shape, horizontal composition 4:3 ratio"),
    ("invitation-card.png", "A folded cream invitation card, standing slightly open at a 30 degree angle, thick premium paper with subtle texture, a faint gold border along the open edges, photographed in soft studio lighting, the card is blank with no text, photorealistic, centered with soft shadow beneath, portrait composition 3:4 ratio, the fold is visible at the center, warm cream tones"),
    ("card-paper-texture.png", "A seamless premium cream paper texture, smooth ivory surface with very subtle linen fiber pattern, no text or marks, flat lay top-down, even studio lighting, tileable, cream color matching FAF8F5, slightly warmer than plain white, minimal texture for an elegant stationery feel"),
]

def generate_image(filename, prompt):
    outpath = os.path.join(OUT, filename)
    if os.path.exists(outpath):
        print(f"  SKIP (exists): {filename}")
        return True

    print(f"  Generating: {filename}")
    payload = {
        "model": "gpt-image-2",
        "prompt": prompt,
        "n": 1
    }

    try:
        resp = requests.post(f"{BASE}/v1/images/generations", headers=HEADERS, json=payload, timeout=120)
        if resp.status_code != 200:
            print(f"  ERROR {resp.status_code}: {resp.text[:200]}")
            return False

        data = resp.json()
        images = data.get("data", [])
        if not images:
            print(f"  ERROR: no image in response")
            return False

        img_data = images[0]
        if "b64_json" in img_data:
            img_bytes = base64.b64decode(img_data["b64_json"])
        elif "url" in img_data:
            img_resp = requests.get(img_data["url"], timeout=60)
            img_bytes = img_resp.content
        else:
            print(f"  ERROR: no b64_json or url in response")
            return False

        with open(outpath, "wb") as f:
            f.write(img_bytes)
        size_kb = len(img_bytes) // 1024
        print(f"  SAVED: {filename} ({size_kb}KB)")
        return True

    except Exception as e:
        print(f"  EXCEPTION: {e}")
        return False

print(f"Generating {len(ASSETS)} assets to {OUT}/")
print("=" * 50)

success = 0
failed = 0
for filename, prompt in ASSETS:
    ok = generate_image(filename, prompt)
    if ok:
        success += 1
    else:
        failed += 1
    time.sleep(1)

print("=" * 50)
print(f"DONE: {success} saved, {failed} failed")
