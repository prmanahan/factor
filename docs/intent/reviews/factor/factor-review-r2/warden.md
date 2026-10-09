# Warden review: factor product brief, Intake round 2

**Mode:** review mode first (ambiguity, scope gaps, missing requirements, contradictions). Then security mode, a discovery-stage read using the `security-implications-checklist` skill.
**Artifact:** `docs/intent/factor.md` @ `8de9127` (worktree `3931-product-brief`).
**Verdict:** Request changes. There is 1 blocker, a fix-induced variant of WR-01, and 1 high, fix-induced from WR-03.

## What this review checked

- **Round-1 findings.** Each of WR-01 to WR-12 (`scratch/factor-review-r1/warden.md`) was read against the brief @ `8de9127` and against `git diff 96ab1bb..HEAD -- docs/decisions.md`. That diff covers D-008, D-016, D-017, D-031 and the new D-037.
- **SC-4 / SC-6 fixture.** I recomputed it from the `docs/design/ui-brief.md` §7 table:
  - The base solve at 7.5 RIP/min gives smelters x3 at 100%, plate x3, rod x2, screw x3 and RIP x2, all at 75%.
  - With the cap at 80/min and counts kept, smelters run at 8/9 and every downstream machine at 75% × 8/9 = 2/3. That matches SC-4 and SC-6.
  - Fewest buildings would give plate x2 at 100%, so the SC-6 check can fail on regression.
- **Display rounding in the design source.** I grepped `[0-9]{2}\.[0-9]{4}%` over `docs/design/` and got 8 hits, all `88.8888%`: 7 in `ui-brief.md` and 1 in `mockups/handoff-round1/README.md`. None show `88.8889%`.
- **NG-5's "carried to D-026".** I grepped `docs/decisions.md` for `remote|latent|small extract|NG-5`.
  - The only hit is D-004's outcome line, which also served as the positive control for the instrument.
  - D-026's block (lines 343–356) was read in full. It does not mention the extract conflict.
- **D-012, D-026 and D-036** were read for SC-2's node-count dependency and for WTB-7.
- **Not checked.** Peter's round-1 to round-3 answers quoted in the brief, including the exact option text of "Whole game, scaled up". Their only source is the review conversation, which this context cannot see. They are inherited as quoted.
- **Mechanism choices** stay `[ARCH-DEFERRED]`.

## Round-1 dispositions

| ID | Disposition | One line |
|---|---|---|
| WR-01 | **Partly resolved** | The SC-3 half is resolved: edits land on the largest connected part. The SC-2 half is not: see W2-01, a fix-induced variant. |
| WR-02 | **Resolved**, by narrowing | The check and the claim now cover the same span, edit to numbers, with an external instrument. Fix-induced cost: the diagram redraw is now unbounded (W2-06). |
| WR-03 | **Resolved** | SC-6 puts the stability question to Peter. The fixture is recomputed correctly under counts-kept and labelled as not hand-planned. Fix-induced: W2-02 (count increase) and W2-05 (rounding). |
| WR-04 | **Partly resolved** | RP-1 now lists six input classes. Still missing: F-130 and F-136, and any statement of which inputs the first build trusts by assumption. Its pointer to the WTB list is mislabelled and cites `scratch/` (W2-12). |
| WR-05 | **Partly resolved** | The trigger is now keyed on the attribute and lists the known features. Nothing names what fires it (W2-08). |
| WR-06 | **Resolved for Intake** | HC-7 requires tests over at least two owner ids. The import-owner rule (Q-F4) belongs in Frame, because foreign plan files are out of the first build (RP-1). |
| WR-07 | **Resolved** | The qualifier is restored. Q-F3 at Frame is acceptable, because it presupposes D-032's unruled interface form. But joining D-031's list is a product call of the same kind as HC-10, so Frame must route the answer back to Peter, not rule it. |
| WR-08 | **Partly resolved** | NG-5 is re-scoped correctly to D-019's icon outcome. The D-004 conflict is "carried to D-026", but D-026 does not hold it (W2-07, fix-induced). |
| WR-09 | **Resolved** as SC-8 | Fix-induced: the check does not cover "or the Mac crashes" (W2-03). |
| WR-10 | **Resolved** | "Declared" is now anchored in time, D-029 has been added to HC-9, and the check no longer presumes a crate. Fix-induced: the new "recorded decision" sentence reopens a criterion-versus-check gap (W2-09). |
| WR-11 | **Resolved in SC-1** | The trigger is named. Fix-induced: the new Glossary entry makes SC-1 circular (W2-04). |
| WR-12 | **Resolved** | D-017 now records F-002 as *later* in round 1 and *skip* in round 2. |

