from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pytest
import shapely
from pyroll.core import Profile

import pyroll.pillar_model
from pyroll.pillar_model import PillarProfile

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
