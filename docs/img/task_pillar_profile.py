from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pytask

from pyroll.core import Profile

import pyroll.pillar_model
from pyroll.pillar_model.profile import PillarProfile

pyroll.pillar_model.Config.PILLAR_COUNT = 5


@pytask.mark.produces([f"pillar_profile.{s}" for s in ["png", "svg", "pdf"]])
def task_pillar_profile(produces: dict[Any, Path]):
    p: Profile | PillarProfile = Profile.diamond(width=10, height=5, corner_radius=1)

    fig: plt.Figure = plt.figure(figsize=(6.4, 3.5), dpi=600)
    ax: plt.Axes = fig.subplots()

    ax.set_aspect("equal")
    ax.axis("off")

    for i, c in enumerate(p.pillar_sections):
        z, y = np.array(c.boundary.xy)
        ax.fill(np.concatenate([-z, z]), np.concatenate([y, y]), alpha=0.5)

    ax.plot(*p.cross_section.boundary.xy, c="k")

    ax.axvline(0, c="k", ls="-.")
    ax.axhline(0, c="k", ls="-.")

    ax.stem(
        p.pillars, p.pillar_heights / 2,
        linefmt="r", markerfmt="_", basefmt="r-",
        label="half pillar heights",
    )

    ax.fill([], [], alpha=0.5, c="gray", label="pillar sections")
    ax.legend()

    fig.tight_layout()

    for f in produces.values():
        fig.savefig(f)

    plt.close(fig)
