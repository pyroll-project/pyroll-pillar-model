import logging

import webbrowser
from pathlib import Path

from pyroll.core import Profile, PassSequence, RollPass, Roll, ConstrictedBoxGroove
import pyroll.pillar_model


@RollPass.DiskElement.pillar_spreads
def pillar_spreads(self: RollPass.DiskElement):
    return self.pillar_draughts ** -0.8


DISK_ELEMENT_COUNT = 15
pyroll.pillar_model.PILLAR_COUNT = 30


def test_solve_round_constricted_box_equidistant(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")
    pyroll.pillar_model.PILLAR_TYPE = "EQUIDISTANT"

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
                label="Constricted Box",
                roll=Roll(
                    groove=ConstrictedBoxGroove(
                        r1=1.805e-3,
                        r2=6.859e-3,
                        r4=31.5875e-3,
                        depth=4.9565e-3,
                        indent=0.361e-3,
                        usable_width=24.2e-3,
                        ground_width=17.5e-3,
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1,
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


def test_solve_round_constricted_box_uniform(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")
    pyroll.pillar_model.PILLAR_TYPE = "UNIFORM"

    in_profile = Profile.round(
        diameter=54e-3,
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
                label="Constricted Box",
                roll=Roll(
                    groove=ConstrictedBoxGroove(
                        r1=5e-3,
                        r2=19e-3,
                        r4=87.5e-3,
                        depth=16.5e-3,
                        indent=1e-3,
                        usable_width=70.11e-3,
                        ground_width=51.06e-3,
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1,
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