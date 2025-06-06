import numpy as np
import pyroll.pillar_model


from pyroll.core import Profile, RollPass, Roll, FlatGroove, root_hooks

def pillar_spreads(self: RollPass.DiskElement):
    return self.pillar_draughts ** -0.5


def test_pillar_entry_angles_flat():
    pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"
    pyroll.pillar_model.Config.PILLAR_COUNT = 10

    with RollPass.DiskElement.pillar_spreads(pillar_spreads):
        root_hooks.add(RollPass.DiskElement.pillar_spreads)
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
        disk_element_count=15
    )

    rp.solve(in_profile)

    local_roll_radii = np.concatenate(
        [rp.roll.max_radius - rp.roll.surface_interpolation(0, center) for center in rp.in_profile.pillars],
        axis=0).flatten()
    entry_points = local_roll_radii * rp.roll.pillar_entry_angles

    assert np.isclose(np.abs(entry_points), rp.roll.total_pillar_contact_lengths, atol=1e-2).all()

    root_hooks.remove_last(RollPass.DiskElement.pillar_spreads)