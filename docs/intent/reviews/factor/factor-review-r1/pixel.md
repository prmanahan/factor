# Pixel review, round 1: docs/intent/factor.md (product altitude, Intake)

Lens: user-facing requirements, interaction model, accessibility. Cross-checked against `docs/design/ui-brief.md` (my own brief) and `docs/decisions.md`.
Range read: brief lines 1-251 in full; ui-brief.md in full; decisions.md D-030, D-031, D-032, D-034, D-024, D-023 plus the status index; `docs/design/feature-verdicts.md` rows F-013, F-017, F-059, F-078 to F-087 only (not all 142 rows). Nothing was screenshotted: no UI exists.
Layout, visual design and toolkit calls are tagged [ARCH-DEFERRED] and not judged.

## Findings

### F1. [high] No accessibility requirement anywhere in the brief
- The brief names a shared-later consumer and carries no accessibility constraint. Hard constraints HC-1 to HC-9, the success criteria and the non-goals contain nothing on contrast, keyboard operation, focus, status-not-by-colour or assistive technology. Canon V-Accessibility binds on any surface a human other than its author uses. The Consumer field says sharing "must not be designed out", and a floor that is absent from the intent cannot be checked at Frame or Spec.
- The floor exists only in `ui-brief.md` constraint 13, which is a design input and not the product intent. F-080 (keyboard) is committed as *mvp*, but "every action reachable without a mouse" is not carried into the brief either.
- Recommend one hard constraint with a check, in the brief's own style. Draft: "HC-x Accessibility floor: WCAG 2.1 AA text contrast 4.5:1 and 3:1 for large text and meaningful non-text, full keyboard operation, visible focus distinct from hover, status never by colour alone, no information on hover only. *Check:* measured contrast per token pair at Spec; a keyboard-only walk of the SC-3 edit loop."
- Anchor: Hard constraints; Consumer.

### F2. [medium] Assistive-technology and diagram-access status is silent, and the UI brief is silent too
- Screen-reader exposure of a diagram with thousands of machines is the hard case. The brief neither requires it nor defers it by name. A silent omission is a decision made by default, and global rule DF1 says a deferral must name what fires it.
- My own UI brief is out of line with V-Accessibility here. Constraint 13 covers contrast, keyboard and focus only. It omits assistive-tech semantics, honouring OS text size (F-079 interface scale is *later*), and a `prefers-reduced-motion` behaviour for the dimmed "re-solving" state. That gap is Pixel's, and I will fix it in the UI brief.
- The non-visual equivalent of the diagram is F-071 (configurable step table), currently *shape*, with a reserved tab and no UI. It is the natural accessible alternative to the canvas. HC-6 (replaceable view) means any accessibility tree is a per-view concern, so the view-to-backend data interface (D-032) must expose enough plan data to build a textual view.
- Recommend the brief states one of two things. Either assistive-tech support is in the first build, or it is deferred with a named trigger, such as the first non-Peter user or the D-036 toolkit decision. The toolkit's accessibility-API support is then a D-036 criterion [ARCH-DEFERRED].
- Anchor: Hard constraints; HC-6; F-071.

### F3. [high] SC-3 does not define the "updated view", and its check does not cover its claim
- SC-3 says "from the edit to the updated view", but the check records "solve time" only. The claim spans edit, solve, layout and render. The check covers one of the four. Under the global rule that a check covers its claim, the budget test as written can pass while the user waits.
- User-facing questions the brief must settle:
  1. Does "updated view" mean the changed numbers are on screen, or the diagram is re-laid-out? Layout is separate from solve (D-009), and F-074 keeps dragged positions across recalculation.
  2. Is the 100 ms applied to a single-node edit, to a target change, or to both? D-017 recomputes only the touched part, so the two have very different costs.
  3. What does the user see if a solve exceeds 100 ms? `ui-brief.md` §2 specifies a dimmed previous diagram. That is consistent with SC-3 but unmeasured, and the brief should say whether a re-solving state counts as a pass.
  4. What is on screen at the 5,000-machine scale? Zoomed out, the UI brief shows compact chips. Is the chip view "the updated view"?
