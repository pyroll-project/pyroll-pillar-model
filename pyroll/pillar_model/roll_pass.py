import numpy as np
import shapely
from pyroll.core import RollPass, Hook

import pyroll.core

pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.OutProfile.pillars)
pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.OutProfile.pillar_heights)
pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.OutProfile.pillar_widths)
pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.OutProfile.pillar_areas)

pyroll.core.root_hooks.add(pyroll.core.Rotator.OutProfile.pillars)
pyroll.core.root_hooks.add(pyroll.core.Rotator.OutProfile.pillar_heights)
pyroll.core.root_hooks.add(pyroll.core.Rotator.OutProfile.pillar_widths)
pyroll.core.root_hooks.add(pyroll.core.Rotator.OutProfile.pillar_areas)


@RollPass.DiskElement.extension_class
class PillarDiskElement(RollPass.DiskElement):
    pillars_in_contact = Hook[np.ndarray]()
    """Array of booleans indicating if a pillar has contact to the rolls."""

    pillar_spreads = Hook[np.ndarray]()
    """Array of spread values for each pillar."""

    pillar_draughts = Hook[np.ndarray]()
    """Array of draught values for each pillar."""

    pillar_elongations = Hook[np.ndarray]()
    """Array of elongation values for each pillar."""

    pillar_log_spreads = Hook[np.ndarray]()
    """Array of log spread values for each pillar."""

    pillar_log_draughts = Hook[np.ndarray]()
    """Array of log draught values for each pillar."""

    pillar_log_elongations = Hook[np.ndarray]()
    """Array of log elongation values for each pillar."""

    pillar_strains = Hook[np.ndarray]()
    """Array of strain values for each pillar."""

    pillar_strain_rates = Hook[np.ndarray]()
    """Array of strain rate values for each pillar."""


RollPass.total_pillar_elongations = Hook[np.ndarray]()
"""Array of total elongation for each pillar for a roll pass."""

RollPass.total_pillar_spreads = Hook[np.ndarray]()
"""Array of total spread for each pillar for a roll pass."""

RollPass.total_pillar_draughts = Hook[np.ndarray]()
"""Array of total drought for each pillar for a roll pass."""

RollPass.total_pillar_log_elongations = Hook[np.ndarray]()
"""Array of total logarithmic elongation for each pillar for a roll pass."""

RollPass.total_pillar_log_spreads = Hook[np.ndarray]()
"""Array of total logarithmic spread for each pillar for a roll pass."""

RollPass.total_pillar_log_draughts = Hook[np.ndarray]()
"""Array of total logarithmic drought for each pillar for a roll pass."""

RollPass.total_pillar_strains = Hook[np.ndarray]()
"""Array of total strains for each pillar for a roll pass."""

RollPass.total_pillar_strain_rates = Hook[np.ndarray]()
"""Array of total strain rates for each pillar for a roll pass."""

RollPass.mean_elongation = Hook[float]()
"""Mean elongation of the profile in the roll pass."""

RollPass.pillar_spread_correction_exponents = Hook[np.ndarray]()
"""Array of correction exponents for pillar spreads of a roll pass."""

pyroll.core.root_hooks.add(pyroll.core.RollPass.total_pillar_elongations)
pyroll.core.root_hooks.add(pyroll.core.RollPass.total_pillar_spreads)
pyroll.core.root_hooks.add(pyroll.core.RollPass.total_pillar_draughts)
pyroll.core.root_hooks.add(pyroll.core.RollPass.total_pillar_log_elongations)
pyroll.core.root_hooks.add(pyroll.core.RollPass.total_pillar_log_spreads)
pyroll.core.root_hooks.add(pyroll.core.RollPass.total_pillar_log_draughts)
pyroll.core.root_hooks.add(pyroll.core.RollPass.total_pillar_strains)
pyroll.core.root_hooks.add(pyroll.core.RollPass.total_pillar_strain_rates)


@PillarDiskElement.pillars_in_contact
def pillars_in_contact(self: PillarDiskElement):
    rp = self.roll_pass
    contour = rp.roll.surface_interpolation(self.out_profile.x, self.out_profile.pillars).squeeze()
    contacts = self.in_profile.pillar_heights / 2 > contour + rp.gap / 2
    return contacts


