# factor — decision log

Every design decision and open question, one block each.

- **ID:** each block is `D-NNN` plus a name, and the ID never changes or gets reused. Feature IDs
  (`F-NNN`) come from the feature catalogue, a separate namespace.
- **Status:**
  - `ruled`: Peter decided it.
  - `applied`: done, but not explicitly ruled.
  - `open`: undecided.
- **Peter's words** are quoted verbatim, typos included. Puck's proposals are labelled as proposals.
  A superseded ruling stays here as a rejected option, with the reason it lost.
- `CLAUDE.md` carries only the ruled outcomes, so read this file for the reasoning and the open questions.

---

## Ruled

### D-001 Platform
- **Status:** ruled 2026-10-05
- **Amended:** 2026-10-08, see D-030 and D-032
- **Peter:** "this will start as a rust based desktop app and will likely stay that way. we can run on mac for now but eventually i'll want a windows version"
- **Peter, 2026-10-08:** "this is a desktop tool initially so the server side and multiple accounts can wait"
- **Peter, 2026-10-08:** "The graphics is a view so we could switch to a webbased one eventually, its also cleaner."
- **Outcome:** a Rust desktop app first. macOS first and Windows later, so nothing may rule Windows out. The calculation backend stays Rust; the drawing is a replaceable view (D-032), and a web view is a possibility Peter named, not a plan.
- **Superseded reading:** "will likely stay that way" read as desktop-only for good. As of 2026-10-08 the desktop is where it *starts*, and the view may move to the web.

### D-002 Multi-game core, no lock-in
- **Status:** ruled 2026-10-05
- **Peter:** "this is more than satisfactory although that is a start there are common things all these games do. i just don't want to lock us in to satisfactory and adding anothr causes a full rewrite, so we'll need to be smart about it."
- **Peter:** "techtonia and foundry and factorio are other examples i have used in terms of playing them. which is why i think there is similaries and differences"
- **Outcome:** the core is game-neutral. Satisfactory is the first game, not the core's template. Design the core from several games' data shapes. Peter's experience playing the other games is primary evidence.
- **Games in scope:** Satisfactory, Factorio, Techtonica, Foundry, Alchemy Factory.
- **Picker, 2026-10-08:** F-135 "Multiple games in one tool" marked *shape*, note: "start with satisfactory". So the model carries multi-game from day one, and the game switcher ships later.

### D-003 Game data pipeline
- **Status:** ruled 2026-10-05
- **Peter:** "for the game resources we'll want a genertor to read them and then generate the rust data files"
- **Peter, on runtime loading over compiled-in source:** "i agree with your lean and is how i approached this initially"
- **Outcome:** each game gets a generator that reads that game's resources and emits data files. The app loads those files at runtime into a strongly typed Rust model, with validation at load.
- **Rejected:** generated Rust source compiled into the app. Every patch, new game or mod pack would mean a rebuild, and modded recipes couldn't be loaded.
- **Open: the format of the generated data files.** Asked on 2026-10-08 whether his preference against text files covers them too, Peter chose "Decide later": settle it when the generator is designed. No tripwire is needed, because designing the generator forces the choice.
- **Peter, 2026-10-08, picker note on F-043:** "when we say hard coded we mean in the schema the model uses correct? not hard constants in the rust code". **Puck's answer, which follows from this ruling:** yes. Game numbers missing from the bundle, such as the purity multipliers, go into a per-game data file that loads like the rest, never into Rust constants.
- **Puck's reading, not confirmed:** "your lean" is taken to mean the runtime-data option, since that was the lean Puck had stated.

### D-004 Raw game bundle stays out of git
- **Status:** ruled 2026-10-05, via the option "Ignore raw bundle"
- **Outcome:** `resources/CommunityResources.zip` and the expanded tree are gitignored. Instead, commit a small extract the calculator produces.
- **Why:** the bundle is 585 MB. It carries no licence or readme, so redistribution terms are unverified.
- **Rejected:**
  - Track the zip only: history grows by about 20 MB per game update, and the raw bundle gets republished.
  - Track en-US plus the small files: same republication issue.
  - Git LFS: adds tooling and quota, and is still a republication.

### D-005 Planning, not simulation
- **Status:** ruled 2026-10-05
- **Peter:** "i don't know that we need to model fluids differently from items really, we aren't running a simulation we are defining the layouts that would use max capacity available."
- **Peter:** "so fluid dymanics shouldn't matter, jsut throughput"
- **Outcome:** steady-state rates at full capacity. Fluids are ordinary items in the maths, and only throughput matters. The generator normalises units at import. Satisfactory appears to store fluid amounts in thousandths of m³: that's inferred from game knowledge, consistent with the Water Extractor's `2000` per 1 s cycle, and not stated in the data.

### D-006 Transport is a first-class generic concept
- **Status:** ruled 2026-10-05; the details are open (D-013, D-014, D-015)
- **Peter:** "transport should be its own thing, there are also trains , trucks and drones."
- **Peter:** "so a generic "conveyor" or whatever we call it, needs multiple specific types for the caps."
- **Outcome:** one generic carrier concept. Each game's generator supplies the specific types (Belt Mk.1–Mk.6, Pipeline Mk.1/2, Truck, Freight Car, Drone, …), each with its own cap.

### D-007 Power and modifiers follow per-game curves
- **Status:** ruled 2026-10-05; how the solver handles it is open (D-016)
- **Peter:** "same with power, some times the cost of adding increasing power output the gain may not be the same, doubling production could cost double+x power vs just double"
- **Outcome:** power and production modifiers are per-game curves, not one linear rule.
- **Data (measured):** Satisfactory machines carry `mPowerConsumptionExponent` 1.321929 and `mProductionBoostPowerConsumptionExponent` 2.0.
- **Inferred from game knowledge:** power = base × clock^exponent. On that basis, doubling output costs:
  - 2× power, plus a building, with a second machine;
  - 2.5× power by overclocking;
  - 4× power with a Somersloop.

