from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pytask

from pyroll.core import Profile, RollPass, Roll, SquareGroove

import pyroll.pillar_model
from pyroll.pillar_model.profile import PillarProfile

pyroll.pillar_model.Config.PILLAR_COUNT = 5


@RollPass.DiskElement.pillar_spreads
def pillar_spreads(self: RollPass.DiskElement):
    return self.pillar_draughts ** -1.1


@pytask.mark.produces([f"pillar_disk_element.{s}" for s in ["png", "svg", "pdf"]])
def task_pillar_disk_element(produces: dict[Any, Path]):
    p: Profile | PillarProfile = Profile.diamond(width=10, height=5, corner_radius=1, flow_stress=1, strain=0)

    rp = RollPass(
        roll=Roll(
            groove=SquareGroove(0.5, 0.5, tip_depth=3.5, tip_angle=90),
            nominal_radius=200,
        ),
        gap=1,
        velocity=1,
        disk_element_count=2,
    )

    rp.solve(p)

    de = rp.disk_elements[0]

    fig: plt.Figure = plt.figure(figsize=(6.4, 4), dpi=600)
    ax: plt.Axes = fig.subplots()

    ax.set_aspect("equal")
    ax.axis("off")

    surface = rp.roll.surface_interpolation(de.out_profile.x, rp.roll.surface_z).squeeze() + rp.gap / 2

    ax.plot(rp.roll.surface_z, surface, color="k", label="roll surface")
    ax.plot(rp.roll.surface_z, -surface, color="k")

    ax.fill(*de.in_profile.cross_section.boundary.xy, alpha=0.5, color="red", label="in profile")
    ax.fill(*de.out_profile.cross_section.boundary.xy, alpha=0.5, color="blue", label="out profile")

    ax.axvline(0, c="k", ls="-.")
    ax.axhline(0, c="k", ls="-.")

    ax.stem(
        -de.in_profile.pillars, de.in_profile.pillar_heights / 2,
        linefmt="red", markerfmt="_", basefmt="k-",
        label="in pillars",
    )
    ax.stem(
        de.out_profile.pillars, de.out_profile.pillar_heights / 2,
        linefmt="blue", markerfmt="_", basefmt="k-",
        label="out pillars",
    )

    ax.legend()

    fig.tight_layout()

    for f in produces.values():
        fig.savefig(f)

    plt.close(fig)
