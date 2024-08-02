import logging
import webbrowser
from pathlib import Path

from pyroll.core import Profile, PassSequence, RollPass, Roll, FlatGroove
import pyroll.pillar_model


@RollPass.DiskElement.pillar_spreads
def pillar_spreads(self: RollPass.DiskElement):
    return self.pillar_draughts ** -0.5


DISK_ELEMENT_COUNT = 15
pyroll.pillar_model.Config.PILLAR_COUNT = 30


def test_solve_round_flat_equidistant(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")
    pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"

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


def test_solve_round_flat_uniform(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")
    pyroll.pillar_model.Config.PILLAR_TYPE = "UNIFORM"

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
