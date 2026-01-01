# Infographic System Handover

**Project:** Infographic generation (Satori + brand templates)
**Owner:** Dr. Shailesh Singh
**Last Updated:** 2026-01-01

---

## What We Are Trying To Do

Build a high-quality, information-dense infographic system that matches the look and attention-grabbing style of the carousel templates, while keeping brand consistency and fast programmatic generation.

---

## Current Status

- **Skill created:** `infographic-generator`
  - Path: `skills/cardiology/infographic-generator/`
  - CLI: `skills/cardiology/infographic-generator/scripts/infographic_cli.py`
- **New template added:** `infographic-dense` in `skills/cardiology/visual-design-system/satori/renderer.js`
- **Palette alignment:** infographic template now uses **carousel brand palette**
- **Demo output:** `skills/cardiology/visual-design-system/outputs/infographics/demo-glp1-rolloff.png`
  - Note: re-render recommended to reflect updated palette

---

## Brand Palette (Decision)

- **Use carousel brand palette for infographics** ✅ (implemented)
- Source of truth:
  - `skills/cardiology/carousel-generator-v2/tokens/brand-tokens.json`
  - `skills/cardiology/visual-design-system/satori/carousel-templates/index.js` (BRAND constants)

---

## Current Output (What It Looks Like)

- Example: `skills/cardiology/visual-design-system/outputs/infographics/demo-glp1-rolloff.png`
- Clean, minimal, information-dense layout with cards and a bottom callout.
- **Missing**: strong visual hook, icons, hero image, bold gradients, and attention-grabbing hierarchy.
- **Palette alignment complete**, but demo should be re-rendered to reflect the new colors.

---

## My Opinion (Assistant)

- The output is readable but looks like a clinic handout.
- Not attention-grabbing for social feed behavior.
- Visual hierarchy is too flat; lacks a hero moment and iconography.

---

## Your Opinion (User)

- Output is **trash**.
- Empty and not attractive.
- Does not match the quality of your carousel designs.

---

## Direction We Should Take

- Infographics must look like the carousel system: bold gradients, punchy hierarchy, icons, and visual hooks.
- Align the palette with carousel brand tokens.
- Add a **hero section** (image or icon cluster) and more expressive layout.
- Increase “stop power” for social feed behavior.

---

## What We Should Do Next (Sequence)

1) **Template overhaul (core)**
   - Rebuild `infographic-dense` to match carousel visual language:
     - Mesh gradients
     - Large headline + hook line
     - Icon bullets
     - Strong contrast blocks
     - Short punchy copy

2) **Add hero visual support**
   - Support optional hero image or icon cluster.
   - Add a standard “doctor portrait + device/heart icon” layout option.

3) **Introduce 2-3 new infographic templates**
   - `infographic-process` (workflow)
   - `infographic-comparison` (two-column)
   - `infographic-myth-truth` (myth vs truth)

4) **Sample set for QA**
   - Generate 3-5 example infographics and review for brand fit.

---

## Files to Focus On

- `skills/cardiology/visual-design-system/satori/renderer.js` (infographic templates)
- `skills/cardiology/visual-design-system/satori/carousel-templates/` (look and feel reference)
- `skills/cardiology/carousel-generator-v2/tokens/brand-tokens.json` (brand palette)
- `skills/cardiology/infographic-generator/SKILL.md` (skill workflow)

---

## Notes

- The current system works technically, but the visual layer needs a full redesign to match carousel quality.
- The next session should prioritize visual style first, then data templates.
