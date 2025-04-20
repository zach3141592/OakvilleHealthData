import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv('DataAnalysis/flu_data_new.csv')

# Convert date strings to datetime objects
df['Date'] = pd.to_datetime(df['Date'])

# Create a new column with numeric representation of dates (days since start)
start_date = df['Date'].min()
df['Days_Since_Start'] = (df['Date'] - start_date).dt.days

# Group by date and count flu shots
daily_counts = df.groupby('Date').size().reset_index(name='Shot_Count')
daily_counts['Days_Since_Start'] = (daily_counts['Date'] - start_date).dt.days

# Prepare data for regression
X = daily_counts[['Days_Since_Start']]
y = daily_counts['Shot_Count']

# Create and fit the regression model
model = LinearRegression()
model.fit(X, y)

# Make predictions
predictions = model.predict(X)

# Print model coefficients
print(f"Slope (shots per day): {model.coef_[0]:.2f}")
print(f"Intercept: {model.intercept_:.2f}")
print(f"R-squared score: {model.score(X, y):.2f}")

# Plot the results
plt.figure(figsize=(10, 6))
plt.scatter(daily_counts['Days_Since_Start'], daily_counts['Shot_Count'], alpha=0.5, label='Actual Data')
plt.plot(daily_counts['Days_Since_Start'], predictions, color='red', label='Regression Line')
plt.xlabel('Days Since Start')
plt.ylabel('Number of Flu Shots')
plt.title('Flu Shot Trend Over Time')
plt.legend()
plt.grid(True)
plt.savefig('DataAnalysis/flu_shot_trend.png')
plt.close()

# Print summary statistics
print("\nSummary Statistics:")
print(f"Total number of flu shots: {len(df)}")
print(f"Average shots per day: {daily_counts['Shot_Count'].mean():.2f}")
print(f"Maximum shots in a day: {daily_counts['Shot_Count'].max()}")
print(f"Minimum shots in a day: {daily_counts['Shot_Count'].min()}")

