import importlib.util

from . import profile
from . import roll_pass

VERSION = "2.0.0"
PILLAR_COUNT = 11

REPORT_INSTALLED = bool(importlib.util.find_spec("pyroll.report"))

if REPORT_INSTALLED:
    from . import report
    import pyroll.report

    pyroll.report.plugin_manager.register(report)
