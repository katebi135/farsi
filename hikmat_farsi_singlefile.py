import streamlit as st
from hijri_converter import convert
import datetime
import calendar

# دیکشنری حروف ابجد
abjad_dict = {
    'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9,
    'ی': 10, 'ک': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80,
    'ص': 90, 'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600,
    'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000
}

# محاسبه ابجد یک رشته
def abjad_calc(name):
    return sum(abjad_dict.get(ch, 0) for ch in name if ch in abjad_dict)

# محاسبه فاز ماه
def moon_phase(date):
    diff = date - datetime.date(2001, 1, 1)
    days = diff.days
    lunations = 29.53058867
    phase = days % lunations
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

# استخراج آیه پیشنهادی و اسم اعظم
def get_quran_insight(abjad_val):
    verse_number = abjad_val + 1
    ism_val = abjad_val % 99 + 1
    return verse_number, ism_val

# تبدیل تاریخ میلادی به قمری
def get_lunar(gdate):
    hijri = convert.Gregorian(gdate.year, gdate.month, gdate.day).to_hijri()
    return hijri

# رابط کاربری
st.title("📿 تحلیل حکمت ابجدی به زبان فارسی")

with st.form("user_form"):
    name = st.text_input("نام کامل شما")
    mother = st.text_input("نام مادر شما")
    father = st.text_input("نام پدر شما")
    spouse = st.text_input("نام همسر")
    spouse_mother = st.text_input("نام مادر همسر")
    
    dob = st.date_input("تاریخ تولد شما", min_value=datetime.date(1900,1,1), max_value=datetime.date(2099,12,31))
    mother_dob = st.date_input("تاریخ تولد مادر", min_value=datetime.date(1900,1,1), max_value=datetime.date(2099,12,31))
    father_dob = st.date_input("تاریخ تولد پدر", min_value=datetime.date(1900,1,1), max_value=datetime.date(2099,12,31))
    
    children_names = st.text_area("نام فرزندان (هر نام در یک خط)")
    children_dobs = st.text_area("تاریخ تولد فرزندان (YYYY-MM-DD هر خط مطابق بالا)")
    
    submitted = st.form_submit_button("🔍 تحلیل کن")

if submitted:
    name_val = abjad_calc(name)
    mother_val = abjad_calc(mother)
    total_val = name_val + mother_val
    moon = moon_phase(dob)
    verse_num, ism_val = get_quran_insight(total_val)

    st.markdown("## 📜 نتایج تحلیل")
    st.write(f"🔢 ارزش ابجدی نام شما و مادرتان: **{total_val}**")
    st.write(f"🌙 فاز ماه هنگام تولد: {moon}")
    st.write(f"📖 شماره آیه پیشنهادی: **{verse_num}**")
    st.write(f"🕊️ اسم اعظم احتمالی بر اساس نام شما: **اسم شماره {ism_val}**")
    
    if spouse and spouse_mother:
        spouse_abjad = abjad_calc(spouse) + abjad_calc(spouse_mother)
        compat_score = abs(total_val - spouse_abjad)
        st.write(f"❤️ امتیاز سازگاری با همسر: {100 - min(compat_score, 100)} از 100")
    
    if children_names.strip() and children_dobs.strip():
        st.markdown("### 👶 فرزندان")
        names = children_names.strip().split("\n")
        dobs = children_dobs.strip().split("\n")
        for i in range(min(len(names), len(dobs))):
            try:
                c_name = names[i].strip()
                c_dob = datetime.datetime.strptime(dobs[i].strip(), "%Y-%m-%d").date()
                c_abjad = abjad_calc(c_name)
                c_moon = moon_phase(c_dob)
                st.write(f"👧 **{c_name}** — تولد: {c_dob}, فاز ماه: {c_moon}, ابجد: {c_abjad}")
            except:
                st.warning(f"⚠️ خطا در خواندن اطلاعات فرزند {names[i]}")