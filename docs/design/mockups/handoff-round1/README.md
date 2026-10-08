# Handoff: factor, round 1 UI mockups (in progress)

## Overview
This bundle hands off the first round of mockups for **factor**, a desktop production calculator for factory games. Work started in Claude Design and is being moved to local Claude Code. `ui-brief.md` (the original brief, included) is the source of truth for scope, content and rules. Section 8 is the paste block.

**Status**
- Done: `factor-tokens.css`, the full token set for light and dark. Contrast ratios are noted inline.
- Done: `S1 Factory View.dc.html`, complete in both themes. Screenshots are in `screenshots/` (01 dark, 02 light, 1440×900 scaled down).
- Not started: S2, S3, S5, S6, a component-states sheet, and an index canvas that lays every artboard out in both themes.

## About the design files
The files are **design references made in HTML**. They show the intended look and behaviour and are not production code. `.dc.html` files are Claude Design "Design Components": inline-styled HTML with `{{ hole }}` placeholders filled by a small JS class. They only render inside Claude Design. Locally, treat them as readable markup, or convert them to plain HTML/CSS or the framework of your choice (the real app will be a desktop app; its stack is not decided in the brief). The brief's handback says another agent ("Pixel") will read the mockups as raw HTML and write a spec from them. Keep the markup machine-legible: `data-artboard`, `data-region`, `data-component`, `data-state`, `data-reserved`, `data-placeholder` attributes, and token names instead of literal values.

## Fidelity
High fidelity. Use the final tokens, type and spacing. Styling follows the **Ironworks Design System**: brass on warm near-black, Cinzel caps for labels, Source Sans 3 for body, IBM Plex Mono for every number. Brass is the single accent. The light theme is derived from the same token names. All numbers use tabular figures and are right-aligned in columns.

## Shell (all screens), 1440×900, must hold at 1100×700
Root grid rows: `--size-topbar` 44px / 1fr / `--size-statusbar` 26px.
Body grid columns: rail `--size-rail` 76px · targets `--size-targets` 256px · canvas `minmax(0,1fr)` · inspector `--size-inspector` 288px (collapses to a 32px column holding a "‹" button).
- **Top bar** (`--color-bg-deep`): a dashed 76×32 reserved slot (undo/redo, pause recalc) · plan name "Reinforced Plates" (Cinzel 15/600) · "Saved" (12px ghost) · game chip "Satisfactory 1.2" (no caret; becomes a menu later) · Recipes chip "RECIPES · 12 of 110 alternates on · [R]" · spacer · a dashed 132×32 reserved slot (units and precision).
- **Left rail**: glyph above a Cinzel 10px caps label. ⚙ Factories (selected: 2px left brass bar plus accent tint) · ◆ Codex · ◈ Milestones · ≡ Plan summary · a dashed reserved slot (future Map entry, do not draw it).
- **Status bar**: Power `54.37 MW` avg · `54.37 MW` peak · `13` buildings · ✓ `0` problems · spacer · Solved in `4 ms`.
- Keyboard hints use `<kbd>`: mono 10px, 1px subtle border, 2px radius.
- Reserved space is always a dashed `--color-border-subtle` box with `data-reserved` and a `title`. It contains no controls.

