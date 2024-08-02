import numpy as np

from pyroll.core import RollPass


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


@RollPass.total_pillar_strains
def total_pillar_strains(self: RollPass):
    p_strains = [de.pillar_strains for de in self.disk_elements]
    return np.sum(p_strains, axis=0)


@RollPass.total_pillar_strain_rates
def total_pillar_strain_rates(self: RollPass):
    p_strain_rates = [de.pillar_strain_rates for de in self.disk_elements]
    return np.sum(p_strain_rates, axis=0)


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


@RollPass.roll_force
def roll_force_disks(self: RollPass):
    return np.sum([
        (de.in_profile.flow_stress + de.out_profile.flow_stress) / 2 * de.contact_area
        for de in self.disk_elements
    ]) / 2  # /2 since two rolls


@RollPass.DiskElement.velocity
def disk_velocity(self: RollPass.DiskElement):
    return self.in_profile.velocity


@RollPass.DiskElement.InProfile.velocity
def disk_in_velocity(self: RollPass.DiskElement.InProfile):
    if self.disk_element is self.roll_pass.disk_elements[0]:
        return self.roll_pass.in_profile.velocity


@RollPass.DiskElement.OutProfile.velocity
def disk_out_velocity(self: RollPass.DiskElement.OutProfile):
    de = self.disk_element
    return de.in_profile.velocity * de.in_profile.cross_section.area / self.cross_section.area


@RollPass.mean_elongation
def mean_elongation(self: RollPass):
    return np.sum(self.out_profile.pillar_areas) / np.sum(self.out_profile.pillar_areas / self.total_pillar_elongations)


@RollPass.pillar_spread_correction_coefficients
def pillar_spread_correction_coefficients(self: RollPass):
    if self.disk_elements[-1].out_profile is None:
        return 1

    def updated_correction_coefficients_to_current_iteration_loop():
        return 1 / (RollPass.mean_elongation.get_result(self) * RollPass.total_pillar_draughts.get_result(
            self) * RollPass.total_pillar_spreads.get_result(self))

    def calculate_coefficients(correction_coefficients, relaxation_factor=0.5):
        return self.pillar_spread_correction_coefficients + (
                self.pillar_spread_correction_coefficients * correction_coefficients - self.pillar_spread_correction_coefficients) * relaxation_factor / self.disk_element_count

    corr_exp = updated_correction_coefficients_to_current_iteration_loop()
    coeff = calculate_coefficients(correction_coefficients=corr_exp)
    return coeff
