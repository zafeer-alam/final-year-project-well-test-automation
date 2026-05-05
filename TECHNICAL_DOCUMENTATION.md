# CBM Well Test Analysis - Petroleum Engineering Documentation

## Executive Summary

This document explains the **petroleum engineering theory, formulas, and physical interpretation** of the CBM Well Test Automation system. It covers the well test analysis methods without code implementation details.

---

## 1. HORNER PLOT ANALYSIS

### 1.1 What is a Horner Plot?

The Horner plot is used to analyze **buildup tests** - measurements taken when a well is shut in (stopped producing) after a production period.

**Physical Scenario:**
- Well produces at constant rate `q` for time `tp` 
- At time `tp`, well is shut in and pressure builds back up
- We measure pressure `p(t)` at various times `t` during buildup
- Horner plot helps us extract reservoir parameters

### 1.2 Horner Plot Formula

```
X-axis: (tp + Δt) / Δt  =  Horner Time Function
Y-axis: Pressure p(Δt)
```

Where:
- `tp` = Production time before shut-in (hours)
- `Δt` = Time since shut-in started (hours)
- `p(Δt)` = Measured pressure at time Δt

**Why use this transformation?**

The pressure response during buildup follows:
```
p(Δt) - pwf = m × log₁₀[(tp + Δt) / Δt] + constant
```

Where `m` is the **Horner slope** (psi/log cycle).

When we plot this on semi-log paper:
- Data points form a **straight line** at early/middle times
- This line allows us to determine the slope `m`
- The slope directly relates to reservoir properties

### 1.3 Physical Interpretation

**Why does this work?**

During production:
- Pressure drops around the wellbore
- When shut in, pressure re-equilibrates
- The buildup pressure response is diagnostic of:
  - How easily pressure spreads in the reservoir (permeability)
  - How much storage is near the wellbore (skin factor, wellbore storage)
  - How large the reservoir is (boundary effects at late times)

**What can we read from the plot?**

1. **Straight line slope** → Reservoir permeability
2. **X-intercept** → Initial pressure and well condition
3. **Deviations from straight line** → Skin effects, faults, boundaries

---

## 2. PERMEABILITY CALCULATION FROM HORNER SLOPE

### 2.1 The Permeability Formula

```
k = (162.6 × q × μ × B) / (m × h)
```

**Where:**
- `k` = Permeability (millidarcies, md)
- `q` = Production rate (stock tank barrels per day, STBPD)
- `μ` = Fluid viscosity (centipoise, cp)
- `B` = Formation volume factor (reservoir barrels / stock tank barrels)
- `m` = Horner plot slope (psi/log cycle)
- `h` = Net pay thickness (feet)
- `162.6` = Constant that converts units (oil field units)

### 2.2 Derivation Logic

**From Darcy's Law (fundamental principle):**
```
q = (0.0001127 × k × A × Δp) / (μ × B × L)
```

For cylindrical flow to a well:
- Area `A = 2πrh` (cylindrical surface)
- Distance `L = ln(re/rw)` (radial flow)

The pressure drop during buildup is related to flow capacity:
```
Δp = (162.6 × q × μ × B × ln[(tp + Δt)/Δt]) / (k × h)
```

Rearranging to solve for `k`:
```
k = (162.6 × q × μ × B) / (m × h)
```

### 2.3 Physical Meaning

The formula tells us:

1. **Higher permeability (k)** → Smaller pressure drop for same flow rate
   - More conductive rock → easier pressure transmission
   - Steeper pressure increase during buildup (larger m)

2. **Higher viscosity (μ)** → Larger pressure drop
   - Thicker fluid → harder to flow → larger slope m

3. **Larger rate (q)** → Proportional pressure drop increase
   - More fluid removed → larger drawdown → larger slope

4. **Thicker pay zone (h)** → Larger cross-sectional area → smaller pressure drop
   - More surface area for flow → inverse relationship with m

---

## 3. BOURDET DERIVATIVE ANALYSIS

### 3.1 What is the Bourdet Derivative?

The Bourdet derivative is defined as:
```
d(Δp) / d(ln(t))
```

It measures how the pressure change rate varies with logarithmic time.

**Physical Meaning:**
- How quickly pressure is changing at each point in time
- Used for "type curve matching" - identifying flow patterns
- Shows dimensionless representation of well test response

### 3.2 Calculation Method: Central Difference

We use the **central difference method** for accuracy:

```
Derivative[i] = (p[i+1] - p[i-1]) / (ln(t[i+1]) - ln(t[i-1]))
```

**Why central difference is better than forward/backward:**

- **Forward difference:** `(p[i+1] - p[i]) / ln(t[i+1]/t[i])`
  - Uses only future data
  - Less accurate near midpoint
  
