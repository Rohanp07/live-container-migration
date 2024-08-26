import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = '/home/rohan/Desktop/live-container-migration/checkpoint_data.csv'
data = pd.read_csv(file_path)

# Set up the plotting environment
sns.set(style="whitegrid")

# 1. Scatter Plot: Time Taken vs. CPU Usage
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Time Taken (ms)', y='CPU Usage (%)', data=data)
plt.title('Time Taken vs. CPU Usage')
plt.show()

# 2. Line Plot: Time Taken vs. CPU Usage (if data is sequential)
plt.figure(figsize=(10, 6))
sns.lineplot(x='Time Taken (ms)', y='CPU Usage (%)', data=data)
plt.title('Time Taken vs. CPU Usage (Line Plot)')
plt.show()

# 3. Scatter Plot: Time Taken vs. Dirty Memory
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Time Taken (ms)', y='Dirty Memory (bytes)', data=data)
plt.title('Time Taken vs. Dirty Memory')
plt.show()

# 4. Scatter Plot: Time Taken vs. Container Size
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Time Taken (ms)', y='Container Size (bytes)', data=data)
plt.title('Time Taken vs. Container Size')
plt.show()

# 5. Histogram: CPU Usage Distribution
plt.figure(figsize=(10, 6))
sns.histplot(data['CPU Usage (%)'], kde=True)
plt.title('CPU Usage Distribution')
plt.show()

# 6. Box Plot: CPU Usage Distribution
plt.figure(figsize=(10, 6))
sns.boxplot(x=data['CPU Usage (%)'])
plt.title('CPU Usage Distribution (Box Plot)')
plt.show()

# 7. Histogram: Dirty Memory Distribution
plt.figure(figsize=(10, 6))
sns.histplot(data['Dirty Memory (bytes)'], kde=True)
plt.title('Dirty Memory Distribution')
plt.show()

# 8. Box Plot: Dirty Memory Distribution
plt.figure(figsize=(10, 6))
sns.boxplot(x=data['Dirty Memory (bytes)'])
plt.title('Dirty Memory Distribution (Box Plot)')
plt.show()

# 9. Histogram: Container Size Distribution
plt.figure(figsize=(10, 6))
sns.histplot(data['Container Size (bytes)'], kde=True)
plt.title('Container Size Distribution')
plt.show()

# 10. Box Plot: Container Size Distribution
plt.figure(figsize=(10, 6))
sns.boxplot(x=data['Container Size (bytes)'])
plt.title('Container Size Distribution (Box Plot)')
plt.show()

# 11. Heatmap: Correlation Matrix
plt.figure(figsize=(10, 8))
corr_matrix = data.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix Heatmap')
plt.show()
