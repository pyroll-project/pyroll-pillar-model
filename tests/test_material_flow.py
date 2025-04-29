import numpy as np
import pyroll.pillar_model

from pyroll.core import Profile, PassSequence, RollPass, Roll, FlatGroove

@RollPass.DiskElement.pillar_spreads
def pillar_spreads(self: RollPass.DiskElement):
    return self.pillar_draughts ** 0

def test_material_flow(monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 3)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")
    monkeypatch.setattr(pyroll.pillar_model.Config,"ELONGATION_CORRECTION", False)

    in_profile = Profile.box(
        height=10e-3,
        width=10e-3,
        corner_radius=0e-3,
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
                        usable_width=25e-3,
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1,
                    neutral_point=-20e-3
                ),
                gap=7e-3,
                disk_element_count=15,
            ),

        ]
    )

    sequence.solve(in_profile)

    roll_pass = sequence[0]
    disk_element_in_profile_widths = np.asarray([de.in_profile.width for de in roll_pass.disk_elements])
    disk_element_out_profile_widths = np.asarray([de.out_profile.width for de in roll_pass.disk_elements])

    disk_element_in_profile_areas = np.asarray([de.in_profile.cross_section.area for de in roll_pass.disk_elements])
    disk_element_out_profile_areas = np.asarray([de.out_profile.cross_section.area for de in roll_pass.disk_elements])

    assert np.all(disk_element_in_profile_widths == roll_pass.in_profile.width)
    assert np.all(disk_element_out_profile_widths == roll_pass.in_profile.width)
    assert np.all(disk_element_in_profile_areas[:-1] >= disk_element_in_profile_areas[1:])
    assert np.all(disk_element_out_profile_areas[:-1] >= disk_element_out_profile_areas[1:])