# Time Series Forecasting App 📈

This is a web application built with **Flask** for performing time series forecasting. It provides a user-friendly interface for uploading your own datasets and visualizing the predictions using advanced forecasting models.

---

## ⚙️ Features

* **User-Friendly Interface**: A simple and intuitive web interface powered by **Flask** for a smooth user experience.
* **Model Integration**: Utilizes the **SARIMA** (Seasonal AutoRegressive Integrated Moving Average) model for accurate forecasting.
* **Data Upload**: Easily upload your own time series datasets in a supported format for personalized predictions.
* **Interactive Visualization**: View forecast results with interactive plots created using **Plotly** and **Matplotlib**.

---

## 🛠️ Technologies Used

* **Backend**: Python, Flask
* **Frontend**: HTML, CSS
* **Database**: MySQL
* **Modeling**: SARIMA
* **Data Handling**: pandas, NumPy
* **Visualization**: Plotly, Matplotlib
* **Environment**: Virtualenv

---

## 📂 Project Structure

```
Time_Series_Forecast/
│
├── app.py                  # Main Flask application  
├── requirement.txt         # Project dependencies
├── models/                 # Directory for trained models
├── static/                 # Static files (CSS, JS)
├── templates/              # HTML templates
├── uploads/                # Folder for user-uploaded datasets
└── myenv/                  # Virtual environment 
```

---

## 🚀 Installation

Follow these steps to set up and run the application on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/SArulRaj24/Time_Series_Forecast.git
cd Time_Series_Forecast
```

### 2. Set Up Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the virtual environment
python -m venv myenv

# Activate the environment
# On macOS and Linux:
source myenv/bin/activate
# On Windows:
myenv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirement.txt
```

### 4. Run the Application

```bash
python app.py
```

The application will now be running on `http://127.0.0.1:5000`. Open this URL in your web browser to access the app.

---
