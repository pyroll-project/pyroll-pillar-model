from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pytest
from pyroll.core import Profile

import pyroll.pillar_model
from pyroll.pillar_model.profile import PillarProfile

pyroll.pillar_model.PILLAR_COUNT = 4


def test_pillars():
    p: Union[PillarProfile, Profile] = Profile.box(width=14, height=1)

    assert np.allclose(p.pillars, [0, 2, 4, 6], rtol=1e-3)


def test_pillar_boundaries():
    p: Union[PillarProfile, Profile] = Profile.box(width=14, height=1)

    assert np.allclose(p.pillar_boundaries, [0, 1, 3, 5, 7], rtol=1e-3)


def test_pillar_heights_box():
    p: Union[PillarProfile, Profile] = Profile.box(width=14, height=1)

    assert np.allclose(p.pillar_heights, 1, rtol=1e-3)


def test_pillar_heights_square():
    p: Union[PillarProfile, Profile] = Profile.square(diagonal=14)

    assert np.allclose(p.pillar_heights, [14, 10, 6, 2], rtol=1e-3)


def test_pillar_boundary_heights_box():
    p: Union[PillarProfile, Profile] = Profile.box(width=14, height=1)

    assert np.allclose(p.pillar_boundary_heights, 1, rtol=1e-3)


def test_pillar_boundary_heights_square():
    p: Union[PillarProfile, Profile] = Profile.square(diagonal=14)

    assert np.allclose(p.pillar_boundary_heights, [14, 12, 8, 4, 0], rtol=1e-3)


@pytest.mark.parametrize(
    "p", [
        Profile.round(radius=10),
        Profile.square(side=10, corner_radius=1),
        Profile.box(height=10, width=5, corner_radius=1),
        Profile.diamond(height=5, width=10, corner_radius=1)
    ]
)
def test_ring_sections(p: Union[PillarProfile, Profile]):
    fig: plt.Figure = plt.figure()
    ax: plt.Axes = fig.subplots()

    ax.set_aspect("equal")

    for c in reversed(p.pillar_sections):
        z, y = np.array(c.boundary.xy)
        plt.fill(np.concatenate([-z, z]), np.concatenate([y, y]), alpha=0.5)

    plt.plot(*p.cross_section.boundary.xy, c="k")
    plt.show()
