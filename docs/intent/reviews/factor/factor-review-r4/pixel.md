# Pixel review, round 4: docs/intent/factor.md (product altitude, Intake)

Lens: user-facing requirements, interaction model, accessibility. Layout, visual and toolkit calls are [ARCH-DEFERRED] and not judged.

Range (re-runnable): `docs/intent/factor.md` lines 1-388 read in full; `scratch/factor-review-r3/pixel.md` read in full. Not opened this round: `docs/decisions.md`, `docs/design/*`. No running UI exists; all findings are from reading the brief.

## Round-3 dispositions

- **F1 (stale mark ended before the diagram's numbers were replaced): resolved.** SC-3 "Stale values" is now per displayed value and covers on-screen and assistive technology. New gap in the same clause: see N1.
- **F2 (SC-9 omitted supply cap and external supply): resolved.** The cap is now the pinned extractor clock (F-009 re-described), and SC-9 states targets and external supply are not pins, with the reason (nothing to release back to). The reason holds. No fix-induced problem.
- **F3 (no exit state for a failed or long solve; "visible" is sighted-only): resolved in substance.** SC-3 says factor says so and the stale marks stay, and covers assistive technology for the marks. Residuals, fix-induced: N2.
- **F4 (SC-7 error location): resolved.** "Shown in the app" is stated, with which file and what is wrong. No fix-induced problem.
- **Shard ruling:** checked against SC-6, SC-9 and I-2. Consistent: shortfall fixes use only shards already placed; shard clocks remain a pin kind that Peter sets by hand. No contradiction found.

## Findings

### N1. [low] SC-3 does not say which values are marked stale at the moment of an edit (fix-induced)
- "Until each displayed value is replaced by its new one, it is marked as stale." D-017 recomputes only the part of the graph an edit touches. Read literally, every displayed value could be marked stale on every edit, including the ones the edit cannot change, and then cleared as each is "replaced". On a 2,000-node plan that is a full-screen flicker on each edit and it makes the mark carry no information. The opposite reading (only values downstream of the edit) is the useful one, but it is not stated, and a test written from the outcome could pass either way.
- Recommend one clause: a value is marked stale only if the edit can change it, and a value whose recomputed result is unchanged still clears its mark. Whether "can change" is computed by dependency or by the incremental recompute's own touched set is Spec-stage (FQ-10).
- Anchor: SC-3 (Stale values).

### N2. [low] The failure state has no stated reach to assistive technology, and "its limit" is undefined (fix-induced)
- SC-3 says the stale marks cover assistive technology, but the sentence "factor says so" about a failed or over-limit solve does not say it reaches assistive technology too. A screen-reader user would be told each value is stale and not told why, or that the state is final. One clause fixes it: the failure message is available to assistive technology.
- "Runs past its limit" refers to a solve time limit that is defined nowhere. FQ-10 lists limits for SC-7 rejection and a sync-interval bound, not a solve limit. The user-facing failure state therefore has no trigger a Spec author can derive. Add the solve limit to FQ-10's list.
- Anchor: SC-3; HC-10; FQ-10.

### N3. [low] An edit whose solve failed is not "completed", so SC-8 loses it on a crash (fix-induced, between the SC-3 and SC-8 rewrites)
- SC-8: "A completed edit is one whose new numbers were displayed." SC-3: on a failed solve the stale marks stay. Together: Peter makes an edit, the solve fails, factor tells him so, and the edit is on screen as his input. A crash then reopens without it, even though SC-8's "lose at most the last edit" is technically met. The edit he sees on screen and the edit that survives differ, with no signal.
- This is a product call, not a defect I can settle: either a failed-solve edit is kept (it is his input, and the failure is a named problem he is meant to fix, as in SC-6's shortfalls) or it is dropped and the app says so. Recommend keeping it, since SC-7 and SC-6 already treat un-solvable states as named problems on a stored plan. Needs Peter's ruling or a stated Puck's reading.
- Anchor: SC-8; SC-3.

## Domain Questions

1. **Target size is still unrecorded (carried from rounds 2 and 3).** HC-10 now names contrast-checked tokens and keyboard reachability but no pointer-target size. The canon floor reads 44 px; the UI brief proposed 24 px minimum and 32 px preferred for a pointer-driven desktop app. Does the floor Peter accepted include 44 px, or is 24/32 px the desktop reading? Recommend 24/32 px for the desktop first build and 44 px at the phone layout (F-085), written as a ruling so Gate B has a number to test against.
2. **OS text size (carried from rounds 2 and 3).** Should the first build honour the operating system's text-size setting, with F-079 (themes and display settings) *later*? Recommend yes in the sense that nothing breaks when text grows; a user-chosen scale stays *later*. HC-7's Chinese, Japanese and Hindi scripts make this matter.
3. **Failed-solve edits (N3).** Is an edit whose solve failed kept in the stored plan? Recommend yes.
