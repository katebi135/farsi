import streamlit as st
import datetime

# فرهنگ ابجد
abjad_dict = {
    'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9,
    'ی': 10, 'ك': 20, 'ک': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70,
    'ف': 80, 'ص': 90, 'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500,
    'خ': 600, 'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000
}

def abjad_calc(name):
    return sum(abjad_dict.get(char, 0) for char in name if char in abjad_dict)

def moon_phase(date):
    base = datetime.date(2001, 1, 1)
    days = (date - base).days
    phase = days % 29.53
    if phase < 1:
        return "🌑 ماه نو"
    elif phase < 7:
        return "🌓 تربیع اول"
    elif phase < 15:
        return "🌕 بدر"
    elif phase < 22:
        return "🌗 تربیع دوم"
    else:
        return "🌘 ماه کهنه"

def get_quran_insight(value):
    verse = (value % 6236) + 1
    ism = (value % 99) + 1
    return verse, ism

st.set_page_config(page_title="تحلیل حکمت فَرْسی", layout="centered")
st.title("🔮 تحلیل حکمت بر اساس حروف ابجد")

with st.form("form"):
    name = st.text_input("نام کامل شما")
    mother = st.text_input("نام مادر شما")
    father = st.text_input("نام پدر شما")
    spouse = st.text_input("نام همسر")
    spouse_mother = st.text_input("نام مادر همسر")
    
    dob = st.date_input("تاریخ تولد شما", min_value=datetime.date(1900,1,1))
    mother_dob = st.date_input("تاریخ تولد مادر")
    father_dob = st.date_input("تاریخ تولد پدر")

    children_names = st.text_area("نام فرزندان (هر نام در یک خط)")
    children_dobs = st.text_area("تاریخ تولد فرزندان (هر خط مطابق بالا، YYYY-MM-DD)")

    submitted = st.form_submit_button("تحلیل کن")

if submitted:
    name_val = abjad_calc(name)
    mother_val = abjad_calc(mother)
    total_val = name_val + mother_val

    moon = moon_phase(dob)
    verse, ism = get_quran_insight(total_val)

    st.markdown("## 🧮 نتایج تحلیل")
    st.write(f"🔢 ارزش ابجدی: **{total_val}**")
    st.write(f"🌙 فاز ماه تولد: {moon}")
    st.write(f"📖 آیه پیشنهادی: **آیه شماره {verse}**")
    st.write(f"🕊️ اسم اعظم احتمالی: **اسم شماره {ism}**")

    if spouse and spouse_mother:
        s_val = abjad_calc(spouse) + abjad_calc(spouse_mother)
        diff = abs(total_val - s_val)
        score = 100 - min(diff, 100)
        st.write(f"❤️ امتیاز سازگاری با همسر: **{score} از ۱۰۰**")

    if children_names.strip() and children_dobs.strip():
        st.subheader("👶 فرزندان")
        names = children_names.strip().split("\n")
        dobs = children_dobs.strip().split("\n")
        for i in range(min(len(names), len(dobs))):
            try:
                cname = names[i].strip()
                cdob = datetime.datetime.strptime(dobs[i].strip(), "%Y-%m-%d").date()
                cabjad = abjad_calc(cname)
                cmoon = moon_phase(cdob)
                st.write(f"👧 {cname} — تولد: {cdob}, فاز ماه: {cmoon}, ابجد: {cabjad}")
            except:
                st.error(f"خطا در پردازش فرزند: {names[i]}")