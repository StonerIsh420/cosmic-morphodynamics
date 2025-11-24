# **Paper I: Theoretical Framework (Post-Critique)**

## **Title**

**Cosmic Morphodynamics: A Reaction–Diffusion–Advection Toy Model for Baryonic Structure Formation**

**Author:** [Stoner]
**Date:** November 23, 2025
**Classification:** Theoretical Astrophysics / Non-Equilibrium Thermodynamics
**Version:** 3.0 (Post-Critique) 

---

### **Abstract**

Reaction–diffusion systems with differential transport and non-linear feedback generate stripes, spots, and spirals in chemistry and biology. This work explores a deliberately minimal, phenomenological application of such systems to galactic and large-scale baryonic structure. We construct a two-field reaction–diffusion–advection (RDA) model on a rotating disk, where a gas-like activator and a radiation-like inhibitor interact under shear, generating spiral and filamentary patterns reminiscent of galaxies and the cosmic web.

In earlier versions, this framework was informally framed as a possible **alternative** to dark matter and ΛCDM. That claim is retracted. The present paper explicitly positions **Cosmic Morphodynamics** as a **toy model** and **morphological analogy**, not as a replacement for collisionless dark matter or gravitational instability. The model does not include self-gravity, is strictly two-dimensional, does not reproduce observed flat rotation curves quantitatively, does not match the measured matter power spectrum, and cannot account for systems where mass and light are spatially decoupled (e.g., the Bullet Cluster).

The scientific value of the framework is therefore limited but precise:

1. It provides a well-posed set of PDEs encoding a Turing-like mechanism for baryonic pattern formation on a rotating manifold.
2. It demonstrates how spiral arms and web-like filaments can arise in an excitable medium without appealing to density-wave theory.
3. It offers a controlled numerical playground for studying **qualitative** morphologies, not for fitting cosmological data.

A companion paper (Paper II) and the associated Python implementation numerically integrate these equations on a 2D grid with a Keplerian-like warp, visualizing the resulting patterns and their Fourier spectra.

---

### **1. Introduction**

The ΛCDM paradigm, combining cold dark matter with a cosmological constant, has been quantitatively successful in reproducing:

* The cosmic microwave background anisotropy spectrum.
* The matter power spectrum and baryon acoustic oscillations.
* The statistical properties of large-scale structure.
* Galaxy rotation curves and cluster dynamics, including systems where lensing mass is offset from baryonic gas.

Tensions such as cusp–core discrepancies and missing satellites have motivated alternative or complementary ideas (MOND, emergent gravity, self-interacting dark matter, exotic baryonic feedback models). Many of these generate attractive visual or heuristic narratives but fail multiple independent observational tests that ΛCDM passes.

This work explores a different kind of deviation: not a competing cosmology, but an **excitable-medium analogy** for baryonic structure formation. The guiding question is narrow and modest:

> If the interstellar medium (ISM) and circumgalactic medium (CGM) were treated as an activator–inhibitor system subject to rotation and shear, what kinds of patterns could arise, and do they bear any qualitative resemblance to galactic spirals or the cosmic web?

To that end, we define the **Cosmic Morphodynamics Hypothesis** in its reduced, defensible form:

* **Hypothesis (Morphological):**
  On sufficiently coarse scales, some aspects of baryonic structure formation can be approximated by a reaction–diffusion–advection system in which cold gas acts as an activator and stellar feedback acts as an inhibitor, producing patterns that are qualitatively reminiscent of observed galactic and web-like morphologies.

* **Non-claims (Explicit):**

  * The model does **not** explain flat rotation curves quantitatively.
  * The model does **not** reproduce the 3D matter distribution inferred from lensing.
  * The model does **not** eliminate the need for non-baryonic dark matter.
  * The model does **not** compete with ΛCDM as a global cosmological theory.

The goal of Paper I is to specify the PDE system, its physical mapping, and its limitations with sufficient clarity that the subsequent numerical work (Paper II) can be interpreted correctly: as a complex-systems toy experiment, not as evidence against dark matter. 

---

### **2. Field Definitions and Physical Mapping**

We work on a 2D manifold representing a thin galactic disk or a slice through a larger baryonic structure. Let $\mathbf{x} = (x, y)$ denote dimensionless planar coordinates and $t$ a dimensionless time variable.

