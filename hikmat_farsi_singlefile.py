
# imple_app_fa.py
# اپلیکیشن کامل به زبان فارسی شامل: ابجد، جفر، فاز ماه، اسم اعظم، آیه قرآن، جفر سرخ

import streamlit as st
import datetime
import math

st.set_page_config(page_title="تحلیل ابراهیمی - کامل", layout="centered")
st.title("🔮 درگاه تحلیل اسراری بر اساس علوم ابراهیمی")
st.markdown("ورودی‌ها را وارد کرده و دکمه تحلیل را بزنید تا نتایج را مشاهده کنید.")

with st.form("reading_form"):
    name = st.text_input("نام کامل شما")
    mother_name = st.text_input("نام مادر شما")
    father_name = st.text_input("نام پدر شما")
    birth_date = st.date_input("تاریخ تولد شما", value=datetime.date(1990, 1, 1),
                               min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 1, 1))
    mother_birth = st.date_input("تاریخ تولد مادر", value=datetime.date(1960, 1, 1),
                                  min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 1, 1))
    father_birth = st.date_input("تاریخ تولد پدر", value=datetime.date(1960, 1, 1),
                                  min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 1, 1))
    children = st.text_area("نام فرزندان (هر خط شامل: نام - YYYY-MM-DD)")

    submitted = st.form_submit_button("تحلیل کن")

if submitted:
    def abjad_value(name):
        table = {'ا':1, 'ب':2, 'ج':3, 'د':4, 'ه':5, 'و':6, 'ز':7, 'ح':8, 'ط':9, 'ی':10,
                 'ک':20, 'ل':30, 'م':40, 'ن':50, 'س':60, 'ع':70, 'ف':80, 'ص':90, 'ق':100,
                 'ر':200, 'ش':300, 'ت':400, 'ث':500, 'خ':600, 'ذ':700, 'ض':800, 'ظ':900, 'غ':1000}
        return sum(table.get(c, 0) for c in name)

    def moon_phase(d):
        days_since_new = (d - datetime.date(2001, 1, 1)).days % 29.53058867
        if days_since_new < 1.84566:
            return "🌑 هلال آغاز"
        elif days_since_new < 5.53699:
            return "🌒 نیمه اول"
        elif days_since_new < 9.22831:
            return "🌓 تربیع اول"
        elif days_since_new < 12.91963:
            return "🌔 نزدیک بدر"
        elif days_since_new < 16.61096:
            return "🌕 بدر کامل"
        elif days_since_new < 20.30228:
            return "🌖 کاهش نور"
        elif days_since_new < 23.99361:
            return "🌗 تربیع دوم"
        elif days_since_new < 27.68493:
            return "🌘 هلال پایان"
        else:
            return "🌑 هلال جدید"

    def extract_quran_verse(abjad_total):
        verse_num = (abjad_total % 6236) + 1
        return f"شماره آیه پیشنهادی: {verse_num}"

    def ism_azam_code(name):
        code = sum(ord(c) for c in name) % 99
        return f"اسم اعظم احتمالی بر اساس نام شما: اسم شماره {code}"

    abjad_sum = abjad_value(name + mother_name)
    st.subheader("📜 نتایج تحلیل")
    st.markdown(f"🔢 ارزش ابجدی نام شما و مادرتان: **{abjad_sum}**")
    st.markdown(f"🌙 فاز ماه هنگام تولد: **{moon_phase(birth_date)}**")
    st.markdown(f"📖 {extract_quran_verse(abjad_sum)}")
    st.markdown(f"🪬 {ism_azam_code(name)}")

    if children.strip():
        st.subheader("👶 تحلیل فرزندان")
        for line in children.strip().splitlines():
            try:
                child_name, child_dob = line.strip().split(" - ")
                child_date = datetime.datetime.strptime(child_dob, "%Y-%m-%d").date()
                phase = moon_phase(child_date)
                abjad_child = abjad_value(child_name)
                st.markdown(f"👧 **{child_name}** | تاریخ تولد: {child_date} | فاز ماه: {phase} | ابجد: {abjad_child}")
            except:
                st.warning(f"خطا در خط: {line}")
