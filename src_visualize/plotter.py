import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_algorithm_performance(csv_file):
    df = pd.read_csv(csv_file)

    # Extract relevant columns and clean data
    df['size'] = df['name'].apply(lambda x: int(x.split('Size: ')[1].split(')')[0]))
    df['algorithm'] = df['name'].apply(lambda x: x.split()[0])
    df['case'] = df['name'].apply(lambda x: x.split()[1])

    # Create a line plot with different colors for each case
    sns.lineplot(data=df, x='size', y='dur', hue='case', style='algorithm', markers=True)

    # Customize plot appearance
    plt.xlabel('Input Size')
    plt.ylabel('Duration (ns)')
    plt.title('Sorting Algorithm Performance')
    plt.grid(True)
    plt.legend(title='Algorithm/Case')

    plt.show()

# Example usage
csv_file = 'src_visualize/results.csv'  # Replace with your CSV file path
plot_algorithm_performance(csv_file)