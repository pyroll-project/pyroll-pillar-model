import numpy as np
import shapely

VERSION = "2.0.0b1"

from pyroll.core import Profile, Hook

PILLAR_COUNT = 11


@Profile.extension_class
class PillarProfile(Profile):
    pillars = Hook[np.ndarray]()
    """Array of z-coordinates of the pillar centers from core to side."""

    pillar_boundaries = Hook[np.ndarray]()
    """Array of z-coordinates of the pillar boundaries from core to side."""

    pillar_heights = Hook[np.ndarray]()
    """Array of the pillars' heights."""


@PillarProfile.pillars
def pillars(self: PillarProfile):
    dw = self.width / 2 / (PILLAR_COUNT - 0.5)
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
