"""
Cosmic Morphodynamics — Stoner–Turing RDA Toy Model

This script implements the reaction–diffusion–advection system described in:

Paper I: "Cosmic Morphodynamics: A Reaction–Diffusion–Advection Toy Model
         for Baryonic Structure Formation" (v3.0)

Fields:
    G(x, y, t) : Gas / activator (cold molecular gas)
    R(x, y, t) : Radiation / inhibitor (stellar feedback)

Numerics:
    - 2D periodic grid (N x N)
    - 5-point Laplacian (von Neumann stencil)
    - Semi-Lagrangian advection via a precomputed rotation map
    - Explicit Euler integration
    - Live FFT power spectrum visualization of G
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.ndimage import map_coordinates

# ----------------------- COSMIC PARAMETERS -----------------------------------

# Grid resolution
N = 200

# Time step (dimensionless)
DT = 1.0

# Diffusion coefficients (dimensionless)
DIFF_G = 0.16  # Gas diffusion (activator)
DIFF_R = 0.08  # Radiation diffusion (inhibitor)

# Gray–Scott style feed/kill parameters (labyrinth regime)
FEED = 0.040   # Accretion rate (Phi)
KILL = 0.060   # Decay rate (Kappa)

# Nonlinear coupling strength (η in the paper); set to 1 in these units
ETA = 1.0

# Rotation / advection settings
ROTATION_STRENGTH = 0.05   # Overall strength of the galactic rotation
STEPS_PER_FRAME = 8        # Physics steps per rendered frame
NUM_FRAMES = 256           # Total animation frames


# -------------------------- NUMERICAL KERNELS --------------------------------


def laplacian(z: np.ndarray) -> np.ndarray:
    """
    5-point Laplacian on a periodic 2D grid.
    """
    return (
        np.roll(z, 1, axis=0)
        + np.roll(z, -1, axis=0)
        + np.roll(z, 1, axis=1)
        + np.roll(z, -1, axis=1)
        - 4.0 * z
    )


def get_power_spectrum(image: np.ndarray) -> np.ndarray:
    """
    Compute a log-magnitude FFT power spectrum of the input field.
    """
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    magnitude = np.log(np.abs(fshift) + 1e-9)
    return magnitude


def build_keplerian_coords(n: int, rotation_strength: float) -> np.ndarray:
    """
    Precompute a radius-dependent rotation map for semi-Lagrangian advection.

    We define a simple angular profile θ(r) ∝ 1 / r, which yields
    a "Keplerian-like" shear without attempting a full Newtonian model.
    """
    y, x = np.meshgrid(
        np.arange(n, dtype=np.float32),
        np.arange(n, dtype=np.float32),
        indexing="ij",
    )

    center = n // 2
    dx = x - center
    dy = y - center
    r = np.sqrt(dx * dx + dy * dy)
    r[r == 0.0] = 1.0  # avoid division by zero at the core

    theta = rotation_strength * (1.0 / r)  # θ(r) ∝ r^-1

    cos_t = np.cos(theta)
    sin_t = np.sin(theta)

    x_warp = dx * cos_t - dy * sin_t + center
    y_warp = dx * sin_t + dy * cos_t + center

    # coords has shape (2, n, n) with order (row, col)
    coords = np.array([y_warp, x_warp], dtype=np.float32)
    return coords


def initialize_fields(
    n: int,
    seed_radius: int = 10,
    noise_level: float = 0.05,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Initialize G and R with a central "Big Bang" perturbation plus small noise.
    """
    g = np.ones((n, n), dtype=np.float32)
    r = np.zeros((n, n), dtype=np.float32)

    center = n // 2
    sl = slice(center - seed_radius, center + seed_radius)

    # Central perturbation
    g[sl, sl] = 0.50
    r[sl, sl] = 0.25

    # Random "vacuum fluctuation" noise in the inhibitor field
    r += (np.random.random((n, n)).astype(np.float32)) * noise_level

    return g, r


def make_figure(initial_g: np.ndarray):
    """
    Set up the two-panel figure: real-space G and its FFT power spectrum.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    img_g = ax1.imshow(
        initial_g,
        cmap="magma",
        interpolation="bicubic",
        origin="lower",
    )
    ax1.set_title("Stoner–Turing Model: Baryonic Density")
    ax1.axis("off")

    img_fft = ax2.imshow(
        np.zeros_like(initial_g),
        cmap="viridis",
        origin="lower",
    )
    ax2.set_title("Power Spectrum (Frequency Domain)")
    ax2.axis("off")

    return fig, img_g, img_fft


# -------------------------- MAIN SIMULATION LOOP -----------------------------


def simulate(
    frames: int = NUM_FRAMES,
    with_advection: bool = True,
):
    """
    Run the Cosmic Morphodynamics simulation and return (fig, anim).

    Args:
        frames: Number of animation frames to render.
        with_advection: If False, disables rotation (pure reaction–diffusion).
    """
    g, r = initialize_fields(N)
    coords = build_keplerian_coords(N, ROTATION_STRENGTH) if with_advection else None

    fig, img_g, img_fft = make_figure(g)

    def update(_frame: int):
        nonlocal g, r

        # 1. Advection (semi-Lagrangian rotation)
        if coords is not None:
            g = map_coordinates(g, coords, order=1, mode="wrap")
            r = map_coordinates(r, coords, order=1, mode="wrap")

        # 2. Reaction–diffusion physics
        for _ in range(STEPS_PER_FRAME):
            lap_g = laplacian(g)
            lap_r = laplacian(r)

            # Nonlinear interaction term
            gr2 = ETA * g * (r * r)

            # Stoner–Turing update (Gray–Scott form, dimensionless units)
            delta_g = (DIFF_G * lap_g - gr2 + FEED * (1.0 - g)) * DT
            delta_r = (DIFF_R * lap_r + gr2 - (FEED + KILL) * r) * DT

            g += delta_g
            r += delta_r

        img_g.set_array(g)
        img_fft.set_array(get_power_spectrum(g))
        return img_g, img_fft

    anim = animation.FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=1,
        blit=False,
    )
    return fig, anim


if __name__ == "__main__":
    
    fig, anim = simulate(with_advection=True)
    print("Saving GIF – this will take 20–50 seconds...")
    anim.save("cosmic_morphodynamics_spiral.gif",
              writer='pillow', fps=30)
    plt.show()