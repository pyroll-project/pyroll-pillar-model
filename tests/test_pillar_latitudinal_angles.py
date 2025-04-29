import numpy as np
import pyroll.pillar_model

from typing import Union
from pyroll.core import Profile
from pyroll.pillar_model.profile import PillarProfile


def test_pillar_latitudinal_angles_box(monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 4)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")

    p: Union[PillarProfile, Profile] = Profile.box(height=10, width=10)
    assert np.allclose(p.pillar_latitudinal_angles, [0, 0, 0, 0], rtol=1e-3)



def test_pillar_latitudinal_angles_square(monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 4)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")

    p: Union[PillarProfile, Profile] = Profile.square(diagonal=14)
    assert np.allclose(np.rad2deg(p.pillar_latitudinal_angles), [0, -45, -45, -45], rtol=1e-3)


def test_pillar_latitudinal_angles_round(monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 4)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")

    p: Union[PillarProfile, Profile] = Profile.round(diameter=10)
    assert np.allclose(p.pillar_latitudinal_angles, [0, -0.29351, -0.61771, -1.18286], rtol=1e-3)
