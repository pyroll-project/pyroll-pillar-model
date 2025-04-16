import numpy as np

from pyroll.core import RollPass


@RollPass.Roll.total_pillar_contact_lengths
def total_pillar_contact_lengths(self: RollPass.Roll):
    contact_lengths = np.zeros_like(self.roll_pass.in_profile.pillars)

    for de in self.roll_pass.disk_elements:
        for i, pillars in enumerate(de.in_profile.pillars):
            if de.pillars_in_contact[i]:
                contact_lengths[i] += de.length

    return contact_lengths


@RollPass.Roll.total_pillar_contact_areas
def roll_contact_area(self: RollPass.Roll):
    contact_areas = np.zeros_like(self.roll_pass.in_profile.pillars)

    for de in self.roll_pass.disk_elements:
        for i, pillars in enumerate(de.in_profile.pillars):
            if de.pillars_in_contact[i]:
                area = (de.in_profile.pillar_widths[i] + de.out_profile.pillar_widths[i]) / 2 * de.length
                contact_areas[i] += area

    return contact_areas


@RollPass.Roll.total_pillar_contact_areas
def roll_contact_area(self: RollPass.Roll):
    contact_areas = np.zeros_like(self.roll_pass.in_profile.pillars)

    for de in self.roll_pass.disk_elements:
        for i, pillars in enumerate(de.in_profile.pillars):
            if de.pillars_in_contact[i]:
                area = (de.in_profile.pillar_widths[i] + de.out_profile.pillar_widths[i]) / 2 * de.length
                contact_areas[i] += area

    return contact_areas


@RollPass.Roll.contact_area
def roll_contact_area(self: RollPass.Roll):
    return self.roll_pass.contact_area / 2
