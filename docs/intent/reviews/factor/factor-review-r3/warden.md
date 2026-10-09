# Warden review: factor product brief, Intake round 3

**Mode:** review mode first (ambiguity, scope gaps, contradictions, and whether each check can fail for the right reason). Then security mode: a discovery-stage read using the `security-implications-checklist` skill.
**Artifact:** `docs/intent/factor.md` @ `93d6c53` (worktree `3931-product-brief`).
**Verdict:** Approve with conditions. **No blocker or high this round.** There are 6 mediums and 1 low. Five mediums are fix-induced (W3-01 to W3-04 and W3-06), and W3-05 is a partial resolution of W2-11.

## What this review checked

- **Round-2 findings.** Each of W2-01 to W2-13, the two nits and the suppressed medium was read against the brief @ `93d6c53`, against `git diff 8de9127..HEAD -- docs/intent/factor.md`, and against `git diff 8de9127..HEAD -- docs/decisions.md`. The decisions diff touches D-018, D-016, D-022 and D-026. D-008's current block was read in full (lines 77–86).
- **SC-4 fixture, recomputed** from the `docs/design/ui-brief.md` §7 recipes at lines 227–237. The per-machine base rates are: smelter 30 ingot/min, plate constructor 20/min, rod constructor 15/min, screw constructor 40/min, and RIP assembler 5/min.
  - Miner at 2/3 gives 80 ore/min. Smelters stay ×3 at 8/9.
  - Ingot splits 3:1 into 60 for plate and 20 for rod. That gives 40 plate/min and 20/3 RIP/min.
  - The shortfall is 5/6. Every downstream machine runs at 2/3. **This matches SC-4.**
- **SC-6 increase fixture, recomputed** at 10 RIP/min. Assemblers are 2 at 100%, plate 3 at 100%, screw 3 at 100% and rod 2 at 100%. Ingot demand is 90 + 30 = 120/min, which needs 4 smelters at 100%.
  - So exactly one machine is added (smelters 3→4), and every node lands at exactly 100%.
  - At 9/min, every node runs at 9/10 and smelters go to 4.
- **Remote.** `git -C <worktree> remote -v` returned nothing, so there is no remote today. There is no positive control for this instrument, so the result is consistent with NG-5's "no remote today" claim but does not independently prove it.
- **Grep `opaque` over the brief: 0 hits.** The control is `owner` over the same file, which returns 4 matching lines.
- **D-019's** "public by default … before the first push" was read at `docs/decisions.md:321`.
- **Not checked.** Peter's round-4 and round-5 answers are inherited as quoted, because their only source is the review conversation.
- **Mechanism choices** stay `[ARCH-DEFERRED]`.

## Round-2 dispositions

| ID | Disposition | One line |
|---|---|---|
| W2-01 | **Resolved for node scale** | SC-2 now floors recipe nodes at 2,000 in one connected plan, by Peter's round-4 "Nodes + machines". That matches D-036's 2,000-node gate, and the memory bound covers all processes. **Not resolved:** multi-factory scale (F-053 and F-054 are *mvp*) is neither floored nor declared out of SC-2, and "one connected plan" is unlabelled. Whether factories were in Peter's round-4 option set isn't visible here. Below threshold for a new finding (confidence 70); the fix is one sentence saying whether SC-2 tests multi-factory scale. |
| W2-02 | **Resolved** by ruling ("Add machines") | Fix-induced: the increase check under-asserts. See W3-06(b). |
| W2-03 | **Resolved** in the claim, which is now split into a process crash and a power loss with a sync interval | Fix-induced: the power-loss check does not assert the "at most" bound. See W3-06(c). |
| W2-04 | **Resolved** | The Glossary defines first build by its register content. |
| W2-05 | **Resolved** | (a) The heading now reads "The exact plan never overdraws", and Peter ruled on overdraw ("Say nothing"). (b) The 88.8888% strings are declared non-governing and routed to #3933. (c) W2Q-2 is **closed, not re-asked**: Peter's round-3 statement that the game rounds to nearest governs. His 2026-10-05 "88.8888" stays only as verbatim history in PI-1 and D-008. |
| W2-06 | **Resolved** in the criterion (redraw within 1 s, stale numbers marked) | Fix-induced: SC-3's check covers neither. See W3-06(a). |
| W2-07 | **Resolved** for the carry | D-026 now holds the D-004 extract conflict. Fix-induced: its stated firing event does not match the event that makes it live. See W3-02. |
| W2-08 | **Resolved** in form | HC-11 is one named gate, and FQ-8 carries its mechanism to Frame. That is a valid deferral at Intake, because Frame reads the FQ list. Fix-induced: two members are keyed on other events (W3-02), and two obligations are missing from the list (W3-03). |
| W2-09 | **Resolved** | "Any other core change fails SC-5 for that game." |
| W2-10 | **Partly resolved** | The game-update case is ruled ("Open and name what's gone"). Still open: SC-7's check contradicts the ruling, and a plan from an older factor schema is not addressed. See W3-01. |
| W2-11 | **Partly resolved** | The no-crash, no-hang and memory clauses are added, but no bound is stated, so "without bound" cannot fail a test. See W3-05. |
| W2-12 | **Resolved** | F-130 and F-136 are listed and the trust assumption is stated. The non-file boundaries are carried inline as FQ-9, with no `scratch/` pointer. |
| W2-13 | **Resolved** | HC-7's sub-bullets now nest correctly. |
| Nits (ordering; "smelters stay ×3") | **Resolved** | |
| Suppressed medium (count-pin release) | **Resolved** | SC-9: "Re-minimise that node". |