---

## Findings

Severity follows the dispatch scale. Confidence (0–100) measures how sure I am that the finding is real. "Fix-induced" means the finding was introduced or reshaped by a round-1 fix, and the prior finding it came from is cited.

### Blocker

**W2-01: SC-2 still does not stress the dimension that scales, and its new memory clause is near-vacuous.** Fix-induced variant of WR-01. Confidence 80.
- **Anchor:** Success criteria, SC-2, and the SC-3 sub-bullet "Not a contradiction with EV-3".
- **What the brief now says.** The reference plan uses all 291 machine recipes, "scaled to at least 5,000 machines". SC-3's sub-bullet states that "5,000 machines do not enlarge the solve". By the brief's own account, then, the scale threshold Peter chose stresses neither the solver nor SC-3: the solve is the 0.9 ms whole-game case from EV-3.
- **The unlabelled reading.** "Whole game, scaled up" is read as *more machines per recipe*. The other reading is *more copies*: more factories (F-053 *mvp*) and nested sub-plans (F-054 *mvp*) linked by import and export (F-052 *mvp*), with recipes repeated across them.
  - The second reading is what a real megabase looks like, and it is EV-3's 300-coupled-copies case at about 666 ms. That case would test SC-3's 100 ms.
  - Round 1 labelled the machine reading as **Puck's reading**. The label is gone, but the inference is still an inference.
- **The memory clause.** "Under 1 GB with the plan loaded, solved and edited" is keyed on machines. A machine count is an integer on a node, so 5,000 machines cost almost no memory.
  - What costs memory is diagram nodes and factories. SC-2 sets no floor on either.
  - How many diagram nodes 5,000 machines produce turns on D-012, which is **open** ("one diagram node may stand for many machines"). The answer could be about 291 nodes or about 5,000.
  - So the memory check cannot fail for the reason Peter gave ("it looks like it runs out of memory").
- **A knock-on.** D-036's spike sizes its gate at 500 and 2,000 nodes. SC-2 is the number it should be sized from, and SC-2 supplies none.
- **Why blocker.** Under the machine reading, SC-2's solve, edit and memory verbs can all pass whatever factor's megabase behaviour is. Downstream tests inherit that hole.
- **Proposed clarification.**
  - Put W2Q-1 to Peter.
  - Then state a floor, in the attributes that scale, for the diagram nodes and factories in the reference plan. EV-3's coupled-copies shape is the evidence-backed candidate.
  - If Peter confirms the machine reading, label it his ruling, and state plainly that SC-2 does not test multi-factory scale.

### High

**W2-02: SC-6 "keep counts, re-clock" has no rule for when the kept count cannot carry the new rate.** Fix-induced from WR-03. Confidence 85.
- **Anchor:** SC-6, and SC-4's "Machine counts come from D-016 … and SC-6". D-016 is refined to match.
- **The gap.** SC-6 is unconditional: "existing machine counts stay as they are and only their clocks change." A target *increase* breaks it.
  - Doubling RIP to 15/min with counts kept puts the smelters at 200%. That needs power shards (F-031 and F-032, both *mvp*, with a shard budget) and changes power along the curve (D-007).
  - Above 2.5× the rate is impossible at any clock the game accepts (D-008).
  - The check covers only the decrease direction, a cap cut, so it cannot catch the gap.
