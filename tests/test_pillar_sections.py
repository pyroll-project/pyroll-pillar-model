from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pytest
from pyroll.core import Profile

import pyroll.pillar_model
from pyroll.pillar_model.profile import PillarProfile


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
            ax.plot(np.concatenate([-z, z]), np.concatenate([-y, y]), alpha=0.5)

        ax.plot(*p.cross_section.boundary.xy, c="k")
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
def test_pillar_sections_equidistant(p: Union[PillarProfile, Profile]):
    try:
        pyroll.pillar_model.Config.PILLAR_COUNT = 4
        pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"
        fig: plt.Figure = plt.figure()
        ax: plt.Axes = fig.subplots()

        ax.set_aspect("equal")

        for c in reversed(p.pillar_sections):
            z, y = np.array(c.boundary.xy)

            plt.fill(np.concatenate([-z, z]), np.concatenate([-y, y]), alpha=0.5)

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
def test_pillar_sections_uniform_validity(p: Union[PillarProfile, Profile]):
    try:
        pyroll.pillar_model.Config.PILLAR_COUNT = 4
        pyroll.pillar_model.Config.PILLAR_TYPE = "UNIFORM"

        res = []
        for c in reversed(p.pillar_sections):
            res.append(c.is_valid)

        assert all(res) is True
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
def test_pillar_sections_equidistant_validity(p: Union[PillarProfile, Profile]):
    try:
        pyroll.pillar_model.Config.PILLAR_COUNT = 4
        pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"

        res = []
        for c in reversed(p.pillar_sections):
            res.append(c.is_valid)

        assert all(res) is True
    finally:
        del pyroll.pillar_model.Config.PILLAR_COUNT
        del pyroll.pillar_model.Config.PILLAR_TYPE