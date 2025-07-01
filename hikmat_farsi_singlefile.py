import streamlit as st
from datetime import datetime, date, timedelta

st.set_page_config(page_title="🕯️ پرتال حکمت ابراهیمی", layout="centered")

st.title("🕯️ پرتال حکمت ابراهیمی")
st.markdown("این برنامه با استفاده از علم ابجد، فاز ماه، و حکمت‌های عرفانی طراحی شده است.")

# محدوده 100 سال برای تاریخ‌ها
today = date.today()
start_date = today.replace(year=today.year - 100)

# ورودی‌ها
with st.form("form"):
    name = st.text_input("نام کامل شما")
    father_name = st.text_input("نام پدر")
    father_dob = st.date_input("تاریخ تولد پدر", value=start_date, min_value=start_date, max_value=today)

    mother_name = st.text_input("نام مادر")
    mother_dob = st.date_input("تاریخ تولد مادر", value=start_date, min_value=start_date, max_value=today)

    dob = st.date_input("تاریخ تولد شما", value=start_date, min_value=start_date, max_value=today)
    
    city = st.text_input("شهر تولد شما")

    spouse_name = st.text_input("نام همسر")
    spouse_dob = st.date_input("تاریخ تولد همسر", value=start_date, min_value=start_date, max_value=today)
    spouse_mother = st.text_input("نام مادر همسر")

    children_names = st.text_area("نام فرزندان (با ویرگول جدا کنید)")
    children_dobs = st.text_area("تاریخ تولد فرزندان (با ویرگول و فرمت YYYY-MM-DD جدا کنید)")

    submitted = st.form_submit_button("🔮 تحلیل کن")

# دیکشنری حروف ابجد
abjad_dict = {
    'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9,
    'ی': 10, 'ک': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80, 'ص': 90,
    'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600, 'ذ': 700,
    'ض': 800, 'ظ': 900, 'غ': 1000, 'ء': 1, 'چ': 3, 'پ': 2, 'ژ': 7,
    'ك': 20, 'ى': 10, 'أ': 1, 'إ': 1, 'آ': 1
}

def normalize_text(text):
    return ''.join(c for c in text if c in abjad_dict)

def abjad_value(text):
    return sum(abjad_dict.get(char, 0) for char in normalize_text(text))

def moon_phase(d: date) -> str:
    known_new_moon = datetime(2000, 1, 6)
    synodic_month = 29.53058867
    days_since = (datetime.combine(d, datetime.min.time()) - known_new_moon).days
    phase = days_since % synodic_month
    if phase < 1.84566:
        return "🌑 ماه نو"
    elif phase < 5.53699:
        return "🌒 هلال اول"
    elif phase < 9.22831:
        return "🌓 تربیع اول"
    elif phase < 12.91963:
        return "🌔 محدب"
    elif phase < 16.61096:
        return "🌕 بدر"
    elif phase < 20.30228:
        return "🌖 محدب کاهش‌یافته"
    elif phase < 23.99361:
        return "🌗 تربیع آخر"
    elif phase < 27.68493:
        return "🌘 هلال آخر"
    else:
        return "🌑 ماه نو"

if submitted:
    if not name or not mother_name:
        st.error("لطفاً نام خود و نام مادر را وارد کنید.")
    else:
        st.success("🧿 تحلیل شما آماده است")

        st.write("### 🧮 محاسبات ابجد")
        st.write(f"ارزش ابجد نام شما: **{abjad_value(name)}**")
        st.write(f"ارزش ابجد نام مادر: **{abjad_value(mother_name)}**")
        st.write(f"ارزش ابجد نام پدر: **{abjad_value(father_name)}**")
        st.write(f"ارزش ابجد همسر: **{abjad_value(spouse_name)}**")
        st.write(f"ارزش ابجد مادر همسر: **{abjad_value(spouse_mother)}**")

        st.write("### 🌙 وضعیت ماه در زمان تولد")
        st.write(f"فاز ماه در تولد شما: **{moon_phase(dob)}**")

        st.write("### 👶 اطلاعات فرزندان")
        names = [n.strip() for n in children_names.split(',') if n.strip()]
        dobs = [d.strip() for d in children_dobs.split(',') if d.strip()]
        if len(names) != len(dobs):
            st.warning("تعداد نام‌ها و تاریخ‌های تولد فرزندان برابر نیست.")
        for i in range(min(len(names), len(dobs))):
            try:
                child_date = datetime.strptime(dobs[i], "%Y-%m-%d").date()
                st.write(f"👧 نام: {names[i]} | تاریخ تولد: {child_date} | فاز ماه: {moon_phase(child_date)} | ابجد: {abjad_value(names[i])}")
            except ValueError:
                st.error(f"تاریخ '{dobs[i]}' برای فرزند '{names[i]}' معتبر نیست. از فرمت YYYY-MM-DD استفاده کنید.")

st.markdown("---")
st.caption("© تمام حقوق محفوظ است | نسخه‌ی ساده‌ی حکمت ابراهیمی")