- Related evidence: EV-3 measured 300 coupled factories at about 666 ms, which already exceeds 100 ms at far less than the SC-2 scale. The brief states "Relaxing the target is a recorded decision", which is good. It should say whether 100 ms binds the whole plan or the touched part.
- Recommend defining the endpoint as "pixels changed on screen for the edited node and its direct neighbours", with solve and render timed separately. The view's render time depends on D-036 [ARCH-DEFERRED].
- Anchor: SC-3.

### F4. [medium] NG-4 contradicts F-081 inside the brief and omits the demo-plan carve-out
- NG-4 says "No walkthroughs or tutorials". The register commits F-081 "Guided tutorial and demo plans", described as "An interactive tutorial and/or prebuilt example plans", with the release note "eventually, not immediately". D-034 rules against needing a walkthrough and explicitly allows a demo plan.
- The register entry reads as a commitment to the very thing NG-4 forbids, so one of the two is out of line with D-034. NG-4 is the one that matches the ruling. F-081 should be annotated or split: "demo plan" is allowed, "guided tutorial" is not.
- NG-4 should also carry the D-034 carve-out ("a demo plan is fine"), which `ui-brief.md` §3 S10 already uses.
- NG-4 has no check, while every success criterion does. For a shared-later consumer who lacks Peter's domain knowledge, "explains itself" is unverifiable as written. This is a non-goal, so a check is optional, but the gap should be a named open point and not silent.
- Anchor: NG-4; F-081; D-034.

### F5. [medium] "Set by you" versus "set by factor" is a core interaction rule and is missing from HC-5
- HC-5 says "edits to the diagram re-solve". D-024 turns every diagram edit into a constraint. A user who cannot tell which values are their own constraints cannot undo a pin, and one-view editing becomes opaque.
- The visible pin marker plus an unpin control is a Pixel proposal in `ui-brief.md` §2 and §10 item 3. It is unruled. The user-facing requirement (a constraint the user set must be distinguishable from a solved value, and removable) belongs in the brief as intent, and the specific cue stays a proposal. Draft addition to HC-5: "A value the user constrained is distinguishable from a solved value, and can be released."
- Anchor: HC-5; D-024.

### F6. [medium] The UI brief draws a Problems strip while the feature register marks the matching features *shape*
- This is a contradiction, and my UI brief is the one out of line. F-013 (infeasibility diagnostics) and F-059 (plan health warnings) are *shape*, meaning backend structure only in the first build. The UI brief nonetheless designs a Problems strip, markers and named fix actions as R1 screens (S1, S2).
- D-023 rules that the plan "comes back with its problems named, never a bare infeasible", which supports having some user-visible naming. The ruling does not rule a strip, fix buttons, or four problem kinds. F-014 (byproduct) and F-052 (supplier cover) are *mvp*, so two of the four kinds do carry user-facing weight.
- The brief itself is silent on where problems surface to the user in the first build. It carries D-023 only inside HC-4 as an engine formulation. Recommend a user-facing line, for example: "A plan always draws. Shortfall and unhandled byproduct are named to the user with the amount and the limiting cause." Peter should then confirm the strip, or I downgrade the UI brief to a plain list.
- Anchor: HC-4; F-013; F-059; `ui-brief.md` §2 and §10.

