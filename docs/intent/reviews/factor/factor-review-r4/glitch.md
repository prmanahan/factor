# Glitch review, round 4: docs/intent/factor.md (Intake, product altitude)

Lens (narrowed by the "Strip to outcomes" ruling): is each outcome observable from outside, can it fail for the right reason, do two outcomes contradict, is anything too vague to test later. Fixture, seam, sample-count and start-state points are [SPEC-DEFERRED]; I only check that FQ-10 holds them.
Read: the brief in full; `scratch/factor-review-r3/glitch.md`; `docs/decisions.md` D-018 (lines 176-184) and the shard ruling (line 208). Nothing was run. SC-4 worked-example arithmetic re-checked by hand: ore 80, smelters 80/30 over 3 = 8/9, downstream 3/4 x 8/9 = 2/3, shortfall 7.5 - 80/12 = 5/6. It holds.

## Findings

### G1 (medium) SC-6 / SC-2: "a resource node's ceiling" has no defined population in a plan
Anchor: SC-6 ceiling bullet; SC-2; D-018 amendment.
SC-6 says demand beyond a node's ceiling is a named shortfall with the fix "add a resource node". That is testable only if the plan knows how many nodes it has, at what purity and type, and what an unpinned extractor's clock may reach. The brief states none of it. D-018 says extraction is a recipe, a recipe node "can stand for many machines" (Glossary), and each node holds one extractor. The two cannot both hold unless the plan carries a node inventory.
- Does a first solve of the SC-2 reference plan, whose ore demand is far above one node, name a shortfall everywhere, or does it create nodes? The brief says factor never adds a node, so the reference plan would need a declared inventory. SC-2 "solves to its known answer" depends on that and says nothing about it.
- The ceiling's clock term is unstated for an unpinned extractor. Is it 100%? Peter's D-018 quote makes 250% reachable only with shards, and factor never adds shards, so 100% is the only consistent reading. Not written down.
- Is an extractor "a machine" for the "add the fewest new machines" rule? The Glossary says yes. SC-6 then says a miner cannot be added. State that extractors are exempt from the add-machines rule.
Fix: one sentence in SC-6 or SC-2 defining ceiling = type x purity x clock cap (unpinned clock <= 100%), and one saying where the plan's nodes come from (F-044 node inventory input is *mvp*, so name it).

### G2 (medium) SC-6 / SC-9: shards and Somersloops. Three outcomes are undefined
Anchor: SC-6 "never added", "at or below 100%", pinned count bullet; SC-9 "clock (including shards and Somersloops)", "Other kinds return to factor's choice".
- **Conflict:** "re-clocks all of them evenly, at or below 100%" versus "a shortfall's fix may use shards already placed". If a machine already has 2 shards placed and its clock is unpinned, may a rising target re-clock it to 200%? Both sentences apply. A test author gets two verdicts.
- **Pinned clock above 100% with no shards allocated:** SC-6 allows "higher only where Peter has also pinned a clock". In the game 150% needs a shard. Is the pin rejected, accepted with the shortfall named, or does clock imply shards? Unstated.
- **Release of a shard or Somersloop pin:** SC-9 says release returns to factor's choice, and factor's choice for shards is "never add". Release therefore silently strips shards Peter placed, or keeps them (then they are not released). Either way the outcome differs from "returns to factor's choice". Fix: state which. I recommend release unpins the clock but keeps the placed shards.

### G3 (medium, fix-induced) SC-7: the three-way split has overlaps and gaps
Anchor: SC-7 three bullets (fix of round-3 F1).
- **Overlap, no precedence:** one file can be old-version, reference removed recipes and be internally inconsistent. Which check runs first? A test cannot say which verdict is right.
- **Gap, newer-than-app:** a plan whose format version is higher than the running factor. It is neither corrupt, nor game-updated, nor older. Reject-with-named-error is the likely answer. It is unstated.
- **Gap, no or unreadable version marker:** corrupt, or oldest-version? Unstated.
- **Typo versus removal:** a recipe id that never existed is indistinguishable from a removed one, so a garbage id opens as a named problem. Fine if intended; say so.
- **Migration failure:** "anything that can't be carried over is named". If the migration itself fails midway, is the file rejected whole, or left untouched? Does migration rewrite the file on open? A silent rewrite that makes the file unreadable by the older build is observable and never mentioned. SC-8's "never corrupt" collides with it.
- **Round-3 F1 residual:** with unresolved nodes, does the rest of the plan solve (nodes excluded) or is it held? "Nothing is silently dropped" does not say what the numbers are.

### G4 (low-medium) SC-3 stale values: "runs past its limit" names no limit
Anchor: SC-3 Stale values.
"If a solve fails or runs past its limit, factor says so." Which limit? None exists in SC-3 or FQ-10 (FQ-10 limits cover input rejection and the sync interval). With no limit, "runs past" cannot fail. Also "until each displayed value is replaced by its new one": a value that does not change is never visibly replaced, so the criterion cannot tell stale from current for it. State that staleness is per solve and clears for the whole display together, or per changed value.

### G5 (low-medium) SC-8: "every completed edit" versus "lose at most the last edit"
Anchor: SC-8 crash bullet.
The outcome says reopening shows every completed edit. The ruling it cites says "lose at most the last edit". These agree only if "last edit" means the in-flight, not-yet-displayed one. SC-3 puts the commit inside the window, so the stronger reading is intended. A test author reading Peter's label asserts the weaker bound and passes an implementation the outcome forbids. Drop the "at most the last edit" label or define it as the incomplete edit.
Also: "the plan file is never left corrupted" has no oracle. Say "passes SC-7's load check after any crash".