#### **2.1 State Variables**

* $G(\mathbf{x}, t)$ – **Gas activator**
  Dimensionless density of cold molecular gas and star-forming material. High $G$ increases the local probability of star formation.

* $R(\mathbf{x}, t)$ – **Radiation inhibitor**
  Dimensionless energy density of stellar feedback (ionizing radiation, winds, supernova shocks). High $R$ suppresses further collapse by heating and dispersing gas.

This mapping is intentionally coarse-grained. It collapses the full multiphase ISM + CGM (cold, warm, hot gas, cosmic rays, magnetic fields) into two scalar fields. Consequently, any “fit” to real data must be interpreted as **illustrative**, not literal.

#### **2.2 Reaction–Diffusion–Advection Equations**

The **Stoner–Turing** model is defined as:

[
\frac{\partial G}{\partial t} = D_G \nabla^2 G - \eta G R^2 + \Phi (1 - G) - \vec{v} \cdot \nabla G,
]

[
\frac{\partial R}{\partial t} = D_R \nabla^2 R + \eta G R^2 - (\Phi + \kappa) R - \vec{v} \cdot \nabla R.
]

Where:

* $D_G$ – diffusion coefficient for gas (slow transport, turbulent mixing).
* $D_R$ – diffusion coefficient for radiation/feedback (fast propagation / effective smoothing).
* $\eta$ – coupling efficiency of feedback-triggered star formation.
* $\Phi$ – “feed” term, representing gas accretion onto the disk or into the considered slice.
* $\kappa$ – effective decay term for the radiation/inhibitor field.
* $\vec{v}(\mathbf{x})$ – imposed velocity field encoding rotation and shear.

The non-linear term $\eta G R^2$ plays the role of a **triggered star-formation kernel**: feedback can both ignite and quench structure. The choice $D_R \gg D_G$ satisfies the Turing-instability condition and is qualitatively consistent with the fact that radiation and hot feedback propagate much faster than cold gas responds.

The advection operator $\vec{v} \cdot \nabla$ is not derived from gravity here; it is prescribed as an external kinematic field. In the numerical work it is instantiated via a radius-dependent angular velocity profile and implemented as a semi-Lagrangian warp of the grid. 

---

### **3. Relation to ΛCDM and Observational Constraints**

This section formalizes what the toy model **can** and **cannot** be expected to reproduce.

#### **3.1 Rotation Curves**

Observed galactic rotation curves remain approximately flat—$v(r) \approx \text{const}$—out to multiple optical radii, with tight scatter across a wide range of masses. In ΛCDM, this is explained by extended dark matter halos whose density profiles yield the required gravitational potential.

In the present model, the apparent “rotation” of features in $G$ arises from:

* The imposed velocity field $\vec{v}(\mathbf{x})$, chosen by hand.
* The phase velocity of reaction–diffusion waves, set by $(D_G, D_R, \eta, \Phi, \kappa)$.

There is no self-consistent gravitational field, no Poisson solver, and no attempt to match observed $v(r)$ profiles. At best, one can tune parameters so that some **pattern speed** of spiral arms sits near an observed range for a single galaxy. Extending that to a population-level Tully–Fisher or baryonic Tully–Fisher relation is out of scope and unsupported.

**Conclusion:** This model does **not** currently explain flat rotation curves and must not be presented as doing so.

#### **3.2 Large-Scale Structure and Power Spectrum**

On cosmological scales, ΛCDM makes precise predictions for the matter power spectrum $P(k)$, which have been validated by surveys such as SDSS and, more recently, by Euclid-like missions. The shape and turnover point are extremely sensitive to the presence of cold, collisionless matter.

A 2D RDA system on a periodic grid can produce:

* A characteristic wavenumber $k_\ast$ at which power is concentrated (a visible ring in the Fourier plane).
* Secondary features depending on non-linear pattern interactions.

This is **qualitatively** similar to seeing a “preferred scale” in the cosmic web, but it is not quantitatively comparable to the 3D matter power spectrum of ΛCDM. There is no early-universe transfer function, no baryon acoustic oscillation physics, and no vertical structure.

**Conclusion:** Any resemblance between the toy-model power spectrum and cosmological $P(k)$ is aesthetic, not evidentiary.

#### **3.3 Bullet Cluster–Type Systems**

Systems like the Bullet Cluster show a clear spatial offset between:

