import logging
import webbrowser
import numpy as np
import pyroll.pillar_model
import pyroll.local_velocity

from typing import Union
from pyroll.pillar_model.profile import PillarProfile
from pyroll.core import Profile, PassSequence, RollPass, Roll, FlatGroove


@RollPass.DiskElement.pillar_spreads
def pillar_spreads(self: RollPass.DiskElement):
    return self.pillar_draughts ** -0.5


def test_pillar_longitudinal_angles_flat():
    pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"
    DISK_ELEMENT_COUNT = 15
    pyroll.pillar_model.Config.PILLAR_COUNT = 10

    in_profile = Profile.round(
        diameter=19.5e-3,
        temperature=1200 + 273.15,
        strain=0,
        material=["C45", "steel"],
        flow_stress=100e6,
        density=7.5e3,
        specific_heat_capcity=690,
    )

    rp = RollPass(
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
        disk_element_count=DISK_ELEMENT_COUNT
    )

    rp.solve(in_profile)
    first_disk_element = rp.disk_elements[0]
    angles_from_cad = [-0.23593, -0.21478, -0.15199, -0.04315, 0, 0, 0, 0, 0, 0]
    assert np.isclose(angles_from_cad, first_disk_element.pillar_longitudinal_angles, rtol=1e-3).all()
