import streamlit as st
from datetime import datetime, timedelta
import calendar
from hijri_converter import convert
import random

st.set_page_config(page_title="تحلیل عرفانی ابجد و جفر", layout="centered")

st.title("📿 برنامه تحلیل ابجد، جفر، سیمیا و تاریخ قمری")

# تابع محاسبه ابجد
def abjad_calc(name):
    abjad_dict = {
        'ا': 1, 'ب': 2, 'پ': 2, 'ت': 400, 'ث': 500, 'ج': 3, 'چ': 3,
        'ح': 8, 'خ': 600, 'د': 4, 'ذ': 700, 'ر': 200, 'ز': 7, 'ژ': 7,
        'س': 60, 'ش': 300, 'ص': 90, 'ض': 800, 'ط': 9, 'ظ': 900,
        'ع': 70, 'غ': 1000, 'ف': 80, 'ق': 100, 'ک': 20, 'گ': 20,
        'ل': 30, 'م': 40, 'ن': 50, 'و': 6, 'ه': 5, 'ی': 10, 'ئ': 10
    }
    return sum([abjad_dict.get(ch, 0) for ch in name])

# فاز ماه
def moon_phase(date):
    diff = (date - datetime(2001,1,1)).days % 29.53
    if diff < 1.5:
        return "🌑 ماه نو"
    elif diff < 7.4:
        return "🌓 تربیع اول"
    elif diff < 14.7:
        return "🌕 بدر"
    elif diff < 22.1:
        return "🌗 تربیع دوم"
    else:
        return "🌘 ماه رو به محاق"

# تاریخ قمری
def lunar_date(greg_date):
    hijri = convert.Gregorian(greg_date.year, greg_date.month, greg_date.day).to_hijri()
    return f"{hijri.day} / {hijri.month} / {hijri.year} هجری قمری"

# استخراج آیه
def get_ayah_by_number(num):
    ayahs = {
        1: "بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ",
        66: "وَاعْبُدْ رَبَّكَ حَتَّىٰ يَأْتِيَكَ الْيَقِينُ",
        786: "اللَّهُ نُورُ السَّمَاوَاتِ وَالْأَرْضِ",
    }
    return ayahs.get(num, "آیه‌ای یافت نشد")

# فرم ورودی
with st.form("main_form"):
    name = st.text_input("🔸 نام کامل", "")
    father = st.text_input("🧔 نام پدر", "")
    mother = st.text_input("👵 نام مادر", "")
    birthdate = st.date_input("📅 تاریخ تولد", min_value=datetime.today() - timedelta(days=365*100), max_value=datetime.today())

    st.markdown("---")
    st.subheader("💍 اطلاعات همسر")
    spouse = st.text_input("نام همسر")
    spouse_mother = st.text_input("نام مادر همسر")
    spouse_birth = st.date_input("تاریخ تولد همسر", min_value=datetime.today() - timedelta(days=365*100), max_value=datetime.today())

    st.markdown("---")
    st.subheader("👶 فرزندان")
    children = []
    for i in range(1, 6):
        col1, col2 = st.columns(2)
        with col1:
            cname = st.text_input(f"نام فرزند {i}", key=f"cname_{i}")
        with col2:
            cbirth = st.date_input(f"تاریخ تولد فرزند {i}", key=f"cbirth_{i}",
                                   min_value=datetime.today() - timedelta(days=365*100), max_value=datetime.today())
        if cname:
            children.append((cname, cbirth))

    submitted = st.form_submit_button("🔮 تحلیل کن")

# پردازش
if submitted:
    st.markdown("## 📜 نتایج تحلیل")
    st.write(f"مقدار ابجد نام شما: {abjad_calc(name)}")
    st.write(f"تاریخ قمری: {lunar_date(birthdate)}")
    st.write(f"فاز ماه در تولد: {moon_phase(birthdate)}")

    ab_val = abjad_calc(name)
    st.success(f"🕋 آیه مرتبط با عدد ابجد: {get_ayah_by_number(ab_val)}")

    st.markdown("### 👥 تحلیل همسر")
    if spouse:
        st.write(f"نام همسر: {spouse} / ابجد: {abjad_calc(spouse)}")
        st.write(f"نام مادر همسر: {spouse_mother}")
        st.write(f"فاز ماه همسر: {moon_phase(spouse_birth)}")

    if children:
        st.markdown("### 👶 تحلیل فرزندان")
        for c in children:
            st.write(f"فرزند: {c[0]} | ابجد: {abjad_calc(c[0])} | فاز ماه: {moon_phase(c[1])}")

    st.info("✨ در نسخه بعدی، تحلیل دقیق جفر سرخ و مسیر روح نیز افزوده خواهد شد.")