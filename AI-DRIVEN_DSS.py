import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Membaca data dari file CSV
file_path = "data.csv"
df = pd.read_csv(file_path)

# Konversi kolom 'tanggal' ke format datetime
df["tanggal"] = pd.to_datetime(df["tanggal"])
df.set_index("tanggal", inplace=True)

# Membangun model SARIMA untuk setiap variabel dan mengumpulkan prediksi
columns_to_forecast = ["b9k", "b10k", "b12k", "b22k", "basin", "totaljual"]
all_forecasts = pd.DataFrame(index=pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=7, freq='D'))

for column in columns_to_forecast:
    print(f"Memproses kolom: {column}")
    model = SARIMAX(df[column], order=(1,1,1), seasonal_order=(1,1,1,7))
    sarima_result = model.fit()
    forecast_steps = 7
    forecast = sarima_result.forecast(steps=forecast_steps)
    all_forecasts[column] = forecast

# Menampilkan Grafik Prediksi Gabungan
plt.figure(figsize=(15, 8))

colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown'] # Daftar warna yang berbeda

for i, column in enumerate(columns_to_forecast):
    plt.plot(df.index, df[column], label=f"Data Aktual ({column})", marker='o', alpha=0.7, color=colors[i])
    plt.plot(all_forecasts.index, all_forecasts[column], label=f"Prediksi ({column})", linestyle="dashed", marker='x', color=colors[i])

plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.title("Prediksi Penjualan Berbagai Jenis Ikan Menggunakan Metode SARIMA")
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Terjual")
plt.grid(True)
plt.tight_layout()
plt.show()

