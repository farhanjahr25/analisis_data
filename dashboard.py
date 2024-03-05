import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

days_df = pd.read_csv("day_data.csv")
days_df["dteday"] = pd.to_datetime(days_df["dteday"])

hours_df = pd.read_csv("hour_data.csv")
hours_df["dteday"] = pd.to_datetime(hours_df["dteday"])
def pertanyaan1():
    st.header('Apakah ada jarak jam tertentu di mana terjadinya peningkatan rental sepeda?')
    hourly_order_df = hours_df.groupby(by='hr').agg({
        "cnt": "sum"
    })
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hourly_order_df.index, hourly_order_df["cnt"], marker='o', linewidth=2, color="#72BCD4")
    ax.set_title("Number of Orders per Hour", loc="center", fontsize=20)
    ax.set_xlabel("Hour", fontsize=12)
    ax.set_ylabel("Number of Orders", fontsize=12)
    ax.set_xticks(range(24))  # Perubahan di sini
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(True)
    st.pyplot(fig)
    rfm_df = hours_df.groupby(by="hr", as_index=False).agg({
        "dteday": "max", # mengambil tanggal order terakhir
        "instant": "nunique", # menghitung jumlah order
        "cnt": "sum" # menghitung jumlah revenue yang dihasilkan
    })
    rfm_df.columns = ["hr", "max_order_timestamp", "frequency", "monetary"]

    # menghitung kapan terakhir pelanggan melakukan transaksi (hari)
    rfm_df["max_order_timestamp"] = pd.to_datetime(rfm_df["max_order_timestamp"])
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = hours_df["dteday"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)

    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

    # Membuat subplot
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

    # Plot untuk Recency
    sns.barplot(y="recency", x="hr", data=rfm_df.sort_values(by="recency", ascending=True).head(5), hue="hr", ax=ax[0], legend=False)
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
    ax[0].tick_params(axis ='x', labelsize=15)

    # Plot untuk Frequency
    sns.barplot(y="frequency", x="hr", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), hue="hr", ax=ax[1], legend=False)
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].set_title("By Frequency", loc="center", fontsize=18)
    ax[1].tick_params(axis='x', labelsize=15)

    # Plot untuk Monetary
    sns.barplot(y="monetary", x="hr", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), hue="hr", ax=ax[2], legend=False)
    ax[2].set_ylabel(None)
    ax[2].set_xlabel(None)
    ax[2].set_title("By Monetary (count)", loc="center", fontsize=18)
    ax[2].tick_params(axis='x', labelsize=15)

    # Menambahkan judul keseluruhan
    plt.suptitle("Best Hour on RFM Parameters (hr)", fontsize=20)

    # Menampilkan plot
    st.pyplot(fig)
    st.write("Kesimpulan:")
    st.write("Pada visualisasi data jumlah count pada tiap Jam, terdapat kenaikan signifikan yang melakukan rental sepeda di jam 8 pagi dan jam 5 sore.")
def pertanyaan2():
    st.header('Kapan saat yang tepat untuk mempromosikan keanggotaan pada pengguna casual?')
    # Pengelompokkan data berdasarkan musim dan menghitung rata-rata jumlah pengguna casual
    casual_season_df = days_df.groupby("season_group").agg({'casual': 'mean'})
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    # Membuat subplot
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

    # Plot untuk musim paling cocok
    sns.barplot(x="casual", y="season_group", data=casual_season_df, palette=colors, ax=ax[0], hue="season_group", legend=False)
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Musim Paling Cocok Untuk Mempromosikan Keanggotaan", loc="center", fontsize=20)
    ax[0].tick_params(axis ='y', labelsize=15)

    # Plot untuk musim paling tidak cocok
    sns.barplot(x="casual", y="season_group", data=casual_season_df.sort_values(by="casual", ascending=True), hue="season_group", palette=colors, ax=ax[1], legend=False)
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Musim Paling Tidak Cocok Untuk Mempromosikan Keanggotaan", loc="center", fontsize=20)
    ax[1].tick_params(axis='y', labelsize=15)

    # Menampilkan plot
    st.pyplot(fig)
    
    bytemp_df = days_df.groupby(by="temp_group").casual.mean().reset_index()
    bytemp_df.rename(columns={"casual": "mean"}, inplace=True)

    bytemp_df['temp_group'] = pd.Categorical(bytemp_df['temp_group'], ["Cold", "Warm", "Hot"])

    fig2, ax = plt.subplots(figsize=(10, 5))

    sns.barplot(
        x="temp_group", 
        y="mean",
        hue="temp_group",
        data=bytemp_df.sort_values(by="temp_group", ascending=False),
        palette={"Cold": "#D3D3D3", "Warm": "#D3D3D3", "Hot": "#72BCD4"},  
        legend=False  # Set legend to False
    )

    plt.title("Jumlah Pengguna Casual berdasarkan Suhu", loc="center", fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='x', labelsize=12)
    st.pyplot(fig2)  # Menampilkan plot kedua
    st.write("Kesimpulan:")
    st.write("Conclution pertanyaan 2: Dapat diasumsikan bahwa pengguna Casual memiliki frekuensi yang tinggi pada musim Fall dan Summer, juga di keadaan Suhu yang tidak Dingin. Maka perusahaan dapat mengambil tindakan mempromosikan keanggotaan pada Casual di Musim Fall atau Summer, dan di Suhu Hangat atau Panas, karena pada saat itu banyak jangkauan pengunjung Casual yang bisa ditawarkan keanggotaan.")

# Menambahkan logo perusahaan
st.sidebar.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

# Menyiapkan kategori pilihan
range_options = ["Pertanyaan 1", "Pertanyaan 2"]

# Mengambil pilihan dari user
selected_range = st.sidebar.selectbox("Pilihan", range_options)  # Perubahan di sini

# Memanggil fungsi sesuai pilihan pengguna
if selected_range == "Pertanyaan 1":  # Perubahan di sini
    pertanyaan1()
elif selected_range == "Pertanyaan 2":  # Perubahan di sini
    pertanyaan2()
