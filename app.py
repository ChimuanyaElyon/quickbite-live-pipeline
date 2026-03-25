


# Sample data
data = {'Category': ['A', 'B', 'C', 'D'], 'Values': [25, 30, 15, 30]}
df = pd.DataFrame(data)

# Create a pie chart
plt.figure(figsize=(8, 6))
plt.pie(df['Values'], labels=df['Category'], autopct='%1.1f%%')
plt.title('Pie Chart Example')
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
