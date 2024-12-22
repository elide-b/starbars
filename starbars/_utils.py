import itertools
import logging

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


def get_tick_position(ax, box1, box2, mode):
    if mode == "vertical":
        tick_positions = ax.get_xticks()
        tick_labels = [tick.get_text() for tick in ax.get_xticklabels()]
    else:
        tick_positions = ax.get_yticks()
        tick_labels = [tick.get_text() for tick in ax.get_yticklabels()]
    try:
        position1 = tick_positions[tick_labels.index(box1)]
        position2 = tick_positions[tick_labels.index(box2)]
    except ValueError:
        position1 = box1
        position2 = box2

    return position1, position2


def get_positions(ax, box1, box2, mode):
    try:
        if check_tuples(box1, box2):
            pass
    except ValueError as e:
        print(f"Validation error: {e}")
        exit()

    if isinstance(box1, tuple) and isinstance(box2, tuple):
        box1, group1 = box1
        box2, group2 = box2
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

            # Get the box positions and hue labels from the patches
            bar_positions = {label: [] for label in hue_labels}
            for i, patch in enumerate(ax.patches[: group_count * hue_count]):
                hue_label = patch_to_hue[i]
                bbox = (
                    patch.get_path().get_extents()
                    if isinstance(patch, PathPatch)
                    else patch.get_bbox()
                )
                if mode == "vertical":
                    bar_positions[hue_label].append(bbox.x0 + (bbox.width / 2))
                else:
                    bar_positions[hue_label].append(bbox.y0 + (bbox.height / 2))

            # Clean up the positions
            cleaned_positions = {
                key: [
                    float(value) if isinstance(value, np.float64) else value
                    for value in values
                ]
                for key, values in bar_positions.items()
            }

            group1_position, group2_position = get_tick_position(
                ax, group1, group2, mode
            )

            position1 = cleaned_positions[box1][group1_position]
            position2 = cleaned_positions[box2][group2_position]

    else:
        position1, position2 = get_tick_position(ax, box1, box2, mode)

    return position1, position2


def get_starbars_logger(level):
    logger = logging.getLogger("✨starbars✨")
    logger.setLevel(level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


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