- **Unaddressed in the same family.** Nodes that an edit creates, such as a recipe swap (F-025) or an alternate toggle (F-019), have no existing count.
- **Why high.** This is mvp behaviour on every target edit. As written, the plan either overclocks silently and spends shards Peter may not have, or it violates SC-4 or SC-6.
- **Proposed clarification.** Ask Peter which of these applies when a kept count would exceed 100% (or the shard budget):
  - add the fewest machines needed;
  - name it as a problem and propose re-minimising;
  - overclock only within the shard budget.

  State that new nodes start at fewest buildings. Add an increase-direction fixture.

### Medium

**W2-03: SC-8's check does not cover its claim.** Fix-induced from WR-09. Confidence 85.
- **Anchor:** SC-8.
- **The mismatch.** The claim is "if factor **or the Mac** crashes … the plan file is never left corrupted". The check is "kill the process at random points".
  - A process kill leaves the OS page cache intact, so it never exercises unflushed writes. Those are exactly what an OS crash or power loss loses or tears.
  - So the check can stay green while the Mac-crash half of the claim fails.
- **Proposed clarification.** Either widen the check with a power-loss or unflushed-write simulation (mechanism `[ARCH-DEFERRED]`), or narrow the claim to a process crash and record the OS-crash half as unverified.

**W2-04: The Glossary's "First build" makes SC-1 circular.** Fix-induced from WR-11. Confidence 80.
- **Anchor:** Glossary, "First build", and SC-1.
- **The circle.** The Glossary defines first build as "the first release Peter uses for real play". SC-1 asks, at the first-build release, whether Peter has stopped using Modeler for real builds.
  - Under the Glossary definition, a release Peter does not use for real play is not the first build. So the check point arrives only after the criterion is met, and a "no" cannot be returned.
  - SC-1's own trigger, "every Committed entry marked first build has landed", is the right one.
- **Proposed clarification.** Make the Glossary define first build by the register set, matching SC-1, not by Peter's use.

**W2-05: SC-4's rounding paragraph states an inference as Peter's acceptance, and the fixture's source still truncates.** Fix-induced from the round-3 D-008 ruling. Confidence 85.
- **Anchor:** SC-4; `docs/design/ui-brief.md` lines 56, 98, 241 and 302; `docs/design/mockups/handoff-round1/README.md` line 51.
- **(a) The heading and the body disagree.** The heading sentence says clocks are "shown … and never overdraw". The body then says shown values can overdraw by up to 0.00005 percentage points.
  - "Which Peter's ruling accepts" is Puck's inference. Peter ruled on display rounding; the quote does not mention overdraw.
  - EV-5 matters here: Peter types what he reads into the game, so the *displayed* value is the one that gets built.
- **(b) The design source contradicts the ruling.** The worked example SC-4 cites (ui-brief §7), and the display spec in §2, still show `88.8888%`. D-037 makes the repo the design source. A fixture author or view implementer following §7 will produce the truncated string, which D-008 now supersedes.
- **(c) An open conflict in Peter's own words.** His 2026-10-05 example "88.8888" is what *truncation* gives for 8/9. His round-3 statement is that the game rounds to nearest, which would show 88.8889. See W2Q-2.
- **Proposed clarification.** Label the overdraw acceptance as Puck's reading, or put it to Peter. Fix the heading sentence to say "the exact plan never overdraws". Route the ui-brief and mockup strings to the design work, as Pixel F6 was routed.

**W2-06: The diagram redraw after an edit has no bound at all.** Fix-induced from WR-02. Confidence 80.
- **Anchor:** SC-3, "The diagram redraw may follow a moment later and is not inside the 100 ms".
- **The gap.** Narrowing SC-3 fixed the key mismatch, but "a moment later" has no number. No other SC bounds view responsiveness. D-036's p95 ≤ 16.7 ms frame-time gate is a proposal, measured on a seeded 500-node plan, not the SC-2 plan.
  - Auto-layout (F-069 *mvp*) at megabase scale can take seconds, and SC-3 would still pass.
  - Modeler's failure is the one Peter named, and it was experienced through the view.
- **Proposed clarification.** Either give the redraw its own looser bound on the SC-2 plan, or record it as deliberately unbounded, Peter's call, with a named firing condition. See W2Q-3.

