#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt


def main():
    # Load the log data
    log_file = 'scripts/type-test/typing_test_log.txt'
    df = pd.read_csv(log_file, names=['Timestamp', 'True WPM', 'Similarity'], parse_dates=['Timestamp'], sep=', ', engine='python')


    df['Similarity'] = df['Similarity'].str.rstrip('%').astype(float) / 100.0

    df.sort_values(by='Timestamp', inplace=True)

    # Plotting
    plt.figure(figsize=(14, 7))

    # Plotting True WPM over time
    plt.subplot(1, 2, 1)
    plt.plot(df['Timestamp'], df['True WPM'], marker='o', linestyle='-', color='blue')
    plt.title('Typing Test Performance Over Time')
    plt.xlabel('Time')
    plt.ylabel('True WPM')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Plotting Similarity over time
    plt.subplot(1, 2, 2)
    plt.plot(df['Timestamp'], df['Similarity'], marker='x', linestyle='-', color='red')
    plt.title('Typing Test Similarity Over Time')
    plt.xlabel('Time')
    plt.ylabel('Similarity Score')
    plt.xticks(rotation=45)
    plt.grid(True)

    plt.tight_layout()

    # Save the figure to a PNG file
    plt.savefig('scripts/type-test/typing_test_performance.png')
if __name__ == "__main__":
    main()