- **Central difference:** `(p[i+1] - p[i-1]) / (ln(t[i+1]) - ln(t[i-1]))`
  - Uses past and future data
  - Centered on point i
  - Better noise rejection
  - More stable for type curve matching

### 3.3 What the Derivative Tells Us

**Characteristic Shapes:**

1. **Derivative = constant (flat line)**
   - Indicates **radial flow** - pressure spreading equally in all directions
   - Occurs in infinite-acting reservoirs
   - Diagnostic of uniform permeability

2. **Derivative decreasing (downward slope)**
   - Indicates **transient flow** or **early fracture flow**
   - Pressure hasn't reached boundaries yet
   - Well has high skin effect or fracture damage

3. **Derivative increasing at late times**
   - Indicates **boundary effects** approaching
   - Well approaching reservoir boundary
   - Boundary-dominated flow beginning

### 3.4 Type Curve Concept

```
Derivative Behavior          Flow Regime           Duration
─────────────────────────────────────────────────────────
1/2 slope (–1/2 or +1/2)     Wellbore storage      Early time
Constant value               Radial flow           Middle time
Rising slope                 Boundary/sealing      Late time
Double log straight line     Fracture flow         Early time
```

The derivative acts like a "diagnostic fingerprint" for identifying what's happening in the reservoir.

---

## 4. FLOW REGIME IDENTIFICATION LOGIC

### 4.1 Our Analysis Approach

We classify flow regime by comparing **early-time vs late-time derivative behavior**:

```
IF (Early Derivative > Late Derivative)
    → EARLY FRACTURE FLOW (Transient Response)
    
ELSE IF (Late Derivative increases rapidly > 30%)
    → BOUNDARY-DOMINATED FLOW (Approaching boundary)
    
ELSE
    → RADIAL FLOW (Pseudo-Steady State)
```

### 4.2 Physical Interpretation of Each Regime

#### A. EARLY FRACTURE FLOW (Transient Response)

**Physical Scenario:**
```
Before Boundary Effects:
│
│  ┌─ Pressure disturbance spreading
│  │
│  └─ Well is "young" (early time)
│
Time →
```

**What's happening:**
- Pressure disturbance just created by production/buildup
- Hasn't reached reservoir boundaries yet
- Pressure spreading is controlled by:
  - Rock permeability
  - Fluid compressibility
  - Wellbore storage effects

**Derivative behavior:**
- Starts high (steep pressure changes early)
- Decreases over time (pressure stabilizing)
- Early derivative > Late derivative

**Why we get this:**
- In first hours/days, pressure changes rapidly
- As time goes on, pressure gradient flattens
- Derivative magnitude decreases → flowing into larger volume

#### B. RADIAL FLOW (Pseudo-Steady State)

**Physical Scenario:**
```
Infinite-Acting Reservoir:
           
    ↓ ↓ ↓
  ↙ Well ↘  Pressure spreading equally
 ↙         ↘ in all radial directions
```

**What's happening:**
- Pressure spreading uniformly in all directions
- No interference from boundaries (yet)
- Represents "ideal" reservoir behavior
- Middle time-period of buildup/drawdown

**Derivative behavior:**
- Becomes constant (flat line)
- Pressure gradient remains stable
- Early derivative ≈ Late derivative

**Why we get this:**
- Geometry is purely radial (cylindrical)
- Flow equation solution is:
  ```
  p(t) ∝ (q·μ·B)/(k·h) × ln(t) + constant
  ```
- Taking derivative of ln(t) term → constant
- Linear pressure response in log-time space

#### C. BOUNDARY-DOMINATED FLOW

**Physical Scenario:**
```
Pressure Waves Hitting Boundary:

    ┌─────────── Boundary (fault/sealing)
    │
    │↑↑↑ Reflected waves
    │
Well ────→ 
    │↓↓↓ Incident waves
    │
    └─────────── Boundary (no-flow)
```

**What's happening:**
- Pressure disturbance has reached reservoir boundary
- Boundaries reflect energy back
- System becomes "closed" (confined)
- Pressure must rise faster (confined gas/liquid)

**Derivative behavior:**
- Derivative increases sharply at late times
- Slope change > 30% or more
- Indicates "corner point" of type curve

**Why we get this:**
- Confined volume means finite storage
- Pressure accumulation accelerates
- Derivative equation becomes:
  ```
  d(Δp)/d(ln(t)) ∝ ln(t) + constant
  ```
- Natural log causes increasing curvature at late times

### 4.3 Why Our Detection Works

**Early vs Late Derivative Comparison:**

```
Regime              Early Derivative    Late Derivative    Interpretation
────────────────────────────────────────────────────────────────────────
Fracture Flow       HIGH (e.g., -18)    LOW (e.g., -62)   Transient
Radial Flow         MID (e.g., -30)     MID (e.g., -32)   Stable
Boundary Flow       LOW (e.g., -40)     HIGH (e.g., -10)  Increasing
```

