import logging
import webbrowser
from pathlib import Path

import numpy as np
import pyroll.pillar_model
from pyroll.core import Profile, PassSequence, RollPass, Roll, CircularOvalGroove, Transport, RoundGroove

DISK_ELEMENT_COUNT = 15


def pillar_spreads(self: RollPass.DiskElement):
    return self.pillar_draughts ** -0.8


def test_solve(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    pyroll.pillar_model.Config.PILLAR_COUNT = 30
    pyroll.pillar_model.Config.PILLAR_TYPE = "EQUIDISTANT"

    hf = RollPass.DiskElement.pillar_spreads.add_function(pillar_spreads)

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
                label="Oval I",
                roll=Roll(
                    groove=CircularOvalGroove(
                        depth=8e-3,
                        r1=6e-3,
                        r2=40e-3
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1,
                ),
                gap=2e-3,
                disk_element_count=DISK_ELEMENT_COUNT,
            ),
            Transport(
                label="I => II",
                duration=1
            ),
            RollPass(
                label="Round II",
                roll=Roll(
                    groove=RoundGroove(
                        r1=1e-3,
                        r2=12.5e-3,
                        depth=11.5e-3
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1
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
        RollPass.DiskElement.pillar_spreads.remove_function(hf)

    try:
        from pyroll.report import report

        report = report(sequence)
        f = tmp_path / "report.html"
        f.write_text(report)
        webbrowser.open(f.as_uri())

    except ImportError:
        pass


def test_solve_uniform(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    pyroll.pillar_model.PILLAR_COUNT = 30
    pyroll.pillar_model.PILLAR_TYPE = "UNIFORM"

    hf = RollPass.DiskElement.pillar_spreads.add_function(pillar_spreads)

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
                label="Oval I",
                roll=Roll(
                    groove=CircularOvalGroove(
                        depth=8e-3,
                        r1=6e-3,
                        r2=40e-3
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1,
                ),
                gap=2e-3,
                disk_element_count=DISK_ELEMENT_COUNT,
            ),
            Transport(
                label="I => II",
                duration=1
            ),
            RollPass(
                label="Round II",
                roll=Roll(
                    groove=RoundGroove(
                        r1=1e-3,
                        r2=12.5e-3,
                        depth=11.5e-3
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1
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
        RollPass.DiskElement.pillar_spreads.remove_function(hf)

    try:
        from pyroll.report import report

        report = report(sequence)
        f = tmp_path / "report.html"
        f.write_text(report)
        webbrowser.open(f.as_uri())

    except ImportError:
        pass
