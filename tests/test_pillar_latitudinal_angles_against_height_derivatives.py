import numpy as np
import pyroll.pillar_model

from typing import Union

from pyroll.pillar_model.profile import PillarProfile
from pyroll.core import Profile


def test_pillar_latitudinal_angles_against_height_derivatives_box():
    try:
        pyroll.pillar_model.Config.PILLAR_COUNT = 4
        pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"

        p: Union[PillarProfile, Profile] = Profile.box(height=10, width=10)

        assert np.allclose(2 * np.tan(p.pillar_latitudinal_angles), p.pillar_latitudinal_height_derivatives,
                           rtol=1e-3)
    finally:
        del pyroll.pillar_model.Config.PILLAR_COUNT


def test_pillar_latitudinal_angles_against_height_derivatives_square():
    try:
        pyroll.pillar_model.Config.PILLAR_COUNT = 4
        pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"

        p: Union[PillarProfile, Profile] = Profile.square(diagonal=14)

        assert np.allclose(2 * np.tan(p.pillar_latitudinal_angles), p.pillar_latitudinal_height_derivatives,
                           rtol=1e-3)
    finally:
        del pyroll.pillar_model.Config.PILLAR_COUNT


def test_pillar_latitudinal_angles_against_height_derivatives_round():
    try:
        pyroll.pillar_model.Config.PILLAR_COUNT = 4
        pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"

        p: Union[PillarProfile, Profile] = Profile.round(diameter=10)

        assert np.allclose(2 * np.tan(p.pillar_latitudinal_angles), p.pillar_latitudinal_height_derivatives,
                           rtol=1e-3)
    finally:
        del pyroll.pillar_model.Config.PILLAR_COUNT
