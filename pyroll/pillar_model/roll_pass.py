import numpy as np
import shapely
from pyroll.core import RollPass, Hook


@RollPass.DiskElement.extension_class
class PillarDiskElement(RollPass.DiskElement):
    pillars_in_contact = Hook[np.ndarray]()
    """Array of booleans indicating if a pillar has contact to the rolls."""

    pillar_spreads = Hook[np.ndarray]()
    """Array of spread values for each pillar."""

    pillar_draughts = Hook[np.ndarray]()
    """Array of draught values for each pillar."""


@PillarDiskElement.pillars_in_contact
def pillars_in_contact(self: PillarDiskElement):
    rp = self.roll_pass
    contour = rp.roll.surface_interpolation(self.out_profile.x, self.in_profile.pillars).squeeze()
    return self.in_profile.pillar_heights / 2 > contour + rp.gap / 2


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
def pillar_spreads(self: PillarDiskElement):
    return np.ones_like(self.in_profile.pillars)


@PillarDiskElement.OutProfile.pillars
def out_pillars(self: PillarDiskElement.OutProfile):
    de = self.disk_element
    rp = de.roll_pass

    if not self.has_set_or_cached("pillars"):
        return de.in_profile.pillars

    pillars = de.in_profile.pillars
    boundaries = de.in_profile.pillar_boundaries

    widths = boundaries[1:] - boundaries[:-1]
    new_widths = widths * de.pillar_spreads

    new_pillars = np.zeros_like(pillars)
    for i in range(1, len(pillars)):
        new_pillars[i] = np.sum(new_widths[:i]) + new_widths[i] / 2

    return new_pillars


@PillarDiskElement.OutProfile.cross_section
def out_cross_section(self: PillarDiskElement.OutProfile):
    coords1 = np.column_stack([self.pillars, self.pillar_heights / 2])
    coords2 = coords1[::-1].copy()
    coords2[:, 1] *= -1
    coords3 = coords1[1:].copy()
    coords3 *= -1
    coords4 = coords2[:-1].copy()
    coords4 *= -1
    outer = self.pillars[-1] + (self.pillars[-1] - self.pillars[-2]) / 2
    return shapely.Polygon(
        np.row_stack([
            coords1,
            [(outer, 0)],
            coords2,
            coords3,
            [(-outer, 0)],
            coords4,
        ])
    )


@RollPass.OutProfile.cross_section
def out_cross_section(self: RollPass.OutProfile):
    if self.roll_pass.disk_elements:
        return self.roll_pass.disk_elements[-1].out_profile.cross_section


@RollPass.OutProfile.width
def out_width(self: RollPass.OutProfile):
    if self.roll_pass.disk_elements:
        return self.cross_section.width
