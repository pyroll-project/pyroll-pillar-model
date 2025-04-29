import numpy as np
import pyroll.pillar_model

from pathlib import Path
from pyroll.core import Profile, PassSequence, RollPass, Roll, CircularOvalGroove


@RollPass.DiskElement.pillar_spreads
def pillar_spreads(self: RollPass.DiskElement):
    return self.pillar_draughts ** -0.5


def test_solve_default_flow_stress(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 30)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")
    monkeypatch.setattr(pyroll.pillar_model.Config, "ELONGATION_CORRECTION", True)

    in_profile = Profile.round(
        diameter=19.5e-3,
        temperature=1200 + 273.15,
        strain=0,
        material=["C45", "steel"],
        flow_stress=100e6,
        density=7.5e3,
        specific_heat_capcity=690,
    )

    sequence = PassSequence([RollPass(
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
        disk_element_count=15,
    )
    ])

    sequence.solve(in_profile)
    for de in sequence[0].disk_elements:
        assert np.isclose(len(de.in_profile.pillars_flow_stress), 30)
        assert np.isclose(de.in_profile.pillars_flow_stress, np.full(pyroll.pillar_model.Config.PILLAR_COUNT,
                                                                     sequence.in_profile.flow_stress)).all()
