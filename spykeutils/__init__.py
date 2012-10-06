"""
:mod:`conversions` Module
-------------------------

.. automodule:: spykeutils.conversions
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`correlations` Module
--------------------------

.. automodule:: spykeutils.correlations

:mod:`progress_indicator` Module
--------------------------------

.. automodule:: spykeutils.progress_indicator
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`rate_estimation` Module
-----------------------------

.. automodule:: spykeutils.rate_estimation
    :members:
    :exclude-members: binned_spike_trains, psth, spike_density_estimation

:mod:`sorting_quality_assesment` Module
---------------------------------------

.. automodule:: spykeutils.sorting_quality_assesment
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`staionarity` Module
-------------------------

.. automodule:: spykeutils.stationarity
    :members:
    :exclude-members: spike_amplitude_histogram

:mod:`spyke_exception` Module
-----------------------------

.. automodule:: spykeutils.spyke_exception
    :members:
    :undoc-members:
    :show-inheritance:
"""

__version__ = '0.1.1'

class SpykeException(Exception):
    """ Exception thrown when a function in spykeutils encounters a
        problem that is not covered by standard exceptions.

        When using Spyke Viewer, these exceptions will be caught and
        shown in the GUI, while general exceptions will not be caught
        (and therefore be visible in the console) for easier
        debugging.
    """
    pass