import pandas as pd
import matplotlib.pyplot as plt

file_path = './/job_data.xlsx'
final_df = pd.read_excel(file_path)

# Create a bar plot using pandas
ax = final_df['Tags'].value_counts().plot(kind='bar', figsize=(10, 6))
ax.set_title('Number of Jobs by Category')
ax.set_xlabel('Category')
ax.set_ylabel('Number of Jobs')

plt.show()
