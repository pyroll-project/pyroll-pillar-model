import math
import numpy as np
import shapely

from pyroll.core import Profile, Hook


@Profile.extension_class
class PillarProfile(Profile):
    pillars = Hook[np.ndarray]()
    """Array of z-coordinates of the pillar centers from core to side."""

    pillar_boundaries = Hook[np.ndarray]()
    """Array of z-coordinates of the pillar boundaries from core to side."""

    pillar_heights = Hook[np.ndarray]()
    """Array of the pillars' heights."""

    pillar_widths = Hook[np.ndarray]()
    """Array of the pillars' widths."""

    pillar_boundary_heights = Hook[np.ndarray]()
    """Array of the pillar boundaries' heights."""

    pillar_sections = Hook[np.ndarray]()
    """Array of the pillar section areas (Polygon geometry objects)."""


@PillarProfile.pillars
def pillars(self: PillarProfile):
    from . import Config
    dw = self.width / 2 / (Config.PILLAR_COUNT - 0.5)
    return np.arange(0, self.width / 2, dw)


@PillarProfile.pillar_boundaries
def pillar_boundaries(self: PillarProfile):
    a = np.zeros(len(self.pillars) + 1)
    a[1:-1] = (self.pillars[1:] + self.pillars[:-1]) / 2
    a[-1] = self.width / 2
    return a


@PillarProfile.pillar_heights
def pillar_heights(self: PillarProfile):
    return np.array(
        [
            shapely.intersection(
                self.cross_section,
                shapely.LineString([(p, self.cross_section.bounds[1]), (p, self.cross_section.bounds[3])])
            ).length
            for p in self.pillars
        ]
    )


@PillarProfile.pillar_widths
def pillar_widths(self: PillarProfile):
    return self.pillar_boundaries[1:] - self.pillar_boundaries[:-1]


@PillarProfile.pillar_boundary_heights
def pillar_boundary_heights(self: PillarProfile):
    return np.array(
        [
            shapely.intersection(
                self.cross_section,
                shapely.LineString([(p, self.cross_section.bounds[1]), (p, self.cross_section.bounds[3])])
            ).length
            for p in self.pillar_boundaries
        ]
    )


@PillarProfile.pillar_sections
def pillar_sections(self: PillarProfile):
    a = np.zeros(len(self.pillars), dtype=object)

    for i in range(0, len(a)):
        a[i] = shapely.clip_by_rect(
            self.cross_section,
            self.pillar_boundaries[i],
            -math.inf,
            self.pillar_boundaries[i + 1],
            math.inf
        )

    return a
