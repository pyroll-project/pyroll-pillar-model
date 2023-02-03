import matplotlib.pyplot as plt
from pyroll.core import Unit, RollPass
from pyroll.report import hookimpl
import matplotlib.animation as mpl_ani


@hookimpl(specname="unit_plot")
def disk_element_pillar_plot(unit: Unit):
    if isinstance(unit, RollPass.DiskElement):
        de: RollPass.DiskElement = unit

        fig: plt.Figure = plt.figure()
        ax: plt.Axes = fig.add_subplot()
        ax.set_aspect("equal")
        ax.grid(True)
        ax.set_title("Pillar Deformation")
        ax.set_xlabel("$z$")
        ax.set_ylabel("$y$")

        rp = de.roll_pass

        surface = rp.roll.surface_interpolation(de.out_profile.x, rp.roll.surface_z).squeeze() + rp.gap / 2

        ax.plot(rp.roll.surface_z, surface, color="k")
        ax.plot(rp.roll.surface_z, -surface, color="k")

        ax.stem(-de.in_profile.pillars, de.in_profile.pillar_heights / 2, linefmt="red", markerfmt="_")
        ax.stem(de.out_profile.pillars, de.out_profile.pillar_heights / 2, linefmt="blue", markerfmt="_")
        ax.fill(*de.in_profile.cross_section.boundary.xy, alpha=0.5, color="red")
        ax.fill(*de.out_profile.cross_section.boundary.xy, alpha=0.5, color="blue")

        return fig


@hookimpl(specname="unit_plot")
def roll_pass_pillar_animation(unit: Unit):
    if isinstance(unit, RollPass):
        rp: RollPass = unit

        fig: plt.Figure = plt.figure()
        ax: plt.Axes = fig.add_subplot()
        ax.set_aspect("equal")
        ax.grid(True)
        ax.set_title("Animation of Deformation")
        ax.set_xlabel("$z$")
        ax.set_ylabel("$y$")

        def yield_artists():
            for de in rp.disk_elements:
                surface = rp.roll.surface_interpolation(de.out_profile.x, rp.roll.surface_z).squeeze() + rp.gap / 2
                s1 = ax.plot(rp.roll.surface_z, surface, color="k")
                s2 = ax.plot(rp.roll.surface_z, -surface, color="k")
                ip = ax.fill(*de.in_profile.cross_section.boundary.xy, alpha=0.5, color="red")
                op = ax.fill(*de.out_profile.cross_section.boundary.xy, alpha=0.5, color="blue")
                t = ax.text(
                    0, 0, f"$x = {de.out_profile.x:.2g}$", transform=ax.transAxes, horizontalalignment="left",
                    verticalalignment="bottom"
                )

                yield s1 + s2 + ip + op + [t]

        arts = list(yield_artists())

        animation = mpl_ani.ArtistAnimation(fig, arts, interval=5e3 / len(rp.disk_elements))

        return animation.to_html5_video()
