# Glitch review, round 1: docs/intent/factor.md (Intake, product altitude)

Lens: testability of SC-1..SC-5, external observability, ability to fail for the right reason, conflicts with NG/HC.
Read: brief; docs/decisions.md D-008, D-022 (grepped for 80/min, 8/9, 5,000, 100 ms, megabase).

## Findings

### F1 (high) SC-3: the 100 ms measurement is under-specified on every axis
Anchor: SC-3.
- "from the edit to the updated view": the end point is undefined. Solve returned? Diagram data model updated? Frame presented? HC-6 makes the view replaceable and the UI toolkit is open (D-036), so "updated view" has no stable observable.
- Statistic undefined: p50, p95, worst-case, or every solve. "A budget test that fails above the target" reads as every sample, which is flaky by construction.
- Hardware undefined. A budget test cannot fail for the right reason on a different machine.
- Edit population undefined. A leaf tweak and a root target change on a 5,000-machine plan are different workloads. Specify the edit mix, or state worst-case edit.
- Warm vs cold undefined. First solve after load and incremental re-solve (D-017) are different numbers. EV-3 measured 666 ms for 300 coupled factories, already 6.6x the budget at smaller scale, so the criterion may be unattainable on the cited evidence.
- Fix: define start (input event accepted) and end (named state, e.g. new solved plan available to the view), statistic and sample count, reference hardware class, edit mix, warm only. Keep the "relax by recorded decision" clause.

### F2 (high) SC-3: pass condition is both aspirational and a hard gate
Anchor: SC-3 title and Peter's quote ("target instant and then move slower if needed").
The quote makes it a target; the body makes it a failing test. A reader cannot tell whether 300 ms is a failure or an expected fallback. State whether 100 ms is a pass gate for the first build or a tracked target, and that the test is intentionally red until a recorded decision relaxes it, if so.

### F3 (high) SC-2: threshold is Puck's reading and the unit and outcomes are undefined
Anchor: SC-2.
- Peter said "i actually don't know". 5,000 is an option label, labelled Puck's reading but placed in the criterion body as the threshold. Confirm at the gate.
- "Machines": whole physical machines or recipe nodes? In a continuous-clock model one node can be N machines (F-016). 5,000 machines could be 200 nodes or 5,000 nodes; solver cost differs by an order of magnitude. State the sizing unit.
- "loads, solves and can be edited": three verbs, no outcome each. Loads from where (SQLite, D-033)? Solves to feasible or optimal? Edited how, and what must be true after? As written, any run that does not crash passes.
- "A generated reference plan": generator unspecified. A synthetic chain is not a megabase (loops, byproducts F-015, multi-factory F-053). State shape (loop density, recipe diversity, fan-out) and that it is deterministic/seeded.
- Memory: Peter's failure mode is running out of memory (PI-1 quote). SC-2 has no memory bound, so a plan that solves using 12 GB passes. Add a bound or state memory is out of scope for the criterion.

### F4 (high) SC-4: "exact", "4 decimal places" and "never overdraw" can conflict; pass condition not stated per case
Anchor: SC-4, D-008, D-022.
- 88.8888% is not 8/9 (88.8888...%). A plan run at the shown clock under-delivers if rounded down (D-008 derivation) or overdraws if rounded to nearest (88.8889). The criterion does not say which wins, nor what shortfall is acceptable. A test author cannot decide whether 88.8889 is a failure.
- Rounding direction is "Puck's derivation, not ruled" in D-008, yet SC-4 depends on it.
- "exact clocks Peter would pick by hand" is a judgement; the check is fixtures, so the criterion is exactly as strong as the fixture set, which is one named fixture plus "for example". Enumerate a minimum set: 2 x 75% (1.5/min from 1/min machines), the 8/9 case, a whole-machine-count boundary, an input exactly at cap, a case where rounding direction flips over/under.
- "values the game accepts": source of truth for acceptance (clock range, shard limits, 4 dp) is per-game data and not named.
- The "80/min-capped iron chain whose clocks are 8/9" fixture is not defined in the brief or in decisions.md (grep for "80" finds nothing relevant; 8/9 appears only in D-008/D-022 prose). Recipe, target and cap are undefined, so the expected 8/9 cannot be reproduced from the spec.

### F5 (high) SC-5: check is a diff, not a behaviour, and can pass vacuously
Anchor: SC-5.
- "no diff to the core model's crate" passes if nothing was added, passes if a game-specific hack goes through an extension point, and fails on an unrelated legitimate core fix in the same change. It measures where code went, not whether the second game plans correctly.
- "plans in factor": no observable outcome. Needs a second-game reference fixture that solves to a known answer through the same entry point as Satisfactory.
- "beyond declared per-game extension points": the list is not in the brief, so any diff is declarable.
- "Factorio (for example)": game unspecified. Games differ materially (modules, beacons, quality; F-036 is only *shape*). A weak second game makes the criterion trivially met. Name the game or the minimum divergences it must exercise.
- Timing: F-135 is *shape* (backend structure only), so nothing in the first build exercises a second game. State when SC-5 is checked, or it is never red.

### F6 (medium) SC-1: no review trigger, no failure definition
Anchor: SC-1.
Honestly labelled non-automatable. It still must be able to fail: "at a review point" names no date or event, and "his real builds" has no minimum (one? all?). Name the trigger (e.g. when the first-build Committed set lands) and what failure records (went back to Modeler, why). SC-1 is the actual goal and SC-2..5 are proxies; say what it means if SC-2..5 pass and SC-1 fails.

### F7 (medium) SC-3 vs SC-4 cost interaction is unstated
Anchor: SC-3, SC-4, HC-4 (D-022).
D-022 re-checks the final answer in exact rationals. If that recheck runs on every re-solve at 5,000 machines, it may consume the 100 ms budget. EV-3 measured float solves only. State whether the exact recheck is inside the SC-3 measurement window. Also SC-3 inherits every SC-2 ambiguity (F3) because it is defined "on the SC-2 reference plan".

### F8 (medium) SC-3's check has no external surface
Anchor: SC-3 "solve time recorded on every solve".
Recording is instrumentation, not a check; nothing reads it. Name an externally observable surface (log line, bench output, exit code) so the budget can be asserted without in-process access. The "updated view" end depends on D-036, which is open.

### F9 (low) Untestable or unexercised constraints
Anchor: NG-4, HC-1.
NG-4 "the interface must explain itself" has no observable outcome. HC-1 "nothing may rule Windows out" has no check (no Windows build or cross-compile criterion), so it reads as covered and is not. No contradictions found between NG-1..6 / HC-1..9 and SC-1..5 beyond F7.

### F10 (low) No criterion covers load-time validation
Anchor: HC-3, RP-1.
RP-1 carries untrusted-file parsing to Frame, but no success criterion has a pass/fail for it; SC-2's "loads" covers only the happy path. Suggest, for Peter's decision: a malformed or truncated data bundle is rejected at load with a named error and no partial plan.

## Domain Questions

1. SC-3: is 100 ms a first-build pass gate, or a tracked target relaxable by recorded decision? (F2)
2. SC-2/SC-3: what is the reference hardware: Peter's current machine, or a stated minimum? (F1)
3. SC-4: when 88.8888% and exact 8/9 disagree, which does the plan honour, and which direction does display rounding go? (F4)
4. SC-2: is "machines" whole physical machines or recipe nodes? (F3)
5. SC-5: which second game, and is the check in the first build or deferred until a second game exists? (F5)

[ARCH-DEFERRED]: none raised; no finding prescribes a framework, harness or runner.
