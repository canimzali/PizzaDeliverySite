import streamlit as st
import sqlite3

# Veritabanı bağlantısı ve cursor oluşturma
conn = sqlite3.connect("pizzadb.sqlite3")
c = conn.cursor()

# Siparişler tablosunu oluşturma
c.execute("""
CREATE TABLE IF NOT EXISTS siparisler(
    isim TEXT, 
    adres TEXT, 
    pizza TEXT, 
    boy TEXT, 
    icecek TEXT, 
    fiyat REAL
)
""")
conn.commit()

# Pizzalar tablosundaki isimleri alma
c.execute("SELECT isim FROM pizzalar")
isimler = c.fetchall()

# Pizzaların isimlerini listeye ekleme
isimlerlist = [i[0] for i in isimler]

# İsimler listesi yazdırma


# Sipariş formu
st.header("Sipariş")

with st.form("siparis", clear_on_submit=True):
    isim = st.text_input("İsim Soyisim")
    adres = st.text_area("Adres")
    pizzalar = st.selectbox("Pizza Seç", isimlerlist)
    boy = st.selectbox("Boy", ["Small", "Medium", "Large", "Double Large"])
    icecek = st.selectbox("İçecek", ["Ayran", "Cola", "Soda", "Meyve Suyu", "Su", "Sıkma Limonata"])
    siparis = st.form_submit_button("Sipariş Ver")

    if siparis:
        # Pizza boyutuna göre fiyatı veritabanından çekme
        if boy == "Small":
            c.execute("SELECT smfiyat FROM pizzalar WHERE isim=?", (pizzalar,))
        elif boy == "Medium":
            c.execute("SELECT mdfiyat FROM pizzalar WHERE isim=?", (pizzalar,))
        elif boy == "Large":
            c.execute("SELECT lgfiyat FROM pizzalar WHERE isim=?", (pizzalar,))
        elif boy == "Double Large":
            c.execute("SELECT dlgfiyat FROM pizzalar WHERE isim=?", (pizzalar,))

        fiyat = c.fetchone()  # Fiyatı çekiyoruz

        if fiyat:  # Eğer fiyat bulunduysa
            fiyat = fiyat[0]  # Tuple'ın ilk elemanını alın

            # İçecek fiyatlarını belirleme
            icecek_fiyatlar = {
                "Ayran": 15,
                "Soda": 15,
                "Meyve Suyu": 15,
                "Su": 10,
                "Cola": 20,
                "Sıkma Limonata": 20
            }

            icecekfiyat = icecek_fiyatlar[icecek]

            toplamfiyat = fiyat + icecekfiyat

            st.write(isim, adres, pizzalar, boy, icecek, toplamfiyat)

            # Veritabanına sipariş ekleme
            try:
                c.execute("INSERT INTO siparisler (isim, adres, pizza, boy, icecek, fiyat) VALUES (?, ?, ?, ?, ?, ?)",
                          (isim, adres, pizzalar, boy, icecek, toplamfiyat))
                conn.commit()
                st.success(f"Sipariş başarılı bir şekilde gerçekleştirildi! Toplam ücret: {toplamfiyat}₺")
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
        else:
            st.error("Seçtiğiniz pizza için fiyat bulunamadı. Lütfen başka bir pizza seçin.")
