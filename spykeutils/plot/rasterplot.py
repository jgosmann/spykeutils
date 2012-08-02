import scipy as sp

from guiqwt.builder import make
from guiqwt.baseplot import BasePlot
from guiqwt.plot import BaseCurveWidget

import neo
import quantities as pq

from dialogs import PlotDialog
import helper
from spykeutils.spyke_exception import SpykeException

@helper.needs_qt
def raster_plot(trains, unit=None, show_lines=True, events=None):
    """ Create a new plotting window with a rasterplot of spiketrains

        :param dict trains: Dictionary of spike trains indexed by a
            Neo object (`Unit` or `Segment`)
        :param Quantity unit: Unit of X-Axis. If None, milliseconds are
            used.
        :param bool show_lines: Determines if a horizontal line is shown
            for each spike train
        :param sequence events: A sequence of neo `Event` objects that will
            be marked on the plot

    """
    if not trains:
        raise SpykeException('No spike trains for rasterplot')

    if not unit:
        unit = pq.ms

    win_title = 'Spike Trains'
    win = PlotDialog(toolbar=True, wintitle=win_title)
    trial_length = None
    if show_lines:
        trial_length = max([t.t_stop - t.t_start for t in trains.itervalues()])
        trial_length.units = unit
    _spike_trains_plot(win, trains, unit, trial_length, events)

def _spike_trains_plot(win, trains, unit, trial_length, events):
    pW = BaseCurveWidget(win)
    plot = pW.plot

    if events is None:
        events = []

    offset = len(trains)
    legend_items = []
    for u, t in sorted(trains.iteritems(), key=lambda (u,v):u.name):
        if not unit:
            unit = t.units
            t2 = t
        else:
            t2 = t.rescale(unit)

        color = helper.get_unit_color(u)

        train = make.curve(t2, sp.zeros(len(trains[u])) + offset,
            u.name, 'k', 'NoPen', linewidth=1, marker='Rect',
            markerfacecolor=color, markeredgecolor=color)

        s = train.symbol()
        s.setSize(1, 21)
        train.setSymbol(s)
        plot.add_item(train)
        if u.name:
            legend_items.append(train)
        if trial_length:
            plot.add_item(make.curve([0, trial_length], [offset, offset], color='k'))
        offset -= 1

    # Copy events in order to not modify originals
    evts = [neo.Event(e.time.rescale(unit), e.label) for e in events]
    helper.add_markers(plot, evts)

    plot.set_axis_title(BasePlot.X_BOTTOM, 'Time')
    plot.set_axis_unit(BasePlot.X_BOTTOM, unit.dimensionality.string)

    win.add_plot_widget(pW, 0)

    legend = make.legend(restrict_items=legend_items)
    plot.add_item(legend)
    win.add_legend_option([legend], True)

    if len(trains) > 1:
        plot.set_axis_limits(BasePlot.Y_LEFT, 0.5, len(trains) + 0.5)

    win.add_custom_curve_tools()
    win.show()

if __name__ == '__main__':
    import guidata
    import quantities as pq
    app = guidata.qapplication()

    unit1 = neo.Unit('Unit 1')
    unit1.annotate(unique_id=1)
    unit2 = neo.Unit('Unit 2')
    unit2.annotate(unique_id=2)

    train1 = neo.SpikeTrain(sp.arange(50)*2, units='s', t_stop=100)
    train1.unit = unit1
    train2 = neo.SpikeTrain(sp.arange(21)*5000, units='ms', t_stop=100000)
    train2.unit = unit2

    raster_plot({unit1:train1, unit2:train2}, pq.s)
    app.exec_()