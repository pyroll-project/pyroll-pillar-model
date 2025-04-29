import logging
import webbrowser
import pyroll.pillar_model

from pathlib import Path
from pyroll.core import Profile, PassSequence, RollPass, Roll, CircularOvalGroove, RoundGroove, Transport, root_hooks


def pillar_spreads(self: RollPass.DiskElement):
    return self.pillar_draughts ** -0.3


def test_solve_round_oval_round_equidistant(tmp_path: Path, caplog, monkeypatch):
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
                    label="Oval",
                    roll=Roll(
                        groove=CircularOvalGroove(
                            depth=5e-3,
                            r1=1e-3,
                            r2=20e-3,
                        ),
                        nominal_radius=160e-3,
                        rotational_frequency=1,
                        neutral_point=-20e-3
                    ),
                    gap=4e-3,
                    disk_element_count=15,
                ),
                Transport(duration=1),
                RollPass(
                    label="Round",
                    roll=Roll(
                        groove=RoundGroove(
                            depth=8e-3,
                            r1=1e-3,
                            r2=9e-3,
                        ),
                        nominal_radius=160e-3,
                        rotational_frequency=1,
                        neutral_point=-20e-3
                    ),
                    gap=2e-3,
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



def test_solve_round_oval_round_uniform(tmp_path: Path, caplog, monkeypatch):
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
                    label="Oval",
                    roll=Roll(
                        groove=CircularOvalGroove(
                            depth=5e-3,
                            r1=1e-3,
                            r2=20e-3,
                        ),
                        nominal_radius=160e-3,
                        rotational_frequency=1,
                        neutral_point=-20e-3
                    ),
                    gap=4e-3,
                    disk_element_count=15,
                ),
                Transport(duration=1),
                RollPass(
                    label="Round",
                    roll=Roll(
                        groove=RoundGroove(
                            depth=8e-3,
                            r1=1e-3,
                            r2=9e-3,
                        ),
                        nominal_radius=160e-3,
                        rotational_frequency=1,
                        neutral_point=-20e-3
                    ),
                    gap=2e-3,
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

