import streamlit as st
from datetime import datetime, timedelta
import math

st.set_page_config(page_title="تحلیل عبری-اسلامی", layout="centered")

st.title("🔮 درگاه تحلیل ابجدی، قمری و قرآنی")

with st.form("form"):
    full_name = st.text_input("نام کامل شما")
    mother_name = st.text_input("نام مادر شما")
    father_name = st.text_input("نام پدر شما")
    birth_date = st.date_input("تاریخ تولد شما", value=datetime(1980, 1, 1), min_value=datetime(1900,1,1), max_value=datetime(2100,1,1))
    father_birth = st.date_input("تاریخ تولد پدر", value=datetime(1960, 1, 1))
    mother_birth = st.date_input("تاریخ تولد مادر", value=datetime(1965, 1, 1))
    children_names = st.text_area("نام فرزندان (هر نام در یک خط)")
    children_births = st.text_area("تاریخ تولد فرزندان (مطابق ترتیب بالا - فرمت YYYY-MM-DD)")
    submit = st.form_submit_button("🔍 تحلیل کن")

# دیکشنری ساده آیات قرآن
quran_verses = {
    1: "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ - بنام خداوند بخشنده مهربان",
    2: "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ - ستایش مخصوص خداوندی است که پروردگار جهانیان است",
    63: "وَعِبَادُ الرَّحْمَٰنِ ... - بندگان واقعی خدای رحمان کسانی هستند که با فروتنی راه می‌روند",
    296: "وَٱصْبِرْ وَمَا صَبْرُكَ إِلَّا بِٱللَّهِ - صبر کن، و صبر تو فقط برای خداست"
}

# محاسبه ابجد ساده
def abjad_value(name):
    abjad_table = {
        'ا':1, 'ب':2, 'ج':3, 'د':4, 'ه':5, 'و':6, 'ز':7, 'ح':8, 'ط':9, 'ی':10, 'ک':20,
        'ل':30, 'م':40, 'ن':50, 'س':60, 'ع':70, 'ف':80, 'ص':90, 'ق':100, 'ر':200,
        'ش':300, 'ت':400, 'ث':500, 'خ':600, 'ذ':700, 'ض':800, 'ظ':900, 'غ':1000
    }
    return sum([abjad_table.get(ch, 0) for ch in name if ch in abjad_table])

# فاز ماه ساده
def moon_phase(date):
    known_new_moon = datetime(2000, 1, 6)  # مرجع فاز ماه
    days = (date - known_new_moon).days
    lunation = 29.53058867
    phase = days % lunation
    if phase < 1.5:
        return "🌑 هلال جدید"
    elif phase < 7:
        return "🌓 تربیع اول"
    elif phase < 15:
        return "🌕 ماه کامل"
    elif phase < 22:
        return "🌗 تربیع دوم"
    else:
        return "🌘 پایان ماه"
    
# اسم اعظم احتمالی (نمونه اولیه ساده)
def probable_ism_azam(name_value):
    if name_value % 9 == 0:
        return "القهار"
    elif name_value % 7 == 0:
        return "اللطیف"
    elif name_value % 5 == 0:
        return "الرزاق"
    elif name_value % 3 == 0:
        return "الغفور"
    else:
        return "الرحمن"

# اجرای تحلیل
if submit:
    st.subheader("📜 نتایج تحلیل")

    total_abjad = abjad_value(full_name) + abjad_value(mother_name)
    st.markdown(f"🔢 ارزش ابجدی نام شما و مادرتان: **{total_abjad}**")

    phase = moon_phase(birth_date)
    st.markdown(f"🌙 فاز ماه هنگام تولد: **{phase}**")

    verse_number = (total_abjad % 300) or 1
    verse = quran_verses.get(verse_number, "آیه‌ای یافت نشد.")
    st.markdown(f"📖 شماره آیه پیشنهادی: **{verse_number}**")
    st.markdown(f"🔊 آیه: {verse}")

    ism = probable_ism_azam(total_abjad)
    st.markdown(f"🕋 اسم اعظم احتمالی بر اساس تحلیل نام شما: **{ism}**")

    if children_names.strip():
        st.markdown("👶 فرزندان:")
        names = children_names.strip().split("\n")
        bds = children_births.strip().split("\n")
        for i, name in enumerate(names):
            abv = abjad_value(name)
            dob = bds[i] if i < len(bds) else "----"
            st.markdown(f"- {name} ({dob}) → ابجد: **{abv}**")