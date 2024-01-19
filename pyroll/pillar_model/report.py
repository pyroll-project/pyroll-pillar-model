import matplotlib.pyplot as plt
import numpy as np
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
    if isinstance(unit, RollPass) and unit.disk_elements:
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


@hookimpl(specname="unit_plot")
def roll_pass_contact_area(unit: Unit):
    if isinstance(unit, RollPass) and unit.disk_elements:
        rp: RollPass = unit

        fig: plt.Figure = plt.figure()
        ax: plt.Axes = fig.add_subplot()
        ax.set_aspect("equal")
        ax.grid(True)
        ax.set_title("Contact Area")
        ax.set_xlabel("$z$")
        ax.set_ylabel("$x$")
        ax.invert_yaxis()

        for de in rp.disk_elements:
            for i in range(len(de.in_profile.pillars)):
                if not de.pillars_in_contact[i]:
                    continue
                x = [de.in_profile.x] * 2 + [de.out_profile.x] * 2
                z = np.array([
                    de.in_profile.pillar_boundaries[i + 1],
                    de.in_profile.pillar_boundaries[i],
                    de.out_profile.pillar_boundaries[i],
                    de.out_profile.pillar_boundaries[i + 1],
                ])
                ax.fill(z, x, alpha=0.5, c="C0")
                ax.fill(-z, x, alpha=0.5, c="C0")

        return fig


@hookimpl(specname="unit_plot")
def roll_pass_strain_strain_rate_over_width(unit: Unit):
    if isinstance(unit, RollPass) and unit.disk_elements:
        rp: RollPass = unit

        fig: plt.Figure = plt.figure()
        ax1: plt.Axes
        ax2: plt.Axes
        ax1, ax2 = fig.subplots(2, sharex="all")
        ax1.grid(True)
        ax2.grid(True)
        ax1.set_title("Strain / Strain - Rate Distribution")
        ax2.set_xlabel("$z$")
        ax1.set_ylabel("Strain ")
        ax2.set_ylabel("Strain rate")

        strains = np.sum([de.pillar_strains for de in rp.disk_elements], axis=0)
        strain_rates = np.sum([de.pillar_strain_rates for de in rp.disk_elements], axis=0)
        ax1.plot(unit.in_profile.pillars, strains, color='C0')
        ax1.plot(-unit.in_profile.pillars, strains, color='C0')
        ax2.plot(unit.in_profile.pillars, strain_rates, color='C1')
        ax2.plot(-unit.in_profile.pillars, strain_rates, color='C1')
        fig.subplots_adjust(hspace=0)

        return fig


@hookimpl(specname="unit_plot")
def roll_pass_forming_values_distribution(unit: Unit):
    if isinstance(unit, RollPass) and unit.disk_elements:
        rp: RollPass = unit

        fig: plt.Figure = plt.figure()
        ax1: plt.Axes
        ax2: plt.Axes
        ax1, ax2 = fig.subplots(2, sharex="all")
        ax1.grid(True)
        ax2.grid(True)
        ax1.set_title("Forming Values Distribution")
        ax2.set_xlabel("$x$")
        ax1.set_ylabel("Local Forming Values ")
        ax2.set_ylabel("Cumulative Forming Values")

        def _gen():
            for de in rp.disk_elements:
                yield de.in_profile.x + 0.5 * de.length, de.out_profile.width / de.in_profile.width

        gamma_ = [de.out_profile.height / de.in_profile.height for de in rp.disk_elements]
        lambda_ = [de.in_profile.cross_section.area / de.out_profile.cross_section.area for de in rp.disk_elements]
        x, beta_ = np.array(list(_gen())).T
        ax1.plot(x, gamma_, label='$\\gamma$')
        ax1.plot(x, lambda_, label='$\\lambda$')
        ax1.plot(x, beta_, label='$\\beta$')
        ax2.plot(x, np.cumprod(gamma_), label='$\\gamma$')
        ax2.plot(x, np.cumprod(lambda_), label='$\\lambda$')
        ax2.plot(x, np.cumprod(beta_), label='$\\beta$')
        ax1.legend()
        fig.subplots_adjust(hspace=0)

        return fig

@hookimpl(specname="unit_plot")
def roll_pass_velocity_over_width(unit: Unit):
    if isinstance(unit, RollPass) and unit.disk_elements:
        rp: RollPass = unit

        fig: plt.Figure = plt.figure()
        ax: plt.Axes = fig.add_subplot()

        ax.grid(True)
        ax.set_title("Velocity Distribution")
        ax.set_xlabel("$z$")
        ax.set_ylabel("Velocity")

        velocities = np.sum([de.pillar_velocities for de in rp.disk_elements], axis=0)

        ax.plot(unit.in_profile.pillars, velocities, color='C0')
        ax.plot(-unit.in_profile.pillars, velocities, color='C0')

        return fig