from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pytest
import shapely
from pyroll.core import Profile

import pyroll.ring_model
from pyroll.ring_model import RingProfile

pyroll.ring_model.RING_COUNT = 4


def test_equivalent_radius():
    p: Union[RingProfile, Profile] = Profile.round(radius=9)

    assert np.isclose(p.equivalent_radius, 9, rtol=1e-3)

    p: Union[RingProfile, Profile] = Profile.diamond(width=10, height=9, corner_radius=1)

    assert np.isclose(p.equivalent_radius ** 2 * np.pi, p.cross_section.area, rtol=1e-3)


def test_rings():
    p: Union[RingProfile, Profile] = Profile.round(radius=7)

    assert np.allclose(p.rings, [0, 2, 4, 6], rtol=1e-3)


def test_ring_boundaries():
    p: Union[RingProfile, Profile] = Profile.round(radius=7)

    assert np.allclose(p.ring_boundaries, [0, 1, 3, 5, 7], rtol=1e-3)


@pytest.mark.parametrize(
    "p", [
        Profile.round(radius=10),
        Profile.square(side=10, corner_radius=1),
        Profile.box(height=10, width=5, corner_radius=1),
        Profile.diamond(height=5, width=10, corner_radius=1)
    ]
)
def test_ring_contours(p: Union[RingProfile, Profile]):
    fig: plt.Figure = plt.figure()
    ax: plt.Axes = fig.subplots()

    ax.set_aspect("equal")

    for c in reversed(p.ring_contours):
        plt.fill(*c.xy)
    plt.plot(*p.cross_section.boundary.xy, c="k")
    plt.show()


@pytest.mark.parametrize(
    "p", [
        Profile.round(radius=10),
        Profile.square(side=10, corner_radius=1),
        Profile.box(height=10, width=5, corner_radius=1),
        Profile.diamond(height=5, width=10, corner_radius=1)
    ]
)
def test_ring_sections(p: Union[RingProfile, Profile]):
    fig: plt.Figure = plt.figure()
    ax: plt.Axes = fig.subplots()

    ax.set_aspect("equal")

    for c in reversed(p.ring_sections):
        lines = c.boundary
        if isinstance(lines, shapely.MultiLineString):
            plt.fill(*lines.geoms[0].xy, alpha=0.5)
            plt.fill(*lines.geoms[1].xy, c="w")
        else:
            plt.fill(*lines.xy, alpha=0.5)
    plt.plot(*p.cross_section.boundary.xy, c="k")
    plt.show()