### G6 (low) Terms: "pin" is used for non-pins
Anchor: SC-9 lead sentence; F-007 "Scale targets to a pinned input"; SC-9 Not pins.
The SC-9 lead, "every value Peter sets for the solver to keep", reads wide enough to take in targets, which the Not-pins bullet then excludes. F-007's "pinned input" is a supply input, which SC-9 says is not a pin. A test enumerating "every pin" from the glossary and one from F-007 disagree. Reword F-007's title in the register or footnote it.

### G7 (low, carried) SC-2 has no time bound on load or first solve; re-minimise is outside SC-3
Anchor: SC-2; SC-3 edit list; FQ-10.
Round-3 F11 is not resolved, and FQ-10 does not hold it (its time limits cover SC-7 rejection only). Either say "completes without exhausting the 1 GB bound" is the deliberate bar, or add bounds to FQ-10. The explicit whole-plan re-minimise (SC-6) is in no timing criterion. Releasing a count pin is covered, since it is a pin release.

### G8 (low, carried) SC-5: core bug fixes, and "plans correctly" has no named oracle
Anchor: SC-5.
Round-3 F13 stands: a defect fix in the core made while adding game 2 is "any other core change" and fails SC-5 as written. State whether a fix adding no game-specific behaviour counts. "Plans correctly" for game 2 needs a known-answer reference for that game; say it is built per game at that time, so the criterion is not vacuous.

### G9 (low) SC-1: "stops using" is asked once
Anchor: SC-1.
A self-report at the first-build release measures intent, not that he stopped. It can pass for the wrong reason. Acceptable if the intent is a one-time question; if "stops" is meant, name a window ("for N weeks of real builds").

Fix-induced fraction: G3 fully (fix to F1), G2 and G1 partly (from the new SC-6 rulings), G4 and G5 from earlier text, G6-G9 not. Two of nine fully fix-induced and two more partly. That is lower than round 3 (11 of 14). No high findings.

## Round-3 dispositions

- F1 SC-7 two outcomes, one fixture: **resolved by the rewrite** (three-way split). Residuals are G3.
- F2 SC-3 window ambiguities: **resolved by the rewrite** (the "largest connected part" wording is gone). Edit locations and sample count are **SPEC-DEFERRED** to FQ-10.
- F3 stale marking cannot fail; no check for the 1 s redraw: **moved to FQ-10** ("solve delay", "how the redraw and stale marks are timed"). Stale marks on screen and to assistive technology is observable. Residual wording is G4.
- F4 SC-2 oracle versus one connected plan: **moved to FQ-7**. FQ-7 should carry the constraint that the join preserves the answer and the edit-reachable component stays megabase-sized (SPEC-DEFERRED, not raised). The "291" is now a measured example, not a hard number.
- F5 SC-4 fixture omitted the miner: **resolved by the rewrite** (Miner Mk.2 on a Normal node is explicit; arithmetic re-checked).
- F6 SC-6 raised-target start state and weakness: **moved to FQ-10** (the 9/min and 10/min cases are named there).
- F7 SC-8 commit inside the window: **resolved by the rewrite** (SC-3 now puts the save of the edit inside the window and the sync outside it). The backend-readable completed-edit signal: FQ-10 does not list it, so add it.
- F8 power-loss seam and observable sync: **moved to FQ-10** (storage seam, sync-interval bound). FQ-10 does not list "each sync is externally observable"; add it.
- F9 SC-9 release for the newly covered kinds: **mostly resolved by the rewrite** (targets are not pins; counts, extractor type and purity have stated release results). Residual: shards and Somersloops (G2).
- F10 SC-7 presupposes FQ-4: **resolved by the rewrite** ("this criterion doesn't decide it").
- F11 SC-2 time bound, SC-3 excludes re-minimise: **still open** (G7).
- F12 5,000 machines as a solved output: **resolved by the rewrite** (Glossary defines machine; the criterion is "on that plan"). Whether extraction recipes count as recipe nodes remains implicit and is deferred to FQ-7.
- F13 SC-5 bug fixes versus extension: **still open** (G8).
- F14 SC-7 oversized, hang, memory numbers: **moved to FQ-10** ("time and memory limits for rejecting bad input"). "Unresponsive" stays undefined until FQ-10 sets a bound.

## Domain Questions

1. **SC-6 / SC-2 (G1):** where does a plan's set of resource nodes come from, and is an unpinned extractor's clock capped at 100%? In particular, does the SC-2 reference plan declare its nodes, or does a first solve name an ore shortfall at one node's ceiling?
2. **SC-6 / SC-9 (G2):** when shards are already placed on a machine, may a rising target push its clock above 100%? And does releasing a shard or Somersloop pin keep the placed items or strip them?
3. **SC-7 (G3):** precedence when a file is in more than one class, and the verdict for a plan from a newer factor than the one running. Reject with a named error?
4. **SC-7 (G3):** does opening an old-version plan rewrite the file in place?
5. **SC-8 (G5):** is "lose at most the last edit" the incomplete, in-flight edit only, so that every displayed edit survives a process crash?

[SPEC-DEFERRED]: nothing above prescribes a fixture, seam or sample count. FQ-10 additions suggested: a backend-readable completed-edit signal and an observable sync record (F7, F8), and load and first-solve time bounds (G7).
