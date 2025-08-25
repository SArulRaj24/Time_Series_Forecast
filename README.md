⚙️ Features

User-Friendly Interface: Built with Flask to offer a seamless web experience.

Model Integration: Incorporates state-of-the-art forecasting models.

Data Upload: Allows users to upload their datasets for personalized predictions.

Visualization: Displays forecast results with interactive plots.

🛠️ Technologies Used

Backend: Python, Flask

Front End: Html, Css

Database: MySQL

Model: Sarima

Data Handling: pandas, NumPy

Visualization: Plotly, Matplotlib

Environment: Virtualenv

📂 Project Structure
Time_Series_Forecast/
│
├── app.py                # Main Flask application
├── requirement.txt       # Project dependencies
├── models/               # Directory for trained models
├── static/               # Static files (CSS, JS)
├── templates/            # HTML templates
├── uploads/              # Folder for user-uploaded datasets
└── myenv/                # Virtual environment

🚀 Installation
1. Clone the Repository
git clone https://github.com/SArulRaj24/Time_Series_Forecast.git
cd Time_Series_Forecast

2. Set Up Virtual Environment
python -m venv myenv
source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`

3. Install Dependencies
pip install -r requirement.txt

4. Run the Application
python app.py