### D-008 Clocks are continuous and exact
- **Status:** ruled 2026-10-05, as a requirement taken from Peter's practice; the implementation is in D-016
- **Peter:** "in satisfactory i optimise the production. need 1.5 items/min from machines that generate 1/min i use two machines at 0.75 i have multiple instances where the most efficient design based on maximising output with limited puts are 4 decimal place. ie 88.8888"
- **Outcome:**
  - Clocks are continuous, not fixed steps.
  - The plan spreads load evenly across whole machines.
  - A clock shown to the user is a value the game accepts, to 4 decimal places.
- **Puck's derivation, not ruled:**
  - Arithmetic uses exact fractions (8/9, not a float).
  - Rounding never overdraws a limited input, so it rounds down when input-limited. **Superseded for display, 2026-10-08:** Peter: "i'll point out that in game the value is rounded to nearest, so i think consistent with the game is the correct answer, this might be a useful config option to think about." Display rounds to nearest, like the game; exact values stay internal, and truncation is an idea for a setting (product brief SC-4).

### D-009 What a machine computes is separate from how it is laid out and drawn
- **Status:** ruled 2026-10-05; the layer split is open (D-012)
- **Peter:** "there is also disply vs internal difference. how a machine displays and its input locations could be different that just the raw calculations of items->outputs"
- **Outcome:** the calculation model has no knowledge of ports, positions or drawing.

### D-010 Where decisions and work are tracked
- **Status:** ruled 2026-10-05, via the options "Decision log in the repo" and "Register factor in brain"
- **Peter:** "many things like that we'll eventually need to track."
- **Outcome:**
  - Decisions go in this file.
  - Work items go in brain (project `factor`, id 40).
  - `CLAUDE.md` keeps ruled outcomes only.
- **Not selected, with no reason given by Peter:** "Keep it all in CLAUDE.md" and "Use quince".
  - Puck's option text, not Peter's reasoning: `CLAUDE.md` costs context on every session and mixes settled with open items; quince's readiness was unchecked.

### D-011 Carry vocabulary and layout from factory_calc, not its code
- **Status:** applied 2026-10-05, not explicitly ruled
- **Peter:** "i may on disk here have a factory cal where i started this work manually last year. maybe some of it is still there an useful"
- **Outcome:** carried from `~/work/repos/factory_calc`: the `cmd/` + `libs/` workspace layout, Rust 2024, and the vocabulary `Unit` / `Formula` / `Fabricator` / `GlobalModifiers`. The code was not carried.
- **Why it isn't marked ruled:** Puck announced the carry-over and asked Peter to object if he wanted any of it out. His reply ("i agree with your lean") was taken to answer D-003, not this.
- **Model fixes noted for the rebuild:**
  - A machine type runs many formulas, and which one it runs belongs to the layout.
  - Identity is by id only.
  - A `GlobalModifiers` field in the old model was never used.

### D-030 Desktop first: server side and accounts wait
- **Status:** ruled 2026-10-08
- **Peter:** "this is a desktop tool initially so the server side and multiple accounts can wait"
- **Outcome:** no server component and no accounts in the first build. Both are deferred, not ruled out, and D-031 still applies to them.
- **Picker:** F-124 live collaborative editing, F-125 shared-plan permissions, F-126 accounts and cross-device sync and F-127 no account required are marked *skip*, which by Peter's definition means known about but not planned now. That is consistent with this ruling. Puck had raised it as a conflict under a wrong reading of *skip*.

### D-031 Hard-to-retrofit concerns are shaped in from the start
- **Status:** ruled 2026-10-08
- **Peter:** "if something is hard to put in later like globaliztion we at least minimally account for it internally. same with tenency."
- **Outcome:** a concern that is expensive to retrofit gets a minimal internal accommodation now, even when its features ship later. This is the picker's *shape* verdict stated as a rule. Globalisation and tenancy are the two Peter named; they are examples, not the full list.
- **Globalisation, Puck's proposal (not ruled):**
  - Identity is the game's class id (`Recipe_IngotIron_C`), never a display name.
  - Display text is looked up by locale key. The data already ships it this way: 55 locale files over the same 2,868 classes, differing only in display text (measured, see `CLAUDE.md`).
  - Number formatting lives in the view, never in the core. The core holds exact values (D-008); the view decides "88.8888" versus "88,8888".
  - Consistent with the picker: F-078 Localisation is marked *shape*.
