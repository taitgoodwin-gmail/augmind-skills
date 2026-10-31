# Offering Studio

Offering Studio turns any input into a launch package for one brand. Point it at a website, an existing offering, notes, files, an article or an idea, name the brand, and it produces the offering deck, then whatever else the offering needs.

## What it makes

| Output | When | Made by |
|---|---|---|
| Offering deck (PowerPoint, evidence-tagged, locked look) | Always | `offering-deck` |
| Technical architecture (diagram and short record) | The offering depends on software the brand runs, touches client systems, holds client data or manages hosting | `offering-package` |
| Home page (desktop and phone, real copy, claims traced to the deck) | Always | `offering-package` |
| Clickable prototype (the core journey) | The offering is a product: users work in screens the brand controls and get value without a person from the brand doing the work | `offering-package` |
| Financial model (internal: costs, capacity, price assumptions, unit economics) | When asked, or once the deck is approved | `offering-package` |

Every output reads from one spec file, so the deck, the page and the prototype cannot describe different offerings. A script checks that every claim on the home page traces to a deck card that is backed or is the brand's own design; an `open` claim cannot ship.

## Use it

1. Say what the offering is and name the brand: "Make an offering deck for Levarum from these notes" or "/offering-studio:offering-deck". The skill reads the input, researches official sources, sends you one outline to approve, then builds the deck.
2. Once the deck exists, ask for the package: "Build the package for this offering." The skill decides which extra outputs apply, says why, and builds them from the same spec.

Brand packs live in `skills/offering-deck/brands/<brand>/brand.json`. The plugin ships `augmind`, `levarum` and `neutral`. A pack holds the logo, the colors, the font and the standing words (eyebrow, confidentiality line, who decides). To add a brand, copy `neutral` and edit it.

## What it needs

Python 3 with `python-pptx`, `Pillow` and `lxml`. Previews need LibreOffice and `pdftoppm`. The scripts run in claude.ai, Cowork and Claude Code; the independent review agents run only in Cowork and Claude Code, and in claude.ai the skill does those reads itself and says so on the evidence slide.

## Data

The plugin sends nothing anywhere until you call a deck final. It reads the files and pages you point it at and writes files to the working folder. Drafts are not uploaded anywhere. When you call a delivered deck final, it is relabeled v1.0 (no "Draft"), re-rendered, and copied with its build files (the spec, source notes and decisions) to the Google Drive folder you name, with the Drive connector. If that folder is shared with anyone else, you are told who and asked first; sharing is never changed. Unattended runs never copy to Drive.

## Maintainers

Tait Goodwin owns the plugin and the `augmind` and `levarum` packs. Levarum was formerly Signal and MindLeverX; its pack lists those as former names, and the brand checks fail any Levarum deck or page that still uses them. The look (`render.py`) changes only when Tait asks, and every change runs the v0.9 renderer regression test before and after. That test is not in this repository yet.
