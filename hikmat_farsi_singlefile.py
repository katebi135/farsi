
import streamlit as st
import datetime
import math

st.set_page_config(page_title="حکمت ابجدی", layout="centered")

st.title("🔮 پورتال حکمت ابجدی")
st.markdown("به پورتال حکمت ابجدی خوش آمدید — ترکیبی از علوم جفر، سیمیا، لیمیاء و فاز قمری")

with st.form("user_form"):
    full_name = st.text_input("نام کامل")
    father_name = st.text_input("نام پدر")
    mother_name = st.text_input("نام مادر")
    birth_date = st.date_input("تاریخ تولد شما", value=datetime.date(1990, 1, 1),
                               min_value=datetime.date(1925, 1, 1),
                               max_value=datetime.date.today())

    father_birth = st.date_input("تاریخ تولد پدر", value=datetime.date(1960, 1, 1),
                                 min_value=datetime.date(1925, 1, 1),
                                 max_value=datetime.date.today())

    mother_birth = st.date_input("تاریخ تولد مادر", value=datetime.date(1965, 1, 1),
                                 min_value=datetime.date(1925, 1, 1),
                                 max_value=datetime.date.today())

    child_names = st.text_area("نام فرزندان (هر نام در یک خط)")
    child_dobs = st.text_area("تاریخ تولد فرزندان (مطابق با ترتیب بالا، فرمت YYYY-MM-DD)")

    submit = st.form_submit_button("🔍 تحلیل کن")

def abjad_value(text):
    abjad_table = {
        'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9, 'ی': 10,
        'ک': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80, 'ص': 90, 'ق': 100,
        'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600, 'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000
    }
    return sum(abjad_table.get(char, 0) for char in text if char in abjad_table)

def moon_phase(date):
    diff = (date - datetime.date(2001, 1, 1)).days
    lunations = diff / 29.53058867
    position = lunations % 1
    if position < 0.03 or position > 0.97:
        return "🌑 ماه نو"
    elif position < 0.25:
        return "🌓 تربیع اول"
    elif position < 0.50:
        return "🌕 بدر کامل"
    elif position < 0.75:
        return "🌗 تربیع دوم"
    else:
        return "🌘 هلال پایان"

if submit:
    st.markdown("## 🧮 نتایج تحلیل")
    total_value = abjad_value(full_name + mother_name)
    st.write(f"ارزش ابجدی نام شما و مادر: {total_value}")
    st.write(f"فاز ماه هنگام تولد: {moon_phase(birth_date)}")

    st.markdown("### 👶 فرزندان")
    child_list = child_names.splitlines()
    dob_list = child_dobs.splitlines()

    for name, dob in zip(child_list, dob_list):
        try:
            dob_parsed = datetime.datetime.strptime(dob.strip(), "%Y-%m-%d").date()
            st.write(f"{name.strip()} ({dob}) - فاز ماه: {moon_phase(dob_parsed)} | ارزش ابجد: {abjad_value(name.strip())}")
        except:
            st.warning(f"⚠️ تاریخ نامعتبر برای {name.strip()}")