* X-ray emitting gas (baryons), and
* Gravitational lensing maps (total mass).

This is widely interpreted as direct evidence for non-baryonic dark matter: the collisionless component passes through, the gas is shocked and lags behind.

In the Cosmic Morphodynamics model, by construction, the only “mass-like” field is the gas activator $G$. Any inferred mass or lensing pattern would therefore track $G$ directly. There is no mechanism for a collisionless component to spatially decouple from the baryonic field, and hence no way to reproduce Bullet Cluster–type observations.

**Conclusion:** The model is incompatible with the strongest existing evidence for non-baryonic dark matter and does not attempt to address it.

---

### **4. Status of the Hypothesis and Built-In Limitations**

To prevent overclaiming, this section codifies the current status of the framework.

#### **4.1 Dimensionality and Missing Gravity**

* The equations are solved in **2D** with no vertical structure.
* There is **no self-gravity**: no Poisson equation, no evolving potential.
* The velocity field $\vec{v}$ is prescribed rather than derived from mass distribution.

As a result, the model cannot address:

* Toomre stability and realistic star-formation thresholds.
* Vertical disk thickening, flaring, or warps.
* Halo mass–baryon fraction relations or the missing baryon problem.

#### **4.2 Phenomenological Parameters**

Parameters such as $(D_G, D_R, \eta, \Phi, \kappa)$ are chosen in simulation units (e.g., “Feed = 0.040, Kill = 0.060”) that are natural for generating patterns but not calibrated to physical units like km/s, pc, or Myr. 

A physically serious application would require:

* Mapping grid spacing to parsecs or kiloparsecs.
* Mapping time steps to Myr or Gyr.
* Expressing diffusion coefficients, reaction rates, and advection speeds in those units.
* Checking consistency with observed ISM turbulence, cooling times, and feedback energetics.

This has not yet been done. Consequently, the model is **not** ready for quantitative comparison to data; it is a pattern-generating sandbox.

#### **4.3 Category of the Proposal**

Given these constraints, Cosmic Morphodynamics should be categorized as:

* A **complex-systems analogy** for baryonic pattern formation.
* A **visual and conceptual tool** to think about how feedback and transport might sculpt gas morphologies on top of an underlying ΛCDM framework.
* Not a standalone cosmological theory and not an explanation of away dark matter.

---

### **5. Computational Experiment Plan**

Despite its limitations, the model is precise enough to warrant numerical exploration. Paper II and the associated Python code implement the following experiment:

1. Discretize the 2D domain on a $200 \times 200$ periodic grid.
2. Initialize $G$ and $R$ with a central perturbation plus small random noise.
3. Evolve the system using explicit Euler integration:

   * 5-point Laplacian for diffusion.
   * Non-linear reaction terms as given above.
   * Semi-Lagrangian application of a radius-dependent rotational warp to approximate advection.
4. Visualize:

   * Real-space snapshots of $G(\mathbf{x}, t)$ as “baryonic density” maps.
   * The Fourier power spectrum of $G$ to reveal characteristic scales and ring-like structures.

The purpose of these simulations is narrowly defined:

* Demonstrate that an RDA system can generate spiral arms that maintain apparent coherence under rotation.
* Show that filamentary webs and clumpy seeds can emerge from a simple activator–inhibitor interaction.
* Explore how changing $(\Phi, \kappa)$ and the rotation profile qualitatively changes morphology.

No cosmological parameter fitting, lensing prediction, or rotation curve matching is attempted.

---

### **6. Outlook and Future Work**

If one wished to push the Cosmic Morphodynamics program beyond a toy model, the minimum technical upgrades would be:

1. **Add self-gravity**

   * Couple $G$ to a gravitational potential $\Phi_{\mathrm{grav}}$ via a Poisson equation.
   * Allow $\vec{v}$ to be derived from the evolving potential rather than prescribed.

2. **Extend to 3D**

   * Include vertical structure and pressure support.
   * Track the interplay between disk thickness, turbulence, and feedback-driven outflows.

3. **Calibrate to physical units**

   * Map all parameters to physically plausible values and constrain them with ISM observations.

4. **Targeted observational tests**

   * Attempt to match rotation curves for a small sample of galaxies.
   * Compare synthetic 3D matter distributions and lensing signatures to cluster-scale observations.