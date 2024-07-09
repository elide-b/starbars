import starbars
import matplotlib.pyplot as plt

# Example data with labels
categories = ['A', 'B', 'C']
values = [10, 20, 15]
annotations = [('A', 'B', 0.01), ('A', 'C', 0.05)]
plt.bar(categories, values)

# Annotate significance
starbars.draw_annotation(annotations)
plt.show()


# Example data with numbers
categories = [1, 2, 3]
values = [10, 20, 15]
annotations = [(2, 3, 0.01), (3, 1, 0.05)]
plt.bar(categories, values)

# Annotate significance
starbars.draw_annotation(annotations)
plt.show()