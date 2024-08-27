from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pytest
from pyroll.core import Profile

import pyroll.pillar_model
from pyroll.pillar_model.profile import PillarProfile


def test_pillars():
    try:
        pyroll.pillar_model.Config.PILLAR_COUNT = 4
        pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"

        p: Union[PillarProfile, Profile] = Profile.box(width=14, height=1)

        assert np.allclose(p.pillars, [0, 2, 4, 6], rtol=1e-3)
    finally:
        del pyroll.pillar_model.Config.PILLAR_COUNT


def test_pillar_boundaries():
    try:
        pyroll.pillar_model.Config.PILLAR_COUNT = 4
        pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"

        p: Union[PillarProfile, Profile] = Profile.box(width=14, height=1)

        assert np.allclose(p.pillar_boundaries, [-1, 1, 3, 5, 7], rtol=1e-3)
    finally:
        del pyroll.pillar_model.Config.PILLAR_COUNT


def test_pillar_heights_box():
    p: Union[PillarProfile, Profile] = Profile.box(width=14, height=1)

    assert np.allclose(p.pillar_heights, 1, rtol=1e-3)


def test_pillar_heights_square():
    try:
        pyroll.pillar_model.Config.PILLAR_COUNT = 4
        pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"

        p: Union[PillarProfile, Profile] = Profile.square(diagonal=14)

        assert np.allclose(p.pillar_heights, [14, 10, 6, 2], rtol=1e-3)
    finally:
        del pyroll.pillar_model.Config.PILLAR_COUNT


def test_pillar_boundary_heights_box():
    p: Union[PillarProfile, Profile] = Profile.box(width=14, height=1)

    assert np.allclose(p.pillar_boundary_heights[:-1], 1, rtol=1e-3)
    assert np.allclose(p.pillar_boundary_heights[-1], 0, rtol=1e-3)


def test_pillar_boundary_heights_square():
    try:
        pyroll.pillar_model.Config.PILLAR_COUNT = 4
        pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"

        p: Union[PillarProfile, Profile] = Profile.square(diagonal=14)

        assert np.allclose(p.pillar_boundary_heights, [12, 12, 8, 4, 0], rtol=1e-3)
    finally:
        del pyroll.pillar_model.Config.PILLAR_COUNT


@pytest.mark.parametrize(
    "p", [
        Profile.round(radius=10),
        Profile.square(side=10, corner_radius=1),
        Profile.box(height=10, width=5, corner_radius=1),
        Profile.diamond(height=5, width=10, corner_radius=1)
    ]
)
def test_pillar_sections_equidistant(p: Union[PillarProfile, Profile]):
    try:
        pyroll.pillar_model.Config.PILLAR_COUNT = 4
        pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"
        fig: plt.Figure = plt.figure()
        ax: plt.Axes = fig.subplots()

        ax.set_aspect("equal")

        for c in reversed(p.pillar_sections):
            z, y = np.array(c.boundary.xy)
            plt.fill(np.concatenate([-z, z]), np.concatenate([y, y]), alpha=0.5)

        plt.plot(*p.cross_section.boundary.xy, c="k")
        plt.show()
    finally:
        del pyroll.pillar_model.Config.PILLAR_COUNT
        del pyroll.pillar_model.Config.PILLAR_TYPE


@pytest.mark.parametrize(
    "p", [
        Profile.round(radius=10),
        Profile.square(side=10, corner_radius=1),
        Profile.box(height=10, width=5, corner_radius=1),
        Profile.diamond(height=5, width=10, corner_radius=1)
    ]
)
def test_pillar_sections_uniform(p: Union[PillarProfile, Profile]):
    try:
        pyroll.pillar_model.Config.PILLAR_COUNT = 4
        pyroll.pillar_model.Config.PILLAR_TYPE = "UNIFORM"

        fig: plt.Figure = plt.figure()
        ax: plt.Axes = fig.subplots()

        ax.set_aspect("equal")

        for c in reversed(p.pillar_sections):
            z, y = np.array(c.boundary.xy)
            plt.fill(np.concatenate([-z, z]), np.concatenate([y, y]), alpha=0.5)

        plt.plot(*p.cross_section.boundary.xy, c="k")
        plt.show()
    finally:
        del pyroll.pillar_model.Config.PILLAR_COUNT
        del pyroll.pillar_model.Config.PILLAR_TYPE


@pytest.mark.parametrize(
    "p", [
        Profile.round(radius=10),
        Profile.square(side=10, corner_radius=1),
        Profile.box(height=10, width=5, corner_radius=1),
        Profile.diamond(height=5, width=10, corner_radius=1)
    ]
)
def test_uniform_pillar_sections_area(p: Union[PillarProfile, Profile]):
    pyroll.pillar_model.Config.PILLAR_COUNT = 4
    pyroll.pillar_model.Config.PILLAR_TYPE = "UNIFORM"

    assert np.all(np.isclose(p.pillar_areas, p.pillar_areas[0], rtol=1e-3))


@pytest.mark.parametrize(
    "p", [
        Profile.round(radius=10),
        Profile.square(side=10, corner_radius=1),
        Profile.box(height=10, width=5, corner_radius=1),
        Profile.diamond(height=5, width=10, corner_radius=1)
    ]
)
def test_equidistant_pillar_widths(p: Union[PillarProfile, Profile]):
    pyroll.pillar_model.Config.PILLAR_COUNT = 4
    pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"

    assert np.all(np.isclose(p.pillar_widths, p.pillar_widths[0], rtol=1e-3))

@pytest.mark.parametrize(
    "p", [
        Profile.round(radius=10),
        Profile.square(side=10, corner_radius=1),
        Profile.box(height=10, width=5, corner_radius=1),
        Profile.diamond(height=5, width=10, corner_radius=1)
    ]
)
def test_equidistant_pillar_boundary_is_profile_boundary_(p: Union[PillarProfile, Profile]):
    pyroll.pillar_model.Config.PILLAR_COUNT = 4
    pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"

    assert np.isclose(p.pillar_boundaries[-1], p.width / 2, rtol=1e-3)

@pytest.mark.parametrize(
    "p", [
        Profile.round(radius=10),
        Profile.square(side=10, corner_radius=1),
        Profile.box(height=10, width=5, corner_radius=1),
        Profile.diamond(height=5, width=10, corner_radius=1)
    ]
)
def test_uniform_pillar_boundary_is_profile_boundary_(p: Union[PillarProfile, Profile]):
    pyroll.pillar_model.Config.PILLAR_COUNT = 4
    pyroll.pillar_model.Config.PILLAR_TYPE = "UNIFORM"

    assert np.isclose(p.pillar_boundaries[-1], p.width / 2, rtol=1e-3)
