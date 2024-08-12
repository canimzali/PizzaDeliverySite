import streamlit as st
import sqlite3

#Müşteri online şekilde katalogdaki pizzalara göz gözdirebilmesi ve sipariş verilmesi amaçlandı
st.header("Katalog")
conn=sqlite3.connect("pizzadb.sqlite3")
c=conn.cursor()
c.execute("SELECT * FROM pizzalar")
pizzalar=c.fetchall()

for pizza in pizzalar:

    col1,col2,col3=st.columns(3)
    with col1:
        st.image(pizza[6])

    with col2:
        st.subheader(pizza[0])
        st.write(pizza[5])

    with col3:
        st.write("Small", pizza[1], "₺")
        st.write("Medium", pizza[2], "₺")
        st.write("Large", pizza[3], "₺")
        st.write("Double Large", pizza[4], "₺")