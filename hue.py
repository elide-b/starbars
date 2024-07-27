import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

import starbars

# Create a simple dataset
data = {
    'Student': ['A', 'B', 'C', 'D', 'E', 'F'],
    'Score': [85, 90, 88, 72, 95, 78],
    'Subject': ['Math', 'Math', 'Science', 'Science', 'Math', 'Science'],
    'Gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female']
}

# Convert the dataset into a DataFrame
df = pd.DataFrame(data)

# Create a bar plot with hue
plt.figure(figsize=(8, 6))
plot = sns.barplot(data=df, x='Subject', y='Score', hue='Gender', palette='deep')


subjects = df['Subject'].unique()
pairs = []

handles, labels = plot.get_legend_handles_labels()
print(handles, labels)
# Get the order of subjects from the x-axis labels
subject_order = [t.get_text() for t in plot.get_xticklabels()]

# for subject in subjects:
#     male_scores = df[(df['Subject'] == subject) & (df['Gender'] == 'Male')]['Score']
#     female_scores = df[(df['Subject'] == subject) & (df['Gender'] == 'Female')]['Score']
#     t_stat, p_value = stats.ttest_ind(male_scores, female_scores, equal_var=False)
#     pairs.append(('Male', 'Female', p_value))
#     print(f"T-test for {subject}: t-statistic = {t_stat}, p-value = {p_value}")
#
# starbars.draw_annotation(pairs)

# Add titles and labels
plt.title("Average Scores by Subject and Gender")
plt.xlabel("Subject")
plt.ylabel("Score")


# Show the plot
plt.show()