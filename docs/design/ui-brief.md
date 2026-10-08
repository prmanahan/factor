# factor: UI design brief for Claude Design

Written 2026-10-08. This is the **input** to Claude Design (Anthropic's design canvas), not a design spec.
The paste block in section 8 is self-contained, because Claude Design cannot see the repo. Everything
outside section 8 is for traceability and may use D-numbers and F-numbers.

**Labels used here.** *Ruled* = Peter decided it (`docs/decisions.md`). *Proposal* = a design call Pixel made
that Peter has not ruled; Claude Design may be shown it, and Peter can overrule it. *Open* = undecided, so
the mockups show a marked placeholder. Peter's verdicts per feature are snapshotted in
`docs/design/feature-verdicts.md` (source of truth: the picker database). Counts there: 49 mvp, 29 shape,
27 later, 37 skip.

---

## 1. Product and user

**Product.** factor is a desktop production calculator for factory games. It does two jobs: it plans a
factory to hit targets you set, and it draws that plan as a diagram. It has to stay correct and fast on very
large factories, which is where Satisfactory Modeler (the benchmark, and what Peter uses today) freezes.
Satisfactory is the first game; Factorio, Techtonica, Foundry and Alchemy Factory follow, so nothing in the UI
may be Satisfactory-shaped in its structure.

**User, task, time budget** (stated because every layout choice below is measured against them):
- **User:** Peter. Experienced Satisfactory player who optimises with exact clocks (e.g. 88.8888%).
  First build is for him alone. Hobby project.
- **Context:** the game runs in one window and factor in another, so he alt-tabs. The factor window is
  probably a half or a second screen, not necessarily full size (*inferred* from F-087 note, not stated as a
  size).
- **Tasks, in order of frequency:** (1) read an existing plan to find the number he needs in-game, a few
  seconds per visit; (2) change a target or a constraint and see what moves; (3) plan a new factory from
  scratch, minutes to an hour; (4) look something up (a recipe, an unlock cost).
- **Primary action per screen:** one. On the factory view it is "change what I want to make" (the target
  rows). Everything else is secondary.

## 2. Core interaction (D-024, ruled)

One view. Peter sets targets; factor solves and lays out the diagram; edits to the diagram become
constraints that re-solve. Free-hand Modeler-style drawing comes later on the same engine (F-003 *shape*), so
the layout reserves space for it but does not draw it.

**Where targets are set.** A **Targets panel** on the left of the factory view. Each row: item icon, item name,
rate field ("per minute" is the default unit), and a mode (exactly this rate, or as much as possible; F-006).
An "Add target" field at the bottom. Under the targets sits a **Supply** group (F-007, F-008, F-009): raw
resources default to "free up to a cap" (D-018) with the cap editable; any item can be marked "arrives from
elsewhere" with a rate (F-008); one resource can be pinned to "use exactly this much" and the targets scale to
it (F-007).

**How the diagram appears.** Centre canvas. After any change factor re-solves and lays out a flow graph,
raw resources on the left to targets on the right (**proposal**: left-to-right flow). Positions Peter drags
are kept across recalculation and sessions (F-074). A node's size is uniform; edges are uniform thin lines
with a rate label, **not** width-scaled (Peter disliked FactorioLab's Sankey, F-070).

**What a node shows** (D-008, D-022: exact values):
- item icon of the main product, machine name, recipe name (alternates carry the "Alternate:" marker);
- machine count, e.g. `x3`;
- clock, shown to 4 decimal places like `75.0000%` or `88.8888%`, with the exact fraction available on
  hover or in the inspector (`8/9`);
- power in MW (variable-power machines show min / avg / max, F-038);
- input and output rates on the edges, exact (`37.5/min`), not rounded to fit.

**What editing a node does.** Selecting a node opens the **Inspector** on the right (F-073). From there
Peter can: swap the recipe to another that makes the same product (F-025; the swap list is the alternate
comparison, F-023); fix the machine count; set clock mode, power shards and somersloops (F-031, F-032, F-033).
Each of these is stored as a **constraint** and the plan re-solves. A constrained field is visibly "set by you"
(a pin marker plus an "unpin" control), against solved values that are "set by factor" (**proposal**: this
is the cue that makes one-view editing legible). Unpinning returns the field to factor's choice.

**How named problems surface (D-023).** The plan always returns an answer; problems are named, never a
bare "infeasible". Three places, none relying on colour alone (icon + word + position):
1. a **Problems strip** pinned under the canvas, one line per problem, e.g. "Reinforced Iron Plate:
   0.8333/min short of target. Limited by Iron Ore cap (80/min)";
2. a marker on the affected node (shape-coded icon plus a short word);
3. the affected edge or supply row labelled with the amount.
Problem kinds in the first build: **shortfall** (target not met, with the limiting input named),
**surplus** (made but unused), **unhandled byproduct** (F-014: would back up in-game), **supplier cannot
cover** (F-052). Each line carries named fix actions with the number they will set (**proposal**, borrowed from
Satisfactory Factories' "Satisfy (240)" and Foreman2's click-to-resolve): e.g. "Raise Iron Ore cap to
90/min", "Send 10/min Heavy Oil Residue to AWESOME Sink". A severity taxonomy beyond these four kinds is
F-059 *shape*: leave room, do not design it.

## 3. Screens for the first round of mockups

Screen IDs below are the names Claude Design must put on artboards (section 8). Grouping is a **proposal**.
Priority **R1** = ask for in the first round; **R2** = describe in the prompt so the shell is right, ask for
later.

### Window shell (applies to every screen)
Native desktop window, resizable. **Proposal:** design at 1440x900, check that it holds at 1100x700.
Regions: a **top bar** (plan name, game chip "Satisfactory 1.2", save state, undo/redo slot reserved, units and
precision slot reserved); a **left rail** (Factories, Codex, Milestones, Plan summary); the **main area**; a
**right Inspector** (collapsible); a **status bar** (power avg/peak, building count, problem count, solve time).
No browser chrome, no marketing furniture, no ads. Menu bar and file dialogs are native, not drawn.

### Group A: Plan a factory (the heart)
| ID | Screen | Must show | Round |
|---|---|---|---|
| S1 | **Factory view** | Targets panel + Supply group, diagram with nodes and exact edge labels, Inspector with a node selected (recipe, count, clock `75.0000%` with `3/4`, shards, sloops, power), status bar, Problems strip empty ("No problems"). Light and dark. | R1 |
| S2 | **Factory view, with problems and an edit** | Same shell. Iron Ore capped at 80/min; shortfall line with named fixes; a node pinned by Peter (pin marker, unpin); one node showing `88.8888%`; an unhandled-byproduct node; a "re-solving" state (previous diagram dimmed, not blanked). | R1 |
| S3 | **Recipes and rules drawer** | Opens from a "Recipes" chip in the top bar, showing a summary like "12 of 110 alternates on". Progression tier (F-021), alternate toggles with search and filter and bulk on/off (F-019), converter recipes on/off as a group (F-020), game-mode multipliers: recipe cost, power, Space Elevator cost (F-026). Advanced options sit behind a "More" step. | R1 |
| S4 | **Supply and extraction** | Per raw resource: cap (default "free up to cap"), nodes owned by purity and miners needed by mark and clock (F-043, F-044), resource wells with pressuriser and satellites (F-045), hand-gathered items marked as such (F-047). | R2 |

### Group B: Understand the whole plan
| ID | Screen | Must show | Round |
|---|---|---|---|
| S5 | **Plan summary and power** | Raw resources, each item's production vs consumption, building counts by type, shards and sloops used (F-057). Power: total avg and peak, variable-power machines as min/avg/max (F-038), Alien Power Augmenter boost (F-042), non-producing buildings with their power (F-061), a "power the plan with its own generators" toggle in one plain sentence (F-040; Peter: "i need to understand this one more", so describe it, do not decide its shape), the power plant planner sized from MW or fuel (F-039, geothermal included per Peter's note), AWESOME Sink points/min and Dimensional Depot uploads as destinations (F-062, F-063). | R1 |
| S6 | **Factories and ledger** | Several factories in one plan (F-053), a nested sub-plan collapsed to a summary (F-054), spin-off of a sub-chain from a shortage or item row, linked back as an import (F-056), import/export ledger: what each factory sends and receives and whether the supplier can cover it (F-052), notes and task list per factory (F-067). **Organisation is OPEN (D-035): everything about nesting and linking is a marked placeholder.** | R1 |

### Group C: Look things up
| ID | Screen | Must show | Round |
|---|---|---|---|
| S7 | **Codex** | Browse items, recipes, buildings, generators (F-088); an item page with "Made by" (every recipe, alternates compared side by side on raw cost, power, buildings; F-023) and "Used in" (F-089). | R2 |
| S8 | **Milestones** | Tick-off list of milestones, MAM research and AWESOME Shop unlocks with costs (F-090). Peter's note says tier gating (F-021) and this tracker look contradictory; mock them as separate and **do not link or reconcile them**. | R2 |

### Group D: Tools and files
| ID | Screen | Must show | Round |
|---|---|---|---|
| S9 | **Splitter calculator** | Peter's own use case (F-049): "build 240/min and send 75 to x and 100 to Y and store the rest". Input flow, a list of destinations with fixed amounts, the remainder computed (65/min), and the resulting splitter/merger arrangement drawn as an abstract schematic (no belt positions). Supports any split, which Modeler cannot. | R2 |
| S10 | **Plans home and empty state** | Named local plans (F-131), open/save as a file (F-129; no JSON anywhere in the UI wording), a demo plan to open (D-034), and the **empty factory view**: no targets yet, one obvious input, no tour. | R2 |

### Reserve space, draw nothing (the *shape* rows)
These must not get a control in the first build, but the layout must not need rearranging when they arrive.
**Proposal** for where each goes:

| Feature | Reserved place |
|---|---|
| F-018 undo/redo, F-017 pause recalculation | top bar, left of the plan name |
| F-076 units and precision (per minute / hour, exact rationals) | top bar, right |
| F-030/F-135 game and version switcher | the "Satisfactory 1.2" chip becomes a menu |
| F-010/F-011 objective and scarcity weights (D-023: behind advanced options) | S3 "More" step |
| F-003 free-hand drawing | a tool strip on the canvas edge |
| F-071 step table | a second tab beside the diagram |
| F-035 research levels, F-036 modules/beacons | Inspector, below shards and sloops |
| F-041 power balance per factory, F-055 group rollups, F-059 severity health | S6 factory card header |
| F-051 transport planning | S6 link between two factories |
| F-058 bill of materials, F-091 dependency explorer, F-092 cost analysis | S5 and S7 as extra sections |
| F-060 Space Elevator phases | S5 as an extra section |
| F-095/F-096 maps | left rail has room for a "Map" entry; **do not draw it**. F-096 (collectibles) is core to Peter but after planning. |
| F-078 localisation | no control; see layout constraints |

Everything marked *later* or *skip* is out of scope for mockups.

## 4. Binding constraints

1. **Desktop app** (D-001): macOS first, Windows later. Do not copy macOS-specific chrome
   into the content area. No server, no accounts, no sign-in, no sharing UI (D-030).
2. **One view** (D-024): never split "targets" and "drawn graph" into two modes.
3. **No walkthrough** (D-034): no tour, no coach marks, no multi-step wizard. Advanced options appear
   step by step ("More" disclosures). A demo plan is allowed.
4. **Exact values** (D-008, D-022): clocks to 4 decimal places, rates as exact numbers (`37.5/min`), the exact
   fraction one step away (`75/2`, `8/9`). Never round a number to make it fit a cell.
5. **Elastic problems** (D-023): a plan always renders; problems are named with amounts and a limiting cause.
6. **Raw resources** default to "free up to a cap" (D-018).
7. **Globalisation shaped in** (D-031): labels may be about 40% longer in other languages (**proposal** for the
   margin), so no fixed-width text buttons and no text baked into icons; numbers are formatted in the view
   (decimal separator may be a comma); layout must survive the longest real names ("Reinforced Iron Plate",
   "Heavy Oil Residue").
8. **Graphics are a replaceable view** (D-032): the mockup is the desktop view only; no behaviour that needs
   to live in the view and not the engine.
9. **Icons** (D-019): real game icons are extracted from Peter's own install later. Mockups use neutral
   **icon slots** (square, 24px in rows, 32px on nodes) with a placeholder glyph, never copied game art. The
   layout must work with any icon.
10. **Light and dark, following the system** (F-079: user-selectable themes, hue and scale are *later*): draw
    both from one set of named tokens; no theme picker.
11. **Large factories:** the diagram must stay legible at hundreds of nodes. **Proposal:** zoomed out, nodes
    shrink to compact chips (icon + count); nested sub-plans collapse to one summary block.
12. **Keyboard** (F-080 *mvp*): every action reachable without a mouse. Needed in the first build: add a
    target, move between nodes along edges (arrow keys), open the recipe swap, edit count and clock, pin and
    unpin, remove a target, nudge a node. Linking nodes belongs to free-hand drawing (later). Show a
    shortcut hint on the main controls. Command palette (Cmd+K) is *later*: do not draw it.
13. **Accessibility floor:** text contrast at least 4.5:1, large text and meaningful non-text (borders on
    controls, focus rings, edge lines, status icons) at least 3:1, in both light and dark; status never by
    colour alone (icon shape + word); visible keyboard focus distinct from hover; no information in hover
    only. Target size: **proposal** 24x24px minimum hit area (WCAG 2.2 AA) at desktop density, 32px
    preferred; the 44px touch floor applies when the phone layout (F-085, *later*) is designed.
14. **Density:** this is a pro tool used beside a game. **Proposal:** compact rows, tabular (equal-width)
    figures right-aligned so rates compare down a column.

## 5. What to avoid

From Modeler and the other tools (`docs/research/calc-tools.md`; *reported* items are third-party):
- Slow or freezing on large builds (*reported*): never imply that the UI blocks. Show a re-solving state and
  keep the last diagram visible.
- Steep learning curve and clunky UI (*reported*): the interface itself has to teach; no walkthrough
  (Satisfactory Logistics' demo/walkthrough was cited by Peter as the thing not to need, D-034).
- Hard-to-follow factory organisation (Peter, D-017): do not copy Modeler's nested sub-canvases as-is, and
  do not decide the replacement (D-035 open).
- Cannot set custom split ratios (*reported*): the splitter screen must take arbitrary amounts.
- Graph layout lost between tabs and no "done" marker on nodes (SatisfactoryTools, *observed*): positions
  persist.
- Cannot pick a recipe from the visualisation (SatisfactoryTools, *observed*): swap is on the node.
- A bare "infeasible" or an unexplained empty result (D-023).
- Sankey diagrams (F-070) and width-scaled edges.
- Advert pop-ups and cookie-style banners (SCIM, *observed*); account prompts; sharing/collab furniture
  (F-124 to F-128 are *skip*).
- Decoration that serves no task: gradients, illustration, hero banners, mascot. If an element cannot be tied
  to reading or changing the plan, leave it out.
- Colour as the only status signal.

## 6. Open points the mockups must treat as placeholders

- **Factory organisation (D-035, open):** what a factory is in the model, how flows between factories are
  represented, how deep nesting goes, how a spun-off sub-chain stays linked. Mock: a list of factories, one
  collapsed nested block, and one import link, all wearing a visible tag **"PLACEHOLDER: factory
  organisation undecided"**.
- **Physical layer (D-012, open):** machine ports, port positions, belt caps as constraints. Mock: edges
  attach to a node as a whole, not to a port. Belt/pipe count per flow (F-048, *mvp*) is shown as plain text
  in the Inspector or an edge tooltip (`1 x Belt Mk.2`), tagged **"PLACEHOLDER: physical layer"**, with no
  port art.
- **Carrier naming (D-013) and route consumption (D-014):** call the thing "Belt / Pipe" and do not draw
  trains, trucks or drones (F-051 is *shape*).
- **Visual style is not ruled.** Nothing in the decisions says what factor should look like. **Proposal:** a
  restrained, dense, tool-like look: one accent colour, neutral surfaces. Peter can change this after
  seeing it. Pixel has no basis for judging whether it is distinctive.
- **Tier gating vs milestone tracker** (F-021 and F-090): Peter flagged them as contradictory; unresolved.
- **Self-powered factory** (F-040): Peter wants to understand it before it is designed.
- **Game numbers not yet in the data** (purity multipliers, node positions): show purity as a label
  (Impure / Normal / Pure), never a multiplier number.

## 7. Worked example (real content for the mockups)

Rates, counts and clocks below are exact arithmetic from the standard Satisfactory recipes. **The six recipes
used (Iron Ingot, Iron Plate, Iron Rod, Screw, Reinforced Iron Plate, Plastic) were checked against
`resources/CommunityResources/Docs/en-US.json` on 2026-10-08: inputs, outputs and durations match.** MW figures are deliberately omitted:
power is not in this example, so ask Claude Design for plausible placeholder MW and have Peter's real data
replace them.

**Target: 7.5 Reinforced Iron Plate/min.** (Recipes: Iron Ingot 1 ore to 1 ingot; Iron Plate 3 ingots to 2
plates; Iron Rod 1 ingot to 1 rod; Screw 1 rod to 4 screws; Reinforced Iron Plate 6 plates + 12 screws to 1.)

| Node | Count | Clock | Output |
|---|---|---|---|
| Iron Ore (free up to cap) | n/a | n/a | 90/min |
| Smelter, Iron Ingot | x3 | 100.0000% | 90/min |
| Constructor, Iron Plate | x3 | 75.0000% (3/4) | 45/min |
| Constructor, Iron Rod | x2 | 75.0000% | 22.5/min |
| Constructor, Screw | x3 | 75.0000% | 90/min |
| Assembler, Reinforced Iron Plate | x2 | 75.0000% | 7.5/min |

Ingot split: 67.5/min to plates, 22.5/min to rods. **Edit example:** pin Iron Plate to 4 machines, and they
re-solve to 56.2500% (9/16) each. **Problem example:** cap Iron Ore at 80/min. Smelters become x3 at
88.8888% (8/9) and every downstream clock scales by 8/9; Reinforced Iron Plate falls to 6.6667/min (20/3),
**0.8333/min (5/6) short of the 7.5/min target, limited by the Iron Ore cap**. Fix actions: "Raise Iron Ore
cap to 90/min" and "Lower the target to 6.6667/min".

**Byproduct example:** Plastic (30 Crude Oil/min to 20 Plastic/min + 10 Heavy Oil Residue/min). The 10/min
Heavy Oil Residue is flagged unhandled, with actions: feed back, send to AWESOME Sink, leave flagged.

**Factories example (S6):** the same plan after "spin off Iron Ingot": factory "Iron Smelting" supplies 90/min
Iron Ingot to "Reinforced Plates"; a second factory "Plastic" shows the byproduct problem. Ledger row: Iron
Ingot, Iron Smelting to Reinforced Plates, 90/min, supplier covers: yes.

## 8. Paste block for Claude Design

Everything between the two rules is the prompt. It has no decision IDs and does not depend on the repo.

---

**Design the first round of screens for "factor", a desktop production calculator for factory games.**

**What it is.** factor plans a factory for you and draws it. You say what you want to make and how fast; factor
chooses the recipes and machine counts, works out the exact machine speeds and power, and draws the result as
a flow diagram. It is for one user: an experienced Satisfactory player who optimises with exact machine speeds
(clock speeds like 88.8888%) and runs the game in one window and this tool in another. He glances at it for
seconds to find a number, changes a target and watches what moves, or plans a new factory over an hour. It must
stay fast and readable on factories with hundreds of machines. Satisfactory is the first game; later games
(Factorio, Techtonica, Foundry, Alchemy Factory) must fit the same structure, so do not make the layout
Satisfactory-specific.

**The core idea: one view.** The user sets targets on the left. factor solves and draws the diagram in the
centre. If the user changes something on the diagram (picks a different recipe on a machine, fixes the number
of machines, limits an input), that becomes a constraint and the plan re-solves. A value the user set is marked
as theirs (a pin marker, with an unpin control); a value factor chose is not.

**Window.** A native desktop window, 1440x900, also working at 1100x700. A top bar (plan name, a game chip
"Satisfactory 1.2", save state; leave empty room left of the name for undo/redo and right of the bar for a units
control), a left rail (Factories, Codex, Milestones, Plan summary; leave room below for one more entry), a main
area, a collapsible right Inspector, and a status bar (power average and peak, building count, problem count,
solve time). No browser chrome. Compact, dense, tool-like; one accent colour, neutral surfaces; no gradients,
illustrations or decoration. Draw every screen in **light and dark** from one set of tokens (follows the system
setting; no theme picker).

**Real content.** Use this, not placeholder text. Target: 7.5 Reinforced Iron Plate per minute. Nodes:
Smelter (Iron Ingot) x3 at 100.0000%, 90/min; Constructor (Iron Plate) x3 at 75.0000%, 45/min; Constructor
(Iron Rod) x2 at 75.0000%, 22.5/min; Constructor (Screw) x3 at 75.0000%, 90/min; Assembler (Reinforced Iron
Plate) x2 at 75.0000%, 7.5/min. Iron Ore is supplied free up to a cap and 90/min is used. Ingots split
67.5/min to plates and 22.5/min to rods. Node content: item icon slot, machine name, recipe name, machine
count, clock to 4 decimals, power in MW (invent plausible numbers). Edges: uniform thin lines with the exact rate
as a label (37.5/min, not 38). Show the exact fraction on hover or in the Inspector (75.0000% is 3/4).
Item icons are not available: use neutral square icon slots (24px in lists, 32px on nodes) with a simple
placeholder glyph, and make sure the layout works with any icon. Never use copied game artwork.

**Screens for this round** (name each artboard with its ID and name):

- **S1 Factory view** (light and dark). Left: a Targets panel (rows of icon, item, rate per minute, and a mode:
  exactly this rate, or as much as possible; "Add target" field at the bottom), and under it a Supply group
  (raw resources "free up to a cap" with the cap editable; items that "arrive from elsewhere" with a rate; one
  resource that can be pinned to "use exactly this much"). Centre: the diagram, flowing left to right, raw
  resources to targets. Right: the Inspector for a selected Assembler node: recipe (with a way to swap to another
  recipe for the same product), machine count, clock 75.0000% with "3/4", power shards, somersloops, power.
  Under the canvas: a Problems strip reading "No problems".
- **S2 Factory view with problems and an edit.** Same layout. Iron Ore is capped at 80/min, so Smelters run x3
  at 88.8888% (8/9) and everything downstream scales; Reinforced Iron Plate makes 6.6667/min and is
  0.8333/min short of the 7.5/min target, limited by the Iron Ore cap. The Problems strip names this with
  buttons that state the number they will set ("Raise Iron Ore cap to 90/min", "Lower the target to
  6.6667/min"). Show a node the user pinned to a fixed machine count (4 Iron Plate constructors at 56.2500%,
  9/16), an unhandled byproduct node (a Plastic refinery with 10/min Heavy Oil Residue not going anywhere, with
  actions: feed back, send to the AWESOME Sink, leave flagged), and a "re-solving" state where the previous
  diagram stays visible but dimmed. Problems must show as icon plus word plus position, never only colour.
- **S3 Recipes and rules drawer.** Opens from a "Recipes" chip in the top bar that shows a summary such as "12
  of 110 alternates on". Contains: progression tier; a searchable, filterable list of alternate recipes with
  on/off toggles and bulk on/off; converter recipes on/off as one group; game-mode multipliers for recipe cost,
  power use and Space Elevator cost. Advanced options sit behind a "More" step, revealed only when asked for.
- **S5 Plan summary and power.** Plan totals: raw resources used, each item's production versus consumption,
  building counts by type, power shards and somersloops used. Power: total average and peak, variable-power
  machines shown as min, average and max, a booster percentage, buildings that make nothing (portals, sink)
  with their power, a toggle "Include the generators and fuel this plan needs, so its power cost shows up as
  raw resources" and a power plant sizer (from a megawatt target or from available fuel). Also AWESOME Sink
  points per minute and Dimensional Depot uploads as places surplus can go.
- **S6 Factories and ledger.** A plan can hold many factories: show a list or cards, with one nested
  sub-plan collapsed to a summary block, a "spin off this chain" action from a shortage, and an import/export
  ledger (what each factory sends to and receives from the others, and whether the supplier can cover it).
  Example: factory "Iron Smelting" sends 90/min Iron Ingot to "Reinforced Plates" (supplier covers: yes); a
  third factory "Plastic" has the byproduct problem. Each factory has notes and a task list. **How factories
  nest and link is undecided: mark all nesting and linking as a visible placeholder.**

Screens to come in a later round (so the shell is ready for them, but do not draw yet): S4 Supply and
extraction (miners per node by purity, resource wells), S7 Codex (browse items and recipes; an item page with
"made by" and "used in", alternates compared side by side), S8 Milestones (tick-off list with costs), S9
Splitter calculator (a flow of 240/min split into 75 to site X, 100 to site Y and 65 stored), S10 Plans home
and the empty factory view.

**Rules the design must follow.**
- One primary action per screen. On the factory view it is changing what to make.
- No tutorial, tour, coach marks or wizard. The interface must be self-explanatory; advanced options appear in
  steps ("More").
- Numbers are exact, never rounded to fit: clocks to 4 decimals, rates like 37.5/min, fractions on demand.
  Use equal-width figures, right-aligned in columns.
- Never show a bare "infeasible". A plan always draws, with named problems: shortfall, surplus, unhandled
  byproduct, supplier cannot cover.
- Layouts must survive labels about 40% longer (other languages) and long names like "Reinforced Iron Plate".
  No fixed-width text buttons; no text inside images.
- The diagram must stay legible with hundreds of nodes: when zoomed out, show compact chips (icon and count)
  and collapse sub-plans to one block. Do not scale edge width by rate and do not draw a Sankey diagram.
- Keyboard: every action reachable without a mouse; show clear focus rings, distinct from hover; show shortcut
  hints on main controls. Do not draw a command palette.
- Accessibility: text contrast at least 4.5:1; large text and meaningful non-text (control borders, focus
  rings, edge lines, status icons) at least 3:1, in both light and dark. Status never by colour alone. No
  information only on hover. Minimum clickable area 24x24px, 32px preferred.
- Do not include: accounts, sign-in, sharing, adverts, collaboration, a theme picker, trains/trucks/drones, or a map.
- Physical layout details are undecided: edges join a node as a whole (no ports). Belt count per flow ("1 x Belt
  Mk.2") may appear as plain text in the Inspector or an edge tooltip, marked as a placeholder.

**Handback.** The canvas will be read afterwards as raw HTML and turned into a written spec by another agent, so
make it machine-legible:
1. Name every artboard with its screen ID and name from the list above (for example "S2 Factory view with
   problems and an edit"), and add "light" or "dark" where it applies.
2. Declare colour, spacing and type tokens once (named, for example `--color-surface`, `--space-3`,
   `--text-body`) and use them by name everywhere; no one-off hex values or pixel sizes in components.
3. Show each reusable component's states as labelled variants: default, hover, selected, error or shortfall,
   disabled, empty (add focus and loading where they apply).
4. Mark every placeholder visibly (factory nesting and linking, ports and belt caps), with the label text
   "PLACEHOLDER" and what is undecided.
5. Use the real example data above (Satisfactory items, exact rates like 37.5/min, clocks like 88.8888%), never
   lorem ipsum.
6. Keep all text as live text, never baked into images, and keep icons as separate swappable slots.

---

## 9. After Claude Design

Peter pastes section 8 into Claude Design and brings the resulting canvas link back to the lead (the session
that dispatched this brief). The lead routes the link to Pixel, who reads the canvas as raw HTML and converts
it into a design spec per screen ID (layout per breakpoint, tokens by name, states, accessibility with
measured contrast ratios, open questions). An implementer builds from that spec, not from the canvas. Nothing
in the canvas counts as ruled: every proposal in this file that survives into the canvas still needs Peter's
confirmation, and the placeholders (D-035, D-012) stay placeholders in the spec.

Why the handback asks for tokens and labelled variants: the spec must name values, and a reader of raw HTML
can only recover a token or a state if it is declared by name. Contrast ratios will be **measured from the
canvas's declared token values**, not taken on trust from the mockup.

## 10. Design calls made here that Peter has not ruled (all proposals)

1. Left-to-right flow, raw resources to targets.
2. Uniform thin edges with rate labels; no width scaling.
3. Pin marker + unpin as the cue for "set by you" versus "set by factor".
4. Named fix buttons on problem lines, each stating the number it will set.
5. Window shell: top bar, left rail, right Inspector, status bar; 1440x900 design size, 1100x700 check.
6. Compact chips when zoomed out; sub-plans collapse to one block.
7. Reserved-space placements for the *shape* rows (table in section 3).
8. Alternate toggles, tier, converter switch and multipliers in one drawer (S3), advanced behind "More".
9. Minimum hit area 24px (32px preferred) at desktop density instead of the 44px touch floor.
10. Labels allow 40% growth for translation.
11. Restrained, one-accent, dense visual style.
12. Tier gating and milestone tracker mocked separately, unreconciled.
13. Screen grouping, IDs and the R1/R2 split.
14. The worked example (recipes checked against the Docs data; MW omitted).
