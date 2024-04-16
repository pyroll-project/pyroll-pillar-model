import math
import shapely
import numpy as np

from scipy.optimize import fsolve
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

    pillar_areas = Hook[np.ndarray]()
    """Array of the pillar section areas (numerical value)."""

    pillar_latitudinal_angles = Hook[np.ndarray]()
    """Array of pillars' angles between pillars in width (z) direction."""


@PillarProfile.pillars
def pillars_equidistant(self: PillarProfile):
    from . import Config
    if Config.PILLAR_TYPE.lower() == "equidistant":
        dw = self.width / 2 / (Config.PILLAR_COUNT - 0.5)
        return np.arange(0, self.width / 2, dw)


@PillarProfile.pillars
def pillars_uniform(self: PillarProfile):
    from . import Config
    if Config.PILLAR_TYPE.lower() == "uniform":
        dw = self.width / 2 / (Config.PILLAR_COUNT - 0.5)
        equidistant_pillar_widths = np.full(Config.PILLAR_COUNT, dw)

        def p_centers(p_widths):
            centers = np.zeros_like(p_widths)
            dist = (p_widths[:-1] + p_widths[1:]) / 2
            centers[1:] = centers[:-1] + np.cumsum(dist)
            return centers

        def p_heights(p_widths):
            return np.array(
                [
                    shapely.intersection(
                        self.cross_section,
                        shapely.LineString([(p, self.cross_section.bounds[1]), (p, self.cross_section.bounds[3])])
                    ).length
                    for p in p_centers(p_widths)
                ]
            )

        def fun(p_widths):
            ph = p_heights(p_widths)
            areas = (p_widths * ph)
            diffs = areas[1:] - areas[:-1]
            w = np.sum(p_widths) - self.width / 2 - p_widths[0] / 2

            return np.append(diffs, w)

        sol = fsolve(fun, x0=equidistant_pillar_widths)

        return p_centers(sol)


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


@PillarProfile.pillar_latitudinal_angles
def pillar_latitudinal_angles(self: PillarProfile):
    dy = np.diff(self.pillar_boundary_heights) / 2

    return np.arctan2(dy, self.pillar_widths)


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


@PillarProfile.pillar_areas
def pillar_areas(self: PillarProfile):
    return np.array([section.area for section in self.pillar_sections])
