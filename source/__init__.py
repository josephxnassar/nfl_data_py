import logging

def setup_logging(level=logging.INFO):
    logging.basicConfig(level = level,
                        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

from .statistics import Statistics
from .schedules import Schedules
from .ndpdepthchart import NDPDepthChart
from .espndepthchart import ESPNDepthChart
from .excel import Excel

__all__ = ['Statistics', 'Schedules', 'NDPDepthChart', 'ESPNDepthChart', 'Excel']