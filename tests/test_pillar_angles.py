from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pytest
from pyroll.core import Profile, RollPass, Roll, FlatGroove, PassSequence

import pyroll.pillar_model
from pyroll.pillar_model.profile import PillarProfile

@RollPass.DiskElement.pillar_spreads
def pillar_spreads(self: RollPass.DiskElement):
    return self.pillar_draughts ** -0.5


def test_angles():
    try:
        pyroll.pillar_model.Config.PILLAR_COUNT = 4
        pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"

        in_profile = Profile.round(
            diameter=19.5e-3,
            temperature=1200 + 273.15,
            strain=0,
            material=["C45", "steel"],
            flow_stress=100e6,
            density=7.5e3,
            specific_heat_capcity=690,
        )

        sequence = PassSequence(
            [
                RollPass(
                    label="Flat",
                    roll=Roll(
                        groove=FlatGroove(
                            usable_width=40e-3,
                        ),
                        nominal_radius=160e-3,
                        rotational_frequency=1,
                        neutral_point=-20e-3
                    ),
                    gap=10e-3,
                    disk_element_count=2,
                ),

            ]
        )
        sequence.solve(in_profile)
        de = sequence[0].disk_elements

        assert np.allclose(de[0].pillar_angles, [-0.25191043, -0.25191043, -0.25191043, -0.25191043], rtol=1e-3)
    finally:
        del pyroll.pillar_model.Config.PILLAR_COUNT
