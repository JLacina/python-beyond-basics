"""
Time-series analytics with pandas and numpy.
(Install with: pip install pandas)

Interview tip: know how to parse timestamps, set a DatetimeIndex, resample,
use rolling windows, handle missing values, and compute basic statistics.
"""
import numpy as np
import pandas as pd

# Build 7 days of half-hourly demand data (kW) with a daily pattern + noise
rng = np.random.default_rng(seed=42)  # Seeded, so results are repeatable
index = pd.date_range("2026-11-01", periods=7 * 48, freq="30min")
hours = (index.hour + index.minute / 60).to_numpy()
daily_pattern = 100 + 60 * np.sin(np.pi * (hours - 6) / 12).clip(0)  # Higher during the day
demand = daily_pattern + rng.normal(0, 5, len(index))

df = pd.DataFrame({"demand_kw": demand}, index=index)
df.iloc[[20, 21, 100]] = np.nan         # Missing readings
df.iloc[200] = 400                      # A spike (meter error?)

print(df.head())
df.info()  # Prints column types and non-null counts

# Basic statistics
print(df.describe())                    # count, mean, std, min, quartiles, max
print("Median:", df["demand_kw"].median())
print("95th percentile:", df["demand_kw"].quantile(0.95))

# Missing values
print("Missing:", df["demand_kw"].isna().sum())
df["demand_kw"] = df["demand_kw"].interpolate(method="time")  # Fill gaps using neighbours

# Selecting by time (works because the index is a DatetimeIndex)
print(df.loc["2026-11-02 08:00":"2026-11-02 10:00"])

# Resampling: change the frequency
hourly = df.resample("1h").mean()       # Downsample: half-hourly -> hourly average
daily = df.resample("D").agg(["mean", "max", "min"])
print(daily)

# Power (kW) vs energy (kWh): energy = power x time. Each reading covers 0.5 hours
daily_energy_kwh = (df["demand_kw"] * 0.5).resample("D").sum()
print(daily_energy_kwh.round(1))

# Rolling window: smooth out noise
df["rolling_3h"] = df["demand_kw"].rolling(window=6).mean()  # 6 x 30min = 3 hours

# Anomaly detection with a z-score: how many standard deviations from the mean?
mean, std = df["demand_kw"].mean(), df["demand_kw"].std()
df["z_score"] = (df["demand_kw"] - mean) / std
print("Anomalies:\n", df[df["z_score"].abs() > 3])

# Peak demand and when it happened
peak_time = df["demand_kw"].idxmax()
print(f"Peak {df.loc[peak_time, 'demand_kw']:.1f} kW at {peak_time}")

# Average profile: mean demand for each hour of the day across all days
profile = df.groupby(df.index.hour)["demand_kw"].mean()
print(profile.round(1))

# Change between readings and shifting (like SQL's LAG)
df["change"] = df["demand_kw"].diff()
df["previous"] = df["demand_kw"].shift(1)

# Correlation between two series
df["temperature"] = 15 - 0.05 * df["demand_kw"] + rng.normal(0, 1, len(df))
print("Correlation:", round(df["demand_kw"].corr(df["temperature"]), 2))
