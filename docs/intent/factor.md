---
spec_type: architecture
frame_relevant: true
---
**Locked: 2026-10-08**

# Product Brief: factor

**Date:** 2026-10-08  ·  **Status:** locked  ·  **Altitude:** product
**Intake gate:** Peter chose "Confirm and lock" on 2026-10-08, which covers every interpretation labelled **Puck's reading** below. **spec_type:** Peter chose "architecture, Frame in core-model run". This product run stops at the locked brief, and its Frame is done once, by the next `/brief` run on the core model. That is a recorded deviation from the skill's product-altitude machinery, which would otherwise run a product-level Frame and Spec.
**Review record:** four Intake review rounds (Warden in review and security mode, Glitch, Ink, Pixel), in `docs/intent/reviews/factor/`. Round 4 returned zero blockers and zero highs.
**Stakes:** high  ·  **Consumer:** mixed (Peter first; other players later; agents read it cold)

> Format note: this is a living document. Its structure is a forward-contract with specops, which owns its evolution via delta-merge. Do not restructure ad hoc.

> Source note: every field below is assembled from Peter's own words, quoted with their date, from his answers in the 2026-10-08 intake, or from a ruled decision in `docs/decisions.md`, cited by its `D-NNN` id, with the name at its main citation. Where Puck has interpreted, the line is labelled **Puck's reading**. Nothing here is Puck's intent.

## Product-level intent  (layer 1 — stable)

### JTBD

**PI-1 Plan a factory exactly, and keep the plan live as it grows.** When Peter plans a factory in a factory-building game, he needs an exact plan: which recipes, how many machines, at what clock speed. He needs it drawn as a diagram, correct at every edit, and recomputed fast enough to plan by changing things and watching what moves. This has to hold at megabase scale, and across the factory games he plays.

- Peter, 2026-10-05, on the tool he uses today: "modeller dies because it can't calculate all the nodes on a change and it looks like it runs out of memory. its java so that is always an issue. it does have some nice features but it isn't structured how i like."
- Peter, 2026-10-05, on how he plans: "in satisfactory i optimise the production. need 1.5 items/min from machines that generate 1/min i use two machines at 0.75 i have multiple instances where the most efficient design based on maximising output with limited puts are 4 decimal place. ie 88.8888"
- Peter, 2026-10-05, on scope: "this is more than satisfactory although that is a start there are common things all these games do. i just don't want to lock us in to satisfactory and adding anothr causes a full rewrite, so we'll need to be smart about it."
- Peter, 2026-10-08, asked what he dislikes about Modeler's structure: chose "Factory organisation" and "Interface and layout" (option labels; D-017).

### Non-goals

