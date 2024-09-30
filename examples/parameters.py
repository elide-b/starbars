import starbars
import matplotlib.pyplot as plt

# Define fun categories and their corresponding values
categories = [
    "Dragon Eggs",
    "Phoenix Feathers",
    "Unicorn Horns",
    "Mermaid Scales",
    "Fairy Dust",
]
values = [20, 15, 30, 10, 25]

# Create a figure and axis
fig, ax = plt.subplots(figsize=(8, 6))

# Plot bar chart
ax.bar(categories, values, color="purple", alpha=0.7)

annotations = [
    ("Dragon Eggs", "Phoenix Feathers", 0.01),
    ("Unicorn Horns", "Dragon Eggs", 0.0003),
    ("Fairy Dust", "Phoenix Feathers", 0.02),
]
starbars.draw_annotation(annotations, top_margin=0.06, text_distance=0.03, bar_gap=0.05)

ax.set_title("Magical Inventory")
ax.set_xlabel("Magical Items")
ax.set_ylabel("Quantity")

# Show the plot
plt.show()
