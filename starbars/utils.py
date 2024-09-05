import itertools

import numpy as np
from matplotlib.patches import PathPatch


def check_tuples(x1, x2):
    # Check if both x1 and x2 are tuples or neither are tuples
    if (isinstance(x1, tuple) and not isinstance(x2, tuple)) or (
        not isinstance(x1, tuple) and isinstance(x2, tuple)
    ):
        raise ValueError(
            "Both variables must either be tuples or neither must be tuples."
        )

    return True


def pvalue_to_asterisks(pvalue):
    try:
        pvalue = float(pvalue)
    except ValueError:
        return pvalue
    else:
        if pvalue <= 0.0001:
            return "****"
        elif pvalue <= 0.001:
            return "***"
        elif pvalue <= 0.01:
            return "**"
        elif pvalue <= 0.05:
            return "*"
        else:
            return "ns"


def get_tick_position(ax, x1, x2):
    tick_positions = ax.get_xticks()
    tick_labels = [tick.get_text() for tick in ax.get_xticklabels()]
    try:
        x1_position = tick_positions[tick_labels.index(x1)]
        x2_position = tick_positions[tick_labels.index(x2)]
    except ValueError:
        x1_position = x1
        x2_position = x2

    return x1_position, x2_position


def get_positions(ax, x1, x2):
    try:
        if check_tuples(x1, x2):
            pass
    except ValueError as e:
        print(f"Validation error: {e}")
        exit()

    if isinstance(x1, tuple) and isinstance(x2, tuple):
        x1, group1 = x1
        x2, group2 = x2
        legend = ax.get_legend()
        if legend:
            hue_labels = [text.get_text() for text in legend.get_texts()]
            hue_count = len(hue_labels)
            # Calculate amount of groups: (n_patches - legend_patches) / n_hues
            group_count = (len(ax.patches) - hue_count) // hue_count
            patch_to_hue = [
                *itertools.chain.from_iterable(
                    [label] * group_count for label in hue_labels
                )
            ]

            # Get the x positions and hue labels from the patches
            bar_positions = {label: [] for label in hue_labels}
            for i, patch in enumerate(ax.patches[: group_count * hue_count]):
                hue_label = patch_to_hue[i]
                bbox = (
                    patch.get_path().get_extents()
                    if isinstance(patch, PathPatch)
                    else patch.get_bbox()
                )
                bar_positions[hue_label].append(bbox.x0 + (bbox.width / 2))

            # Clean up the positions
            cleaned_positions = {
                key: [
                    float(value) if isinstance(value, np.float64) else value
                    for value in values
                ]
                for key, values in bar_positions.items()
            }

            group1_position, group2_position = get_tick_position(ax, group1, group2)

            x1_position = cleaned_positions[x1][group1_position]
            x2_position = cleaned_positions[x2][group2_position]

    else:
        x1_position, x2_position = get_tick_position(ax, x1, x2)

    return x1_position, x2_position
