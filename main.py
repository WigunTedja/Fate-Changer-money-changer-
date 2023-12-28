import streamlit as st
import requests
from datetime import datetime

def denominasi_uang(jumlah_uang):
    denominasi = [100000, 50000, 20000, 10000, 5000]
    hasil = {}
    total_denom = 0

    for denom in denominasi:
        if jumlah_uang >= denom:
            jumlah_denom = jumlah_uang // denom
            hasil[denom] = jumlah_denom
            jumlah_uang -= denom * jumlah_denom
            total_denom += denom * jumlah_denom

    hasil["total"] = total_denom

    return hasil

def get_open_exchange_rates(api_key):
    base_url = f"https://api.openexchangerates.org/latest.json?app_id={api_key}"

    try:
        response = requests.get(base_url)
        data = response.json()
        if 'error' in data:
            st.error(data['description'])
            return None
        return data['rates']
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

def show_menu(exchange_rates):
    st.sidebar.title("Money Changer App")
    st.sidebar.subheader("Mata Uang yang Tersedia:")

    from_currency = st.sidebar.selectbox("Pilih mata uang asal:", list(exchange_rates.keys()))
    to_currency = st.sidebar.selectbox("Pilih mata uang tujuan:", list(exchange_rates.keys()))
    amount = st.sidebar.number_input("Masukkan jumlah yang ingin Anda konversi:", min_value=1, step=1)

    if st.sidebar.button("Konversi"):
        return from_currency, to_currency, amount
    
    return None, None, None

def display_result(amount, from_currency, converted_amount, to_currency, hasil_denominasi):
    if amount and from_currency and to_currency:
        st.success(f"{amount} {from_currency} setara dengan {converted_amount:.2f} {to_currency}")

        st.subheader(f"\nDenominasi:")
        for denom, jumlah in hasil_denominasi.items():
            if denom == "total":
                st.write(f"Total denominasi: Rp.{jumlah:.0f}")
            else:
                st.write(f'Pecahan Rp.{denom}: {jumlah:.0f} lembar')

        # Display profit
        tax = converted_amount - hasil_denominasi.get("total", 0)
        st.info(f'Jumlah keuntungan : Rp.{tax:.2f}')

        # Save to history
        save_to_history(from_currency, to_currency, amount, converted_amount, tax)

        # Display conversion history
        display_history()

def save_to_history(from_currency, to_currency, amount, converted_amount, tax):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conversion_history = f"{from_currency},{to_currency},{amount},{converted_amount},{tax},{timestamp}"
    with open("conversion_history.txt", 'a') as file:
        file.write(conversion_history + '\n')

def display_history():
    st.subheader("\n=== Conversion History ===")
    if not st.file_uploader("conversion_history.txt"):
        st.write("No history available.")
    else:
        with open("conversion_history.txt", 'r') as file:
            history_data = file.readlines()
            history_table = [entry.strip().split(",") for entry in history_data]
            headers = ["Mata Uang Asal", "Mata Uang Tujuan", "Jumlah", "Hasil", "Keuntungan", "Tanggal"]

            # Format large numbers without scientific notation
            for entry in history_table:
                entry[3] = '{:,.2f}'.format(float(entry[3]))
                entry[4] = '{:,.2f}'.format(float(entry[4]))

            st.write(history_table)
    st.write("===========================\n")

# Main Streamlit program
if _name_ == "_main_":
    api_key = "f1f1333c0ffb423da8298d40975611a8"
    exchange_rates = get_open_exchange_rates(api_key)

    if exchange_rates:
        from_currency, to_currency, amount = show_menu(exchange_rates)

        if from_currency in exchange_rates and to_currency in exchange_rates:
            conversion_rate = exchange_rates[to_currency] / exchange_rates[from_currency]
            converted_amount = amount * conversion_rate
            hasil_denominasi = denominasi_uang(converted_amount)

            display_result(amount, from_currency, converted_amount, to_currency, hasil_denominasi)
        else:
            st.warning("Mata uang asal atau tujuan tidak valid.")
    else:
        st.error("Gagal mengambil data kurs mata uang. Pastikan API Key Anda valid.")
