import numpy as np
import shapely
from pyroll.core import RollPass, Hook

import pyroll.core

pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.OutProfile.pillars)


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
def rp_out_cross_section(self: RollPass.OutProfile):
    if self.roll_pass.disk_elements:
        return self.roll_pass.disk_elements[-1].out_profile.cross_section


@RollPass.OutProfile.width
def rp_out_width(self: RollPass.OutProfile):
    if self.roll_pass.disk_elements:
        return self.cross_section.width
