# /// script
# dependencies = ["highspy", "numpy"]
# ///
"""Satisfactory whole-game LP/MILP timing with HiGHS (via highspy).

Model per copy ("factory"):
  x_r >= 0      machines of recipe r at 100% clock (continuous)
  s_i >= 0      surplus of item i (penalised)
  u_i >= 0      supply of raw resource i (weighted cost)
  row i:  sum_r a_ir x_r + u_i - s_i = demand_i
Coupled scale-up: K copies share one row per raw resource: sum_k u_ik <= cap_i.
MILP variant: n_r integer, x_r - n_r <= 0, small cost on n_r.
"""
import json, re, sys, time, statistics, platform
import numpy as np
import highspy

DATA = sys.argv[1] if len(sys.argv) > 1 else "en.json"
d = json.loads(open(DATA, "rb").read().decode("utf-8-sig"))

MACHINES = {"AssemblerMk1", "ConstructorMk1", "ManufacturerMk1", "OilRefinery", "Converter", "Packager",
            "Blender", "FoundryMk1", "HadronCollider", "SmelterMk1", "QuantumEncoder"}
form, raw = {}, set()
recipes = []
for g in d:
    nat = g["NativeClass"]
    for c in g["Classes"]:
        if "mForm" in c:
            form[c["ClassName"]] = c["mForm"]
        if "FGResourceDescriptor" in nat:
            raw.add(c["ClassName"])
    if "FGRecipe" in nat:
        for c in g["Classes"]:
            prod = set(re.findall(r"\.Build_([A-Za-z0-9]+)_C", c.get("mProducedIn", "")))
            if prod & MACHINES:
                recipes.append(c)

def parse(s):
    return [(m.group(1), float(m.group(2))) for m in re.finditer(r"\.([A-Za-z0-9_]+)'\"?,Amount=([0-9.]+)", s or "")]

def per_min(item, amt, dur):
    scale = 1000.0 if form.get(item) in ("RF_LIQUID", "RF_GAS") else 1.0
    return amt / scale * 60.0 / dur

rows = {}
cols = []  # (name, {item: coef}, is_alt)
for r in recipes:
    dur = float(r["mManufactoringDuration"])
    coef = {}
    for it, a in parse(r["mIngredients"]):
        coef[it] = coef.get(it, 0) - per_min(it, a, dur)
    for it, a in parse(r["mProduct"]):
        coef[it] = coef.get(it, 0) + per_min(it, a, dur)
    for it in coef:
        rows.setdefault(it, len(rows))
    cols.append((r["ClassName"], coef, "Alternate" in r["ClassName"] or r.get("mDisplayName", "").startswith("Alternate")))
items = list(rows)
raw_items = [i for i in items if i in raw]
print(f"recipes(machine)={len(cols)} items={len(items)} raw={len(raw_items)}")

RAW_W = {i: (0.0 if i == "Desc_Water_C" else 1.0) for i in raw_items}
SURPLUS_W = 1e-3
MACHINE_W = 1e-2

def build(targets, copies=1, allow_alt=True, integer=False, raw_cap=None):
    """Return a highspy model. Columns per copy: recipes, surplus, raw-supply, [int machines]."""
    nI, nR = len(items), len(cols)
    use = [k for k, c in enumerate(cols) if allow_alt or not c[2]]
    h = highspy.Highs(); h.setOptionValue("output_flag", False)
    lp = highspy.HighsLp()
    cost, lo, up, integ = [], [], [], []
    starts, idx, val = [0], [], []
    def addcol(c, entries, l=0.0, u=highspy.kHighsInf, isint=False):
        cost.append(c); lo.append(l); up.append(u); integ.append(isint)
        for (ri, v) in entries:
            idx.append(ri); val.append(v)
        starts.append(len(idx))
    nrow_per = nI + (len(use) if integer else 0)
    cap_row0 = copies * nrow_per
    rowlo, rowup = [], []
    for k in range(copies):
        base = k * nrow_per
        for i, it in enumerate(items):
            dem = targets.get(it, 0.0)
            rowlo.append(dem); rowup.append(dem)
        if integer:
            for _ in use:
                rowlo.append(-highspy.kHighsInf); rowup.append(0.0)
        for j, kcol in enumerate(use):
            name, coef, _ = cols[kcol]
            ent = [(base + rows[it], v) for it, v in coef.items()]
            if integer:
                ent.append((base + nI + j, 1.0))
            addcol(0.0, ent)
        for i, it in enumerate(items):
            addcol(SURPLUS_W, [(base + i, -1.0)])
        for r_i, it in enumerate(raw_items):
            ent = [(base + rows[it], 1.0)]
            if raw_cap is not None:
                ent.append((cap_row0 + r_i, 1.0))
            addcol(RAW_W[it], ent)
        if integer:
            for j, _ in enumerate(use):
                addcol(MACHINE_W, [(base + nI + j, -1.0)], isint=True)
    if raw_cap is not None:
        for it in raw_items:
            c = raw_cap.get(it, 1e5 * copies) if isinstance(raw_cap, dict) else raw_cap
            rowlo.append(-highspy.kHighsInf); rowup.append(c)
    lp.num_col_ = len(cost); lp.num_row_ = len(rowlo)
    lp.col_cost_ = np.array(cost); lp.col_lower_ = np.array(lo); lp.col_upper_ = np.array(up)
    lp.row_lower_ = np.array(rowlo); lp.row_upper_ = np.array(rowup)
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = np.array(starts, dtype=np.int32)
    lp.a_matrix_.index_ = np.array(idx, dtype=np.int32)
    lp.a_matrix_.value_ = np.array(val)
    if integer:
        lp.integrality_ = [highspy.HighsVarType.kInteger if b else highspy.HighsVarType.kContinuous for b in integ]
    h.passModel(lp)
    return h, use

