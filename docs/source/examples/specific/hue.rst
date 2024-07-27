Plots with hue
==============

When using Seaborn plots with hue, pairs can be specified by including the hue label and its corresponding group in the tuple. These should then be combined with the other label, group tuple, and the p-value in the final tuple `((hue_label1, group1), (hue_label2, group2), pvalue)`.
For example:

.. plot:: ../../examples/hue.py
   :include-source: True
   :scale: 80