import numpy as np
import pyroll.pillar_model
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.cm import ScalarMappable

from pyroll.core import Profile, PassSequence, RollPass, Roll, CircularOvalGroove, root_hooks


def pillar_spreads(self: RollPass.DiskElement):
    return self.pillar_draughts ** -0.5


def test_pillar_strains_with_corner_correction(monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 30)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")
    monkeypatch.setattr(pyroll.pillar_model.Config, "ELONGATION_CORRECTION", False)
    monkeypatch.setattr(pyroll.pillar_model.Config, "CORNER_CORRECTION", True)

    with RollPass.DiskElement.pillar_spreads(pillar_spreads):
        root_hooks.add(RollPass.DiskElement.pillar_spreads)

        in_profile = Profile.round(
            diameter=19.5e-3,
            temperature=1200 + 273.15,
            strain=0,
            material=["C45", "steel"],
            flow_stress=100e6,
            density=7.5e3,
            specific_heat_capcity=690,
        )

        sequence = PassSequence(
            [
                RollPass(
                    label="Oval",
                    roll=Roll(
                        groove=CircularOvalGroove(
                            depth=5e-3,
                            r1=0.2e-3,
                            r2=16e-3,
                        ),
                        nominal_radius=160e-3,
                        rotational_frequency=1,
                        neutral_point=-20e-3
                    ),
                    gap=3e-3,
                    disk_element_count=30,
                ),

            ]
        )

    sequence.solve(in_profile)

    p_strains = []
    p_strain_rates = []
    for de in sequence[0].disk_elements:
        p_strains.append(de.out_profile.pillar_strains)
        p_strain_rates.append(de.pillar_strain_rates)

    min_strain = np.min(p_strains)
    max_strain = np.max(p_strains)

    min_strain_rates = np.min(p_strain_rates)
    max_strain_rates = np.max(p_strain_rates)

    norm_strain = mcolors.Normalize(vmin=min_strain, vmax=max_strain)
    norm_strain_rate = mcolors.Normalize(vmin=min_strain_rates, vmax=max_strain_rates)
    cmap = plt.get_cmap("hsv")

    fig, axes = plt.subplots(1, 2, figsize=(12, 8))

    axes[0].set_title("Pillar Strains")
    axes[1].set_title("Pillar Strain Rates")

    for ax in axes:
        ax.set_aspect("equal")
        ax.grid(True)
        ax.set_xlabel("$z$")
        ax.set_ylabel("$x$")
        ax.invert_yaxis()

    for de in sequence[0].disk_elements:
        for i in range(len(de.in_profile.pillars)):
            if not de.pillars_in_contact[i]:
                continue

            strain = de.out_profile.pillar_strains[i]
            color_strain = cmap(norm_strain(strain))
            color_strain_rate = cmap(norm_strain(strain))

            x = [de.in_profile.x] * 2 + [de.out_profile.x] * 2
            z = np.array([
                de.in_profile.pillar_boundaries[i + 1],
                de.in_profile.pillar_boundaries[i],
                de.out_profile.pillar_boundaries[i],
                de.out_profile.pillar_boundaries[i + 1],
            ])
            axes[0].fill(z, x, alpha=0.7, color=color_strain)
            axes[0].fill(-z, x, alpha=0.7, color=color_strain)

            axes[1].fill(z, x, alpha=0.7, color=color_strain_rate)
            axes[1].fill(-z, x, alpha=0.7, color=color_strain_rate)

    sm_strain = ScalarMappable(cmap=cmap, norm=norm_strain)
    sm_strain.set_array([])
    cbar = plt.colorbar(sm_strain, ax=axes[0], label="Strain")

    sm_strain_rate = ScalarMappable(cmap=cmap, norm=norm_strain_rate)
    sm_strain_rate.set_array([])
    cbar = plt.colorbar(sm_strain_rate, ax=axes[1], label="Strain Rate")

    fig.show()

    fig.show()

    root_hooks.remove_last(RollPass.DiskElement.pillar_spreads)


def test_pillar_strains_without_corner_correction(monkeypatch):
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 30)
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")
    monkeypatch.setattr(pyroll.pillar_model.Config, "ELONGATION_CORRECTION", False)
    monkeypatch.setattr(pyroll.pillar_model.Config, "CORNER_CORRECTION", False)

    with RollPass.DiskElement.pillar_spreads(pillar_spreads):
        root_hooks.add(RollPass.DiskElement.pillar_spreads)

        in_profile = Profile.round(
            diameter=19.5e-3,
            temperature=1200 + 273.15,
            strain=0,
            material=["C45", "steel"],
            flow_stress=100e6,
            density=7.5e3,
            specific_heat_capcity=690,
        )

        sequence = PassSequence(
            [
                RollPass(
                    label="Oval",
                    roll=Roll(
                        groove=CircularOvalGroove(
                            depth=5e-3,
                            r1=0.2e-3,
                            r2=16e-3,
                        ),
                        nominal_radius=160e-3,
                        rotational_frequency=1,
                        neutral_point=-20e-3
                    ),
                    gap=3e-3,
                    disk_element_count=30,
                ),

            ]
        )

    sequence.solve(in_profile)

    p_strains = []
    p_strain_rates = []
    for de in sequence[0].disk_elements:
        p_strains.append(de.out_profile.pillar_strains)
        p_strain_rates.append(de.pillar_strain_rates)

    min_strain = np.min(p_strains)
    max_strain = np.max(p_strains)

    min_strain_rates = np.min(p_strain_rates)
    max_strain_rates = np.max(p_strain_rates)

    norm_strain = mcolors.Normalize(vmin=min_strain, vmax=max_strain)
    norm_strain_rate = mcolors.Normalize(vmin=min_strain_rates, vmax=max_strain_rates)
    cmap = plt.get_cmap("hsv")

    fig, axes = plt.subplots(1, 2, figsize=(12, 8))

    axes[0].set_title("Pillar Strains")
    axes[1].set_title("Pillar Strain Rates")

    for ax in axes:
        ax.set_aspect("equal")
        ax.grid(True)
        ax.set_xlabel("$z$")
        ax.set_ylabel("$x$")
        ax.invert_yaxis()

    for de in sequence[0].disk_elements:
        for i in range(len(de.in_profile.pillars)):
            if not de.pillars_in_contact[i]:
                continue

            strain = de.out_profile.pillar_strains[i]
            color_strain = cmap(norm_strain(strain))
            color_strain_rate = cmap(norm_strain(strain))

            x = [de.in_profile.x] * 2 + [de.out_profile.x] * 2
            z = np.array([
                de.in_profile.pillar_boundaries[i + 1],
                de.in_profile.pillar_boundaries[i],
                de.out_profile.pillar_boundaries[i],
                de.out_profile.pillar_boundaries[i + 1],
            ])
            axes[0].fill(z, x, alpha=0.7, color=color_strain)
            axes[0].fill(-z, x, alpha=0.7, color=color_strain)

            axes[1].fill(z, x, alpha=0.7, color=color_strain_rate)
            axes[1].fill(-z, x, alpha=0.7, color=color_strain_rate)

    sm_strain = ScalarMappable(cmap=cmap, norm=norm_strain)
    sm_strain.set_array([])
    cbar = plt.colorbar(sm_strain, ax=axes[0], label="Strain")

    sm_strain_rate = ScalarMappable(cmap=cmap, norm=norm_strain_rate)
    sm_strain_rate.set_array([])
    cbar = plt.colorbar(sm_strain_rate, ax=axes[1], label="Strain Rate")

    fig.show()

    root_hooks.remove_last(RollPass.DiskElement.pillar_spreads)
