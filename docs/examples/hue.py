import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import starbars

# Example with hue used in plots
data = {
    'Student': ['A', 'B', 'C', 'D', 'E', 'F'],
    'Score': [85, 90, 88, 72, 95, 78],
    'Subject': ['Math', 'Math', 'Science', 'Science', 'Math', 'Science'],
    'Gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female']
}
df = pd.DataFrame(data)
plt.figure(figsize=(8, 6))
plot = sns.barplot(data=df, x='Subject', y='Score', hue='Gender', palette='deep')
plt.title("Average Scores by Subject and Gender")
plt.xlabel("Subject")
plt.ylabel("Score")

annotations = [(('Male', 'Math'), ('Female', 'Science'), 0.01), ('Science', 'Math', 0.03)]
starbars.draw_annotation(annotations)

plt.show()