## S1 Factory view (light + dark)
- **Targets panel**: "TARGETS" (Cinzel 11 caps, accent) with "per minute" on the right. Target row: a 24px icon slot, "Reinforced Iron Plate", and a ✕ remove button (24px). Second line: rate field `7.5 /min` (mono, right-aligned, inset) and a mode select "Exactly ▼" (the other option is "As much as possible"). The "+ Add target [N]" field is drawn in its focus state to mark it as the primary action. Focus is a 2px `--color-focus` outline at 2px offset, kept distinct from hover (tint plus accent border).
- **Supply**: Iron Ore "Free up to cap", Cap field `120 /min`, "90 used", and a 4px gauge filled to 75%. "Arrives from elsewhere" is empty, with a "+ Add item with a rate" button. "Use exactly this much" is empty, with a "◉ Pin one resource" button and the line "Targets scale to match it."
- **Canvas**: a 34px tab row ("DIAGRAM" selected, dashed reserved tab for the step table, then zoom − 100% + and Fit [F]). The diagram uses a 16px dot grid. There is a dashed 28px reserved tool strip on the left edge for free-hand drawing. The graph layer is 832×480, absolute at top 96px, and scaled for zoom.
  - Nodes are 112px wide: 2px brass top rule, 32px icon slot, count `x3` (mono 15/600) top right, recipe/item name (13/600), machine (11 ghost), divider, then `clk 75.0000%` and `pwr 8.20 MW` (mono 11).
  - Positions (left, top): Iron Ore resource node (40,150), 80 wide with a dashed border and "cap 120". Smelter / Iron Ingot x3 100.0000% 12.00 MW at (180,132). Constructor / Iron Plate x3 75.0000% 8.20 MW at (352,22). Constructor / Iron Rod x2 75.0000% 5.47 MW at (352,242). Constructor / Screw x3 75.0000% 8.20 MW at (524,242). Assembler / Reinforced Iron Plate x2 75.0000% 20.50 MW at (696,132). The Assembler is **selected** (2px accent border, `--color-surface-high`) and carries a "◎ TARGET" tag plus "out 7.5/min" below it at (696,282). The graph layer is offset left:-10px so the output arrow fits the 820px canvas.
  - Edges are orthogonal 1.5px `--color-edge` lines with arrowheads, all the same width (no Sankey). Paths: `M120 194 H180` · `M292 194 H322 V84 H352` · `M322 194 V304 H352` · `M464 304 H524` · `M464 84 H682 V180 H696` · `M636 304 H664 V208 H696`. Label pills (mono 10.5, canvas background, subtle border): 90/min @(150,194), 67.5/min @(322,139), 22.5/min @(322,249), 22.5/min @(494,304), 45/min @(580,84), 90/min @(664,256).
  - Bottom right: hint "Arrows move between nodes ← → ↑ ↓".
- **Problems strip**: "PROBLEMS" plus "✓ No problems" in `--color-ok`.
- **Inspector** (Assembler): header "INSPECTOR" with a collapse button [ ] ]. Title row: icon, "Reinforced Iron Plate", "Assembler · 2 machines". RECIPE: current recipe plus "Swap [S]", and "3 alternates make this item · 0 on". Fields:
  - Machines `2`, labelled "Set by factor", with a "◉ Pin [P]" button.
  - Clock `75.0000 %`, labelled "Set by factor · same for all", with `= 3/4` beside it.
  - Power shards stepper `0 / 3` and Somersloops stepper `0 / 2` (32px buttons).
  - Power `20.50 MW (2 × 10.25)`.
  - FLOWS: in Iron Plate 45/min, in Screw 90/min, out Reinforced Iron Plate 7.5/min. Below that, a dashed placeholder box: "PLACEHOLDER: physical layer (ports, belt caps undecided)" with "Screw in: 1 x Belt Mk.2".
  - A dashed reserved slot (research levels, modules/beacons).

**S1 logic** (written). It takes props `theme` ('dark'|'light'), `inspectorOpen` (default true) and `zoom` (default 1), and must expose:
`theme`, `inspectorOpen`, `inspectorClosed = !inspectorOpen`, `inspectorCol = inspectorOpen ? 'var(--size-inspector)' : '32px'`, `zoomLabel = Math.round(zoom*100)+'%'`, `graphTransform = 'scale('+zoom+')'`. The 1100×700 check renders with the inspector collapsed at zoom 0.88.

Power figures are placeholders: base MW × clock^1.321928. Smelter 4, Constructor 4, Assembler 15, Refinery 30.

## S2 Factory view with problems and an edit (planned)
**Correction to the brief:** with Iron Ore capped at 80/min, 4 pinned Iron Plate constructors run at **50.0000% (1/2)**, not 56.25% (9/16). 56.25% only holds at 90/min ore. Show 50.0000% and flag the change on the canvas. This was confirmed with Peter.

