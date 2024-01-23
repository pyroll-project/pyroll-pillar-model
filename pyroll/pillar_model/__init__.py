import importlib.util

from . import profile
from . import roll_pass

VERSION = "2.1.3"

from pyroll.core import config as _config


@_config("PYROLL_PILLAR_MODEL")
class Config:
    PILLAR_COUNT = 30
    PILLAR_TYPE = "EQUIDISTANT"
    ELONGATION_CORRECTION = True


REPORT_INSTALLED = bool(importlib.util.find_spec("pyroll.report"))

if REPORT_INSTALLED:
    from . import report
    import pyroll.report

    pyroll.report.plugin_manager.register(report)
