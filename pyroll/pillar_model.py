import numpy as np
import shapely

VERSION = "2.0.0b1"

from pyroll.core import Profile, Hook

RING_COUNT = 11


@Profile.extension_class
class RingProfile(Profile):
    equivalent_radius = Hook[float]()
    """Radius of an equivalent round profile."""

    rings = Hook[np.ndarray]()
    """Array of radius coordinates of the ring centers from core to surface."""

    ring_boundaries = Hook[np.ndarray]()
    """Array of radius coordinates of the ring boundaries from core to surface."""

    ring_contours = Hook[np.ndarray]()
    """Array of the contour lines of the ring boundaries (LineString geometry objects)."""

    ring_sections = Hook[np.ndarray]()
    """Array of the ring section areas (Polygon geometry objects)."""


@RingProfile.equivalent_radius
def equivalent_radius(self: RingProfile):
    return np.sqrt(self.cross_section.area / np.pi)


@RingProfile.rings
def rings(self: RingProfile):
    dr = self.equivalent_radius / (RING_COUNT - 0.5)
    return np.arange(0, self.equivalent_radius, dr)


@RingProfile.ring_boundaries
def ring_boundaries(self: RingProfile):
    a = np.zeros(len(self.rings) + 1)
    a[1:-1] = (self.rings[1:] + self.rings[:-1]) / 2
    a[-1] = self.equivalent_radius
    return a


@RingProfile.ring_contours
def ring_contours(self: RingProfile):
    a = np.zeros(len(self.rings) + 1, dtype=object)
    a[0] = shapely.LinearRing()
    x, y = np.array(self.cross_section.boundary.xy)
    angles = np.arctan2(y, x)
    radii = np.sqrt(x ** 2 + y ** 2)
    for i in range(1, len(a)):
        scaled_radii = radii * self.ring_boundaries[i] / self.equivalent_radius
        a[i] = shapely.LinearRing(
            np.column_stack(
                [
                    scaled_radii * np.cos(angles),
                    scaled_radii * np.sin(angles)
                ]
            )
        )

    return a


@RingProfile.ring_sections
def ring_sections(self: RingProfile):
    a = np.zeros(len(self.rings), dtype=object)
    a[0] = shapely.Polygon(
        shell=self.ring_contours[1],
    )

    for i in range(1, len(a)):
        a[i] = shapely.Polygon(
            shell=self.ring_contours[i + 1],
            holes=[self.ring_contours[i]]
        )

    return a