- Iron Ore resource node: `80/min`, "AT CAP · limiting". Smelter x3 88.8888% (8/9) 10.27 MW, output 80/min. Ingot split 60 → plates, 20 → rods.
- Iron Plate x4 at 50.0000% (1/2), 6.40 MW, **pinned**. Show a ◉ pin marker by the count and the tag "PINNED". Output 40/min.
- Rod x2 66.6667% 4.68 MW, 20/min. Screw x3 66.6667% 7.02 MW, 80/min. Assembler x2 66.6667% 17.56 MW, out 6.6667/min, with node marker "▼ SHORT 0.8333/min".
- Plastic lane below: Crude Oil 30/min → Refinery (Plastic) x1 100.0000% 30.00 MW. It sends 20/min Plastic to its target (met) and 10/min Heavy Oil Residue to a dangling "◆ UNHANDLED 10/min" terminal.
- Targets: Reinforced Iron Plate 7.5 Exactly, with the row status "6.6667 made · ▼ 0.8333 short". Plastic 20 Exactly, "✓ met".
- Problems strip (auto height), one line per problem, each with icon + word + text + fix buttons that state the number they will set:
  - `▼ SHORTFALL` "Reinforced Iron Plate: 0.8333/min short of target. Limited by Iron Ore cap (80/min)." Buttons: [Raise Iron Ore cap to 90/min] [Lower the target to 6.6667/min].
  - `◆ UNHANDLED BYPRODUCT` "Heavy Oil Residue: 10/min from Refinery (Plastic) has nowhere to go. Would back up in-game." Buttons: [Feed back] [Send 10/min to AWESOME Sink] [Leave flagged].
- Inspector shows Iron Plate. Machines `4` with "◉ Set by you" and an [Unpin] button. Clock 50.0000% `= 1/2`, "Set by factor".
- Status bar: 75.93 MW avg/peak · 15 buildings · 2 problems · 6 ms.
- **Re-solving variant**, a third artboard. The previous diagram stays visible at about 45% opacity (never blanked), with a banner at the top of the canvas: "◌ Re-solving · showing previous plan" and a timer. Status bar reads "Solving…".

## S3 Recipes and rules drawer (planned)
Opens from the Recipes chip (drawn active). The shell sits behind a `--color-scrim`. A 600px right drawer below the top bar holds, in order:
- Header "RECIPES AND RULES" with ✕ [Esc].
- Progression tier (a segmented row, up to the selected tier).
- Alternate recipes "12 of 110 on": search [/], filter chips (All · On · Off), and [All on] [All off]. Rows: toggle · name · makes · machine. Use real names: Adhered / Bolted / Stitched Iron Plate (Assembler), Cast Screw, Steel Screw, Steel Rod (Constructor), Pure Iron Ingot, Residual Plastic, Recycled Plastic, Heavy Oil Residue (Refinery), Iron Alloy Ingot (Foundry), Coated Iron Plate (Assembler).
- Converter recipes: one group toggle.
- Game-mode multipliers: Recipe cost ×1, Power use ×1, Space Elevator cost ×1.
- A closed "More ▸" disclosure, the reserved home for objective/scarcity weights.

## S5 Plan summary and power (planned, S1 data)
Rail shows Plan summary selected. The inspector is collapsed. Two columns.
- **Left**:
  - Raw resources (Iron Ore 90 of 120 cap).
  - Production vs consumption, columns made / used / net: Ingot 90/90/0, Plate 45/45/0, Rod 22.5/22.5/0, Screw 90/90/0, Reinforced Iron Plate 7.5/0/+7.5 target.
  - Buildings: Smelter 3, Constructor 8, Assembler 2, total 13.
  - Shards 0, sloops 0.
