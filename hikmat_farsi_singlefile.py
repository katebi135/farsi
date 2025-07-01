import streamlit as st
from datetime import datetime, timedelta
import arabic_reshaper
from bidi.algorithm import get_display
import jdatetime

st.set_page_config(page_title="تحلیل روحی بر اساس نام", layout="centered")

st.markdown("<h1 style='text-align: right; color: #4B0082;'>تحلیل جامع روحی و اسمی</h1>", unsafe_allow_html=True)

# دیکشنری ابجد کبیر
abjad_dict = {
    'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9,
    'ی': 10, 'ک': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80,
    'ص': 90, 'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600,
    'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000
}

def abjad_calc(name):
    total = 0
    for char in name.replace(" ", ""):
        if char in abjad_dict:
            total += abjad_dict[char]
    return total

def get_gregorian_and_lunar(date):
    try:
        lunar = jdatetime.date.fromgregorian(date=date)
        return lunar.strftime('%Y/%m/%d')
    except:
        return "نامعتبر"

def moon_phase(date):
    known_new_moon = datetime(2000, 1, 6)  # arbitrary reference
    days_since = (date - known_new_moon).days
    phase = days_since % 29.53
    if phase < 1: return "ماه نو"
    elif phase < 7: return "هلال در حال رشد"
    elif phase < 15: return "تربیع اول تا بدر"
    elif phase < 22: return "کاهش نور"
    else: return "ماه تاریک"

# -- ورودی‌ها --
st.markdown("### اطلاعات اصلی", unsafe_allow_html=True)

name = st.text_input("نام کامل شما:", key="main_name")
mother_name = st.text_input("نام مادر:", key="mother_name")
father_name = st.text_input("نام پدر:", key="father_name")
birthdate = st.date_input("تاریخ تولد شما (میلادی):", min_value=datetime(1925,1,1), max_value=datetime.today())

st.markdown("### اطلاعات والدین", unsafe_allow_html=True)
mother_birth = st.date_input("تاریخ تولد مادر:", min_value=datetime(1925,1,1), max_value=datetime.today())
father_birth = st.date_input("تاریخ تولد پدر:", min_value=datetime(1925,1,1), max_value=datetime.today())

st.markdown("### اطلاعات همسر", unsafe_allow_html=True)
spouse_name = st.text_input("نام همسر:")
spouse_mother_name = st.text_input("نام مادر همسر:")
spouse_birth = st.date_input("تاریخ تولد همسر:", min_value=datetime(1925,1,1), max_value=datetime.today())

# فرزندان
st.markdown("### فرزندان", unsafe_allow_html=True)
children = []
num_children = st.number_input("تعداد فرزندان:", 0, 10, step=1)
for i in range(num_children):
    col1, col2 = st.columns(2)
    with col1:
        child_name = st.text_input(f"نام فرزند {i+1}", key=f"child_name_{i}")
    with col2:
        child_birth = st.date_input(f"تاریخ تولد فرزند {i+1}", key=f"child_birth_{i}",
                                    min_value=datetime(1925,1,1), max_value=datetime.today())
    children.append((child_name, child_birth))

if st.button("تحلیل کن"):
    st.markdown("## نتایج:", unsafe_allow_html=True)
    total_abjad = abjad_calc(name)
    st.write(f"عدد ابجد نام شما: {total_abjad}")
    st.write(f"تاریخ قمری تولد: {get_gregorian_and_lunar(birthdate)}")
    st.write(f"مرحله ماه در روز تولد: {moon_phase(birthdate)}")
    
    # آیه ساده نمونه‌ای
    ayah_number = total_abjad % 6236
    st.write(f"شماره آیه متناظر: {ayah_number if ayah_number != 0 else 1}")
    st.write(f"ترجمه نمونه‌ای (نمایشی): «خدا نور آسمان‌ها و زمین است...»")

    st.markdown("---")
    st.write("### تحلیل جفری مقدماتی:")
    if total_abjad % 2 == 0:
        st.write("روحیه شما متعادل، منطقی و ساختارگراست.")
    else:
        st.write("روحیه شما احساسی، خلاق و شهودی است.")

    st.markdown("---")
    if spouse_name:
        spouse_abjad = abjad_calc(spouse_name)
        compat = abs(spouse_abjad - total_abjad)
        if compat < 50:
            st.success("سازگاری روحی بالا با همسر")
        elif compat < 150:
            st.warning("سازگاری متوسط با همسر")
        else:
            st.error("سازگاری پایین - نیاز به تعمق بیشتر")

    if num_children > 0:
        st.markdown("### اطلاعات فرزندان:")
        for idx, (cname, cbirth) in enumerate(children):
            cabjad = abjad_calc(cname)
            cmoon = moon_phase(cbirth)
            st.write(f"فرزند {idx+1}: {cname} | ابجد: {cabjad} | مرحله ماه: {cmoon}")