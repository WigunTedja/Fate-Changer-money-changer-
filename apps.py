import streamlit as st
import requests



# Fungsi get_open_exchange_rates dari kode Anda
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

# Fungsi untuk menampilkan menu pilihan konversi dengan Streamlit
def show_menu(exchange_rates):
    st.sidebar.title("Money Changer App")
    st.sidebar.subheader("Mata Uang yang Tersedia:")
    from_currency = st.sidebar.selectbox("Pilih mata uang asal:", list(exchange_rates.keys()))
    amount = st.sidebar.number_input("Masukkan jumlah yang ingin Anda konversi:", min_value=0.01, step=0.01)
    
    return from_currency, amount

