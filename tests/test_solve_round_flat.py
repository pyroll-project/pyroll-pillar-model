import logging
import webbrowser
import pyroll.pillar_model

from pathlib import Path
from pyroll.core import Profile, PassSequence, RollPass, Roll, FlatGroove, root_hooks


def pillar_spreads(self: RollPass.DiskElement):
    return self.pillar_draughts ** -0.5


def test_solve_round_flat_equidistant(tmp_path: Path, caplog, monkeypatch):
    caplog.set_level(logging.INFO, logger="pyroll")
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "EQUIDISTANT")
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 30)

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
                    label="Flat",
                    roll=Roll(
                        groove=FlatGroove(
                            usable_width=40e-3,
                        ),
                        nominal_radius=160e-3,
                        rotational_frequency=1,
                        neutral_point=-20e-3
                    ),
                    gap=10e-3,
                    disk_element_count=15,
                ),

            ]
        )

    try:
        sequence.solve(in_profile)
    finally:
        print("\nLog:")
        print(caplog.text)
        root_hooks.remove_last(RollPass.DiskElement.pillar_spreads)
    try:
        from pyroll.report import report

        report = report(sequence)
        f = tmp_path / "report.html"
        f.write_text(report, encoding="utf-8")
        webbrowser.open(f.as_uri())

    except ImportError:
        pass



def test_solve_round_flat_uniform(tmp_path: Path, caplog, monkeypatch):
    caplog.set_level(logging.INFO, logger="pyroll")
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_TYPE", "UNIFORM")
    monkeypatch.setattr(pyroll.pillar_model.Config, "PILLAR_COUNT", 30)

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
                label="Flat",
                roll=Roll(
                    groove=FlatGroove(
                        usable_width=40e-3,
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1,
                    neutral_point=-20e-3
                ),
                gap=10e-3,
                disk_element_count=15,
            ),

        ]
    )

    try:
        sequence.solve(in_profile)
    finally:
        print("\nLog:")
        print(caplog.text)
        root_hooks.remove_last(RollPass.DiskElement.pillar_spreads)
    try:
        from pyroll.report import report

        report = report(sequence)
        f = tmp_path / "report.html"
        f.write_text(report, encoding="utf-8")
        webbrowser.open(f.as_uri())

    except ImportError:
        pass


