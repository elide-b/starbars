"""
Visualize statistical significance on existing Matplotlib plots by adding
significance bars and p-value labels between chosen pairs of columns.
"""

import logging
import os

import matplotlib.pyplot as plt

from ._utils import pvalue_to_asterisks, get_positions, get_starbars_logger, find_level

__version__ = "3.0.0"


DEBUG = bool(os.environ.get("DEBUG_STARBARS", False))
_logger = get_starbars_logger(logging.DEBUG if DEBUG else logging.INFO)


def draw_annotation(
    annotations,
    ax=None,
    ns_show=True,
    bar_gap=0.03,
    tip_length=0.03,
    top_margin=0.05,
    text_distance=0.02,
    fontsize=10,
    mode="vertical",
    line_width=1.5,
    color="k",
    text_args=None,
    line_args=None,
    h_gap=0.03,
):
    """
    Draw statistical significance bars and p-value labels between chosen pairs of columns on existing plots.

    :param annotations: list of tuples containing the x-axis labels and the p-value of the pair.
    :type annotations: list[tuple[float | str, float | str, float]]
    :param ax: The axis of subplots to draw annotations on. If `ax` is not provided, it implies that you are working with a single plot rather than a set of subplots. In such cases, the annotations apply to the only existing plot in the figure.
    :type ax: matplotlib.axes.Axes
    :param ns_show: whether to show non-statistical bars. (Default: True)
    :param bar_gap: margin of the bar from data. Default is 3% of the data axis.
    :param tip_length: length of the tip of the bar. Default is 3% of the data axis.
    :param top_margin: margin of the last annotation from the top of the graph. Default is 5% of the data axis.
    :param text_distance: distance between the bar and the text of the text. Default is 2% of the data axis.
    :param fontsize: font size of the annotations. Default is 10.
    :param mode: orientation of the data representation, 'horizontal' or 'vertical'. Default is 'vertical'.
    :param color: color of the annotations, as matplotlib color value. Default is black.
    :param line_width: width of the line. Default is 1.5.
    :param dict line_args: Additional dictionary of arguments which will be passed to ax.plot for drawing lines.
    :param dict text_args: Additional dictionary of arguments which will be passed to ax.text for drawing text.
    """

    if ax is None:
        ax = plt.gca()
    if line_args is None:
        line_args = {}
    if text_args is None:
        text_args = {}

    if mode == "vertical":
        annot_axis = 1
        unit_vector = (0, 1)
        get_lim = lambda: ax.get_ylim()
        set_lim = lambda *args: ax.set_ylim(*args)
    elif mode == "horizontal":
        annot_axis = 0
        unit_vector = (1, 0)
        get_lim = lambda: ax.get_xlim()
        set_lim = lambda *args: ax.set_xlim(*args)
    else:
        raise ValueError("mode must be either 'vertical' or 'horizontal' :)")

    coords_to_px = create_coordinate_transformer(ax, mode)
    px_to_coords = create_coordinate_transformer(ax, mode, True)

    # Transform the annot axis interval from (0, 0) to (0, 1) into pixels
    px_ax = (
        ax.transAxes.transform(unit_vector)[annot_axis]
        - ax.transAxes.transform((0, 0))[annot_axis]
    )

    # Get annot axis limit maximum
    annot = get_lim()[1]

    # Take annot axis limit maximum and add the first bar gap in axis pixels as starting point
    annot = px_to_coords((0, coords_to_px((0, annot))[annot_axis] + px_ax * bar_gap))[
        annot_axis
    ]
    y = ax.transData.inverted().transform(
        (0, ax.transData.transform((0, ax.get_ylim()[1]))[1] + px_ax * bar_gap)
    )[1]

    dpi = ax.figure.dpi
    text_height = (fontsize / 72) * dpi / px_ax

    # Find levels
    leveled_annotations = find_level(ax, annotations, mode)

    bars = []
    text_positions = []
    text_labels = []
    max_annot_px = 0

    # Get the positions of the values
    for annotation in leveled_annotations:
        result = calculate_bar(
            annotation,
            ns_show,
            annot,
            annot_axis,
            coords_to_px,
            px_ax,
            tip_length,
            h_gap,
            px_to_coords,
            text_distance,
            bar_gap,
            text_height,
        )
        if result:
            points, text_pos, label, bar_max = result
            bars.append(points)
            text_positions.append(text_pos)
            text_labels.append(label)
            max_annot_px = max(max_annot_px, bar_max)

    draw_bars(
        ax,
        bars,
        text_positions,
        text_labels,
        mode,
        line_width,
        color,
        fontsize,
        text_args,
        line_args,
    )


def create_coordinate_transformer(ax, mode, inverse=False):
    if inverse:
        transformation = lambda *args: ax.transData.inverted().transform(*args)
    else:
        transformation = lambda *args: ax.transData.transform(*args)

    if mode == "vertical":

        def coords_to_px(coords):
            return transformation(coords)

    else:

        def coords_to_px(coords):
            return transformation(tuple(reversed(coords)))

    return coords_to_px


def calculate_bar(
    annotation,
    ns_show,
    annot,
    annot_axis,
    coords_to_px,
    px_ax,
    tip_length,
    h_gap,
    px_to_coords,
    text_distance,
    bar_gap,
    text_height,
):
    box1_pos, box2_pos, level, pvalue = annotation

    label = pvalue_to_asterisks(pvalue)
    if label == "ns" and not ns_show:
        return

    box1_px = coords_to_px((box1_pos + h_gap / 2, annot))[+(not annot_axis)]
    box2_px = coords_to_px((box2_pos - h_gap / 2, annot))[+(not annot_axis)]
    annot_px = coords_to_px((box1_pos, annot))[annot_axis]

    bar_box = [box1_px, box1_px, box2_px, box2_px]
    level_offset = px_ax * (bar_gap + tip_length + text_distance + text_height)
    offset = annot_px + level_offset * level

    bar_annot = [
        offset,
        px_ax * tip_length + offset,
        px_ax * tip_length + offset,
        offset,
    ]

    text_pos = px_to_coords(
        (
            (box1_px + box2_px) / 2,
            px_ax * tip_length + px_ax * text_distance + offset,
        )
    )

    points = [px_to_coords((_box, _annot)) for _box, _annot in zip(bar_box, bar_annot)]

    return points, text_pos, label, annot_px + level_offset * (level + 1)


def draw_bars(
    ax,
    bars,
    text_positions,
    text_labels,
    mode,
    line_width,
    color,
    fontsize,
    text_args,
    line_args,
):

    # Draw the statistical annotation
    for bar, text_pos, label in zip(bars, text_positions, text_labels):
        ax.plot(
            [c[0] for c in bar],
            [c[1] for c in bar],
            lw=line_width,
            c=color,
            **line_args
        )
        ax.text(
            text_pos[0],
            text_pos[1],
            label,
            ha="center",
            va="center",
            fontsize=fontsize,
            color=color,
            rotation=-90 * (mode == "horizontal"),
            **text_args
        )