@PillarDiskElement.OutProfile.pillar_heights
def pillar_heights(self: PillarDiskElement.OutProfile):
    de = self.disk_element
    rp = de.roll_pass
    heights = de.in_profile.pillar_heights.copy()
    heights[de.pillars_in_contact] = rp.roll.surface_interpolation(
        de.out_profile.x,
        de.out_profile.pillars[de.pillars_in_contact]
    ).squeeze() * 2 + rp.gap
    return heights


@PillarDiskElement.pillar_draughts
def pillar_draughts(self: PillarDiskElement):
    return self.out_profile.pillar_heights / self.in_profile.pillar_heights


@PillarDiskElement.pillar_spreads
def pillar_spreads(self: PillarDiskElement, cycle: bool):
    if cycle:
        return None

    from . import Config
    if Config.ELONGATION_CORRECTION:
        return (yield) ** self.roll_pass.pillar_spread_correction_exponents

    return np.ones_like(self.in_profile.pillars)


@PillarDiskElement.pillar_elongations
def pillar_elongations(self: PillarDiskElement):
    return 1 / (self.pillar_draughts * self.pillar_spreads)


@PillarDiskElement.pillar_log_draughts
def pillar_log_draughts(self: PillarDiskElement):
    return np.log(self.pillar_draughts)


@PillarDiskElement.pillar_log_spreads
def pillar_log_spreads(self: PillarDiskElement):
    return np.log(self.pillar_spreads)


@PillarDiskElement.pillar_log_elongations
def pillar_log_elongations(self: PillarDiskElement):
    return np.log(self.pillar_elongations)


@RollPass.total_pillar_draughts
def total_pillar_draughts(self: RollPass):
    if self.disk_elements:
        p_draughts = [de.pillar_draughts for de in self.disk_elements]
        return np.prod(p_draughts, axis=0)


@RollPass.total_pillar_spreads
def total_pillar_spreads(self: RollPass):
    if self.disk_elements:
        p_spreads = [de.pillar_spreads for de in self.disk_elements]
        return np.prod(p_spreads, axis=0)


@RollPass.total_pillar_elongations
def total_pillar_elongations(self: RollPass):
    if self.disk_elements:
        p_elongations = [de.pillar_elongations for de in self.disk_elements]
        return np.prod(p_elongations, axis=0)


@RollPass.total_pillar_log_draughts
def total_pillar_log_draughts(self: RollPass):
    p_log_draughts = [de.pillar_log_draughts for de in self.disk_elements]
    return np.sum(p_log_draughts, axis=0)


@RollPass.total_pillar_log_spreads
def total_pillar_log_spreads(self: RollPass):
    p_log_spreads = [de.pillar_log_spreads for de in self.disk_elements]
    return np.sum(p_log_spreads, axis=0)


@RollPass.total_pillar_log_elongations
def total_pillar_log_elongations(self: RollPass):
    p_log_elongations = [de.pillar_log_elongations for de in self.disk_elements]
    return np.sum(p_log_elongations, axis=0)


@PillarDiskElement.pillar_strains
def pillar_strains(self: PillarDiskElement):
    return np.sqrt(
        2 / 3 * (self.pillar_log_elongations ** 2 + self.pillar_log_spreads ** 2 + self.pillar_log_draughts ** 2))


@PillarDiskElement.pillar_strain_rates
def pillar_strain_rates(self: PillarDiskElement):
    local_roll_radii = np.concatenate(
        [self.roll_pass.roll.max_radius - self.roll_pass.roll.surface_interpolation(0, center) for center in
         self.in_profile.pillars],
        axis=0).flatten()

    return self.roll_pass.velocity * self.pillar_strains / local_roll_radii


@RollPass.total_pillar_strains
def total_pillar_strains(self: RollPass):
    p_strains = [de.pillar_strains for de in self.disk_elements]
    return np.sum(p_strains, axis=0)


@RollPass.total_pillar_strain_rates
def total_pillar_strain_rates(self: RollPass):
    p_strain_rates = [de.pillar_strain_rates for de in self.disk_elements]
    return np.sum(p_strain_rates, axis=0)


