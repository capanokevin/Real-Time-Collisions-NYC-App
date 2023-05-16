# Near Real-Time Analysis of Motor Vehicle Collisions in NYC

This repository contains a Streamlit dashboard application for analyzing motor vehicle collisions in New York City. The application provides visualizations and insights based on the data obtained from the NYC Open Data API.

## Installation

To run this application locally, please follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Make sure you have the necessary data files in the specified paths (`DATA_URL`, `crashes_url`).
2. Run the following command to start the Streamlit application:
   ```
   streamlit run app.py
   ```
3. Access the application by opening the provided URL in your web browser.

## Features

- **Raw Data**: Click the checkbox to view the raw data loaded from the NYC Open Data API. This allows you to explore the dataset used for the analysis.
- **Accident Distribution**: Visualize the distribution of accidents on a map during a specific hour. Select the type of accidents (all, pedestrians, cyclists, or motorists) and the time period (last week, last month, or overall) to analyze the data.
- **Accident Breakdown**: Analyze the breakdown of accidents by minute within a specific hour. This visualization provides insights into when accidents occur more frequently during the selected hour.
- **Injured/Killed People**: Explore the locations where the highest number of people have been injured or killed in accidents. Select the type of people's involvement (injured or killed), the time period, and the number of people involved to view the corresponding data on a map.
- **Top Dangerous Streets**: Discover the top 5 dangerous streets based on the type of affected people (pedestrians, cyclists, or motorists). This feature helps identify the streets with the highest number of injuries or fatalities for each category.

Feel free to explore the different features and visualize the motor vehicle collision data in New York City using this Streamlit dashboard.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributions

Contributions to this project are welcome. If you encounter any issues or have suggestions for improvements, please create a new issue or submit a pull request.

## Contact

For any questions or inquiries, please contact [kevin.capano99@gmail.com](mailto:your-email@gmail.com).

---