**W2-07: NG-5's "carried to D-026" did not land, and its trip-wire cannot fire.** Fix-induced from WR-08. Confidence 90.
- **Anchor:** NG-5, last sentence; `docs/decisions.md` D-026 and D-004.
- **The missing carry.** NG-5 says the D-004 extract conflict "is carried to D-026". D-026 contains no such text, and neither does any other block. The grep is recorded above, with its positive control. D-004's outcome, "commit a small extract", stands unqualified.
- **The trip-wire.** "Once the repo has a public remote" is the event that makes it live. Nothing watches for a remote being added. D-019 notes that visibility is "public by default", which makes this matter before the first push.
- **Proposed clarification.** Write the conflict into D-026, or as a qualifier on D-004, quoting the open question. Then either name a mechanism that fires on adding a public remote or label the item *parked*, with a cadence.

**W2-08 [security]: RP-3's re-trigger, and every other first-share gate, has nothing that fires it.** Partial resolution of WR-05. Confidence 80.
- **Anchor:** RP-3; also HC-10, RP-1 (the last item), RP-4 and NG-5.
- **RP-3.** The re-trigger is now keyed on network, credential or external-model reach, which fixes round 1's attribute complaint. But "enters a slice's scope" names no reader. Nothing says the feature-level `/brief` for F-118 or F-119 reads RP-3, and that dispatch is the lead's to make.
- **The wider pattern, newly visible.** The brief now has five gates hanging on two or three external events, and none of them carries a mechanism:
  - HC-10: the accessibility floor on first share;
  - RP-1: a foreign plan file becomes a boundary "when sharing starts";
  - RP-3: the security re-trigger;
  - RP-4: legal items gate a public release;
  - NG-5: the public remote.

  The events are first use by another person, a public remote, and a public release. Each gate reads as handled and none will fire.
- **Proposed clarification.** One named gate list in the brief (for example "First-share gate: HC-10, RP-1, RP-3, RP-4, NG-5"), plus one firing mechanism or an explicit *parked* label with a cadence. The mechanism is `[ARCH-DEFERRED]`.

**W2-09: SC-5's new "recorded decision" sentence reopens the criterion-versus-check gap.** Fix-induced variant of WR-10. Confidence 80.
- **Anchor:** SC-5.
- **The gap.** The criterion now says "Any other core change is a recorded decision, so it can't land silently". The check still says the diff "touches only declared extension points".
  - Read as permission, the sentence lets a full core rewrite pass SC-5 once a decision is recorded. That is a vacuous-pass hole in a criterion titled "without a core rewrite".
  - Read as SC-3's relaxation clause, it is fine, but the text does not say which reading is meant.
- **Proposed clarification.** "Any other core change fails SC-5. Proceeding anyway is a recorded decision", mirroring SC-3's "Relaxing the target is a recorded decision".

**W2-10: SC-7's all-or-nothing rule has no answer for a plan that predates the current game data or plan schema.** Fix-induced, from round 1's fail-closed recommendation. Confidence 80.
- **Anchor:** SC-7, "never loaded silently or partly"; F-030 Game version switcher (*shape*); D-003's rejection reason ("every patch").
- **The problem.** Game data updates are routine. A patch that renames or removes a recipe leaves Peter's saved plans referencing something the current data lacks. Read literally, SC-7 rejects those plans outright: loading with a flagged missing recipe is "partly".
  - The same question applies to an older plan schema (D-033, documented schema), where migration is not mentioned.
  - Either SC-7 makes Peter's plans unopenable after a patch, which undercuts SC-1, or "invalid" means structural invalidity only. The brief does not say which.
- **Proposed clarification.** Split SC-7:
  - structurally malformed or hostile input is rejected;
  - a plan that is well formed but stale against the current data or schema is opened, migrated or flagged, per Peter's choice.

  Name the stale case as a requirement.

**W2-11 [security]: SC-7 bounds the error message but not the failure mode.** Partial take-up of round 1's add-to-v1 recommendation. Confidence 80.
- **Anchor:** SC-7 and RP-1.
- **What is missing.** SC-7 makes rejection observable with a named error. It does not require that malformed or hostile input never crashes or hangs the app and stays within bounded memory and time.
  - The parsers this touches include a hand-written Unreal text parser (WTB-1), bundled native SQLite (WTB-3) and Oodle (WTB-4).
  - The check, "seeded malformed fixtures", covers only the malformations its author thought of.
  - The threat class is CWE-400 and CWE-20 (resource exhaustion, improper input validation).
