.. starbars documentation master file, created by
   sphinx-quickstart on Sat Jul  6 12:03:10 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ✨ starbars' ✨ documentation!
==========================================

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   starbars
   examples/examples


This Python tool helps visualize statistical significance on existing Matplotlib plots by adding significance bars and p-value labels between chosen pairs of columns.

Features
========

- Converts p-values to asterisk notations for easy interpretation.
- Draws statistical significance bars on Matplotlib plots.
- Customizable bar margins, tip lengths, font sizes, and top margins.
- More features to ✨ come ✨.

Installation
============

You can install the package via pip:

.. code-block:: bash

   pip install starbars

Parameters
==========

- ``annotations``: List of tuples `(x1, x2, p)` containing the x-axis labels and the p-value of the pair.
- ``ax``: The axis of subplots to draw annotations on. If `ax` is not provided, it implies that you are working with a single plot rather than a set of subplots. In such cases, the annotations apply to the only existing plot in the figure.
- ``ns_show``: Whether to show bars for non-statistical pvalues. (Default: True)
- ``bar_gap``: Gap in between the bars of data. Default is 3% of the y-axis.
- ``tip_length``: Length of the tip of the statistical bar. Default is 3% of the y-axis.
- ``top_margin``: Margin of the last annotation from the top of the graph. Default is 5% of the y-axis.
- ``text_distance``: Distance between the bar and the text. Default is 2% of the y-axis.
- ``fontsize``: Font size of the annotations. Default is 10.

Example
=======

.. plot::
   :include-source:


   import starbars
   import matplotlib.pyplot as plt

   # Example data
   categories = ['A', 'B', 'C']
   values = [10, 20, 15]
   annotations = [('A', 'B', 0.01), ('B', 'C', 0.05)]

   plt.bar(categories, values)

   # Annotate significance
   starbars.draw_annotation(annotations)

   plt.show()

Custom labels
=============

If you prefer different labels on the annotation bars, instead of passing your p-value,
you may also pass any string you'd like. Starbars will then render it:

.. plot::
   :include-source:


   import starbars
   import matplotlib.pyplot as plt

   # Example data
   categories = ['A', 'B', 'C']
   values = [10, 20, 18]
   annotations = [('A', 'B', 'p < 0.01'), ('B', 'C', 'not significant :(')]

   plt.bar(categories, values)

   # Annotate significance
   starbars.draw_annotation(annotations)

   plt.show()


License
=======

This project is licensed under the MIT License. See the LICENSE file for more details.
