import numpy as np
import pyroll.pillar_model

from typing import Union
from pyroll.core import Profile
from pyroll.pillar_model.profile import PillarProfile


def test_pillar_latitudinal_angles_against_height_derivatives_box(monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 4)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")

    p: Union[PillarProfile, Profile] = Profile.box(height=10, width=10)
    assert np.allclose(2 * np.tan(p.pillar_latitudinal_angles), p.pillar_latitudinal_height_derivatives, rtol=1e-3)



def test_pillar_latitudinal_angles_against_height_derivatives_square(monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 4)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")

    p: Union[PillarProfile, Profile] = Profile.square(diagonal=14)
    assert np.allclose(2 * np.tan(p.pillar_latitudinal_angles), p.pillar_latitudinal_height_derivatives,
                           rtol=1e-3)


def test_pillar_latitudinal_angles_against_height_derivatives_round(monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 4)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")

    p: Union[PillarProfile, Profile] = Profile.round(diameter=10)
    assert np.allclose(2 * np.tan(p.pillar_latitudinal_angles), p.pillar_latitudinal_height_derivatives,
                           rtol=1e-3)
