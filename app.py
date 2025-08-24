import os
import io
import base64
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # Non-GUI backend for Flask
import matplotlib.pyplot as plt
from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
from models.model_runner import run_model  # Forecasting logic here

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'raj24'
app.config['MYSQL_PASSWORD'] = 'dexter242raj'
app.config['MYSQL_DB'] = 'cts'
mysql = MySQL(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith((".xlsx", ".csv")):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Load into pandas
            if file.filename.endswith(".csv"):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)

            # Ensure datum is datetime
            df["datum"] = pd.to_datetime(df["datum"])

            # Insert into MySQL
            cursor = mysql.connection.cursor()
            for _, row in df.iterrows():
                cursor.execute(
                    """
                    INSERT INTO daily 
                    (datum, M01AB, M01AE, N02BA, N02BE, N05B, N05C, R03, R06)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        row['datum'],
                        row['M01AB'],
                        row['M01AE'],
                        row['N02BA'],
                        row['N02BE'],
                        row['N05B'],
                        row['N05C'],
                        row['R03'],
                        row['R06']
                    )
                )
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for("analyze"))

    return render_template("upload.html")


@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    drugs = ["M01AB", "M01AE", "N02BA", "N02BE", "N05B", "N05C", "R03", "R06"]
    ranges = ["Daily", "Weekly", "Monthly"]

    analysis_graph = None
    forecast_graph = None
    selected_drug = None
    selected_range = None
    summary = None

    if request.method == "POST":
        selected_drug = request.form["drug"]
        selected_range = request.form["time_range"]

        # Load from DB
        query = f"SELECT datum, {selected_drug} FROM daily ORDER BY datum"
        df = pd.read_sql(query, mysql.connection)

        df["datum"] = pd.to_datetime(df["datum"])
        df.set_index("datum", inplace=True)

        # Aggregate based on time range
        if selected_range == "Daily":
            grouped = df
            steps = 5   # predict next 5 days
        elif selected_range == "Weekly":
            grouped = df.resample("W").sum()
            steps = 1   # predict next 1 week
        elif selected_range == "Monthly":
            grouped = df.resample("ME").sum()
            steps = 1   # predict next 1 month
        else:
            grouped = df
            steps = 5

        # ---------- Graph 1: Analysis Graph ----------
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        ax1.plot(grouped.index, grouped[selected_drug], marker="o", linestyle="-", label="Actual")
        ax1.set_title(f"Analysis - {selected_drug} ({selected_range})")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Value")
        ax1.legend()
        plt.xticks(rotation=45)

        buf1 = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf1, format="png")
        buf1.seek(0)
        analysis_graph = base64.b64encode(buf1.getvalue()).decode("utf-8")
        plt.close(fig1)

        # ---------- Graph 2: Forecast Graph ----------
        forecast = run_model(grouped[selected_drug], steps=steps)

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.plot(grouped.index, grouped[selected_drug], marker="o", linestyle="-", label="Actual")
        if forecast is not None:
            ax2.plot(forecast.index, forecast.values, marker="x", linestyle="--", color="red", label="Forecast")
        ax2.set_title(f"Forecast - {selected_drug} ({selected_range})")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Value")
        ax2.legend()
        plt.xticks(rotation=45)

        buf2 = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf2, format="png")
        buf2.seek(0)
        forecast_graph = base64.b64encode(buf2.getvalue()).decode("utf-8")
        plt.close(fig2)

        # ---------- Summary Insights ----------
        total_sales = grouped[selected_drug].sum()
        avg_sales = grouped[selected_drug].mean()

        # Trend direction (last vs first)
        if grouped[selected_drug].iloc[-1] > grouped[selected_drug].iloc[0]:
            trend = "Increasing 📈"
        elif grouped[selected_drug].iloc[-1] < grouped[selected_drug].iloc[0]:
            trend = "Decreasing 📉"
        else:
            trend = "Stable ➖"

        # Forecast trend
        if forecast is not None:
            if forecast.values[-1] > grouped[selected_drug].iloc[-1]:
                forecast_trend = "Expected to Increase 📈"
            elif forecast.values[-1] < grouped[selected_drug].iloc[-1]:
                forecast_trend = "Expected to Decrease 📉"
            else:
                forecast_trend = "Expected to Stay Stable ➖"
        else:
            forecast_trend = "Not Available"

        summary = {
            "total_sales": round(total_sales, 2),
            "avg_sales": round(avg_sales, 2),
            "trend": trend,
            "forecast_trend": forecast_trend
        }

    return render_template(
        "analyze.html",
        drugs=drugs,
        ranges=ranges,
        analysis_graph=analysis_graph,
        forecast_graph=forecast_graph,
        selected_drug=selected_drug,
        selected_range=selected_range,
        summary=summary
    )


if __name__ == "__main__":
    app.run(debug=True)
