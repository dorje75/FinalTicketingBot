import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from plot_functions import plot_time_series, plot_booking_counts, plot_pie_chart, plot_histogram, plot_scatter_plot, plot_box_plot, plot_heatmap, create_canvas

class AdminDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(100, 100, 1000, 800)

        # Central widget and layout
        central_widget = QWidget()
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Create buttons for different visualizations
        self.plot_buttons = {
            "Booking Trends": self.show_booking_trends,
            "Booking Counts": self.show_booking_counts,
            "Gender Distribution": self.show_gender_distribution,
            "Entry Time Distribution": self.show_entry_time_distribution,
            "Indian vs Foreign Bookings": self.show_indian_vs_foreign_bookings,
            "Booking Counts Box Plot": self.show_booking_counts_box_plot,
            "Heatmap": self.show_heatmap
        }

        # Apply dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E;
            }
            QPushButton {
                background-color: #4E4E4E;
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #6E6E6E;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
        """)

        # Add buttons to layout
        for text, method in self.plot_buttons.items():
            button = QPushButton(text)
            button.clicked.connect(method)
            button.setCursor(Qt.PointingHandCursor)
            button.enterEvent = lambda event, b=button: self.on_button_hover(b, True)
            button.leaveEvent = lambda event, b=button: self.on_button_hover(b, False)
            self.layout.addWidget(button)

        # Add a placeholder for the plot and takeaways
        self.plot_widget = QWidget()
        self.plot_layout = QVBoxLayout()
        self.plot_widget.setLayout(self.plot_layout)
        self.layout.addWidget(self.plot_widget)

        self.takeaway_label = QLabel()
        self.plot_layout.addWidget(self.takeaway_label)

    def on_button_hover(self, button, enter):
        if enter:
            self.animate_button(button, QRect(button.x(), button.y(), button.width() + 10, button.height() + 10))
        else:
            self.animate_button(button, QRect(button.x(), button.y(), button.width() - 10, button.height() - 10))

    def animate_button(self, button, target_rect):
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(200)
        animation.setStartValue(button.geometry())
        animation.setEndValue(target_rect)
        animation.start()

    def fetch_data(self):
        # Fetch data from the database or use example data
        dates = ['2024-09-01', '2024-09-02', '2024-09-03']
        indian_counts = [100, 150, 200]
        foreign_counts = [50, 75, 100]
        children_counts = [10, 15, 20]
        entry_times = [1, 2, 3]  # Example times
        male_count = 200
        female_count = 150
        other_count = 50

        # Example heatmap data
        data_matrix = [
            [10, 20, 30],
            [20, 30, 40],
            [30, 40, 50]
        ]
        row_labels = ['Row1', 'Row2', 'Row3']
        col_labels = ['Col1', 'Col2', 'Col3']

        return dates, indian_counts, foreign_counts, children_counts, entry_times, male_count, female_count, other_count, data_matrix, row_labels, col_labels

    def show_booking_trends(self):
        dates, indian_counts, foreign_counts, children_counts, *_ = self.fetch_data()

        fig = plot_time_series(dates, indian_counts, foreign_counts, children_counts)
        canvas = create_canvas(fig)

        # Clear previous widgets
        self.clear_plot_widgets()

        # Add new plot and takeaways
        self.plot_layout.addWidget(canvas)
        self.takeaway_label.setText("Takeaways: Booking trends show a steady increase in Indian visitors over time.")

    def show_booking_counts(self):
        dates, indian_counts, foreign_counts, children_counts, *_ = self.fetch_data()

        fig = plot_booking_counts(indian_counts, foreign_counts, children_counts, dates)
        canvas = create_canvas(fig)

        # Clear previous widgets
        self.clear_plot_widgets()

        # Add new plot and takeaways
        self.plot_layout.addWidget(canvas)
        self.takeaway_label.setText("Takeaways: Booking counts by category show varying trends over time.")

    def show_gender_distribution(self):
        _, _, _, _, _, male_count, female_count, other_count, *_ = self.fetch_data()

        fig = plot_pie_chart(male_count, female_count, other_count)
        canvas = create_canvas(fig)

        # Clear previous widgets
        self.clear_plot_widgets()

        # Add new plot and takeaways
        self.plot_layout.addWidget(canvas)
        self.takeaway_label.setText("Takeaways: Gender distribution indicates the proportions of male, female, and other attendees.")

    def show_entry_time_distribution(self):
        _, _, _, _, entry_times, *_ = self.fetch_data()

        fig = plot_histogram(entry_times)
        canvas = create_canvas(fig)

        # Clear previous widgets
        self.clear_plot_widgets()

        # Add new plot and takeaways
        self.plot_layout.addWidget(canvas)
        self.takeaway_label.setText("Takeaways: Distribution of entry times shows the frequency of different entry times.")

    def show_indian_vs_foreign_bookings(self):
        dates, indian_counts, foreign_counts, *_ = self.fetch_data()

        fig = plot_scatter_plot(indian_counts, foreign_counts)
        canvas = create_canvas(fig)

        # Clear previous widgets
        self.clear_plot_widgets()

        # Add new plot and takeaways
        self.plot_layout.addWidget(canvas)
        self.takeaway_label.setText("Takeaways: Scatter plot of Indian vs Foreign bookings reveals the correlation between the two.")

    def show_booking_counts_box_plot(self):
        _, _, _, children_counts, *_ = self.fetch_data()

        fig = plot_box_plot([children_counts])
        canvas = create_canvas(fig)

        # Clear previous widgets
        self.clear_plot_widgets()

        # Add new plot and takeaways
        self.plot_layout.addWidget(canvas)
        self.takeaway_label.setText("Takeaways: Box plot of booking counts provides insight into the distribution and outliers.")

    def show_heatmap(self):
        _, _, _, _, *_ , data_matrix, row_labels, col_labels = self.fetch_data()

        fig = plot_heatmap(data_matrix, row_labels, col_labels)
        canvas = create_canvas(fig)

        # Clear previous widgets
        self.clear_plot_widgets()

        # Add new plot and takeaways
        self.plot_layout.addWidget(canvas)
        self.takeaway_label.setText("Takeaways: Heatmap shows the density or correlation between different data points.")

    def clear_plot_widgets(self):
        for i in reversed(range(self.plot_layout.count())):
            widget = self.plot_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminDashboard()
    window.show()
    sys.exit(app.exec_())
