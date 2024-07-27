import starbars
import matplotlib.pyplot as plt

# Example data with labels and ns_show=False
categories = ['A', 'B', 'C', 'D']
values = [10, 30, 45, 5]
plt.bar(categories, values)

annotations = [('A', 'B', 0.5), ('A', 'C', 0.05)]
starbars.draw_annotation(annotations, ns_show=False)

plt.show()

# Example data with numbers
categories = [1, 2, 3]
values = [10, 20, 15]
plt.bar(categories, values)

annotations = [(2, 3, 0.01), (3, 1, 0.5)]
starbars.draw_annotation(annotations)

plt.show()