def raw_use(h, use, copies=1):
    sol = h.getSolution().col_value
    per = len(use) + len(items) + len(raw_items)
    off = len(use) + len(items)
    return {it: sol[off + r] for r, it in enumerate(raw_items) if sol[off + r] > 1e-9}

# ---- positive controls (no alternates) ----
for tgt, expect in ((("Desc_IronIngot_C", 60.0), {"Desc_OreIron_C": 60.0}),
                    (("Desc_IronPlate_C", 60.0), {"Desc_OreIron_C": 90.0})):
    h, use = build({tgt[0]: tgt[1]}, allow_alt=False)
    h.run()
    got = raw_use(h, use)
    ok = all(abs(got.get(k, 0) - v) < 1e-6 for k, v in expect.items())
    print("CONTROL", tgt, "->", {k: round(v, 6) for k, v in got.items()}, "PASS" if ok else "FAIL")
    assert ok

# ---- late-game target set ----
want = ["Desc_SpaceElevatorPart_9_C", "Desc_SpaceElevatorPart_10_C", "Desc_SpaceElevatorPart_11_C",
        "Desc_SpaceElevatorPart_12_C", "Desc_SingularityCell_C", "Desc_FicsiteMesh_C"]
targets = {w: 5.0 for w in want if w in rows}
print("targets:", targets)

def timeit(fn, n):
    ts = []
    for _ in range(n):
        t = time.perf_counter(); r = fn(); ts.append(time.perf_counter() - t)
    return r, statistics.median(ts), min(ts), max(ts)

print(f"highspy HiGHS version {highspy.Highs().version()}  python {platform.python_version()}  {platform.platform()}")
print("case | copies | cols | rows | nnz | build_ms(med) | solve_ms(med) [min-max] | status | obj")
for copies, runs in ((1, 7), (10, 5), (100, 3), (300, 3)):
    cap = 1e5 * copies  # coupled caps; loose enough to be feasible
    (h, use), bmed, _, _ = timeit(lambda: build(targets, copies=copies, raw_cap=cap), runs)
    lp = h.getLp()
    def solve():
        hh, _u = build(targets, copies=copies, raw_cap=cap)
        t = time.perf_counter(); hh.run(); return hh, time.perf_counter() - t
    sts = []
    for _ in range(runs):
        hh, dt = solve(); sts.append(dt)
    print(f"LP coupled | {copies} | {lp.num_col_} | {lp.num_row_} | {len(lp.a_matrix_.value_)} | {bmed*1e3:.1f} | "
          f"{statistics.median(sts)*1e3:.1f} [{min(sts)*1e3:.1f}-{max(sts)*1e3:.1f}] | {hh.modelStatusToString(hh.getModelStatus())} | {hh.getInfo().objective_function_value:.4f}")

for copies in (1, 10, 100):
    sts = []
    for _ in range(3):
        hh, use = build(targets, copies=copies, integer=True, raw_cap=1e5 * copies)
        hh.setOptionValue("time_limit", 120.0)
        t = time.perf_counter(); hh.run(); sts.append(time.perf_counter() - t)
    lp = hh.getLp()
    print(f"MILP int-machines | {copies} | {lp.num_col_} | {lp.num_row_} | {len(lp.a_matrix_.value_)} | - | "
          f"{statistics.median(sts)*1e3:.1f} [{min(sts)*1e3:.1f}-{max(sts)*1e3:.1f}] | {hh.modelStatusToString(hh.getModelStatus())} | "
          f"gap={hh.getInfo().mip_gap:.2e} nodes={hh.getInfo().mip_node_count}")

print("--- uncoupled (no shared cap rows): monolithic block-diagonal solve vs one-copy solve x copies")
for copies in (100, 300):
    sts = []
    for _ in range(3):
        hh, _u = build(targets, copies=copies, raw_cap=None)
        t = time.perf_counter(); hh.run(); sts.append(time.perf_counter() - t)
    lp = hh.getLp()
    print(f"LP uncoupled monolithic | {copies} | {lp.num_col_} | {lp.num_row_} | {statistics.median(sts)*1e3:.1f} ms | {hh.modelStatusToString(hh.getModelStatus())}")
# binding cap: tighten iron ore so alternates must be chosen
h1,_=build(targets, copies=1, raw_cap=None); h1.run(); base=raw_use(h1,_)
print("one-copy raw use:", {k: round(v,1) for k,v in base.items()})

print("--- BINDING caps: iron+copper ore capped at 70% of one-copy use x copies (alternates must take over)")
for copies in (1, 10, 100, 300):
    caps = {"Desc_OreIron_C": 0.7 * base["Desc_OreIron_C"] * copies, "Desc_OreCopper_C": 0.7 * base["Desc_OreCopper_C"] * copies}
    sts = []
    for _ in range(3):
        hh, _u = build(targets, copies=copies, raw_cap=caps)
        t = time.perf_counter(); hh.run(); sts.append(time.perf_counter() - t)
    lp = hh.getLp()
    duals = hh.getSolution().row_dual
    nI = len(items); cap0 = copies * nI
    binding = [raw_items[r] for r in range(len(raw_items)) if abs(duals[cap0 + r]) > 1e-9]
    print(f"LP binding-cap | {copies} | {lp.num_col_} | {lp.num_row_} | {statistics.median(sts)*1e3:.1f} ms [{min(sts)*1e3:.1f}-{max(sts)*1e3:.1f}] | {hh.modelStatusToString(hh.getModelStatus())} | obj {hh.getInfo().objective_function_value:.1f} (loose {13229.2939*copies:.1f}) | binding rows (nonzero dual): {binding}")