### F7. [medium] SC-2 uses machines and the UI brief uses nodes
- SC-2 sets "at least 5,000 machines". `ui-brief.md` constraint 11 sizes legibility at "hundreds of nodes", and a node carries a count such as `x3`. The two figures differ by an unstated factor.
- SC-2 also says "loads, solves and can be edited". It has no user-facing legibility or navigation clause. A plan that exists but cannot be read or located is a pass by that wording. The checkable part is "reference plan as a test", which says nothing about being usable.
- Recommend stating the unit (machines or nodes, with the generator's expected node count) and adding one user-facing clause, for example: "an item or node is findable and the selected node's numbers are readable at this scale". The load-time budget is also unstated, and Peter's complaint was the freeze, so it matters to the user.
- Anchor: SC-2.

### F8. [medium] SC-1 has no parity list, so it cannot fail for a reason the team can act on
- SC-1 is a self-report by design, which is honest. It names no feature the user must have before he can stop using Modeler. Peter said only that Modeler "does have some nice features" and disliked its "factory organisation" and "interface and layout". Those are unnamed.
- Without a parity list, a failed SC-1 review gives no direction. It also leaves open whether SC-1 is gated on D-035 (factory organisation, open), because the factory organisation was his named complaint.
- Recommend one Domain Question to Peter: which Modeler features must exist before he switches?
- Anchor: SC-1; PI-1 quotes.

### F9. [low] SC-4 does not say which way a displayed clock rounds
- "88.8888%" displayed is below the exact 8/9, which is 88.88888…%. A user who types the shown value into the game gets slightly less than the plan. D-008 says clocks are "values the game accepts, to 4 decimal places". The brief's "never overdraw a limited input" implies rounding must not overdraw, but the user-facing rule (round toward not overdrawing, with the exact fraction available) is unstated.
- The fixture "80/min-capped iron chain whose clocks are 8/9" checks the exact value, not the displayed one.
- Anchor: SC-4; D-008; D-022.

### F10. [low] "Shared later" is unbounded as written
- The Consumer field says sharing "must not be designed out" without naming what. User-facing items that follow from D-030, D-031 and D-019, and that the brief could list:
  - Accessibility (F1).
  - Localisation shape (already HC-7).
  - First run on a machine with no game install: NG-5 puts icons and data in Peter's own install, and D-026 is open. The UI brief covers the icon part with neutral icon slots, but not what a non-Peter user sees before data exists.
  - F-129 (file export and import) is *mvp*, so plan files can reach other people in the first build. RP-1 names game data and saves as untrusted input but not plan files from another person. This one is a Warden matter; flagged for the lead, not judged here.
- Anchor: Consumer; NG-5; RP-1.

### Contradiction check (brief vs UI brief)
- NG-2 / D-030 versus UI brief constraint 1 "no sharing UI": consistent.
- HC-6 versus UI brief constraint 8: consistent.
- NG-4 versus UI brief constraint 3 and S10: consistent in intent, but NG-4's wording is stricter than D-034 (F4).
- HC-5 versus UI brief §2: consistent. The pin cue is a proposal only (F5).
- F-079 themes are *later* while the UI brief draws light and dark following the system. The brief is silent. Not a contradiction: the UI brief draws system-follow with no picker. Peter should confirm. Low; not raised as a finding.

## Domain Questions

1. **Accessibility floor.** Does the first build carry WCAG 2.1 AA contrast, full keyboard operation, visible focus and status-not-by-colour as a hard constraint? Recommend yes, as a new HC (F1). Is assistive-tech (screen-reader) support in the first build, or deferred with the trigger "first non-Peter user, or the D-036 decision"? Recommend deferred with that named trigger, and F-071's step table kept as the intended accessible view (F2). Does Peter himself have any accessibility needs (colour vision, text size)?
2. **SC-3 endpoint.** Does "updated view" mean changed numbers on screen for the edited node and its neighbours, or a fully re-laid-out diagram? Recommend the first, with solve and render timed separately (F3). Does 100 ms bind a single-node edit only, or a whole-plan target change too?
3. **NG-4 versus F-081.** Is a demo plan the only part of F-081 that stays, with "guided tutorial" dropped? Recommend yes, to match D-034 (F4).
4. **SC-1.** Which Modeler features must factor have before Peter will stop using Modeler? Is the answer gated on D-035 (F8)?
5. **Problem naming.** Is a visible Problems strip with named fix actions in the first build, given F-013 and F-059 are *shape* and D-023 requires problems named? Recommend yes for shortfall and byproduct only, and I will amend the UI brief to match whichever Peter chooses (F6).