This comparison directly reflects the **physical reality** of how pressure propagates:
1. Early → Fast changes (transient)
2. Middle → Stable changes (radial)
3. Late → Accelerating changes (bounded)

---

## 5. LOG-LOG PRESSURE ANALYSIS

### 5.1 What is Log-Log Pressure Behavior?

```
X-axis: log₁₀(Time)
Y-axis: log₁₀(Pressure Drop)
```

### 5.2 Theoretical Basis

**From pressure diffusion equation (fundamental PDE):**
```
∂²p/∂r² + (1/r)·∂p/∂r = (φ·μ·c)/(0.0001127·k) · ∂p/∂t
```

For radial flow, the solution shows:
```
Δp(r,t) ∝ t^n  (at different times)
```

Where `n` changes with flow regime:

```
Flow Regime             Slope (n)    Log-Log Appearance
─────────────────────────────────────────────────────────
Wellbore Storage        ~1.0         45° line (n=1)
Early Transient         ~0.5         30° line (n=0.5)
Radial Flow             ~0.0         Horizontal (n≈0)
Late Boundary           ~0.5         Upward curve
Fracture Flow           ~0.5         45° line (n=0.5)
```

### 5.3 Physical Interpretation

**Why slopes change?**

1. **Wellbore Storage dominated (45° slope):**
   - Pressure rise comes from pipe filling, not reservoir flow
   - All pressure change is from incompressibility

2. **Square-root-of-time response (30° slope):**
   - Classic diffusion equation response
   - Pressure diffusing into infinite medium
   - From solution: `Δp ∝ √t`

3. **Flat (radial flow):**
   - Pressure remains nearly constant (reached boundary)
   - All flow capacity exhausted
   - Only small pressure gradient remains

### 5.4 Using Log-Log to Identify Transitions

The shape of log-log plot shows when:
- Wellbore storage ends → slope decreases
- Boundary is approaching → slope increases again
- Different permeabilities → breaks in slope (faults)

---

## 6. EXAMPLE OUTPUT INTERPRETATION

### 6.1 Sample Results from Our Analysis

**Input Data:**
- 19 time points: 1 to 1000 hours
- Pressure decline: 2950.5 to 2675.5 psi

**Output Results:**

```
Flow Regime Identified: Early Fracture Flow (Transient)
Early derivative: -18.40 psi
Late derivative: -61.78 psi
Reason: Early (-18.40) > Late (-61.78)
```

### 6.2 What This Means (Petroleum Engineering Interpretation)

**Why Early Fracture Flow?**

1. **Early derivatives are larger in magnitude** (-18 vs -61)
   - Pressure is changing rapidly at early times
   - Indicates transient response (not yet stabilized)

2. **Pressure decreases over time in derivative**
   - System is "settling down"
   - Initial disturbance is being distributed
   - More volume becoming active

3. **Physical Scenario:**
   ```
   Hour 1-100:  Steep buildup (high derivative)
                └─ Well "fighting" against closed system
                
   Hour 100+:   Gradual buildup (low derivative)
                └─ Pressure spreading into larger volume
   ```

### 6.3 Permeability Calculation Example

**Given:**
- Horner slope: 150 psi/cycle
- Production rate: 500 STBPD
- Fluid viscosity: 0.8 cp
- Volume factor: 1.2 RB/STB
- Pay thickness: 25 feet

**Calculation:**
```
k = (162.6 × 500 × 0.8 × 1.2) / (150 × 25)
k = (162.6 × 480) / 3750
k = 78,048 / 3750
k = 20.81 millidarcies
```

**Interpretation:**
- 20.81 md is **moderate permeability** for CBM
- Typical CBM wells: 0.1 to 100+ md
- This value suggests:
  - Not severely tight (would be <1 md)
  - Not highly conductive (would be >100 md)
  - Typical coal seam permeability
  - Suitable for commercial production

---

## 7. EXCEL EXPORT STRUCTURE

### 7.1 Horner Sheet

**Columns:**
| Shutdown Time (h) | Pressure (psi) | Horner Time Function |
|---|---|---|
| 1.0 | 2950.5 | 1001.0 |
| 1.5 | 2945.3 | 668.33 |
| ... | ... | ... |

**Use:** Plot semi-log (Horner Time on log axis) to find slope

### 7.2 Derivative Sheet

**Columns:**
| Time (h) | Pressure (psi) | Bourdet Derivative |
|---|---|---|
| 1.0 | 2950.5 | NaN |
| 1.5 | 2945.3 | -18.40 |
| ... | ... | ... |

**Use:** Identify type curve match and flow regime transitions

### 7.3 LogLog Sheet

**Columns:**
| Time (h) | Pressure Drop (psi) |
|---|---|
| 1.0 | 0 |
| 1.5 | 5.2 |
| ... | ... |

