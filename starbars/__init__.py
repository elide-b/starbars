"""
Visualize statistical significance on existing Matplotlib plots by adding
significance bars and p-value labels between chosen pairs of columns.
"""

import matplotlib.pyplot as plt

from .utils import pvalue_to_asterisks, get_positions

__version__ = "2.0.1"


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
):
    """
    Draw statistical significance bars and p-value labels between chosen pairs of columns on existing plots.

    :param annotations: list of tuples containing the x-axis labels and the p-value of the pair.
    :type annotations: list[tuple[float | str, float | str, float]]
    :param ax: The axis of subplots to draw annotations on. If `ax` is not provided, it implies that you are working with a single plot rather than a set of subplots. In such cases, the annotations apply to the only existing plot in the figure.
    :type ax: matplotlib.axes.Axes
    :param ns_show: whether to show non-statistical bars. (Default: True)
    :param bar_gap: margin of the bar from data. Default is 3% of the y-axis.
    :param top_margin: margin of the last annotation from the top of the graph. Default is 5% of the y-axis.
    :param text_distance: distance between the bar and the text of the text. Default is 2% of the y-axis.
    :param fontsize: font size of the annotations. Default is 10.
    """
    if ax is None:
        ax = plt.gca()

    if mode == "vertical":
        annot_axis = 1
        unit_vector = (0, 1)
        get_lim = lambda: ax.get_ylim()
        set_lim = lambda *args: ax.set_ylim(*args)
    elif mode == "horizontal":
        annot_axis = 0
        unit_vector = (1, 0)
        get_lim = lambda: ax.get_xlim()
        set_lim = lambda *args: ax.get_xlim(*args)
    else:
        raise ValueError("mode must be either 'vertical' or 'horizontal' :)")

    coords_to_px = create_coordinate_transformer(ax, mode)
    px_to_coords = create_coordinate_transformer(ax, mode, True)

    dpi = ax.figure.dpi
    px_txt = (fontsize / 72) * dpi
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

    bars = []
    text_positions = []
    text_labels = []

    # Get the positions of the values
    for box1, box2, pvalue in annotations:
        label = pvalue_to_asterisks(pvalue)
        if label == "ns" and not ns_show:
            continue
        box1_position, box2_position = get_positions(ax, box1, box2, mode)
        box1_px = coords_to_px((box1_position, annot))[+(not annot_axis)]
        box2_px = coords_to_px((box2_position, annot))[+(not annot_axis)]
        annot_px = coords_to_px((box1_position, annot))[annot_axis]

        bar_box = [box1_px, box1_px, box2_px, box2_px]
        bar_annot = [
            annot_px,
            px_ax * tip_length + annot_px,
            px_ax * tip_length + annot_px,
            annot_px,
        ]
        text_pos = px_to_coords(
            (
                (box1_px + box2_px) / 2,
                px_ax * tip_length + annot_px + px_ax * text_distance,
            )
        )

        points = [
            px_to_coords((_box, _annot)) for _box, _annot in zip(bar_box, bar_annot)
        ]
        bars.append(points)
        text_positions.append(text_pos)
        text_labels.append(label)

        # Move up the annot point to the next bar's start annot
        annot = px_to_coords(
            (box1_px, annot_px + px_ax * tip_length + px_ax * bar_gap + px_txt)
        )[annot_axis]

    # Draw the statistical annotation
    for bar, text_pos, label in zip(bars, text_positions, text_labels):
        ax.plot([c[0] for c in bar], [c[1] for c in bar], lw=1.5, c="k")
        ax.text(
            text_pos[0],
            text_pos[1],
            label,
            ha="center",
            va="center",
            fontsize=fontsize,
            color="k",
            rotation=90 * (mode == "horizontal"),
        )

    if len(annotations) == 0:
        return

    # Adjust the annot axis limit of the current subplot to accommodate the top margin
    annot_px = coords_to_px((box1_position, annot))[annot_axis]
    annot_final = px_to_coords((0, annot_px + px_ax * top_margin))[annot_axis]
    annot = px_to_coords((0, coords_to_px((0, annot_final))[annot_axis]))[annot_axis]

    # If final annotation is out of bounds, adjust the annot limit to include it.
    if annot_final > 1:
        annot0, annot_max = get_lim()
        set_lim(annot0, annot)


def create_coordinate_transformer(ax, mode, inverse=False):
    if inverse:
        transformation = ax.transData.inverted().transform
    else:
        transformation = ax.transData.transform

    if mode == "vertical":

        def coords_to_px(coords):
            return transformation(coords)

    else:

        def coords_to_px(coords):
            return transformation(coords.reversed())

    return coords_to_px
