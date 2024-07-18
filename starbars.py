"""
Visualize statistical significance on existing Matplotlib plots by adding
significance bars and p-value labels between chosen pairs of columns.
"""

import matplotlib.pyplot as plt

__version__ = "1.1.1"


def pvalue_to_asterisks(pvalue):
    if pvalue <= 0.0001:
        return "****"
    elif pvalue <= 0.001:
        return "***"
    elif pvalue <= 0.01:
        return "**"
    elif pvalue <= 0.05:
        return "*"
    return "ns"


def draw_annotation(annotations, ns_show=True, bar_margin=0.03, tip_length=0.03, fontsize=10, top_margin=0.03):
    """
    Draw statistical significance bars and p-value labels between chosen pairs of columns on existing plots.

    :param annotations: list of tuples containing the x-axis labels and the p-value of the pair.
    :type annotations: list[tuple[float | str, float | str, float]]
    :param ns_show: whether to show non-statistical bars. (Default: True)
    :param bar_margin: margin of the bar from data. Default is 3% of the data.
    :param tip_length: length of the tip of the statistical bar. Default is 3% relative to data range.
    :param fontsize: font size of the annotations.
    :param top_margin: margin of the last annotation from the top of the graph. Default is 3% of the data.
    """

    y_min, y_max = plt.gcf().axes[0].get_ylim()
    height = y_max
    for (x1, x2, pvalue) in annotations:
        tick_positions = plt.gca().get_xticks()
        tick_labels = [tick.get_text() for tick in plt.gca().get_xticklabels()]
        try:
            x1_position = tick_positions[tick_labels.index(x1)]
            x2_position = tick_positions[tick_labels.index(x2)]
        except ValueError:
            x1_position = x1
            x2_position = x2
        y1 = height + bar_margin * 0.8 * (height - y_min)
        h = tip_length * 0.8 * (height - y_min)
        col = 'k'
        if ns_show:
            plt.plot([x1_position, x1_position, x2_position, x2_position], [y1, y1 + h, y1 + h, y1], lw=1.5, c=col)
            height = y1 + 2.5 * h
            plt.text((x1_position + x2_position) * .5, y1 + h + bar_margin, pvalue_to_asterisks(pvalue), ha='center',
                         va='bottom', color=col, fontsize=fontsize)
        else:
            if pvalue_to_asterisks(pvalue) == 'ns':
                pass
            else:
                plt.plot([x1_position, x1_position, x2_position, x2_position], [y1, y1 + h, y1 + h, y1], lw=1.5, c=col)
                height = y1 + 2.5 * h
                plt.text((x1_position + x2_position) * .5, y1 + h + bar_margin, pvalue_to_asterisks(pvalue),
                         ha='center',
                         va='bottom', color=col, fontsize=fontsize)

    y_min, y_max = plt.gcf().axes[0].get_ylim()
    plt.gcf().axes[0].set_ylim(y_min, y_max + top_margin * (y_max - y_min))
