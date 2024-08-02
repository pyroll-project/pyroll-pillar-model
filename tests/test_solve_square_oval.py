import logging
import webbrowser
from pathlib import Path

from pyroll.core import Profile, PassSequence, RollPass, Roll, CircularOvalGroove, Transport, RoundGroove

import pyroll.pillar_model


@RollPass.DiskElement.pillar_spreads
def pillar_spreads(self: RollPass.DiskElement):
    return self.pillar_draughts ** -0.8


DISK_ELEMENT_COUNT = 15
pyroll.pillar_model.Config.PILLAR_COUNT = 30


def test_solve_square_oval_equidistant_pillars(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")
    pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"

    in_profile = Profile.square(
        side=24e-3,
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
                        depth=8e-3,
                        r1=6e-3,
                        r2=40e-3
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1,
                    neutral_point=-20e-3
                ),
                gap=2e-3,
                disk_element_count=DISK_ELEMENT_COUNT,
            ),

        ]
    )
    try:
        sequence.solve(in_profile)
    finally:
        print("\nLog:")
        print(caplog.text)

    try:
        from pyroll.report import report

        report = report(sequence)
        f = tmp_path / "report.html"
        f.write_text(report)
        webbrowser.open(f.as_uri())

    except ImportError:
        pass


def test_solve_square_oval_uniform_pillars(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")

    pyroll.pillar_model.Config.PILLAR_TYPE = "UNIFORM"

    in_profile = Profile.square(
        side=24e-3,
        temperature=1200 + 273.15,
        strain=0,
        material=["C45", "steel"],
        flow_stress=100e6,
        density=7.5e3,
        thermal_capacity=690,
    )

    sequence = PassSequence(
        [
            RollPass(
                label="Oval",
                roll=Roll(
                    groove=CircularOvalGroove(
                        depth=8e-3,
                        r1=6e-3,
                        r2=40e-3
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1,
                    neutral_point=-20e-3
                ),
                gap=2e-3,
                disk_element_count=DISK_ELEMENT_COUNT,
            ),
        ]
    )

    try:
        sequence.solve(in_profile)
    finally:
        print("\nLog:")
        print(caplog.text)

    try:
        from pyroll.report import report

        report = report(sequence)
        f = tmp_path / "report.html"
        f.write_text(report)
        webbrowser.open(f.as_uri())

    except ImportError:
        pass