---

## Findings

"Fix-induced" means the finding was introduced or reshaped by a round-2 fix; the prior finding is cited.

### Blocker

None.

### High

None.

### Medium

**W3-01: SC-7's check rejects what its criterion says opens, and factor's own schema changes are unaddressed.** Fix-induced from W2-10. Confidence 85.
- **Anchor:** SC-7: the "A valid plan that refers to recipes or items a game update removed or renamed opens" sub-bullet, and the *Check* line's fixture "a missing reference".
- **(a) The contradiction.** A plan that refers to a recipe the current game data lacks *is* a missing reference.
  - The check says that fixture is "rejected with its named error and leaving no partial plan". Peter's round-5 ruling says it opens, with named problems.
  - A test author working from the check alone builds a test for "Refuse to open", which is the option Peter rejected.
- **(b) The other half of W2-10 is still open.** A plan written by an older factor (D-033's documented schema, HC-8) is not addressed.
  - Read literally, it is "invalid" against the current schema and is rejected whole. Peter's plans would then become unopenable on a factor upgrade, which undercuts SC-1 the same way the game-update case would have.
- **Proposed clarification.**
  - Split the fixtures into two kinds. A dangling reference *inside* the file (an edge to a node that does not exist) is rejected. A reference to game data the current data lacks opens, with named problems.
  - Add an opens-with-named-problems fixture to the check.
  - Put the older-schema case to Peter (W3Q-3). It is the same kind of question as the game-update one he already answered.

**W3-02 [security]: HC-11's single trigger does not match the events of two of its own members.** Fix-induced from W2-07 and W2-08. Confidence 85.
- **Anchor:** HC-11 ("Several obligations wait for the first time factor is used by anyone other than Peter"); NG-5; RP-3; `docs/decisions.md` D-026 ("The first-share gate (product brief HC-11, FQ-8) is what fires this"); D-019 at line 321.
- **(a) NG-5 and D-026.** What turns D-004's committed extract into redistribution is a **public remote or push**, not another person using factor.
  - The repo can go public before anyone else runs factor. D-019 says visibility is "public by default", and that this matters "before the first push".
  - D-026 now says HC-11 fires it, but HC-11's event comes later than the one that matters, or never comes at all. The trip-wire is named but keyed on the wrong attribute.
  - **Warden's inference:** RP-4's licence item (D-025, factor's own licence) also becomes live at the push, because a public repo with no licence is a licensing state of its own. D-025's block (lines 337–344) does not say this; it lists only the options.
- **(b) RP-3 contradicts its own listing.**
  - RP-3 says the security review re-triggers when a networked, credentialed or external-model feature "enters a slice's scope, **not only 'sharing'**".
  - HC-11 lists "network-feature security review (RP-3)" among obligations that wait for first share.
  - A reader of HC-11 alone concludes that the review of a local F-119 LLM interface waits until someone else uses factor. That surface has risk even with Peter as the only user: game, mod and note strings flow into a model that can call factor's backend.
- **Proposed clarification.** Make HC-11 name its events, and key each obligation to its event:
  - another person uses factor: HC-10 and RP-1;
  - the repo gets a public remote or first push: NG-5, D-026 and the D-025 licence;
  - a public release: RP-4 and W3-03's items.

  Take RP-3 out of HC-11, or list it with its own slice-scope event. FQ-8's mechanism then has to fire on each event, not on one.

**W3-03 [security]: HC-11's enumeration is missing two first-share obligations.** Fix-induced from W2-08. The list in W2-08 that HC-11 copied omitted them; they sat separately in round 2's scope-level recommendations. Confidence 80.
- **Anchor:** HC-11's list; RP-4; F-129 *File export and import* (*mvp*, first build).
- **What is missing.**
  - **What a plan file carries when it leaves the machine.** That means the owner id, local install or save paths, F-067 free-text notes, and SQLite free-page residue (deleted notes survive in the file until it is vacuumed). F-129 export is *first build*, so a file can leave the machine before any other-user event. This is a data-minimisation question, not only a confidentiality one.
  - **Release distribution integrity.** That means code signing, macOS notarisation, and the integrity of any update channel. RP-4 gates a public release on legal items only.
- **Why it matters.** HC-11 is now *the* gate. An obligation left off an enumeration that gates is a silent false-green: the gate fires, passes, and the item never ran.
- **Proposed clarification.** Add both to HC-11, under the event each belongs to (W3-02).

**W3-04 [security]: SC-7's "unknown or foreign owner id" fixture pre-decides FQ-4 and defines no "known".** Fix-induced from W2-11: the fixture arrived with that fix, and touches WR-06's FQ-4. Confidence 80.
- **Anchor:** SC-7's *Check* fixture list; FQ-4; RP-2; HC-7 Tenancy; F-129 (*mvp*).
- **(a) It pre-decides an open question.** FQ-4 (what owner id an imported plan gets) is open at Frame. The check already answers part of it: reject.
- **(b) "Known" is undefined.** If the owner id is per-install or derived from the machine or OS user, Peter's own plans are "unknown" on a new Mac, a reinstall, or Windows later (HC-1). They would then be rejected whole: an availability lockout of his own data.
- **(c) It is not a security control.** A plan file states its own owner id. Rejecting a mismatch authenticates nothing, because anyone who can write the file can write the expected id. Calling it a rejection fixture makes it read as a boundary it is not.
- **Related, and still open from round 2:** the add-to-v1 recommendation of an *opaque* owner id, not derived from the OS username or machine, was neither adopted nor recorded as declined (`opaque`: 0 hits).
- **Proposed clarification.** Drop the owner-id fixture from SC-7 until FQ-4 is answered. State at product level that the owner id is a scoping key, not a credential, and put W3Q-4 to Peter.

**W3-05 [security]: SC-7's "never growing memory without bound" and "never … hanging" cannot fail a test.** Partial resolution of W2-11. Confidence 80.
- **Anchor:** SC-7, the heading sentence and the *Check* line.
- **Calibration: Medium, not Blocker.** The push-back rule calls a criterion clause that cannot fail a blocker, and these two are clauses of SC-7's criterion sentence. But the rest of SC-7 stays checkable: the named error, rejection of the whole file, no crash, and the oversized fixture. Only two clauses are hollow. W2-01 was a blocker because every verb of SC-2 was hollow. The lead may overrule this; if it becomes a blocker, the verdict and the stopping-rule line change with it.
- **The gap.** Any finite test run uses finite memory and finite time, so "without bound" and "hanging" have no threshold a test can cross.
  - The "oversized input" fixture is checkable, but only for the one size its author picks.
  - The check is still "seeded fixtures" only, so it covers just the malformations its author thought of. Parser inputs include a hand-written Unreal text parser, bundled SQLite and Oodle (RP-1).
- **Proposed clarification.**
  - Tie the memory bound to SC-2's 1 GB peak, applied to any rejected input too.
  - Give rejection a time bound, for example "named error within N s on any input" (the number is a Frame call).
  - Record that a generative or fuzz-style check is the candidate mechanism, `[ARCH-DEFERRED]`.

**W3-06: Three newly ruled clauses have proposed checks that pass on a regression of the clause.** Fix-induced from W2-06, W2-02 and W2-03. Confidence 85.
- **Calibration.** Each criterion is well formed, and each check catches *some* regressions. So these are under-asserting checks, not vacuous criteria: Medium, not Blocker. They are grouped because they share one shape, and so need one kind of fix.
- **(a) SC-3, redraw and stale marking.**
  - The check times "from the edit to the updated numbers" only. The 1 s redraw bound and the stale marking are never measured, so a 5 s redraw or an unmarked stale diagram passes.
  - The 1 s has no percentile, unlike the 100 ms at p95.
  - "Until the new numbers land" is ambiguous. The numbers land within 100 ms, so marking stale *numbers* is at most a 100 ms flash. The meaningful case is the diagram's node labels during the up-to-1 s redraw.
  - **Fix:** extend the instrument to time edit-to-redraw, at p95 or as a maximum (Peter's call if it is not obvious). Say which surface carries the stale mark. Assert that the mark is present before the redraw and gone after it.
- **(b) SC-6, the increase fixture.**
  - "Raising the target from 7.5 to 10/min adds machines, with none above 100%" also passes an implementation that adds *more* machines than needed. The ruled clause is "the **fewest** new machines".
  - Recomputed above, the exact answer is: smelters 3→4, every other count unchanged, and every node at exactly 1/1. That is a useful boundary, because it lands at the 100% edge.
  - **Fix:** assert exact counts and exact clock fractions, mirroring SC-4's "Assertions use the exact fractions". Optionally add a non-boundary target: at 9/min, smelters are ×4 and every node runs at 9/10.
- **(c) SC-8, the power-loss check.**
  - "Edits since the last sync may be missing, and the file still passes the integrity check" never asserts that edits *before* the last completed sync are present. So an implementation that never syncs passes, provided the file stays consistent.
  - The ruled claim is "loses **at most** the edits since the last sync".
  - The sync interval is a setting with no stated range. If it can be set to "never", the power-loss half is vacuous by configuration.
  - **Fix:** assert that every edit completed before the last sync survives. Put the setting's range to Peter (W3Q-2).

### Low

**W3-07: The success-criteria source list is stale after rounds 4 and 5.** Confidence 90.
- **Anchor:** "Sources, criterion by criterion".
- **The drift.**
  - It says "rounds 1 to 4", but SC-3 (redraw), SC-7 (stale plans) and SC-8 (sync) quote round-5 answers.
  - The list of criteria carrying Peter's review answers omits SC-4 (round-3 rounding, round-4 "Say nothing") and SC-7 (round 5).
  - SC-7 is attributed only to review findings, though it now carries a ruling of Peter's.
- **Proposed fix:** update the list. Provenance is what tells a cold reader which lines are ruled.

### Nit

None reported.

---

## Suppressed findings (confidence < 80)

Counts only.

| Severity | Found | Suppressed |
|---|---|---|
| Blocker | 0 | 0 |
| High | 0 | 0 |
| Medium | 8 | 2 |
| Low | 4 | 3 |
| Nit | 1 | 1 |

- **Suppressed medium (70).** Multi-factory scale is neither floored nor declared out of SC-2; see the W2-01 disposition.
- **Suppressed medium (65).** SC-2's "composed from fixtures whose answers are known" may not preserve those answers once fixtures share a scarce input under D-023's scarcity-weighted objective. FQ-7 should say how the oracle survives composition.
- **Suppressed lows.**
  - SC-8 makes "completed = numbers displayed" survive a process crash, so the plan *write* (not the sync) must happen before or at display. The brief places only the sync outside SC-3's window, and an asynchronous after-display write would break SC-8 (70).
  - SC-1 says the first build's content is "the parity list against Modeler", while the Glossary defines it by register entries. That gives two definitions, and "parity list" is undefined (70).
  - SC-2's generated plan under D-018 amended needs node purities and inventory, which are not in the Docs data (CLAUDE.md). This is probably answerable by generating Normal nodes only (55).
- **Suppressed nit.** "Per the option Peter chose … (**Puck's reading**)" mixes attribution in one clause in SC-2 (60).

---

## Security Implications (Warden, discovery stage)

**Trigger surfaces detected:**
- Multi-tenancy: shaped, not built.
- Network and auth: none in the first build, with *shape* hooks F-118 and F-119.
- PII and data minimisation: latent, with an exit path in the first build through F-129 export.
- Untrusted file parsing: carried because RP-1 names it; it is outside the checklist's four triggers.

### Surface assessments

#### Multi-tenancy
- **What's in scope.** An owner/workspace id on every stored plan; tests exercise at least two ids (HC-7). One tenant value, and no cross-tenant or admin operation.
- **Silent gaps in requirements.**
  - The SC-7 owner-id fixture treats a scoping key as a credential and pre-decides FQ-4 (W3-04).
  - Whether the owner id is opaque or derived from the machine is still unstated, and that decides whether Peter's plans survive a machine change.
- **Severity:** medium (W3-04).

#### Network and auth
- **What's in scope.** Nothing in the first build (D-030). F-118 and F-119 are *shape*. F-083, F-112 and F-134 are *skip*.
- **Silent gaps in requirements.** RP-3's trigger is contradicted by its HC-11 listing (W3-02b). FQ-2 (local or hosted F-119) stays at Frame.
- **Severity:** medium.
- **Uncovered lens.** F-118 and F-119 are AI/LLM surfaces. RP-3 names the gap correctly. No lens for them ships in this plugin.

#### PII and data minimisation
- **What's in scope.** None while plan files stay on Peter's machine. F-129 export (*first build*) is the first path off it.
- **Silent gaps in requirements.** Nothing says what an exported file may carry: owner id, paths, notes, or free-page residue (W3-03).
- **Severity:** low to medium; it rises at the first export to anyone.

#### Untrusted file parsing
- **What's in scope.** RP-1's classes, now complete, with the first-build trust assumption stated. Own plan files are validated on open (SC-7).
- **Silent gaps in requirements.**
  - The memory and time bounds have no number (W3-05).
  - The stale-plan and malformed-plan line is contradicted by the check, and an older factor schema is unaddressed (W3-01).
- **Severity:** medium.

### Scope-level recommendations

- **Defer to v2:** unchanged. F-118 and F-119 stay at *shape*, and foreign plan files stay out of the first build (RP-1, ruled).
- **Add to v1:**
  - Stated memory and time bounds on all loading (W3-05).
  - An opaque owner id, or Peter's explicit decline of it (W3-04).
  - HC-11 keyed per event and completed (W3-02, W3-03).
- **Out-of-scope dependencies to state:**
  - The first build trusts Peter's own install and generator output. This is now stated.
  - FModel, CUE4Parse and Oodle are third-party dependencies.
  - Release distribution integrity has still no catalogue row; it is proposed for HC-11 in W3-03.

### Items for Architecture Threat Modeling

Round 1's WTB-1 to WTB-8 and round 2's WTB-9 stand. The brief now carries the non-file boundaries inline as FQ-9. The deltas:

- **WTB-9 (crash consistency of the plan store) should join FQ-9 or its own FQ.** SC-8 now has a power-loss half, which is an app-to-OS-to-disk integrity boundary.
  - Warden's platform knowledge, not measured here: on macOS, `fsync()` does not flush the drive's write cache. Durability needs `F_FULLFSYNC`, which SQLite exposes as `PRAGMA fullfsync` and leaves off by default.
  - A simulated "discard unsynced writes" test therefore trusts that the app's notion of "synced" means durable. Frame should check that equivalence; SC-8's power-loss simulation cannot.
- **WTB-10, new (exported plan file as an egress boundary):** F-129 is *first build*, so data leaves the machine before first share (W3-03).
- **WTB-11, new (F-119 local model):** even with Peter as the only user, untrusted strings from game data, mods and notes reach a model that can call the backend. This is pre-share, per RP-3's own trigger (W3-02b). No lens covers it.
- **Quality attributes:**
  - Integrity is high: exact plans (SC-4), and crash and power-loss safe plans (SC-8).
  - Availability is high: SC-2 and SC-3 scale, bad input must not crash or hang (SC-7), and Peter's own plans must stay openable across game and factor updates (W3-01, W3-04).
  - Confidentiality is low in the first build, and rises at the first export or share.

### Security Scan
- **Dependency audit:** not applicable at Intake. There is no code and no manifest, and none was run.
- **Dangerous patterns:** not applicable at Intake. There is no code.

---

## Domain Questions

| ID | Domain area | Question | What I can't see from the doc |
|---|---|---|---|
| W3Q-1 | First-share gate | Is a public remote or first push of the repo its own gate event, separate from another person using factor? | D-019 says it matters "before the first push", but HC-11 keys every obligation on use by another person (W3-02). |
| W3Q-2 | Crash safety | Should the sync interval have a limit, for example no "never" and a maximum interval? | Peter said "allow it to be tuned". If it can be turned off, SC-8's power-loss half holds only by default (W3-06c). |
| W3Q-3 | Plan compatibility | When a newer factor opens a plan saved by an older one, should it open and migrate, open and name what it can't read, or refuse? | SC-7 rules on game updates only. Read literally, an older schema is "invalid" and gets rejected whole (W3-01b). |
| W3Q-4 | Tenancy | Should your plans open on a new Mac, or later on Windows, as yours: one owner id for you, not one per install? | The brief does not say what the owner id is tied to. SC-7 rejects an "unknown" one (W3-04). |

---

## Summary

No blocker or high this round, so Warden's lens contributes no stopping-rule trigger. Five of the six mediums are fix-induced from round-2 fixes, but each is a narrow clarification to a check or a gate list, not a design problem; one more medium-only round should close them. The most consequential is W3-01: SC-7's check would reject exactly the stale plans Peter ruled must open.
