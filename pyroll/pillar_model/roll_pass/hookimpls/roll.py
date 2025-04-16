import numpy as np

from pyroll.core import RollPass


@RollPass.Roll.total_pillar_contact_lengths
def total_pillar_contact_lengths(self: RollPass.Roll):
    contact_lengths = np.zeros_like(self.roll_pass.in_profile.pillars)

    for de in self.roll_pass.disk_elements:
        for i, pillars in enumerate(de.in_profile.pillars):
            if de.pillars_in_contact[i]:
                contact_lengths[i] += de.length


@RollPass.Roll.contact_area
def roll_contact_area(self: RollPass.Roll):
    return self.roll_pass.contact_area / 2


@RollPass.Roll.contact_length
def contact_length(self: RollPass.Roll):
    return np.mean(self.total_pillar_contact_lengths)
