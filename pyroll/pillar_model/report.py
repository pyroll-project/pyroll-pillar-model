import matplotlib.pyplot as plt
from pyroll.core import Unit, RollPass
from pyroll.report import hookimpl


@hookimpl(specname="unit_plot")
def disk_element_pillar_plot(unit: Unit):
    if isinstance(unit, RollPass.DiskElement):
        fig: plt.Figure = plt.figure()
        ax: plt.Axes = fig.add_subplot()
        ax.set_aspect("equal")

        rp = unit.roll_pass

        surface = rp.roll.surface_interpolation(unit.out_profile.x, rp.roll.surface_z).squeeze() + rp.gap / 2

        ax.plot(rp.roll.surface_z, surface, color="k")
        ax.plot(rp.roll.surface_z, -surface, color="k")

        ax.stem(-unit.in_profile.pillars, unit.in_profile.pillar_heights / 2, linefmt="red", markerfmt="_")
        ax.stem(unit.out_profile.pillars, unit.out_profile.pillar_heights / 2, linefmt="blue", markerfmt="_")
        ax.fill(*unit.in_profile.cross_section.boundary.xy, alpha=0.5, color="red")
        ax.fill(*unit.out_profile.cross_section.boundary.xy, alpha=0.5, color="blue")

        return fig
