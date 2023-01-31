from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pytask
import shapely

from pyroll.core import Profile

import pyroll.ring_model
from pyroll.ring_model import RingProfile
import matplotlib.patches as mpatches

pyroll.ring_model.RING_COUNT = 5


@pytask.mark.produces([f"ring_model{s}" for s in [".png", ".svg", ".pdf"]])
def task_ring_model(produces: dict[Any, Path]):
    fig: plt.Figure = plt.figure(figsize=(7, 2), dpi=600)
    axs: list[plt.Axes] = fig.subplots(1, 3, sharey="all", width_ratios=[1, 0.4, 0.75])

    p: Profile | RingProfile = Profile.diamond(width=10, height=5, corner_radius=1)

    for i in range(3):
        axs[i].set_aspect("equal")
        axs[i].axis("off")

    for c in reversed(p.ring_sections):
        lines = c.boundary
        if isinstance(lines, shapely.MultiLineString):
            axs[0].fill(*lines.geoms[0].xy, alpha=0.5)
            axs[0].fill(*lines.geoms[1].xy, c="w")
        else:
            axs[0].fill(*lines.xy, alpha=0.5)

    axs[0].plot(*p.cross_section.boundary.xy, c="k")

    p2: Profile | RingProfile = Profile.round(radius=p.equivalent_radius)

    for c in reversed(p2.ring_sections):
        lines = c.boundary
        if isinstance(lines, shapely.MultiLineString):
            axs[2].fill(*lines.geoms[0].xy, alpha=0.5)
            axs[2].fill(*lines.geoms[1].xy, c="w")
        else:
            axs[2].fill(*lines.xy, alpha=0.5)

    axs[2].plot(*p2.cross_section.boundary.xy, c="k")

    axs[1].arrow(0, 0, 1, 0, color="k", width=0.1)
    axs[1].arrow(0, 0, -1, 0, color="k", width=0.1)

    fig.tight_layout()

    for f in produces.values():
        fig.savefig(f)