- **Globalisation scope, ruled 2026-10-08** (product brief HC-7; Peter chose "Left-to-right only for now"): left-to-right scripts, including Chinese, Japanese and Hindi, are shaped in; right-to-left scripts are out of scope until a real need appears.
- **Accessibility added to the list, 2026-10-08** (product brief HC-10; Peter chose "Shape now, enforce on share"). Now: the toolkit can expose factor to a screen reader, every action is reachable by keyboard, and contrast is checked. The full floor is the release gate when anyone other than Peter first runs a build (Gate B, product brief HC-11).
- **Tenancy, ruled 2026-10-08** (Peter chose "Yes, that shape" on Puck's proposal): every stored plan carries an owner or workspace id, and storage is reached through that scope, even while there is only ever one value.

### D-032 The graphics are a view, separate from the backend
- **Status:** ruled 2026-10-08; extends D-009, and settles the presentation boundary of D-012
- **Peter:** "Asssume the graphics and the backend are separate. The graphics is a view so we could switch to a webbased one eventually, its also cleaner."
- **Outcome:** the drawing is a view over the backend and can be replaced without touching it. A web-based view is named as a possible future.
- **Puck's derivation, not ruled:** for a web view to be swappable in, the view-to-backend boundary has to be a data interface (requests and results that can be serialised), not shared in-process state. Building the desktop view against that interface from the start is what keeps the swap cheap.

### D-020 Graph semantics: conservation and ratios, or in-game splitter behaviour
- **Status:** ruled 2026-10-08. The engine brief calls it the decision that shapes the engine most (brief §7 D1).
- **Peter:** "go ahead with ideal ratios, jams check later"
- **Outcome:** option (a). The core solves conservation plus ideal ratios as a linear program. In-game behaviour comes back as a separate check over a solved plan: loops that back up and jam, and which machines starve under even or priority splitters when supply is short. That check is tracked as brain task #3924, so it is deferred with a tracked task, not parked.
- **What was weighed (Puck's summary given to Peter before the ruling):** ideal ratios lose (1) ratios the game's even splitters can't build, which matters little on a saturated manifold, per D-005; (2) which machines starve when under-supplied; (3) jams in recycling loops, the real loss. They keep sub-millisecond whole-game solves.
- **Rejected:** (b) in-game behaviour in the core. It is Modeler's approach and the cause of its slowness (D-017 research).
- **Options:**
  - **(a) Conservation plus fixed ratios:** a linear program, fast and well understood. *Recommended by the brief.*
  - **(b) In-game behaviour:** even splits, priority splitters, backpressure, deadlock or starvation detection. This is what Modeler's users praise **and** what makes it slow. The only route the brief found is an untested sequence of linear programs.
- **Brief's recommendation:** (a) as the core. In-game simulation would be **parked**, not deferred, because nothing would trigger it automatically. It returns only if Peter decides the diagram must flag in-game deadlocks, and then as a separate analysis pass over a solved plan. (Superseded by the ruling: Peter wants the check, so it is now a tracked task.)
- **Picker, 2026-10-08:** F-004 Splitter/merger behaviour simulation marked *later*, not *skip*. Puck's reading, not ruled: (a) now, with simulation as a later pass, which is the brief's shape. Asked whether that settles D-020, Peter chose "Not yet" (2026-10-08). That was Puck's option, worded as wanting to talk through what losing in-game splitter behaviour costs before ruling.

### D-017 Core calculation model
- **Status:** ruled 2026-10-08, via the option "Yes, rule it" (Puck's wording, his answer is the label)
- **Outcome:** option (a). The core is a linear program, mixed-integer only where whole machines force it. A change recomputes only the connected part of the graph it touches, and loops are solved directly as equations. Follows from D-020 (ideal ratios) and F-001 LP auto-solve at *mvp*.
- **Rejected:** (b) SAT / constraint programming, Peter's starting assumption: rates are continuous and the questions are optimisation questions, which SAT doesn't answer. (c) Modeler-style propagation: it recomputes every node on every change, and has to iterate loops until they settle.
- **Peter:** "i assume currenly we need something like a sat solver, but we can discussion. modeller dies because it can't calculate all the nodes on a change and it looks like it runs out of memory. its java so that is always an issue. it does have some nice features but it isn't structured how i like."
- **Options:**
  - **(a) Linear programming,** mixed-integer only where whole machines are required. Used for planning ("hit these targets") and for propagating flows through a drawn graph. *Puck's recommendation.*
  - **(b) SAT / constraint programming.** Peter's starting assumption. Puck's view: SAT answers yes/no over true/false variables, while factory rates are continuous and the questions are optimisation questions.
  - **(c) Graph propagation, Modeler-style.** It fails at scale when every node is recomputed on each change, and loops have to be iterated until they settle.
- **Proposal (Puck), whatever the solver:** recompute only the connected part a change touches, and solve loops directly as equations.
- **Related features:** F-001 to F-005 in the feature catalogue are the five calculation models found in existing tools.
- **Picker verdicts, 2026-10-08:**
  - F-001 LP auto-solve to target rates: *mvp*
  - F-002 Recursive tree expansion: *later* in round 1, changed to *skip* in round 2 (after Puck's suggestion that the solver covers it)
  - F-003 Manual node graph with rate propagation: *shape*
  - F-004 Splitter/merger behaviour simulation: *later* (bears on D-020)
  - F-005 Manual ledger with satisfy/trim sizing: *later*
- **Research (engine brief (docs/research/engine-2026-10.md) §1–2, 2026-10-05):**
  - **Linear programming is enough.** Neither SAT nor a mixed-integer model is needed for rates.
  - **Measured by Sage, and re-run by Puck with matching results** (HiGHS 1.15.1 via Python, Apple M4):
    - whole-game Satisfactory, 291 machine recipes: about 0.9 ms;
    - 300 coupled factory copies (141,600 columns) with binding resource caps: about 666 ms.
  - **Proving a model infeasible is the slow case:** 8.9 s, against 0.47 s for a feasible one (Sage, not re-run).
  - **Modeler is slow because of its semantics, not its solver** (observed, from its 2025-03-26 devlog). It simulates in-game splitter and merger behaviour, and its own manual calculators "always run quickly". That makes D-020 the deciding question.
- **Answered 2026-10-08:** asked what "isn't structured how i like" meant, Peter chose two of Puck's options: "Factory organisation" (how factories, sub-factories and outposts nest and link) and "Interface and layout". He did not choose "Drawing it all by hand" or "Speed only". Factory organisation is open as D-035.

### D-018 Raw resources: free up to a cap, or must be sourced
- **Status:** ruled 2026-10-08, via the option "Yes, rule it"
- **Outcome:** the model treats extraction as a recipe with no inputs, so miners, nodes and their power can appear in a plan. The screen defaults to "free up to a cap" until sourcing is turned on. Per-node sourcing can come later without a model change.
- **Context:** feature F-046. Most optimisers assume raw supply is free up to a cap. One tool (Satisfactory Factories) made "must be mined or imported" a deliberate breaking change. The choice changes how many other features read.
- **Picker, round 2 (2026-10-08):** F-046 marked *shape*, after reading Puck's lean: extraction is modelled as a recipe with no inputs, and the screen defaults to "free up to a cap".
- **Picker, round 1:** F-046 had no verdict. Peter's note: "need to understand the ramifications of this one. seems all the games have to be mined, factorio has limited supply, what does this option provide of value"
- **Amended 2026-10-08.** Relayed from the design session, then confirmed by Peter in the lead session (round-5 review of the product brief): "Yes, each resource node can only have one miner on it. So to get past the cap you need inputs from multiple resource nodes." On the ore default, Peter picked "Miner sets the cap": every raw resource names its extractor and node attributes (purity), and its ceiling is derived from them, never typed. Peter, verbatim as relayed: "a miner has a default clock of 100% and on a normal node that means 120/min. If i add three shards that is 250% of the 120, so 300. Additionally i can unclock as well, so the actual cap is 300 in this case and I can change that value from 0-300 manually to a percentage. So 75% would be 90." And, on miner and purity: "factor picks a default and i can change it if needed". On why ore would fall short: "The only way an ore falls short is if the miner has no power, it turned off, or is clocked below what is required downstream?"
  - **F-009 Per-resource caps, re-described (round-6 review, 2026-10-08):** Peter chose "Cap = pinned extractor clock". There is no separate typed cap: a resource is limited by pinning its extractor's clock, for example 2/3 of a Mk.2 on a Normal node is 80/min.
  - **Effect on the Outcome above:** the screen no longer defaults to a typed "free up to a cap". The cap is the extractor's derived ceiling, and a shortfall comes from a pinned extractor clock. Measured miner data (en-US.json, relayed): Mk.1 60/min at 5 MW, Mk.2 120/min at 15 MW, Mk.3 240/min at 45 MW; exponent 1.321929. The purity multipliers (×0.5 / ×1 / ×2) are game knowledge, not in the data.

### D-034 Interface over tutorials
- **Status:** ruled 2026-10-08, via the option "Yes, as stated"
- **Outcome:** design so that no walkthrough is needed, and reveal advanced options step by step. A shipped demo plan is allowed: an example factory to open, which doubles as test data.
- **Peter, 2026-10-08, picker note on F-081 Guided tutorial and demo plans:** "i will say i saw satisfactory logistics demo/walkthrough. if the interface is bad enough you need that i think maybe making a better interface if possible. or incrementally add advanced options"
- **Puck's reading, which Peter then ruled:** prefer an interface that needs no walkthrough, with advanced options revealed step by step (progressive disclosure). A shipped demo plan is a separate thing from a walkthrough: an example factory to open, and one that doubles as a test fixture.

### D-033 Plan file format
- **Status:** ruled 2026-10-08, via the option "Rule SQLite"
- **Outcome:** plans are stored in SQLite: a documented schema, with the `sqlite3` tool or a factor reader as the way to get text out. The deciding reasons, as Puck put them before the ruling: changes on a large factory save incrementally; transactions give crash-safe autosave; the tenancy scope (D-031) is a column; format versions are schema migrations; and it bundles through `rusqlite` with no system dependency, Windows included.
- **Rejected:** a binary serialisation (postcard or bincode). It is smaller and simpler, but rewrites the whole file on every save, needs hand-rolled versioning, and can't be queried. Text formats (JSON, TOML, RON) were rejected first, by Peter's preference.
- **Peter, 2026-10-08, picker note on F-129 File export and import:** "not json please."
- **Peter, asked why not JSON:** "i don't like text files unless they are required. I think the web with json made a mistake tbh, well that was because whenever i ask why json, i hear "so i as a person can read it" i am used to compiled formats, small, parquat etc. efficient. so Ron would be out too. binary or sqlite, i think sqlite might be interesting if we need to search the data and query on it and it is sql so kind of standard. We can document the format and provide a reader for people to generate a text format if they want."
- **Ruled with it:** the format is documented, and a reader can turn it into text for anyone who wants that.
- **Context:** F-129 is now *mvp*: on desktop a saved plan is a file, so saving is export. The format needs a version from day one.
- **Options as they stood:**
  - **TOML, RON:** rejected 2026-10-08. Text formats, which Peter doesn't want for data.
  - **Binary (postcard or bincode) plus a text export:** compact and fast on large factories, but not readable by hand.
  - **SQLite:** one file per plan or a library of plans; queryable, and transactional saves. The heaviest option.

### D-016 Nonlinear power and clocks in the solver
- **Status:** ruled 2026-10-08, via the option "Fix clock, then size"
- **Outcome:** option (c), the brief's option A. Rates are solved exactly as a linear program. Whole machines are chosen afterwards, by fewest buildings or a count Peter sets, with clock = rate ÷ (count × base), exact. Power is computed from the per-game curve afterwards, and fed back into the solve only where it binds. Somersloops change material flow, so they are set before the solve (brief §3).
- **Shards, 2026-10-08:** Peter: "should note that adding shards would be a manual task unless i ask for it to be sharded." And: "so a shortfall shouldn't add shards that are not already allocated". factor never adds power shards by itself; a shortfall's fix may use shards already placed, never new ones.
- **Refined again 2026-10-08 (product brief SC-6, round-6 review):** a pinned count that can't make a rising target at 100% holds. The rest is a named shortfall with fixes such as "unpin the count"; Peter chose "Hold the pin, name a shortfall". Demand beyond one resource node's ceiling is a named shortfall with the fix "add a resource node"; Peter chose "Name a shortfall".
- **Refined further 2026-10-08 (product brief SC-6, SC-9):** when a target rises past what kept machines make at 100%, factor adds the fewest new machines and re-clocks all of them evenly, at or below 100%. Peter chose "Add machines" over "Overclock first" and "Name a shortfall". A released count pin re-minimises that node: Peter chose "Re-minimise that node" over "Keep current count".
- **Refined 2026-10-08 (product brief SC-6):** after a target or cap change, existing machine counts are kept and only re-clocked; re-minimising is an explicit action. Peter chose "Keep counts, re-clock" over "Re-minimise every time" and "Keep only what I pinned". So fewest buildings applies at a first solve and on an explicit re-minimise (and, per the later refinement above, to a released count pin).
- **Not selected:** optimising shard and Somersloop placement from stock (the brief's option B, mixed-integer), offered as "also optimise shards/sloops". Not rejected: the brief suggests adding it when it's wanted. Piecewise approximation (option b) was not selected either.
- **Context:** D-007, D-008.
- **Options:**
  - **(a) Fixed clock steps** as separate solver options. *Weakened by D-008:* Peter uses arbitrary exact clocks.
  - **(b) Piecewise-linear approximation:** mixed-integer, approximate power, any clock.
  - **(c) Solve rates as a linear program, then size machines.** The machine count comes from Peter or a rule (fewest buildings, least power). Clock = rate ÷ (count × base), exact. Power is computed from the curve afterwards. Power enters the solver only when it is the binding limit ("most output from 500 MW"). *Puck's current lean, revised after D-008.*
- **Research (engine brief (docs/research/engine-2026-10.md) §3, 2026-10-05):**
  - Every tool read fixes the clock per recipe before solving and computes power afterwards. For a fixed clock, power is linear in rate; that's Sage's derivation, labelled inferred.
  - Somersloops change material flow, so they have to go inside the solve, not after it.
  - Whole machines come from rounding up after the solve in every tool read.
  - The brief's recommendation is "option A first": clock fixed before the solve, which is (c) above. Somersloop-stock optimisation as a mixed-integer model (its "option B") is added only when wanted.
  - This is the brief's D2.
- **Note 2026-10-08:** where this block says "target or cap change", read "target change or pin" (D-018 amendment: no typed caps). Placed shards give headroom that factor may use before adding machines, and releasing a shard pin removes the shards (product brief SC-6, SC-9; Peter chose "Use placed headroom", round-7 review).

### D-021 Solver dependency
- **Status:** ruled 2026-10-08 (brief §7 D3), via the option "HiGHS, own trait"
- **Outcome:** HiGHS through the `highs` crate directly, behind factor's own solver interface (build model → solve → primal values, duals, status). microlp is kept compiling as a toolchain-free fallback and a cross-check. Building needs CMake and a C++ compiler, plus LLVM/Clang on Windows; nothing extra for whoever runs the app.
- **Rejected:** microlp alone (slower, less proven, no duals, and its README makes no optimality guarantee); HiGHS through `good_lp` (CBC copyleft default, hides HiGHS's diagnostics, no determinism promise).
- **Options:**
  - **(a) HiGHS:** MIT licence, fast, gives duals. Needs CMake and a C++ compiler to build, plus libclang on Windows.
  - **(b) microlp:** pure Rust, Apache-2.0, no duals, slower and less proven.
- **Recommended by the brief:** HiGHS behind factor's own trait, with microlp kept compiling as a fallback that needs no toolchain.
- **Traps:**
  - `good_lp` defaults to the CBC backend (EPL-2.0 licence, system library), so set `default-features = false`.
  - The `highs` crate doesn't wrap HiGHS's IIS, ranging or warm-start calls, so those need unsafe FFI.
- **Unverified:** whether HiGHS still needs `libomp` on macOS. The build-cleanly claims rest only on CI configuration files.

### D-022 Exactness: floats with a residual check, or exact rationals for results
- **Status:** ruled 2026-10-08 (brief §7 D4), via the option "Exact fractions"
- **Outcome:** solve in floating point for speed, then re-check the final answer in exact rational arithmetic, and show the rationals (37.5 = 75/2, 88.8889% ≈ 8/9). The exact plan never overdraws a limited input (D-008). **Amended 2026-10-08:** display rounds to nearest, like the game (see D-008's supersession). A clock rounded up can exceed its exact value by at most 0.00005 percentage points, and Peter chose "Say nothing" when asked whether factor should flag it (product brief SC-4). The original wording here, "Rounding for display never overdraws a limited input", is superseded.
- **Rejected:** floats with only a residual tolerance check: rounding can still overdraw by a hair.
- **Context:** D-008 requires exact clock values to 4 decimal places. The exact plan never overdraws a limited input; display rounding is covered by this block's amended Outcome.
- **Recommended by the brief:** show rationals, and re-check the final basis in exact arithmetic. YAFC's precision bugs are the cautionary tale.

### D-023 Default objective and penalty weights
- **Status:** ruled 2026-10-08 (brief §7 D5), via the option "Scarce resources + tuning"
- **Outcome:** by default the plan minimises raw resources weighted by how scarce each is, with fewer buildings as the tie-break. The weights are re-tunable (power, buildings, a specific resource) behind advanced options, per D-034. The formulation is elastic: every item carries penalised surplus, import and "can't produce" slack, so a plan always comes back with its problems named, never a bare "infeasible" (picker F-013 *shape*).
- **Not selected:** fewest buildings, least power, or fully user-tunable weights with no strong default.
- **Options:**
  - least raw resources, weighted by scarcity;
  - fewest buildings;
  - least power;
  - user-tunable, as in FactorioLab.
- Each option changes which alternate recipes the plan picks.
- **Related:** the brief recommends an *elastic* model by default. Every item gets penalised surplus, import and "can't produce" slack, so a plan always comes back with its problems named, never a bare "infeasible". IIS stays a developer tool. That elastic default was part of the option Peter chose.

### D-024 "Plan to targets" and "the graph I drew": one view or two
- **Status:** ruled 2026-10-08 (brief §7 D6), via the option "One view, edit feeds back"
- **Outcome:** one view. Peter sets targets and factor lays out the diagram. Editing the diagram (pin a recipe on a node, fix a machine count, cap an input) becomes a constraint and triggers a re-solve. Free-hand, Modeler-style drawing comes later on the same engine (picker F-003 *shape*).
- **Not selected:** two views from the start (a targets table plus a free canvas), and canvas-first like Modeler.
- **Context:** YAFC's linked tables, Foreman2's nodes and Modeler's canvases are three interaction models over the same linear program. The brief's proposed engine shape compiles both front ends to one solver layer (brief §6).

---

## Open

Research behind these lives in `docs/research/`:
- `engine-2026-10.md`: the engine brief. "Brief §N" below refers to it. Its own decision labels D1–D6 are mapped onto D-016 and D-020 to D-024 here.
- `lp_bench*.py`: its benchmarks. Run them with `uv run lp_bench.py <en.json as UTF-8>`.
- `calc-features.json` and `calc-tools.md`: the feature catalogue (`F-NNN`) and the tool survey behind it.
- `data-sources-2026-10.md`: the data-sources brief, covering save parsers, missing-data sources, publisher terms and the cross-game model matrix. "Data brief §N" refers to it; its §8 decisions are mapped onto D-019 and D-025 to D-029.

**Feature picker, rounds 1 and 2 (2026-10-08).** In round 2 Peter marked against Puck's suggestions, which are kept in the separate `suggest` collection. All 142 rows now carry his verdict; he and Puck still differ on F-049, F-070, F-090, F-096 and F-141, and his verdict stands on each. Peter marked the catalogue in the picker Artifact (https://claude.ai/artifact/J15Nsun9doxDoF6ewfuHZH); the marks live in its `picks` collection. Verdicts, as Peter defines them: "i took skip to mean that we know about them but not right now, later is we will implement and shape was ensure it has the backend structured for it."
- *mvp*: in the first build.
- *shape*: the backend is structured for it from the start; the feature itself comes later.
- *later*: will be implemented eventually, not immediately. Peter: "later means eventually not immeduately".
- *skip*: known about, not planned now. **Not** a rejection.
- **Superseded reading (Puck, 2026-10-08):** *skip* as "not wanted" and *later* as "not now". Wrong on both: it read his skips as refusals.

A verdict is Peter's label on a catalogue row, not his words about a decision. Where a row maps to a decision below, the verdict is recorded there as evidence, and the decision stays open until he rules it.
- **Note 2026-10-08:** "cap an input" above predates D-018's amendment. A resource is now limited by pinning its extractor's clock; there is no typed cap (product brief SC-9).

### D-012 Layer split: calculation, physical, presentation
- **Status:** open, except the presentation boundary, which D-032 ruled on 2026-10-08: presentation is a separate, replaceable view. The physical layer and how physical limits reach the solver are still open.
- **Context:** D-009, D-032.
- **Proposal (Puck):** three layers.
  - **Calculation:** formulas and rates.
  - **Physical:** footprint, port count, positions and kinds, per-port and per-carrier caps.
  - **Presentation:** diagram nodes, grouping, positions. One diagram node may stand for many machines.
- **The catch:** physical limits feed back into the calculation, since whether a plan can actually be built depends on belt caps and port counts. Proposal: the solver takes physical limits as optional constraints.
- **Data gap (measured):** Docs has machine footprints (`mClearanceData`) but no port data. `mFactoryInputConnections` and `mPipeInputConnections` are empty on all 11 manufacturers.

### D-013 Name for the generic carrier concept
- **Status:** open
- **Options:**
  - **Conveyance:** the most general; covers belts and drone routes equally. *Puck's pick.*
  - **Carrier:** plain, reads well in code; leans toward vehicles.
  - **Conduit:** fits belts and pipes, a stretch for trains.
  - **Conveyor:** Peter's placeholder word. In Satisfactory it already means the belt, which risks confusion.

### D-014 Carrier families and route consumption
- **Status:** open
- **Proposal (Puck):** two families.
  - **Continuous** (belts, pipes): a fixed rate cap per tier.
  - **Route** (trains, trucks, drones): throughput = capacity per trip ÷ round-trip time.
    - Capacity = inventory slots × the item's stack size.
    - Round-trip time is user-supplied, since it depends on the route and isn't in the game data.
    - A route consumes batteries, fuel or power. That makes it a recipe-like consumer which feeds back into the calculation.
- **Data (measured, Docs):**
  - Inventory slots: Freight Car 32, Truck 48, Tractor 25, Drone 9.
  - Drone Port `mTripPowerCost` and `mTripPowerPerMeterCost`.
  - Vehicle `mAutopilotFuelConsumption`.
  - Electric Locomotive power min/max.
  - Item stack-size enums.

### D-015 Matching items to belts or pipes
- **Status:** open
- **Options:**
  - **(a) Each carrier type declares the item forms it accepts:** solid, liquid or gas, all already in Docs as `mForm`. No new tag on items. *Puck's pick.*
  - **(b) A belt/pipe tag on each item.** Proposed first, before D-006.
- Either way, the calculation never sees it; it serves the physical layer only.

### D-019 Icons and map data: source and redistribution
- **Status:** open
- **Context:** features F-094, F-095, F-096. The CommunityResources bundle has texture paths but no images, and no node, collectible or port positions. Extraction from a local install is possible (FModel or CUE4Parse plus the bundle's `.usmap`). Whether extracted art and data may be redistributed is a licence question; SCIM's licence forbids reusing its map data. Repo visibility (public by default) makes this matter before the first push.
- **Research (data brief §2–5, 2026-10-05):**
  - **Coffee Stain:** no published terms on redistributing extracted data or art were found. The modding docs say redistributing extracted assets "should not be done without permission". The Satisfactory wiki's text is CC BY-NC-SA 4.0, which is non-commercial.
  - **Where the missing data can come from:** node positions, default purity and icons can be extracted from the user's own install with CUE4Parse or FModel, using the bundle's `.usmap` and `CustomVersions.json`. The projects that do this keep extracted data out of their repos.
  - **Purity multipliers:** 0.5× / 1× / 2× is reported, not extracted.
  - **No source anywhere** for machine port counts or positions.
- **Icons sub-question (data brief §8.4):** ship them, have users extract them, or use none.
- **Picker verdicts, 2026-10-08:**
  - F-094 Game icon extraction: *mvp*
  - F-095 Resource node map: *shape*
  - F-096 Collectibles map: *shape*, kept in round 2 over Puck's *skip*. Peter's note: "my primary use case for use case for sat calc is the map with the collectable, i even load my save to see what i missed and where things are. So to me this is core, but it can be after the planning part."
  - So collectibles matter to Peter, after planning, and they come with loading his save. That puts the save parser, which hangs on the licence decision (D-025), and randomised worlds (D-027) on the map's path.
- **Peter, 2026-10-08, asked how the first build gets icons:** "this is initially for me only, we'll need a windows build of it i guess or i can copy a save over, want to get it working first before worrying about sharing."
- **Outcome (icons, first build):** extracted from Peter's own install for his own use. Nothing is redistributed, so the redistribution question waits until factor is shared: at whichever sharing gate comes first, the first public remote or the first build packaged for distribution (product brief HC-11).
- **Still open:** how the files reach the extractor. Peter's options: a Windows build, or copying files over to the Mac ("i guess" — not settled). **Puck's note:** a save file carries node data (D-027) but no icons. Icons sit in the install's asset archives, so "copy a save over" covers the map side, not the icons.

### D-025 factor's own licence
- **Status:** open (data brief §8.1)
- **Context:**
  - The only Rust Satisfactory save parser found (`valentinps/satisfactorymap`) reads 1.2. It is AGPL-3.0 under a "non-transferable" permission from GreyHak, tied to a browser tool, so it can't simply be reused.
  - The only permissively licensed parser claiming 1.2 support is `etothepii4/satisfactory-file-parser` (TypeScript, MIT). Its history before 2024-10-06 isn't visible, so its ancestry is unconfirmed.
  - moritz-h's format document covers save version 58. The bundle is at 60 (measured: `CustomVersions.json` `SaveVersion` = 60). Versions 59 and 60 look like data migrations only, inferred from the header comments.
  - Which parser factor builds on, or ports, follows from this licence choice.
- **Options:** AGPL; permissive (MIT/Apache); commercial or closed.

### D-026 How game data reaches users
- **Status:** open (data brief §8.2, §8.3)
- **Options, per game:**
  - **(a) Ship generated data files.** Needs redistribution rights, which are unconfirmed for every game.
  - **(b) Ship only the generators,** run by users against their own install. Nothing is redistributed.
  - **(c) Ask the publishers.** Coffee Stain, and Wube before any commercial release.
- **Publisher terms found:**
  - **Wube:** its ToS requires "express consent" for commercial asset use, but it publishes its Lua prototype data and names calculators as an intended use.
  - **Foundry (Paradox):** user-generated content, "scripts and programs" included, is non-commercial only.
  - **Techtonica, Alchemy Factory, DSP:** no policy found.
- **⚠ Platform tension, raised by the research:** with option (b), users extract from their own install, but four of the five games are Windows-only; only Factorio has a native macOS build. factor is macOS-first (D-001). The extractors are probably portable (inferred); getting Windows game files onto the Mac is the problem.
- **Licences not checked:** the Satisfactory and Alchemy Factory pipelines depend on Oodle decompression.
- **Related:** D-003 (generators) and D-004 (raw bundle out of git).
- **Carried from the product brief (NG-5), 2026-10-08:** D-004 says to commit "a small extract" of the game data instead of the raw bundle. Once the repo has a public remote, that extract is redistribution, so it falls under this decision. The repo has no remote today. It must clear at whichever sharing gate comes first: the first public remote, or the first build packaged for distribution (product brief HC-11, FQ-8).

### D-027 Randomised 1.2 worlds
- **Status:** open (data brief §8.5)
- **Context:** Satisfactory 1.2 can randomise each node's resource and purity. Saves carry `mResourceClassOverride` and `mPurityOverride` on node actors (observed in two parsers). That the override is written on every non-geyser node is the parser author's report, untested. If true, a fixed node table is right only for the default world, and node data has to come from the save.

### D-028 Acceptable community data inputs
- **Status:** open (data brief §8.6, §8.7)
- **Context:** whether to use unlicensed or reuse-restricted community datasets, and whether numbers or text may be copied from the non-commercial Satisfactory wiki. SCIM's licence forbids reusing its data.

### D-029 Scope of the shared core model
- **Status:** open (data brief §6, §8.8)
- **Evidence-backed core (inferred from the 6-game matrix; a concept qualifies if it appears in at least 5 of 6 games):**
  1. Items and fluids as one thing with a form tag.
  2. Recipes as inputs → outputs over a cycle time, with multiple outputs and catalysts allowed.
  3. Random outputs as expected rates.
  4. Machines with a speed and a list of recipes they can run.
  5. Extraction as a recipe with no inputs, times a site multiplier.
  6. Two carrier families: continuous (rate per tier) and route (slots × stack size). Also a global belt multiplier.
  7. Game-wide modifiers, with exemptions for individual recipes.
  8. Per-machine utility consumption under a per-game rule.
  9. An unlock graph.
- **Per-game extensions, not core:**
  - Satisfactory: Somersloops, shards, the nonlinear power curve.
  - Factorio: modules, beacons, quality.
  - DSP: the proliferator, which is a consumed input.
  - Foundry: robot stations.
  - Alchemy Factory: cauldron, catalyst charges, heat, nutrients, money.
  - Fluid temperature.
- **Open sub-questions:**
  - A per-machine modifier slot appears in 4 of 6 games, one short of the bar. The data brief suggests it as a core *hook*, not core data.
  - Alchemy Factory's value-based cauldron recipes (447,580 combinations) can't be listed as Formulas.
  - Power as a generic per-game "utility resource" (heat in Alchemy Factory).
  - Currency as a resource. Peter, 2026-10-08, on F-062 AWESOME Sink: "the tickets/points are a kind of coin as well." Satisfactory's sink points join Alchemy Factory's money as a second currency-like case.
- **Vocabulary check (D-011):**
  - `Unit` and `Fabricator` hold.
  - `Formula` needs flags (such as cost-multiplier exemption) plus conversion of batch multipliers and catalyst charges.
  - `GlobalModifiers` breaks, since most modifiers are per machine, some act on belts or fuel, and DSP's proliferator is an input.
- **Prior art:** FactorioLab (MIT) already serves more than ten games from one schema, and puts purity, Somersloops, the proliferator and Foundry's robots under a single "module" idea with per-game flags. Compare against it before designing.
- **Supports D-014:** Factorio and Foundry measure wagon capacity in stacks, which backs the slots × stack-size proposal.

### D-035 Factory organisation
- **Status:** open
- **Context:** one of the two things Peter dislikes about Modeler's structure (D-017, answered 2026-10-08): how factories, sub-factories and outposts nest and link in a big build. The other was its interface and layout.
- **Picker marks:**
  - F-053 Multiple factories per plan: *mvp*
  - F-054 Nested sub-plans: *mvp*
  - F-056 Spin off a sub-chain: *mvp*
  - F-055 Factory groups with rollups: *shape*
  - F-057 Plan statistics and building summary: *mvp*
  - F-067 Notes and tasks per factory: *mvp*
- **Prior art (tool survey, `docs/research/calc-tools.md`):** Modeler nests outposts as sub-canvases, and reuses blueprints as sub-modules with limits. Satisfactory Factories keeps a ledger of up to 300 factories with imports and exports between them, plus groups with rollups. Satisfactory Logistics links factories through tracked inputs and outputs.
- **Questions to settle:** what a factory is in the model (a solve boundary or only a grouping); how flows between factories are represented (as transport, D-006); how deep nesting goes; and how a spun-off sub-chain stays linked to its parent.

### D-036 UI toolkit
- **Status:** open
- **Peter, 2026-10-08:** "i was considering dioxus, i'd prefer close to native vs web format but that will cause some concerns :-)"
- **Peter, 2026-10-08:** "i'd prefer for the local version to be naitive drawn, libraries will be the key or we need to roll some up. we could also maybe use something like opengl or bevy or UE5 but they seem overkill."
- **Research:** `docs/research/ui-toolkit-2026-10.md` (Sage, brain #3930). It ranks without deciding; nothing was rendered or benchmarked, and every performance statement in it is a vendor claim or an inference until the spike runs.
- **Shortlist (research §7):**
  1. **egui** (eframe + egui_table). Pure Rust, permissive licences, screen-reader support on by default, a virtual-scrolling table, idle at zero CPU, and raw wgpu available for the diagram. Risk: no bidirectional text (egui #1016), so right-to-left scripts are not covered (bears on D-031).
  2. **GPUI with gpui-kit.** The broadest widget set, and the closest to the CSS mockups. Risk: supply chain. No crates.io GPUI release since 0.2.2; gpui-kit depends on a third party's weekly repackaging of Zed's code. Screen-reader support is recent (2026-05-27).
  3. **Slint.** Stable 1.x API, the best text stack, screen-reader support, and a company behind it. Risk: its licence. It is GPL-3.0, royalty-free with required attribution and a ban on exposing its APIs (which matters for plugins), or paid. That ties the choice to D-025. The UI is also written in Slint's own language.
  - **Not shortlisted:** Iced and Makepad/Floem (no screen-reader support), Bevy (no table widget), Freya/vizia (single maintainer), Xilem (experimental), UE5 (not Rust; royalty), Tauri (webview; comparison arm only).
- **Peter's "overkill" (research §5):** right for UE5, and right as a build-cost argument for raw wgpu or OpenGL. For Bevy the obstacle is its young widget set, not its weight. No native toolkit ships a diagram component proven at 500+ nodes, so factor draws the diagram itself in every option.
- **Decisions the research hands back (§8), each with its recommendation:** rule D-036 only after the spike; whether right-to-left scripts are in D-031's scope; that Slint's licence must not settle D-025 by default; the spike's pass thresholds; which agent implements native Rust UI (none does today); whether to run the Tauri comparison arm.
- **Spike (research §9), S-UI-1:** egui, GPUI and Slint, plus an optional Tauri arm. Each renders the same seeded 500-node plan (and a 2,000-node stretch), and frame time is measured externally. Gating thresholds proposed: p95 frame time ≤ 16.7 ms at 500 nodes, idle CPU ≤ 1%, a Windows build, and a working arm within 2 days.
- **Why it matters now:** the UI brief for Claude Design (`docs/design/ui-brief.md`) produces HTML/CSS mockups. How directly those carry into code depends on this choice, and so does which agent can implement the view (D-032).
- **Options as first written (Puck, before the research; the Dioxus and Slint lines are superseded below):**
  - **Dioxus.** Rust throughout, React-like components, styled with HTML/CSS, so Claude Design's tokens and layouts carry over closely. The same components can target the web later (D-032). ⚠ **Its desktop renderer today is a system webview** (Wry): "Dioxus desktop is built upon the Wry library … using a WebView", and the WGPU-based native renderer (Blitz) is described as "experimental" (Dioxus 0.7 docs, read via Context7 on 2026-10-08). So "close to native" means betting on Blitz maturing. Its API has also changed between minor versions (0.6 to 0.7).
  - **Tauri with a web front end.** The same webview model, with the view in TypeScript (Svelte), which is the frontend agent's stack. That adds a second language, which Peter's Rust preference weighs against.
  - **A native Rust UI** (egui, Iced or Slint). Truly native rendering. egui suits dense tool UIs and node graphs; Iced and Slint are declarative. None of them uses CSS, so the mockups become a reference that has to be translated by hand. Licences not checked. **Superseded by the research:** Slint's licence was checked and is not permissive (see the shortlist).
- **The real test, which applies to every option (Puck's derivation):** the diagram must stay fast with hundreds of nodes, the whole point against Modeler. Proposal: a spike that renders a generated 500-node plan diagram in the leading candidate, measuring frame time and memory, before ruling.
- **Agent coverage:** no current implementer agent builds in Dioxus or the native toolkits. Forge is backend Rust, and Rune is Svelte/TypeScript. A Dioxus choice means extending Forge's scope or hiring a view agent.
- **Superseded on the Dioxus line (research §6):** the Blitz README now says "beta" (0.3.0-beta.2), but stable `dioxus-native` 0.7.10 still pulls the older Blitz line. The beta needs Dioxus 0.8 alpha, which is a third API cycle. Blitz bundles 15 MPL-2.0 packages (Servo's Stylo), can't style SVG fill or stroke, and doesn't support `unicode-bidi`. The webview statement still holds. Dioxus is not shortlisted.

### D-037 The repo holds the design source; the Claude Design canvas is a view of it
- **Status:** ruled 2026-10-08, by Peter accepting the design session's account
- **Peter:** asked whether to record "the repo holds the design source, and the Claude Design canvas is a view published from it", he answered: "sure, that was how it told me it worked."
- **Outcome:** design source lives in `docs/design/mockups/` (artboards, `canvas.json`, `factor-tokens.css`). The Claude Design canvas is published from it and is never edited as the original. Round-1 handoff material is kept verbatim under `docs/design/mockups/handoff-round1/`.
- **Provenance:** the arrangement was set up by a separate Claude Design handoff session (task #3932). Its wording reached this log through that session, and Peter confirmed it here.
