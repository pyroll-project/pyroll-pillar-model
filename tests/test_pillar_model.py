import pytest
import numpy as np
import pyroll.pillar_model

from typing import Union
from pyroll.core import Profile
from pyroll.pillar_model.profile import PillarProfile


def test_pillars(monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 4)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")

    p: Union[PillarProfile, Profile] = Profile.box(width=14, height=1)
    assert np.allclose(p.pillars, [0, 2, 4, 6], rtol=1e-3)



def test_pillar_boundaries(monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 4)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")

    p: Union[PillarProfile, Profile] = Profile.box(width=14, height=1)
    assert np.allclose(p.pillar_boundaries, [-1, 1, 3, 5, 7], rtol=1e-3)



def test_pillar_heights_box(monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 4)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")

    p: Union[PillarProfile, Profile] = Profile.box(width=14, height=1)
    assert np.allclose(p.pillar_heights, 1, rtol=1e-3)



def test_pillar_heights_square(monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 4)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")

    p: Union[PillarProfile, Profile] = Profile.square(diagonal=14)
    assert np.allclose(p.pillar_heights, [14, 10, 6, 2], rtol=1e-3)



def test_pillar_boundary_heights_box(monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 4)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")

    p: Union[PillarProfile, Profile] = Profile.box(width=14, height=1)

    assert np.allclose(p.pillar_boundary_heights[:-1], 1, rtol=1e-3)


def test_pillar_boundary_heights_square(monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 4)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")

    p: Union[PillarProfile, Profile] = Profile.square(diagonal=14)
    assert np.allclose(p.pillar_boundary_heights, [12, 12, 8, 4, 0], rtol=1e-3)



@pytest.mark.parametrize(
    "p", [
        Profile.round(radius=10),
        Profile.square(side=10, corner_radius=1),
        Profile.box(height=10, width=5, corner_radius=1),
        Profile.diamond(height=5, width=10, corner_radius=1)
    ]
)
def test_uniform_pillar_sections_area(p: Union[PillarProfile, Profile], monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 4)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "UNIFORM")

    assert np.all(np.isclose(p.pillar_areas, p.pillar_areas[0], rtol=1e-3))


@pytest.mark.parametrize(
    "p", [
        Profile.round(radius=10),
        Profile.square(side=10, corner_radius=1),
        Profile.box(height=10, width=5, corner_radius=1),
        Profile.diamond(height=5, width=10, corner_radius=1)
    ]
)
def test_equidistant_pillar_widths(p: Union[PillarProfile, Profile], monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 4)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")

    assert np.all(np.isclose(p.pillar_widths, p.pillar_widths[0], rtol=1e-3))


@pytest.mark.parametrize(
    "p", [
        Profile.round(radius=10),
        Profile.square(side=10, corner_radius=1),
        Profile.box(height=10, width=5, corner_radius=1),
        Profile.diamond(height=5, width=10, corner_radius=1)
    ]
)
def test_equidistant_pillar_boundary_is_profile_boundary_(p: Union[PillarProfile, Profile], monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 4)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")

    assert np.isclose(p.pillar_boundaries[-1], p.width / 2, rtol=1e-3)


@pytest.mark.parametrize(
    "p", [
        Profile.round(radius=10),
        Profile.square(side=10, corner_radius=1),
        Profile.box(height=10, width=5, corner_radius=1),
        Profile.diamond(height=5, width=10, corner_radius=1)
    ]
)
def test_uniform_pillar_boundary_is_profile_boundary_(p: Union[PillarProfile, Profile], monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 4)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")

    assert np.isclose(p.pillar_boundaries[-1], p.width / 2, rtol=1e-3)
