# Fungsi denominasi_uang dari kode Anda
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