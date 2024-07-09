# ✨ starbars ✨

This Python tool helps visualizing statistical significance on existing Matplotlib plots by adding significance bars and p-value labels between chosen pairs of columns.

## Features

- Converts p-values to asterisk notations for easy interpretation.
- Draws statistical significance bars on Matplotlib plots.
- Customizable bar margins, tip lengths, font sizes, and top margins.

## Installation

You can install the package via pip:

```bash
pip install starbars
```

### Example

```python
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
```

This example creates a simple bar plot and uses the `draw_annotation` function to add statistical significance annotations between the specified pairs.
For more detailed examples, please check the [example](https://github.com/elide-b/starbars/blob/main/example.py)
folder.

#### Parameters

- `annotations`: List of tuples `(x1, x2, p)` containing the x-axis labels and the p-value of the pair.
- `bar_margin`: Margin of the bar from data. Default is 3% of the data.
- `tip_length`: Length of the tip of the statistical bar. Default is 3% relative to data range.
- `fontsize`: Font size of the annotations.
- `top_margin`: Margin of the last annotation from the top of the graph. Default is 3% of the data.

## Contributing

We welcome contributions!
If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also
simply open an issue with the tag **"enhancement"**.

To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature-branch`)
5. Open a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
