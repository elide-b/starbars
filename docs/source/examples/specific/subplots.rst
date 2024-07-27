Subplots examples
=================

In Matplotlib, ax represents an individual subplot or axis in a figure. When working with multiple subplots, you can use the ax argument in the `draw_annotation` function to specify which subplot you want to annotate.
If you do not specify the `ax` argument, it implies that you are working with a single plot rather than a set of subplots. In such cases, the annotations apply to the only existing plot in the figure.

.. plot:: ../../examples/subplots.py
   :include-source: True
   :scale: 60