- **Right**:
  - Power avg/peak 54.37 MW.
  - Per-machine rows.
  - Variable-power machines (min/avg/max): empty "None in this plan".
  - Alien Power Augmenter boost 0%.
  - Non-producing buildings: empty.
  - The toggle, verbatim: "Include the generators and fuel this plan needs, so its power cost shows up as raw resources".
  - Power plant sizer, From MW | From fuel. Example: 54.37 MW on Coal Generator (75 MW) gives 1 × at 72.4933% with fuel and water. Recompute exactly; geothermal is listed as an option.
  - Destinations: AWESOME Sink points/min and Dimensional Depot uploads (both empty, no surplus).
- Dashed reserved blocks: bill of materials, Space Elevator phases.

## S6 Factories and ledger (planned)
Factory cards:
- "Iron Smelting": Smelter x3, sends 90/min Iron Ingot, ✓.
- "Reinforced Plates": imports 90/min Iron Ingot. Holds a collapsed nested sub-plan block "Screws". Item rows carry a "Spin off this chain" action.
- "Plastic": ◆ 1 problem, unhandled Heavy Oil Residue 10/min.

Each card has notes and a task list, plus a dashed reserved header slot (power balance, rollups, health). Draw a link between Iron Smelting and Reinforced Plates labelled "90/min Iron Ingot", with a reserved transport slot on the link.

Ledger table: Item | From | To | Rate | Supplier covers. Rows: Iron Ingot · Iron Smelting → Reinforced Plates · 90/min · ✓ Yes, and Heavy Oil Residue · Plastic → (unassigned) · 10/min · ◆ unhandled.

**Every nesting and link element carries the tag "PLACEHOLDER: factory organisation undecided".**

## Component-states sheet (planned, both themes)
Labelled variants (default, hover, focus, selected, disabled, error/shortfall, empty, loading where they apply) for:
- Button and fix button
- Rate field: default, focus, error, disabled, pinned
- Target row
- Supply row
- Node: default, hover, selected, focus, pinned, shortfall, byproduct, compact zoomed-out chip (icon + count), re-solving
- Sub-plan summary block
- Problem line (shortfall, surplus, unhandled byproduct, supplier cannot cover, empty)
- Toggle
- Rail item
- Tab
- Placeholder tag

## Status vocabulary (never colour alone)
| Kind | Glyph | Word | Token |
|---|---|---|---|
| Shortfall | ▼ | SHORTFALL / SHORT | `--color-short` |
| Surplus | ▲ | SURPLUS | `--color-surplus` |
| Unhandled byproduct | ◆ | UNHANDLED BYPRODUCT | `--color-byproduct` |
| Supplier cannot cover | ■ | SUPPLIER SHORT | `--color-short` |
| OK | ✓ | No problems | `--color-ok` |
| Pinned (set by you) | ◉ | Set by you / PINNED | `--color-accent` |

## Design tokens
All tokens are in `factor-tokens.css`, under `[data-theme]` (type, spacing, radii, sizes), `[data-theme="dark"]` and `[data-theme="light"]` (colours, shadows). Key values:
- Type: Cinzel (caps labels only, 0.1em tracking), Source Sans 3, IBM Plex Mono. Sizes 10/11/12/13/15/18/22.
- Spacing: 2/4/8/12/16/24/32. Radii: 2/3/6. Hit areas: 24 min, 32 preferred.
- Dark: bg #1a1612, surface #2a2219, text #e8e0d0, accent #d4af70 (fill #b08d57), control border #8a6a35, focus #e8c97a.
- Light: bg #efe9de, surface #faf7f1, text #241d15, accent #7a5a26 (fill #8a6a35), control border #8a7458, focus #1c2a3a.

## Assets
None. Icons are neutral dashed square slots (24px in rows, 32px on nodes) with a "◇" glyph, because real game icons get extracted later. Glyphs are unicode only. No icon library, no emoji, no game art.

## Files
- `ui-brief.md`: the original brief, the source of truth.
- `factor-tokens.css`: the token set (complete).
- `S1 Factory View.dc.html`: S1 (complete).
- `screenshots/01-S1-factory-view.png` (dark), `screenshots/02-S1-factory-view.png` (light).