- **Proposed clarification.** Add "never crashes, hangs, or exceeds a stated memory bound on any input" to SC-7. A fuzzing-style check is a candidate, `[ARCH-DEFERRED]`.

### Low

**W2-12 [security]: RP-1's residue.** Partial resolution of WR-04. Confidence 85.
- **Anchor:** RP-1, last line.
- **Three problems.**
  - (a) The brief says "Warden's appendix lists these as WTB-1 to WTB-8". It doesn't: WTB-6 (native FFI: HiGHS and SQLite), WTB-7 (the view-to-backend boundary and webview rendering) and WTB-8 (external callers) are not file inputs. They appear nowhere in the brief except through this pointer.
  - (b) The pointer targets `scratch/`, so a durable, agent-primary brief depends on a scratch file surviving.
  - (c) F-130 (another tool's export format) and F-136 (custom game data) are still unlisted, and RP-1 does not say which inputs the first build trusts by assumption ("Peter's own install and generator").
- **Proposed clarification.** Carry the boundary list inline in the Risk profile, or as a Frame-carried item, with its own IDs. Add the two features and the trust assumption.

**W2-13: HC-7's Tenancy bullet is inline, not a list item.** Confidence 90.
- **Anchor:** HC-7, "…not the full list. - **Tenancy:** …".
- **The problem.** The Tenancy bullet sits inside HC-7's paragraph, so the Globalisation and Accessibility sub-bullets attach to the wrong parent. A parser reading this agent-primary document will mis-nest it.

### Nit

- **SC and HC ids out of order** (confidence 90). SC-9 sits before SC-8 and SC-7, and HC-10 before HC-9. The IDs are stable, so this is reading order only.
- **SC-4 fixture wording** (confidence 85). "Smelters go to 3 at 8/9": they are already 3. Better: "Smelters stay at 3 and run at 8/9".

---

## Suppressed findings (confidence < 80)

Counts only.

| Severity | Found | Suppressed |
|---|---|---|
| Blocker | 1 | 0 |
| High | 1 | 0 |
| Medium | 10 | 1 |
| Low | 5 | 3 |
| Nit | 2 | 0 |

- **The suppressed medium (70).** When Peter releases a count pin (SC-9), it is unclear what "factor's choice" means: the SC-6 kept count or fewest buildings.
- **The suppressed lows.**
  - "Peter's Mac" is not a re-runnable test environment, because no model is named (60).
  - SC-8's "the edit in progress" is stricter than Peter's option label, "lose at most the last edit" (60).
  - Q-F3's tier: noted in the WR-07 disposition instead (60).

---

## Security Implications (Warden, discovery stage)

**Trigger surfaces detected:**
- Multi-tenancy: shaped, not built.
- Network and auth: none in the first build, with *shape* hooks F-118 and F-119.
- PII: latent. It is lower than in round 1, because foreign plan files are out of the first build.
- Untrusted file parsing: carried because RP-1 names it; it is outside the checklist's four triggers.

### Surface assessments

#### Multi-tenancy
- **What's in scope.** An owner/workspace id on every stored plan, with tests exercising at least two ids (HC-7, D-031). There is one tenant value and no cross-tenant or admin operation.
- **Silent gaps in requirements.**
  - The owner id on import goes to Frame (Q-F4), which is acceptable.
  - Still unaddressed: nothing requires the owner id to be opaque, rather than derived from the OS username or machine. It lands in the persisted format, so it is hard to change once plan files circulate.
- **Severity:** low. The round-1 isolation gap is closed.

#### Network and auth
- **What's in scope.** Nothing in the first build (D-030). F-118 and F-119 are *shape*. F-083, F-112 and F-134 are *skip* (Idea tier).
- **Silent gaps in requirements.** The re-trigger has no firing mechanism (W2-08). Whether F-119 is local or hosted goes to Frame (Q-F2).
- **Severity:** medium.
- **Uncovered lens.** F-118 and F-119 are AI/LLM surfaces. RP-3 now names the gap, which is correct. No lens for them ships in this plugin.

#### PII and sensitive data
- **What's in scope.** None while plan files stay on Peter's machine (RP-1).
- **Latent carriers on first share:** the owner id, local install or save paths, F-067 notes, and SQLite free-page residue.
- **Silent gaps in requirements.** Nothing says what a plan file may carry when it leaves the machine. This belongs on the first-share gate list (W2-08).
- **Severity:** low.

#### Untrusted file parsing
- **What's in scope.** RP-1's six classes. Own plan files are validated on open (SC-7).
- **Silent gaps in requirements.**
  - No crash, hang or resource bound (W2-11).
  - Two input classes are missing, and the trust assumption is unstated (W2-12).
  - Stale-but-valid plans (W2-10).
- **Severity:** medium. It was high in round 1; SC-7 now closes the observability half.

### Scope-level recommendations

- **Defer to v2:** unchanged from round 1. F-118 and F-119 stay at *shape*, and foreign plan files stay out of the first build. Peter has now ruled the second (RP-1).
- **Add to v1:**
  - The crash, hang and memory bound on all loading (W2-11).
  - An opaque owner id.
  - One first-share gate list (W2-08).
- **Out-of-scope dependencies to state:**
  - The first build trusts Peter's own install and his own generator output (W2-12).
  - FModel, CUE4Parse and Oodle are third-party dependencies.
  - Release distribution integrity (code signing, notarisation, any update channel) still has no catalogue row. RP-4 gates public release on legal items only.

### Items for Architecture Threat Modeling

Round 1's WTB-1 to WTB-8 stand, with these deltas. The brief should carry them inline (W2-12) rather than through this scratch file.

- **WTB-3 (plan file into the app):** foreign plan files are out of the first build. Own plan files still cross bundled native SQLite on open, and through schema migration (W2-10).
- **WTB-7 (view to backend):** the risk is lower for the first build, because D-036's shortlist is native-only (egui, GPUI, Slint) and Tauri is a comparison arm only. It stays live for the Tauri arm and for D-032's future web view, where game, mod and note strings render in HTML and the IPC bridge exposes backend commands.
- **New, WTB-9 (crash consistency of the plan store):** SC-8's mechanism (journaling, fsync discipline) is an integrity boundary between the app and the OS. It needs the OS-crash case, not only a process kill (W2-03).
- **Quality attributes:**
  - Integrity is high: exact plans (SC-4), crash-safe plans (SC-8).
  - Availability is high: SC-2 and SC-3 scale, and hostile input must not crash or hang the app (W2-11).
  - Confidentiality is low in the first build and rises at first share.

### Security Scan
- **Dependency audit:** not applicable at Intake. There is no code and no manifest, and none was run.
- **Dangerous patterns:** not applicable at Intake. There is no code.

---

## Domain Questions

| ID | Domain area | Question | What I can't see from the doc |
|---|---|---|---|
| W2Q-1 | Scale | Does "Whole game, scaled up" mean more machines per recipe, or more factories and copies of chains, as in a real megabase? | The option text is not in the brief. The machine reading leaves SC-2 and SC-3 testing only a 0.9 ms solve (W2-01). |
| W2Q-2 | Clock display | For a clock of 8/9, does the game's own UI show 88.8888% or 88.8889%? | Peter's 2026-10-05 example shows truncation, while his round-3 statement says the game rounds to nearest. The display spec, SC-4 and ui-brief §7 depend on which is true (W2-05). |
| W2Q-3 | View responsiveness | Is an unbounded diagram redraw after an edit acceptable, or should it have its own looser target on the SC-2 plan? | Peter chose "Numbers under 100 ms", but nothing says whether excluding the redraw meant "unbounded" (W2-06). |
| W2Q-4 | Re-clocking | When an increased target would push a kept machine count past 100%, or past the shard budget, what should factor do? | SC-6 covers only the decrease case (W2-02). |
