# Main program Streamlit
from apps import *
from greedy import *


if __name__ == "__main__":
    # Masukkan API Key Open Exchange Rates
    api_key = "f1f1333c0ffb423da8298d40975611a8"

    # Ambil data kurs mata uang dari Open Exchange Rates
    exchange_rates = get_open_exchange_rates(api_key)

    if exchange_rates:
        from_currency, amount = show_menu(exchange_rates)

        if from_currency in exchange_rates:
            # Hitung konversi mata uang
            to_currency = "IDR"  # Target currency disetel ke IDR
            conversion_rate = exchange_rates[to_currency] / exchange_rates[from_currency]
            converted_amount = amount * conversion_rate
            
            # Hitung denominasi uang
            hasil_denominasi = denominasi_uang(converted_amount)
            total_denom = hasil_denominasi.get("total", 0)  # Ambil nilai total_denom dari hasil_denominasi
            tax = converted_amount - total_denom

            # Tampilkan hasil konversi dengan Streamlit
            st.success(f"{amount} {from_currency} setara dengan {converted_amount:.2f} {to_currency}")

            # Tampilkan denominasi uang dengan Streamlit
            st.subheader("Denominasi Uang:")
            for denom, jumlah in hasil_denominasi.items():
                if denom == "total":
                    st.write(f"Total denominasi: Rp.{jumlah:.0f}")
                else:
                    st.write(f'Pecahan Rp.{denom}: {jumlah:.0f} lembar')

            # Tampilkan keuntungan dengan Streamlit
            st.info(f'Jumlah keuntungan: Rp.{tax:.2f}')
        else:
            st.error("Mata uang asal tidak valid.")
    else:
        st.error("Gagal mengambil data kurs mata uang. Pastikan API Key Anda valid.")
