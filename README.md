
# Credit Union Data Visualization with Streamlit and PostgreSQL

## Project Overview

This project is designed to visualize credit union data interactively using Streamlit and a PostgreSQL database. It aims to provide insights into credit union operations, financial performance, member demographics, and more through dynamic and interactive visualizations.

## Features

- **Interactive Dashboards**: Explore various aspects of credit union data through interactive charts and graphs.
- **Filtering and Search**: Narrow down the data based on specific criteria to find exactly what you're looking for.
- **Data Insights**: Get valuable insights into trends, patterns, and anomalies within the data.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or newer
- PostgreSQL 12 or newer
- pipenv (for dependency management)

### Installation

1. **Clone the repository**
   
   ```bash
   git clone https://github.com/Nihar0071/DataVisualisation-and-Analysis-.git
   cd credit-union-visualization
   ```

2. **Set up a virtual environment and install dependencies**

   ```bash
   pipenv install
   ```

3. **Configure PostgreSQL Database**

   - Create a new PostgreSQL database named `credit_union`.
   - Run the SQL scripts located in `sql/` directory to create the required tables and insert sample data.

4. **Set up environment variables**

   Create a `.env` file in the root directory and add the following variables:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/credit_union
   ```

5. **Run the Streamlit application**

   ```bash
   pipenv run streamlit run app.py
   ```

   This will start the Streamlit application and open it in your default web browser.

## Usage

Navigate through the app using the sidebar to select different data visualizations. Use the available filters to customize the displayed data.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

- Credit Union Data Providers
- Streamlit Documentation
- PostgreSQL Community

---

This README provides a basic template for getting started with the project. You might need to adjust paths, dependencies, and commands based on your specific setup and preferences. Additionally, consider adding screenshots of the application in action or a section on the project's architecture if the setup is complex.
