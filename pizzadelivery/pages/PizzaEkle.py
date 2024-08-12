import streamlit as st
import sqlite3
#veri tabanı oluşturma
conn=sqlite3.connect("pizzadb.sqlite3")
c=conn.cursor()
#Oluşturulan veri tabanında yazılacak sütunları belirlendi
c.execute("CREATE TABLE IF NOT EXISTS pizzalar(isim TEXT, smfiyat REAL,mdfiyat REAL,lgfiyat REAL,dlgfiyat REAL,icindekiler TEXT, resim TEXT)")
conn.commit()

#Pizza işletmesi menüye pizza eklemesi, pizzanın boytuna göre fiyatı ve resim ekleme özellikleri
st.header("Pizza Ekle")

with st.form("Pizza Ekle", clear_on_submit=True):
    isim = st.text_input("Pizza isim")
    smfiyat=st.number_input("Small Fiyat")
    mdfiyat=st.number_input("Medium Fiyat")
    lgfiyat=st.number_input("Large Fiyat")
    dlgfiyat=st.number_input("Double Large Fiyat")


    icindekiler=st.multiselect("icindekiler", ["Sucuk", "Mantar", "Ton Balığı", "Sebze",
                                       "Fesleğen", "Mozzarella", "Fileto", "Mısır","Bol Baharatlı"])

    resim= st.file_uploader("Pizza Resmi Ekleyiniz")
    ekle=st.form_submit_button("Pizza Ekle")

    if ekle:
        icindekiler = ", ".join(icindekiler)
        st.write(icindekiler)

        #resim ekleme
        resimurl="img/"+resim.name
        open(resimurl, "wb").write(resim.read())

        # Pizzayı veritabanına ekleme
        c.execute(
            "INSERT INTO pizzalar VALUES (?, ?, ?, ?, ?, ?, ?)",
            (isim, smfiyat, mdfiyat, lgfiyat, dlgfiyat, icindekiler, resimurl))
        conn.commit()
        st.success("Pizza başarıyla eklendi!")