- **NG-1 Not a simulation.** Plans are steady-state rates at full capacity. No time-based behaviour, no fluid dynamics, no storage fill levels (D-005 Planning, not simulation; F-064 Storage buffers is *skip*). In-game splitter, jam and starvation behaviour is not in the core solve; it comes back later as a separate check over a solved plan (D-020 Graph semantics; brain #3924).
- **NG-2 No server side, accounts or collaboration in the first build.** Deferred, not ruled out (D-030 Desktop first). Peter: "this is a desktop tool initially so the server side and multiple accounts can wait".
- **NG-3 Not a Satisfactory tool.** Satisfactory is the first game, not the template (D-002 Multi-game core).
- **NG-4 No walkthroughs or tutorials.** The interface must explain itself; advanced options are revealed step by step (D-034 Interface over tutorials). D-034's carve-out stands: a shipped demo plan (an example factory to open) is allowed.
- **NG-5 No redistribution of game art in the first build.** Icons come from Peter's own install, for his own use. This part of D-019 (Icons and map data) has an outcome; D-019 is otherwise open. Peter: "want to get it working first before worrying about sharing." **Game data:** how it reaches anyone but Peter is open (D-026 How game data reaches users). ⚠ D-004 (Raw game bundle stays out of git) says to commit "a small extract" of the data instead, which is redistribution once the repo has a public remote. The repo has no remote today, so the conflict is latent; it is carried to D-026.
- **NG-6 The 37 catalogue features marked *skip*** are known about and not planned now (Peter's definition of *skip*: "we know about them but not right now"). They are listed in the Idea tier of the feature register below.

### Success criteria

Each criterion states the **observable outcome** that must hold. How each is tested (fixtures, start states, test seams, sample counts) is designed at the Spec stage: FQ-10 carries it, together with the checks for the hard constraints. Thresholds that are outcomes but not yet set (SC-2 load time; SC-7 rejection time and memory) are also set at Spec and labelled as such. Peter ruled this split in round-6 review ("Strip to outcomes", over "Keep the Check lines").

Sources, criterion by criterion:
- **Peter's chosen labels (2026-10-08 intake):** SC-1, SC-2, SC-4 and SC-5.
- **His review answers (rounds 1 to 7, 2026-10-08), quoted at each criterion with what he chose over:** SC-1's second tool, SC-2's test plan and memory bound, SC-3's numbers and redraw, SC-4's display rounding, SC-6, SC-7, SC-8 and SC-9.
- **Review findings:** SC-7 comes from Glitch round-1 F10 and Warden round-2 W2-11. It makes D-003's validation-at-load observable, and **Puck's reading** extends it to plan files.

- **SC-1 Peter stops using his current planners.** Peter plans his real Satisfactory builds in factor instead of Satisfactory Modeler and SatisfactoryTools. Peter chose "Both tools" (round-7 review), over "Any planning tool" and "Modeler only", after saying "sat tools which i use mostly now because modeller has problems".
  - He is asked at the first-build release.
  - The parity list is the register's *mvp* entries, the ones marked "first build" (**Puck's reading**).
  - A "no" names the missing capability, which becomes a register entry.
  - It is a self-report by design.
- **SC-2 Megabase scale.** Peter: "i actually don't know, lets use megabase, i no longer have my largest save". He chose "Whole game, scaled up" in round-1 review, then "Nodes + machines" in round 4, over "Many linked factories" and "Both, as two tests". The **reference plan** is one connected plan with:
  - **at least 2,000 recipe nodes:** separate uses of recipes, each drawn as a diagram node;
  - **every recipe the game makes in a machine:** 291 for Satisfactory, measured in the Docs data;
  - **byproduct loops;**
  - **at least 5,000 machines.** The glossary's definition, which counts miners and generators, is **Puck's reading** of the option Peter chose.

  On that plan it **loads**, it **solves** to its known answer, SC-3 holds on it, and **all of factor's processes together stay under 1 GB of memory at their peak during the run**. Peter chose "Under 1 GB" (round-3 review), over 2 GB, 4 GB and "Measure first". How the plan and its known answer are built is FQ-7; its load-time bound is FQ-10.
- **SC-3 Edits feel instant.** Peter: "lets target instant and then move slower if needed. The goal would be instant, that may not be realistic or may cause too many hoops to jump through." He chose "Numbers under 100 ms" (round-1 review), over "Whole view under 100 ms" and "Number to be measured", and "Under 1 second" for the redraw (round-5 review), over "Under 250 ms" and "No bound".
  - **Numbers:** after an edit to the SC-2 reference plan, the recomputed numbers are shown in **under 100 ms at the 95th percentile**, on the Mac Peter plays on. The edit can be a target change, or setting or releasing a pin (SC-9). The numbers are rates, machine counts, clocks and named problems, wherever factor displays them.
  - **What the 100 ms covers (Puck's reading):** the exact re-check (D-022) and the save of the edit (SC-8) are inside it; only the sync to disk is outside.
  - **Diagram:** it is redrawn within **1 second** of the edit.
  - **Stale values (Puck's reading, from Pixel's round-3 and round-4 reviews):**
    - When an edit lands, every displayed value it can change is marked stale, on screen and to assistive technology, until its recomputed value replaces it. A value that comes back unchanged is cleared too.
    - If a solve fails or runs past its limit (set at Spec, FQ-10), factor says so on screen and to assistive technology, and the stale marks stay.
  - **Instrumented:** factor records solve time and edit-to-numbers time on every edit (**Puck's reading**, from canon P-InstrumentBefore).
  - **Relaxing a target:** only by a recorded decision made on measured evidence. Until then, a result over target is a failure.
- **SC-4 Clocks are exact.** For a given machine count, the clock is exact: rate ÷ (count × base rate). For example, two machines at 75% for 1.5/min from a 1/min machine. The exact plan never overdraws a limited input (D-008 Clocks are continuous and exact; D-022 Exactness). Machine counts come from D-016 (fewest buildings, or a count Peter sets) and SC-6.
  - **Display** rounds to nearest, like the game. Peter, round-3 review: "i'll point out that in game the value is rounded to nearest, so i think consistent with the game is the correct answer, this might be a useful config option to think about." So 8/9 shows as 88.8889%, and the exact fraction is available on request.
  - **Rounding over a limit:** a clock rounded up can exceed its exact value by at most 0.00005 percentage points (Puck's arithmetic). Asked whether factor should say anything when that draws a hair over a limited input, Peter chose "Say nothing" (round-4 review), over "Mark it" and "Truncate on capped inputs".
  - **Truncating instead** is register idea I-1.
  - **Worked example:** the iron chain in `docs/design/ui-brief.md` §7, with the ore from a Miner Mk.2 on a Normal node. Pinning that miner to 2/3 gives 80/min. The smelters keep their count of 3 and run at 8/9, every downstream machine runs at 2/3, and the 5/6/min shortfall is named against the miner's pinned clock. Exact fractions govern; the UI brief's "88.8888%" strings predate the display ruling.
- **SC-5 A second game works without a core rewrite.** A second game from the D-002 list (Peter's example: Factorio) plans correctly in factor through its own data generator. The game-neutral core changes only at extension points declared before that game's work starts (D-002; D-029 Scope of the shared core model).
  - **Any other core change fails SC-5 for that game,** and is recorded as a decision, as evidence that D-029's scope needs revising. A fix to a defect in existing core behaviour is not a scope change. This is **Puck's reading** of Peter's "adding anothr causes a full rewrite".
  - It is checked when the second game is added; multiple games are *shape* in the first build (F-135).
- **SC-6 Edits keep what is built.** After an edit, existing machine counts stay and their clocks change, and kept counts survive closing and reopening the plan. Re-minimising is an explicit action Peter takes. Peter chose "Keep counts, re-clock" (round-1 review), over "Re-minimise every time" and "Keep only what I pinned". This refines D-016: fewest buildings applies at a first solve, on an explicit re-minimise, and to a released count pin (SC-9).
  - **A rising target past what kept machines can make:** factor adds the fewest new machines of that node's type and re-clocks all of them evenly. "Can make" means at 100%, or up to the headroom of shards Peter has placed on them. Peter chose "Add machines" (round-4 review), over "Overclock first" and "Name a shortfall". He chose "Use placed headroom" (round-7 review), over "Only with a pinned clock".
  - **Shards are never added by factor on its own.** Peter, 2026-10-08: "should note that adding shards would be a manual task unless i ask for it to be sharded" and "so a shortfall shouldn't add shards that are not already allocated". Shards come from Peter's own hand, or from factor only when he asks it to shard: F-032's "plan within a shard budget" is that request (round-7 review). Releasing a shard pin removes those shards. Automatic sharding is register idea I-2.
  - **A pinned count that can't make a rising target:** the pin holds, and the pinned machines run up to what they can make. The rest is a named shortfall, with fixes such as "unpin the count" or "set count to N". Peter chose "Hold the pin, name a shortfall" (round-6 review), over "Overclock the pinned machines" and "Unpin automatically".
  - **Resource nodes:**
    - When a raw resource is first needed, the plan gets one resource node for it, with factor's default purity and extractor, whose clock runs up to 100% or up to its placed-shard headroom.
    - Demand past that ceiling is a named shortfall, with fixes such as "add a node" or "upgrade the extractor". factor never adds nodes or upgrades extractors by itself.
    - Peter, round-7 review, describing how he plans today: "i state the item i want produced and the then it has requirements. i fulfill each one until i get to the raw resource, sat tools which i use mostly now because modeller has problems puts in the raw resource req. So i think we go with 1. but understand some of the resoures may come from other locations and are shipped in. So i would then remove the node and replace it as input to that factory". So Peter can replace a node with external supply into that factory (F-008).
    - His rule on nodes: "each resource node can only have one miner on it. So to get past the cap you need inputs from multiple resource nodes" (round-5 review). He chose "Name a shortfall" for demand past a node's ceiling (round-6 review), over "Add a default node".
  - **Puck's reading, not ruled:**
    - A node created by an edit, or whose recipe swap changes its machine type, is sized by fewest buildings.
    - Below the game's minimum clock, factor names a surplus instead of removing machines.
- **SC-7 Bad input is handled safely.** For data files factor loads at runtime and for plan files, checked in this order:
  1. **A file that is corrupt or contradicts itself** (wrong encoding, truncated, malformed, internally inconsistent, or missing its format version) is rejected whole, with a named error **shown in the app**, and to assistive technology, that says which file and what is wrong. It never loads in part, never crashes factor and never leaves it unresponsive. Its time and memory bounds are set at Spec.
  2. **A plan saved by a newer factor** opens read-only, with a notice.
  3. **A plan saved by an older factor** is migrated to a new copy, and the original is kept until Peter accepts the migration. Anything that can't be carried over is named, and remains in the original.
     - For rules 2 and 3, plan files carry a format version. Peter chose "Keep original; newer = read-only" (round-7 review), over "Migrate in place" and "Refuse newer files". This refines his round-6 "Migrate forward", which was chosen over "Refuse with a message".
  4. **A valid plan that refers to recipes or items a game update removed or renamed** opens. Each affected node is a named problem Peter can fix (swap the recipe, delete the node), and nothing is silently dropped. Peter chose "Open and name what's gone" (round-5 review), over "Refuse to open" and "Migrate automatically".
  - The generator's own inputs are the generator's concern (D-003).
  - How factor treats a plan file's owner id is FQ-4, not this criterion.
- **SC-8 Crashes lose little and never corrupt.** The plan file is never left corrupted: it passes SC-7's checks on reopen. A completed edit is one whose new numbers were displayed. An edit whose solve failed is still a completed edit, and it is saved and shown as a named problem. Peter chose "Keep it" (round-7 review), over "Don't keep it".
  - **If factor crashes,** reopening shows every completed edit. Only an edit still in progress can be lost. Peter chose "Yes, lose at most the last edit" (round-2 review), over "Yes, explicit saves only" and "No criterion".
  - **If the Mac loses power or hard-crashes,** reopening loses at most the completed edits since the last sync to disk. Everything synced before that survives.
  - **The sync interval is a setting.** Peter, round-5 review: "balance, lets try disk sync but allow it to be tuned, maybe every 10secs or 10edits. a config item." His suggested starting value is every 10 seconds or 10 edits ("maybe": a default, not a ruling). The setting can't be turned off, and its maximum is 60 seconds. Peter chose "Max 60 seconds, never off" (round-7 review), over "Allow off".
- **SC-9 Pins are visible and releasable.** A pin is a value Peter sets on a machine node or an extractor for the solver to keep. Every pin is marked as his, distinguishable from values factor chose, and releasable. He chose "Yes, visible and releasable" (round-3 review), over "No, keep it simple".
  - **Pin kinds:**
    - recipe;
    - machine count;
    - clock, including placed shards and Somersloops;
    - extractor settings: extractor type, node purity, and extractor clock.
    - The extractor clock is how a resource is limited and how targets scale to a resource (F-009 and F-007, re-described per Peter's round-6 "Cap = pinned extractor clock" and round-7 "Pin the extractor, scale targets", over "Keep a typed override", "Typed amount stays here" and "Drop F-007").
    - The list is **Puck's reading**; the round-3 question named examples ("a recipe, a machine count, a cap").
  - **Not pins:** targets, external supply (F-008) and maximise-output goals (F-006) are inputs Peter adds or removes.
  - **On release:**
    - a machine count re-minimises that node. Peter chose "Re-minimise that node" (round-4 review), over "Keep current count".
    - Placed shards and Somersloops are removed.
    - Extractor type and purity return to factor's default; Peter: "factor picks a default and i can change it if needed" (relayed from the design session, D-018).
    - A recipe or clock returns to factor's choice.
  - **Where marks live:** in the plan data, readable by any view, not only drawn on screen (HC-6).

### Hard constraints

- **HC-1 Rust desktop app, macOS now, Windows later;** nothing may rule Windows out (D-001 Platform; canon P-RustDefault).
- **HC-2 Game-neutral core** (D-002 Multi-game core).
- **HC-3 Per-game data generators;** the app loads their output at runtime into a typed model, validated at load (D-003 Game data pipeline). The raw Satisfactory bundle stays out of git (D-004 Raw game bundle stays out of git).
- **HC-4 Planning engine as ruled:**
  - a linear-programming core with incremental recompute (D-017 Core calculation model);
  - ideal ratios (D-020 Graph semantics);
  - clocks sized after the rate solve (D-016 Nonlinear power and clocks);
  - HiGHS behind factor's own solver interface (D-021 Solver dependency);
  - exact rational results (D-022 Exactness);
  - a scarcity-weighted default objective with an elastic formulation (D-023 Default objective);
  - extraction modelled as a recipe whose ceiling comes from its extractor, node purity and clock, never typed. A resource node holds one extractor, and a resource is limited by pinning its extractor's clock (D-018 Raw resources, amended).
- **HC-5 One view:** targets drive the diagram, and edits to the diagram re-solve (D-024 One view).
- **HC-6 The graphics are a replaceable view** over the backend (D-032).
- **HC-7 Hard-to-retrofit concerns are shaped in from the start** (D-031). Globalisation and tenancy are Peter's examples, not the full list. FQ-3 is a candidate addition whose answer comes back to Peter.
  - **Tenancy:** an owner/workspace id on every stored plan, and scoping by it must be able to fail a test.
  - **Globalisation scope:** left-to-right scripts, including Chinese, Japanese and Hindi, are shaped in. Right-to-left scripts (Arabic, Hebrew) are out of scope until a real need appears. Peter chose "Left-to-right only for now" (round-2 review), over "In scope, shaped now" and "Let the spike decide".
  - **Accessibility:** HC-10.
- **HC-8 Plans are stored in SQLite** with a documented schema (D-033 Plan file format).
- **HC-9 Open, and not constraints yet:**
  - UI toolkit (D-036): researched; a spike comes before ruling. The spike also records each toolkit's screen-reader support, including for a custom-drawn diagram, because the choice can rule out HC-10.
  - factory organisation (D-035);
  - shared core model scope (D-029);
  - physical layer (D-012);
  - icons and map data beyond the first-build icon outcome (D-019);
  - licence (D-025);
  - how game data reaches other users (D-026).
- **HC-10 Accessibility is shaped now and enforced at Gate B.** Peter chose "Shape now, enforce on share" (round-2 review), over "Floor from the first build" and "Defer to sharing".
  - **Now (Puck's reading of "shape now"):**
    - The chosen toolkit can expose factor's controls and diagram to a screen reader.
    - Every action is reachable by keyboard.
    - Text and controls use contrast-checked tokens.
  - **At Gate B (HC-11):** the full accessibility floor (canon V-Accessibility) is the release gate.
- **HC-11 Two sharing gates.** Peter chose "Two events" (round-6 review), over "One gate, earliest event". He then chose "Distribution build fires B; legal at first" (round-7 review), over keeping Gate B on a person running a build. Each gate's firing mechanism is FQ-8.
  - **Gate A: the repo's first public remote.** Plan files committed to the repo, such as demo plans and fixtures, are published at this gate.
  - **Gate B: the first build packaged for distribution** (an installer or a signed app). At this gate:
    - the accessibility floor (HC-10) applies;
    - foreign plan files become a trust boundary (RP-1);
    - what an exported plan file carries is decided;
    - releases are signed and notarised. That item comes from the option text Peter chose ("signed and notarised releases").
  - **At whichever gate comes first:** factor's licence (D-025), redistribution of game data and art, including D-004's committed extract (D-019, D-026; NG-5), and acceptable community data inputs (D-028).
  - Network-feature security reviews are not part of either gate. They fire per slice (RP-3).

### Evidence

- **EV-1 Peter's own play.** He plays Satisfactory with Satisfactory Modeler today and hits its scale failure (PI-1 quotes). He has played Factorio, Techtonica and Foundry: "techtonia and foundry and factorio are other examples i have used in terms of playing them. which is why i think there is similaries and differences" (2026-10-05).
- **EV-2 Tool survey,** 2026-10-05: 46 tools, with Modeler's complaints drawn from Steam reviews (`docs/research/calc-tools.md`).
- **EV-3 Engine research,** 2026-10-05. **Measured** with HiGHS: a whole-game Satisfactory solve in about 0.9 ms, and 300 coupled copies of the whole game (141,600 columns) in about 666 ms (`docs/research/engine-2026-10.md`; D-017). **Observed** from Modeler's own devlog: its slowness comes from its semantics (simulating splitters), not its solver.
- **EV-4 Feature verdicts.** Peter's verdict on all 142 catalogue features, rounds 1 and 2, snapshotted at `docs/design/feature-verdicts.md` (commit `c60f8db`).
- **EV-5 Use case: plan beside the game.** Peter runs the game in one window and the tool in another (his F-087 note: "i run the game in one window and the tools in another today"). He sets a target, reads the exact machine counts and clocks, and builds them in game.
- **EV-6 Exploratory, hunch-stage, deferred out:** factories as containers that solve fast locally while the rest of the model updates in the background. Peter: "One reason for having factories as containers is that within  a single factory it might be fast and we can maybe background updating the rest of the model. but that is premature optimization so we'll need to see and test it." Deferred to the core-model run's factory-organisation question (D-035). Not part of this brief's intent.

### Consumer

**Mixed.** Peter first. Other players later: he chose "Me now, shared later" on 2026-10-08 (option label), after saying "this is initially for me only" and "if i ship factor this can be a feature request from someone". Sharing is a real later goal and must not be designed out. Agents consume this brief cold.

### Risk profile

Declared by Puck from Peter's rulings at intake. The security review runs at Frame, where the mechanisms are known. Trust assumption for the first build: the only user is Peter, on his own Mac. Every file input below is still treated as possibly malformed (SC-7).

- **RP-1 Untrusted file input: yes.** factor parses files it did not write. Each is a trust boundary carried to Frame as a required constraint:
  - the game data bundle (the generator's input);
  - generated data files at runtime, and other people's generated files once they are shared (D-026 option a);
  - game asset archives for icons (F-094 *mvp*), including their native decompression (Oodle, per D-026);
  - mod content (F-028 *shape*), custom game data (F-136 *Custom game data editor*), and other tools' plan files (F-130 *Import from another tool*);
  - save files (F-096 collectibles come through loading his save);
  - plan files written by someone else: **not in the first build.** Peter chose "No, mine only for now" (round-2 review). Plan files are still validated on open (SC-7), and a foreign plan file becomes a trust boundary at Gate B (HC-11).

  Warden's round-1 review also named three boundaries that are not file inputs, carried as FQ-9: Rust calling native code (HiGHS, SQLite, Oodle), a webview if D-036 picks one, and future API or model callers.
- **RP-2 Multi-tenancy: shaped, not built.** Every stored plan carries an owner/workspace id (D-031), and tests exercise at least two (HC-7). What owner id an imported plan file gets, so that a file can't claim another owner's scope, is FQ-4.
- **RP-3 Network, auth, PII: none in the first build** (D-030). The security review re-triggers when **any** feature with network, credential or external-model reach enters a slice's scope, not only "sharing". The known ones:
  - F-083 New-version notice;
  - F-112 Pull save from a dedicated server;
  - F-118 Programmatic API;
  - F-119 Natural-language/LLM interface;
  - F-134 Anonymous usage telemetry;
  - every sharing feature.

  F-118 and F-119 are AI/LLM surfaces that no current review lens covers; that gap is named here, not absorbed. The re-trigger is per slice: when one of these features enters a slice's scope, that slice's Frame runs the security review. What makes that fire is part of FQ-8.
- **RP-4 Legal, not security:** redistribution of game data and art, factor's own licence, and community data inputs (D-019, D-025, D-026, D-028). Open, and must clear at whichever sharing gate comes first (HC-11).

## Glossary

- **Machine:** one instance of a production building: a manufacturer, an extractor such as a miner, or a generator. Belts, splitters, mergers, lifts and power poles are not machines. SC-6's "new machines of that node's type" never means new extractors; those need a new resource node.
- **Recipe node / diagram node:** a node in factor's diagram. One can stand for many machines (D-012). Not the same as a **resource node**, which is a spot in the game world where ore is mined.
- **Clock:** a machine's speed setting as a percentage of its base rate; Satisfactory sets it to 4 decimal places. Other games may have no clock, or a different one; that is a per-game extension (D-029).
- **Pin:** a value Peter sets on a machine node or extractor for the solver to keep (SC-9). Targets, external supply and maximise goals are inputs, not pins.
- **Megabase:** the SC-2 reference plan.
- **First build:** the release that contains every Committed register entry marked "first build", and the backend structure for every entry marked "first build: backend structure only". It is defined by its content, so SC-1 can be asked at a known point.
- **Modeler:** Satisfactory Modeler, the desktop tool Peter uses today.
- **Picker:** the Artifact page where Peter gave a verdict on each of the 142 catalogue features.
- **Release note:** the "first build", "first build: backend structure only" or "eventually, not immediately" label on a Committed register entry.
- **Structural fence:** the rule that no register tier, and no release note, authorises building anything. Only a feature-level `/brief` run does.
- **Core-model run:** the next `/brief` run, at feature altitude, on the shared core model, factory organisation and physical layer.
- **Round-N review:** Peter's answers during review rounds 1 to 6 of this intake, 2026-10-08.

## Consultations

None yet.

## Questions carried to the Frame

Raised in review, and belonging to a later stage rather than to product intent. **FQ-3's answer comes back to Peter**, because adding to D-031's list is product intent.
- **FQ-1 (Warden WQ-2):** does factor parse the game's asset archives itself, or read the output of a separate extractor? This decides whether RP-1's archive and Oodle boundary sits inside factor.
- **FQ-2 (Warden WQ-3):** is an F-119 language-model interface local or a hosted provider? It decides RP-3's external-model reach. F-119 is *shape*.
- **FQ-3 (Warden WR-07):** a candidate hard-to-retrofit concern: input validation at the view-to-backend interface (D-032), which F-118 and F-119 would also call.
- **FQ-4 (Warden WR-06 and W3-04, security):** what owner id an imported plan file gets (RP-2), whether an owner id is tied to Peter or to an install (so a new Mac doesn't lock him out of his own plans), and what, if anything, makes an id "known". The file states its own owner id, so the id alone authenticates nothing.
- **FQ-5 (Pixel round-1 F2, F7):** non-visual access to the diagram (F-071 Configurable step table as the accessible alternative), and diagram legibility at SC-2 scale.
- **FQ-6 (Ink round-1 F14, Warden WR-10):** which extension points the core declares, and when (SC-5, D-029).
- **FQ-7:** how the SC-2 reference plan is composed from known-answer fixtures.
- **FQ-8 (Warden W2-08 and W3-02, security):** the mechanisms that fire Gate A, Gate B (HC-11) and RP-3's per-slice re-trigger, so none depends on someone remembering.
- **FQ-9 (Warden round-1 and round-3 appendices):** the trust boundaries that are not file inputs:
  - native code called from Rust (HiGHS, SQLite, Oodle);
  - a webview, if D-036 picks one;
  - future API or model callers;
  - a local model for F-119, by Gate B (WTB-11);
  - the exported plan file as an outbound boundary (WTB-10);
  - durable sync on macOS: whether a plain fsync is enough for SC-8 (WTB-9, from Warden's platform knowledge, not measured);
  - SQLite opening a plan file factor did not write, whose triggers and views can run when queried (WTB-12; Warden cites SQLite's trusted-schema and defensive settings from platform knowledge, not measured);
  - migration as a write path over Peter's only copy of a plan (WTB-13), which SC-7's keep-the-original rule addresses.
- **FQ-10 (round-6 restructure):** how each success criterion is tested. This takes in the mechanics the reviews raised:
  - the starting state of each fixture and its expected exact counts and clocks; for SC-6 these include the 9/min and 10/min cases Glitch and Warden worked out;
  - test-only seams: a solve delay to observe stale marks, and a storage seam to simulate power loss;
  - the sample counts behind the p95;
  - time and memory limits for rejecting bad input (SC-7);
  - an upper bound on the sync-interval setting (SC-8);
  - how the redraw and the stale marks are timed (SC-3);
  - the solve time limit after which SC-3 reports a solve as failed;
  - SC-2's load-time bound, and SC-7's rejection time and memory bounds. These are outcome thresholds set at Spec, not only test mechanics;
  - recording the Mac model, chip and memory with every SC-3 measurement;
  - the checks for the hard constraints: HC-7's two-owner-id scoping and HC-10's contrast and keyboard walk.

## Dismissed review flags

- **Pixel round-1 F6** (the UI brief draws a Problems strip, but F-013 and F-059 are *shape*). Dismissed for this document: it is a defect in `docs/design/ui-brief.md`, not in product intent. The brief's named problems rest on D-023 and on F-014 Byproduct handling and F-052 Factory-to-factory import/export ledger, which are *mvp*. Routed to the design work.
- **Ink round-1 F11** (decisions sometimes cited by id alone). Carried as a known low limitation: every id resolves in `docs/decisions.md`. The source note now promises an id, with the name at its main citation.
- **Glitch round-1 F9** (NG-4 and HC-1 have no observable check). Carried as a known low limitation: both are enforced through review of the Frame and Spec, not by a product-level test.
- **Glitch round-4 G9** (SC-1 is a one-time self-report, so it can pass for the wrong reason). Carried as a known low limitation: the self-report is by design. A "no" becomes a register entry, so a later change of mind is captured.
- **Pixel round-4 questions on target size (24/32 px on desktop, 44 px at the phone layout) and honouring the OS text-size setting.** These are design-spec questions, not product intent. Routed to the design work with C1–C6, and to FQ-5.
- **Ink round-4 R4-9 "never typed" wording.** Kept as written: it is Peter's ruling (D-018, F-009), and the residual uses of "cap" in D-016 and D-024 now carry dated notes.
- **Round-2 contradictions in the design docs** (Pixel C1–C6 and Ink's note on `ui-brief.md`: 88.8888% strings, fonts without Chinese, Japanese or Hindi coverage, 10px text, the Problems strip, pin marks, the UI brief's accessibility constraint). Not defects in this document. Routed to the design work, task #3933 and its follow-up.

## Feature register  (layer 2 — grows; each entry has a lifecycle tier)

Tier mapping from Peter's picker verdicts (**Puck's reading, for confirmation at the intake gate**):
- *mvp*, *shape* and *later* are **Committed**. Each is decided worth pursuing, and its provenance is the verdict snapshot at commit `c60f8db`. The release note on each line keeps the verdict: "first build", "first build: backend structure only" (*shape*), or "eventually, not immediately" (*later*).
- *skip* is **Idea**: known about, not planned now.
- **Designed** and **Live** are empty. No feature has a Frame or Spec yet, and no code exists.

The structural fence holds: no tier is a build trigger, and neither is a release note.

### Idea

- **I-1 Clock display: truncate instead of round** (UI). Peter: "this might be a useful config option to think about" (2026-10-08). Not a catalogue feature.
- **I-2 Shards allocated automatically to cover a shortfall** (Production modifiers). Peter, after ruling that shortfalls never add unallocated shards: "althought later that might be feature" (2026-10-08). Not a catalogue feature.
- **F-002 Recursive tree expansion (no optimiser)** (Solver).
- **F-012 Solver cost tuning** (Solver).
- **F-050 Manifold fill time** (Logistics).
- **F-064 Storage buffers in model** (Factory network).
- **F-070 Sankey diagram** (Visualisation).
- **F-082 In-app feedback with plan attached** (UI).
- **F-083 New-version notice** (UI).
- **F-084 Installable offline app (PWA)** (Platform).
- **F-087 Kiosk / second-screen mode** (Platform).
- **F-097 Build-site ranking** (Map & world).
- **F-098 World seed viewer and finder (1.2)** (Map & world).
- **F-100 3D factory view** (Map & world).
- **F-105 Save editing** (Save files).
- **F-106 Auto-detect factories in a save** (Save files).
- **F-107 Idle and starved machine detection** (Save files).
- **F-108 Upstream trace / bottleneck finder** (Save files).
- **F-109 Power circuit analysis** (Save files).
- **F-110 Plan from save state** (Save files).
- **F-111 Inventory and storage search** (Save files).
- **F-112 Pull save from a dedicated server** (Server & live).
- **F-113 Server status and admin** (Server & live).
- **F-114 Live factory telemetry** (Server & live).
- **F-115 Production history** (Server & live).
- **F-116 Alerts and notifications** (Server & live).
- **F-117 What changed since last visit** (Server & live).
- **F-120 In-game planner** (Platform).
- **F-121 In-game throughput instruments** (Platform).
- **F-123 Server-hosted snapshot link** (Sharing).
- **F-124 Live collaborative editing** (Sharing).
- **F-125 Shared-plan permissions** (Sharing).
- **F-126 Accounts and cross-device sync** (Sharing).
- **F-127 No account required** (Sharing).
- **F-128 Offline editing with conflict resolution** (Sharing).
- **F-132 Community gallery** (Sharing).
- **F-133 Shared-text safety rules** (Sharing).
- **F-134 Anonymous usage telemetry** (Platform).
- **F-142 World leaderboards** (Misc).

### Committed

- **F-001 LP auto-solve to target rates** (Solver) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-003 Manual node graph with rate propagation** (Solver) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-004 Splitter/merger behaviour simulation** (Solver) — eventually, not immediately. **Puck's reading:** this is the later jams-and-starvation check over a solved plan (D-020; brain #3924), never part of the core solve (NG-1). Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-005 Manual ledger with satisfy/trim sizing** (Solver) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-006 Maximize output under limits** (Solver) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-007 Scale targets to a pinned input** (Solver) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`. Re-described in round-7 review: Peter pins an extractor (its clock or nodes) and the targets scale to consume exactly that; no typed amount (SC-9).
- **F-008 Use on-hand / external supply** (Solver) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-009 Per-resource caps** (Solver) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`. Re-described in round-6 review: a resource is limited by pinning its extractor's clock, not by typing a cap (D-018).
- **F-010 Resource scarcity weighting** (Solver) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-011 Selectable optimisation goal** (Solver) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-013 Infeasibility diagnostics** (Solver) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-014 Byproduct handling** (Solver) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-015 Recipe loops and recursive recipes** (Solver) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-016 Whole-machine counts and clock spreading** (Solver) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-017 Pause or manual recalculation** (Solver) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-018 Undo / redo** (UI) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-019 Alternate recipe toggles** (Recipes) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-020 Converter recipe switch** (Recipes) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-021 Progression gating (tier / research)** (Recipes) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-022 Unlocked recipes read from a save** (Recipes) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-023 Alternate recipe comparison** (Recipes) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-024 Hard drive research advisor** (Recipes) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-025 Recipe swap from the graph or row** (Recipes) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-026 Game-mode multipliers (1.2)** (Recipes) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-027 Seasonal content toggle** (Recipes) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-028 Mod content support** (Recipes) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-029 User-editable recipe database** (Data) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-030 Game version switcher** (Data) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-031 Overclock / underclock per machine** (Production modifiers) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-032 Power shard count and budget** (Production modifiers) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-033 Somersloop production amplification** (Production modifiers) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-034 Auto-place a limited somersloop supply** (Production modifiers) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-035 Research and upgrade levels** (Production modifiers) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-036 Modules, beacons, proliferators, quality** (Multi-game) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-037 Plan power total** (Power) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-038 Variable-power machines** (Power) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-039 Power plant planner** (Power) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-040 Self-powered factory** (Power) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-041 Power balance per factory or group** (Power) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-042 Power augmenter boost** (Power) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-043 Extractor sizing by mark, purity and clock** (Extraction) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-044 Node inventory input** (Extraction) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-045 Resource well planning** (Extraction) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-046 Raw resources must be sourced** (Extraction) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-047 Hand-gathered items** (Extraction) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-048 Belt and pipe sizing** (Logistics) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-049 Splitter and balancer design** (Logistics) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-051 Transport capacity planning** (Logistics) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-052 Factory-to-factory import/export ledger** (Logistics) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-053 Multiple factories per plan** (Factory network) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-054 Nested sub-plans** (Factory network) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-055 Factory groups with rollups** (Factory network) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-056 Spin off a sub-chain** (Factory network) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-057 Plan statistics and building summary** (Factory network) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-058 Construction bill of materials** (Factory network) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-059 Plan health warnings** (Factory network) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-060 Space Elevator phase targets** (Factory network) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-061 Non-producing buildings in plan** (Factory network) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-062 AWESOME Sink planning** (Factory network) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-063 Dimensional Depot uploads** (Factory network) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-065 Build checklist** (Workflow) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-066 Kanban build status** (Workflow) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-067 Notes and tasks per factory** (Workflow) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-068 Plan vs save diff** (Workflow) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-069 Flow graph with auto layout** (Visualisation) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-071 Configurable step table** (Visualisation) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-072 Tree view of the chain** (Visualisation) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-073 Edit from the graph** (Visualisation) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-074 Persisted manual layout** (Visualisation) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-075 Graph image export** (Visualisation) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-076 Display units and number format** (UI) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-077 Command palette and search** (UI) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-078 Localisation** (UI) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-079 Themes and display settings** (UI) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-080 Keyboard shortcuts** (UI) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-081 Guided tutorial and demo plans** (UI) — eventually, not immediately. Limited by D-034: demo plans only; a guided tutorial is excluded (NG-4). Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-085 Phone-friendly layout** (Platform) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-086 Native desktop app** (Platform) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-088 Codex / database browser** (Data) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-089 Recipe usage lookup** (Data) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-090 Milestone / MAM / AWESOME Shop tracker** (Data) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-091 Dependency explorer** (Data) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-092 Per-item cost analysis** (Data) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-093 Official data ingest pipeline** (Data) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-094 Game icon extraction** (Data) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-095 Resource node map** (Map & world) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-096 Collectibles map** (Map & world) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-099 Map measuring and annotations** (Map & world) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-101 2D layout planner** (Layout) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-102 Generated layout or blueprint from a plan** (Layout) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-103 Save upload with map overlay** (Save files) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-104 Save statistics** (Save files) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-118 Programmatic API to plan data** (Sharing) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-119 Natural-language / LLM interface** (Sharing) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-122 URL-encoded sharing** (Sharing) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-129 File export and import** (Sharing) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-130 Import from another tool** (Sharing) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-131 Named local saved plans** (Sharing) — first build. Provenance: verdict *mvp*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-135 Multiple games in one tool** (Multi-game) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-136 Custom game data editor** (Multi-game) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-137 Sell value and profit** (Multi-game) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-138 Secondary resource budgets** (Multi-game) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-139 Footprint estimate** (Multi-game) — first build: backend structure only. Provenance: verdict *shape*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-140 World seed statistics (non-Satisfactory)** (Multi-game) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.
- **F-141 Customisation helpers** (Misc) — eventually, not immediately. Provenance: verdict *later*, `docs/design/feature-verdicts.md` @ `c60f8db`.

### Designed

None yet.

### Live

None yet.
