"""
Visualize statistical significance on existing Matplotlib plots by adding
significance bars and p-value labels between chosen pairs of columns.
"""

import matplotlib.pyplot as plt

from .utils import pvalue_to_asterisks, get_positions

__version__ = "2.0.0"


def draw_annotation(
    annotations,
    ax=None,
    ns_show=True,
    bar_gap=0.03,
    tip_length=0.03,
    top_margin=0.05,
    text_distance=0.02,
    fontsize=10,
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

    dpi = ax.figure.dpi
    px_txt = (fontsize / 72) * dpi
    px_ax = ax.transAxes.transform((0, 1))[1] - ax.transAxes.transform((0, 0))[1]
    y = ax.get_ylim()[1]
    y = ax.transData.inverted().transform(
        (0, ax.transData.transform((0, y))[1] + px_ax * bar_gap)
    )[1]

    bars = []
    texts = []

    # Get the positions of the values
    for x1, x2, pvalue in annotations:
        x1_position, x2_position = get_positions(ax, x1, x2)
        x1_px = ax.transData.transform((x1_position, y))[0]
        x2_px = ax.transData.transform((x2_position, y))[0]
        y_px = ax.transData.transform((x1_position, y))[1]

        bar_x = [x1_px, x1_px, x2_px, x2_px]
        bar_y = [y_px, px_ax * tip_length + y_px, px_ax * tip_length + y_px, y_px]
        text = ax.transData.inverted().transform(
            ((x1_px + x2_px) / 2, px_ax * tip_length + y_px + px_ax * text_distance)
        )

        points = [
            ax.transData.inverted().transform((_x, _y)) for _x, _y in zip(bar_x, bar_y)
        ]
        bars.append(points)
        texts.append(text)

        # Move up the y point to the next bar's start y
        y = ax.transData.inverted().transform(
            (x1_px, y_px + px_ax * tip_length + px_ax * bar_gap + px_txt)
        )[1]

    # Draw the statistical annotation
    for bar, text, (_, _, pvalue) in zip(bars, texts, annotations):
        ax.plot([c[0] for c in bar], [c[1] for c in bar], lw=1.5, c="k")
        if ns_show or pvalue != "ns":
            ax.text(
                text[0],
                text[1],
                pvalue_to_asterisks(pvalue),
                ha="center",
                va="center",
                fontsize=fontsize,
                color="k",
            )

    if len(annotations) == 0:
        return

    # Adjust the y-axis limit of the current subplot to accommodate the top margin
    y_px = ax.transData.transform((x1_position, y))[1]
    y_final = ax.transAxes.inverted().transform((0, y_px + px_ax * top_margin))[1]
    y = ax.transData.inverted().transform((0, ax.transAxes.transform((0, y_final))[1]))[
        1
    ]

    if y_final > 1:
        y0, ym = ax.get_ylim()
        ax.set_ylim(y0, y)
