import logging
from pathlib import Path

import numpy as np
from pyroll.core import Profile, RollPass, Roll, CircularOvalGroove
import pyroll.pillar_model


@RollPass.DiskElement.pillar_spreads
def pillar_spreads(self: RollPass.DiskElement):
    return self.pillar_draughts ** -0.5


DISK_ELEMENT_COUNT = 15
pyroll.pillar_model.Config.PILLAR_COUNT = 30


def test_solve_default_flow_stress(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")
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

    rp = RollPass(
        label="Oval",
        roll=Roll(
            groove=CircularOvalGroove(
                depth=5e-3,
                r1=0.2e-3,
                r2=16e-3,
            ),
            nominal_radius=160e-3,
            rotational_frequency=1,
            neutral_point=-20e-3
        ),
        gap=4e-3,
        disk_element_count=DISK_ELEMENT_COUNT,
    )

    rp.solve(in_profile)
    for de in rp.disk_elements:
        assert np.isclose(len(de.in_profile.pillars_flow_stress), 30)
        assert np.isclose(de.in_profile.pillars_flow_stress, np.full(pyroll.pillar_model.Config.PILLAR_COUNT,
                                                                     rp.in_profile.flow_stress)).all()
