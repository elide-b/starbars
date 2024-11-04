import matplotlib.pyplot as plt
import starbars

# Example data
categories = ["A", "B", "C", "D"]
values = [3, 7, 2, 5]

# Create a horizontal bar plot
plt.barh(categories, values, color="skyblue")

# Add annotations
annotations = [("A", "B", 0.01), ("B", "C", 0.5), ("A", "C", 0.0002)]
starbars.draw_annotation(annotations, mode="horizontal")

# Add labels and title
plt.xlabel("Values")
plt.ylabel("Categories")
plt.title("Horizontal Bar Plot Example")

# Show plot
plt.show()
