.. starbars documentation master file, created by
   sphinx-quickstart on Sat Jul  6 12:03:10 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ✨ starbars' ✨ documentation!
==========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   starbars


This Python tool helps visualize statistical significance on existing Matplotlib plots by adding significance bars and p-value labels between chosen pairs of columns.

Features
========

- Converts p-values to asterisk notations for easy interpretation.
- Draws statistical significance bars on Matplotlib plots.
- Customizable bar margins, tip lengths, font sizes, and top margins.
- More features to ✨ come ✨

Installation
============

You can install the package via pip:

.. code-block:: bash

   pip install starbars

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



Parameters
==========

- ``annotations``: List of tuples `(x1, x2, p)` containing the x-axis labels and the p-value of the pair.
- ``bar_margin``: Margin of the bar from data. Default is 3% of the data.
- ``tip_length``: Length of the tip of the statistical bar. Default is 3% relative to data range.
- ``fontsize``: Font size of the annotations.
- ``top_margin``: Margin of the last annotation from the top of the graph. Default is 3% of the data.

License
=======

This project is licensed under the MIT License. See the LICENSE file for more details.
