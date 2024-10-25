import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def plot_time_series(dates, indian_counts, foreign_counts, children_counts):
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(dates, indian_counts, label='Indian Count', marker='o', color='b')
    ax.plot(dates, foreign_counts, label='Foreign Count', marker='o', color='g')
    ax.plot(dates, children_counts, label='Children Count', marker='o', color='r')

    ax.set_xlabel('Booking Date', fontsize=12)
    ax.set_ylabel('Counts', fontsize=12)
    ax.set_title('Booking Trends Over Time', fontsize=14)
    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig

def create_canvas(fig):
    return FigureCanvas(fig)
#bar chart
def plot_booking_counts(indian_counts, foreign_counts, children_counts, dates):
    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.25
    index = range(len(dates))

    ax.bar(index, indian_counts, bar_width, label='Indian Bookings', color='b')
    ax.bar([i + bar_width for i in index], foreign_counts, bar_width, label='Foreign Bookings', color='g')
    ax.bar([i + 2 * bar_width for i in index], children_counts, bar_width, label='Children Bookings', color='r')

    ax.set_xlabel('Booking Date', fontsize=12)
    ax.set_ylabel('Counts', fontsize=12)
    ax.set_title('Booking Counts by Category', fontsize=14)
    ax.set_xticks([i + bar_width for i in index])
    ax.set_xticklabels(dates, rotation=45)
    ax.legend()

    plt.tight_layout()

    return fig

#pie chart
def plot_pie_chart(male_count, female_count, other_count):
    sizes = [male_count, female_count, other_count]
    labels = ['Male', 'Female', 'Other']
    colors = ['blue', 'pink', 'grey']

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.set_title('Gender Distribution', fontsize=14)

    return fig

#histogram
def plot_histogram(entry_times):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(entry_times, bins=30, color='blue', edgecolor='black')

    ax.set_xlabel('Entry Time', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title('Histogram of Entry Times', fontsize=14)

    plt(rotation=45)
    plt.tight_layout()

    return fig

#scatter plot
def plot_scatter_plot(indian_counts, foreign_counts):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(indian_counts, foreign_counts, color='blue', alpha=0.5)

    ax.set_xlabel('Indian Bookings', fontsize=12)
    ax.set_ylabel('Foreign Bookings', fontsize=12)
    ax.set_title('Scatter Plot of Indian vs Foreign Bookings', fontsize=14)

    plt.tight_layout()

    return fig

#box plot
def plot_box_plot(data):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.boxplot(data, labels=['Booking Counts'])

    ax.set_ylabel('Counts', fontsize=12)
    ax.set_title('Box Plot of Booking Counts', fontsize=14)

    plt.tight_layout()

    return fig

#heatmap
import numpy as np

def plot_heatmap(data_matrix, row_labels, col_labels):
    fig, ax = plt.subplots(figsize=(10, 8))

    cax = ax.imshow(data_matrix, interpolation='nearest', cmap='coolwarm')
    fig.colorbar(cax)

    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    plt.xlabel('Columns', fontsize=12)
    plt.ylabel('Rows', fontsize=12)
    plt.title('Heatmap', fontsize=14)
    plt.xticks(rotation=45)

    plt.tight_layout()

    return fig

def clear_plot_widgets(self):
    for i in reversed(range(self.plot_layout.count())):
        widget = self.plot_layout.itemAt(i).widget()
        if widget and widget != self.takeaway_label:
            widget.deleteLater()