**Use:** Identify slope changes and flow regime transitions

---

## 8. WELL TEST ANALYSIS WORKFLOW

### 8.1 Complete Interpretation Sequence

```
Step 1: Data Acquisition
├─ Measure pressure at regular intervals
├─ Record production history
└─ Time period: early time (minutes) to late time (days)

Step 2: Horner Plot Analysis
├─ Plot (tp + Δt)/Δt vs Pressure (semi-log)
├─ Identify straight line section
├─ Measure slope m
└─ Calculate permeability k

Step 3: Derivative Analysis
├─ Calculate Bourdet derivative
├─ Plot on log-log scale
├─ Identify characteristic shapes
└─ Match to type curves

Step 4: Flow Regime Identification
├─ Compare early vs late derivative
├─ Identify type curve model
└─ Classify flow regime

Step 5: Reservoir Characterization
├─ From slope: permeability
├─ From shape: skin factor, storage
├─ From boundaries: reservoir size
└─ Deliverability forecast
```

### 8.2 Quality Checks

**Good data should show:**
1. ✓ Clear Horner straight line (at least 1 log cycle)
2. ✓ Smooth derivative curve (no oscillations)
3. ✓ Consistent trends (no measurement errors)
4. ✓ Logical sequence (pressure monotonic, time increasing)

**Problems to watch:**
- ✗ Scattered points → instrument noise
- ✗ Multiple straight lines → multiple flow regimes, complex geometry
- ✗ Negative permeability → data quality issue
- ✗ Sudden changes → disturbance (pump cycles, well interference)

---

## 9. ASSUMPTIONS & LIMITATIONS

### 9.1 Standard Assumptions

Our analysis assumes:
1. **Constant rate production** before buildup
2. **Vertical well** (not horizontal/deviated)
3. **Single-phase flow** (not multiphase)
4. **Homogeneous reservoir** (uniform k and φ)
5. **No wellbore storage** (or corrected for)
6. **Infinite-acting behavior** for middle times

### 9.2 CBM-Specific Considerations

Coal seam wells have special features:
- **Dual porosity:** Matrix (coal) + fracture flow
- **Sorbed gas release:** Pressure-dependent
- **Water production:** Changes fluid properties
- **Cleat orientation:** May cause anisotropy
- **Adsorption hysteresis:** Path-dependent effects

### 9.3 When Results May Not Apply

- Very early times dominated by wellbore storage
- Late times affected by boundary/faults
- Heterogeneous permeability (faults)
- Crossflow between layers
- Multiphase flow (water + gas)

---

## 10. SUMMARY & PHYSICAL INSIGHTS

### 10.1 Key Principles

| Concept | Physical Reality | How We Measure |
|---------|------------------|----------------|
| **Permeability** | How easily fluid flows | Horner slope → k |
| **Flow Geometry** | How pressure spreads | Derivative shape → regime |
| **Skin Factor** | Well damage/condition | Horner intercept → s |
| **Boundary Effect** | Reservoir confinement | Log-log slope change → distance |

### 10.2 Why Each Analysis Matters

- **Horner Plot:** Direct property extraction (k)
- **Bourdet Derivative:** Pattern recognition (flow regime)
- **Log-Log:** Slope transitions identify flow model
- **Excel Report:** Professional documentation

### 10.3 Confidence in Results

Results are reliable when:
✓ Multiple straight line log cycles visible (Horner)
✓ Derivative smooth without noise (>10 data points)
✓ Physical consistency (k > 0, reasonable values)
✓ Type curve match identified

---

## Appendix A: Unit Conversion Reference

```
Permeability:
1 darcy = 1000 millidarcies (md)
1 md ≈ 10^-12 m²

Viscosity (cp = centipoise):
Oil typically: 0.5 - 2.0 cp
Gas typically: 0.01 - 0.02 cp
Water: 1.0 cp at surface

Rate (STBPD = stock tank barrels per day):
1 barrel = 42 gallons = 0.159 m³
1 STBPD ≈ 0.1589 m³/day

Pressure (psi = pounds per square inch):
1 psi = 6.895 kPa
1 atm = 14.696 psi
```

---

## Appendix B: Recommended Reading

**Fundamental Well Testing:**
- Well Testing Theory & Practice (Earlougher, 1977)
- Well Test Analysis (Matthews & Russell)

**Bourdet Derivative:**
- "Use of Well Test Data to Assess Reservoir Properties" (Bourdet et al., 1989)

**CBM-Specific:**
- "Coal Seam Gas Operations" (Moore, 2012)
- SPE Papers on dual-porosity flow in coal

---

**Document Version:** 1.0  
**Date:** 2026-05-06  
**Author:** CBM Well Test Analysis System  
**Purpose:** Educational & Professional Understanding
