import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.animation as animation

# ---------------------------
# MODEL SELECTION & TRAINING
# ---------------------------
def run_model(y, steps=5, freq="ME", model_type="sarima"):
    """
    Run forecasting model.
    y: pandas.Series (time series data with datetime index)
    steps: number of future predictions
    freq: 'D', 'W', 'M'
    model_type: 'sarima'
    """

    if model_type == "sarima":
        try:
            model = SARIMAX(y, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
            model_fit = model.fit(disp=False)
            forecast = model_fit.forecast(steps=steps)
        except Exception as e:
            print(f"Model error: {e}")
            forecast = np.zeros(steps)
    else:
        raise ValueError(f"Model type {model_type} not supported")

    # Create forecast index
    last_date = y.index[-1]
    future_dates = pd.date_range(start=last_date, periods=steps+1, freq=freq)[1:]
    forecast_df = pd.DataFrame({"Forecast": forecast}, index=future_dates)

    return forecast_df


# ---------------------------
# PLOTTING FUNCTIONS
# ---------------------------
def plot_analysis(y, column_name="Value"):
    """Plot historical data (Analysis Graph)."""
    plt.figure(figsize=(30, 30))
    plt.plot(y.index, y.values, label="Actual", marker="o")
    plt.title(f"Analysis Graph - {column_name}")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("static/analysis.png")
    plt.close()


def plot_forecast(y, forecast_df, column_name="Value"):
    """Plot historical + forecast data (Forecast Graph)."""
    plt.figure(figsize=(20, 10))
    plt.plot(y.index, y.values, label="Actual", marker="o")
    plt.plot(forecast_df.index, forecast_df["Forecast"], label="Forecast",
             color="red", linestyle="--", marker="x")

    # Connector between last actual & first forecast
    plt.plot(
        [y.index[-1], forecast_df.index[0]],
        [y.iloc[-1], forecast_df.iloc[0]],
        color="gray", linestyle="dotted", linewidth=2
    )

    plt.title(f"Forecast - {column_name}")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("static/forecast.png")
    plt.close()


# ---------------------------
# MAIN PIPELINE
# ---------------------------
def run_pipeline(df, column, steps=5, freq="ME", model_type="sarima"):
    """
    df: DataFrame with Date index and one value column
    column: column name to forecast
    """

    y = df[column].dropna()

    # 1. Plot analysis graph
    plot_analysis(y, column)

    # 2. Run model & forecast
    forecast_df = run_model(y, steps=steps, freq=freq, model_type=model_type)

    # 3. Plot forecast graph
    plot_forecast(y, forecast_df, column)

    # 4. Business insights
    total_sales = y.sum()
    avg_sales = y.mean()

    # Trend detection (simple slope)
    if len(y) > 1:
        slope = (y.iloc[-1] - y.iloc[0]) / len(y)
    else:
        slope = 0

    trend = "increasing 📈" if slope > 0 else "decreasing 📉" if slope < 0 else "stable ➡️"

    # Forecast trend: compare first vs last prediction
    if len(forecast_df) > 1:
        f_slope = forecast_df["Forecast"].iloc[-1] - forecast_df["Forecast"].iloc[0]
    else:
        f_slope = 0

    forecast_trend = "will increase 🚀" if f_slope > 0 else "will decrease 📉" if f_slope < 0 else "stay stable ➡️"

    summary = {
        "total_sales": round(total_sales, 2),
        "avg_sales": round(avg_sales, 2),
        "trend": trend,
        "forecast_trend": forecast_trend
    }

    return forecast_df,summary