@PillarDiskElement.OutProfile.pillar_widths
def out_pillar_widths(self: PillarDiskElement.OutProfile):
    de = self.disk_element
    return de.in_profile.pillar_widths * de.pillar_spreads


@PillarDiskElement.OutProfile.pillar_boundaries
def out_pillar_boundaries(self: PillarDiskElement.OutProfile):
    a = np.zeros(len(self.pillar_widths) + 1)
    a[1:] = np.cumsum(self.pillar_widths)
    return a


@PillarDiskElement.OutProfile.pillars
def out_pillars(self: PillarDiskElement.OutProfile):
    if not self.has_set_or_cached("pillars"):
        return self.disk_element.in_profile.pillars

    a = np.zeros(len(self.pillar_boundaries) - 1)
    a[1:] = (self.pillar_boundaries[2:] + self.pillar_boundaries[1:-1]) / 2
    return a


@PillarDiskElement.OutProfile.cross_section
def out_cross_section(self: PillarDiskElement.OutProfile):
    coords1 = np.column_stack([self.pillars, self.pillar_heights / 2])
    coords2 = coords1[::-1].copy()
    coords2[:, 1] *= -1
    coords3 = coords1[1:].copy()
    coords3 *= -1
    coords4 = coords2[:-1].copy()
    coords4 *= -1
    outer = self.pillar_boundaries[-1]
    return shapely.Polygon(
        np.row_stack(
            [
                coords1,
                [(outer, 0)],
                coords2,
                coords3,
                [(-outer, 0)],
                coords4,
            ]
        )
    )


@RollPass.OutProfile.cross_section
def rp_out_cross_section(self: RollPass.OutProfile):
    if self.roll_pass.disk_elements:
        return self.roll_pass.disk_elements[-1].out_profile.cross_section


@RollPass.OutProfile.width
def rp_out_width(self: RollPass.OutProfile):
    if self.roll_pass.disk_elements:
        return self.cross_section.width


@RollPass.DiskElement.contact_area
def disk_contact_area(self: RollPass.DiskElement):
    contact_width = (
            np.sum(self.in_profile.pillar_widths[self.pillars_in_contact])
            + np.sum(self.out_profile.pillar_widths[self.pillars_in_contact])
    )  # /2 missing since pillars only on half profile
    return contact_width * self.length * 2  # *2 since two rolls


@RollPass.contact_area
def pass_contact_area(self: RollPass):
    if self.disk_elements:
        return np.sum([de.contact_area for de in self.disk_elements])


@RollPass.surface_area
def pass_surface_area(self: RollPass):
    if self.disk_elements:
        return np.sum([de.surface_area for de in self.disk_elements])


@RollPass.Roll.contact_area
def roll_contact_area(self: RollPass.Roll):
    return self.roll_pass.contact_area / 2


@RollPass.roll_force
def roll_force_disks(self: RollPass):
    return np.sum([
        (de.in_profile.flow_stress + de.out_profile.flow_stress) / 2 * de.contact_area
        for de in self.disk_elements
    ]) / 2  # /2 since two rolls


@RollPass.mean_elongation
def mean_elongation(self: RollPass):
    return np.sum(self.out_profile.pillar_areas) / np.sum(self.out_profile.pillar_areas / self.total_pillar_elongations)


@RollPass.pillar_spread_correction_exponents
def pillar_spread_correction_exponents(self: RollPass):
    if self.disk_elements[-1].out_profile is None:
        return 1

    def updated_correction_exponents_to_current_iteration_loop():
        return - np.log(
            RollPass.mean_elongation.get_result(self) * RollPass.total_pillar_draughts.get_result(self)) / np.log(
            RollPass.total_pillar_spreads.get_result(self))

    def calculate_coefficients(correction_exponents, relaxation_factor=0.5):
        return self.pillar_spread_correction_exponents + (
                self.pillar_spread_correction_exponents * correction_exponents - self.pillar_spread_correction_exponents) * relaxation_factor

    corr_exp = updated_correction_exponents_to_current_iteration_loop()
    coeff = calculate_coefficients(correction_exponents=corr_exp)
    return coeff
