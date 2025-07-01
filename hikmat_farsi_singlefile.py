import streamlit as st
from datetime import datetime

st.set_page_config(page_title="تحلیل ابجدی و قمری", layout="centered")
st.title("🔮 درگاه تحلیل عرفانی")

# ------------------------ ابزارهای جفر ------------------------
abjad_dict = {
    'ا': 1, 'ب': 2, 'پ': 2, 'ت': 400, 'ث': 500, 'ج': 3, 'چ': 3, 'ح': 8,
    'خ': 600, 'د': 4, 'ذ': 700, 'ر': 200, 'ز': 7, 'ژ': 7, 'س': 60,
    'ش': 300, 'ص': 90, 'ض': 800, 'ط': 9, 'ظ': 900, 'ع': 70, 'غ': 1000,
    'ف': 80, 'ق': 100, 'ک': 20, 'ك': 20, 'گ': 20, 'ل': 30, 'م': 40,
    'ن': 50, 'و': 6, 'ه': 5, 'ی': 10, 'ي': 10, 'ء': 1, 'آ': 1, 'ؤ': 6, 'ئ': 10
}

def clean_text(text):
    return ''.join(c for c in text if c in abjad_dict)

def get_abjad_value(name):
    name = clean_text(name)
    return sum(abjad_dict.get(char, 0) for char in name)

# ------------------------ ابزار قمر ------------------------
def get_moon_phase(date):
    known_new_moon = datetime(2001, 1, 24)
    days = (date - known_new_moon).days
    phase = days % 29.53
    if phase < 1.84566:
        return "🌑 ماه نو"
    elif phase < 5.53699:
        return "🌒 هلال در حال رشد"
    elif phase < 9.22831:
        return "🌓 تربیع اول"
    elif phase < 12.91963:
        return "🌔 بدر در حال رشد"
    elif phase < 16.61096:
        return "🌕 ماه کامل"
    elif phase < 20.30228:
        return "🌖 بدر در حال کاهش"
    elif phase < 23.99361:
        return "🌗 تربیع دوم"
    elif phase < 27.68493:
        return "🌘 هلال در حال کاهش"
    else:
        return "🌑 ماه نو"

# ------------------------ ورودی‌ها ------------------------
with st.form("form"):
    name = st.text_input("نام کامل شما")
    mother = st.text_input("نام مادر شما")
    father = st.text_input("نام پدر شما")

    dob = st.date_input("تاریخ تولد شما", format="YYYY-MM-DD")
    dob_mother = st.date_input("تاریخ تولد مادر", format="YYYY-MM-DD")
    dob_father = st.date_input("تاریخ تولد پدر", format="YYYY-MM-DD")

    child_names_raw = st.text_area("نام فرزندان (هر نام در یک خط)")
    child_dobs_raw = st.text_area("تاریخ تولد فرزندان (مطابق ترتیب بالا، فرمت: YYYY-MM-DD)")

    submitted = st.form_submit_button("🔍 تحلیل کن")

# ------------------------ تحلیل و نمایش ------------------------
if submitted:
    if not name or not mother:
        st.error("لطفا نام کامل و نام مادر را وارد کنید.")
    else:
        name_val = get_abjad_value(name)
        mother_val = get_abjad_value(mother)
        abjad_total = name_val + mother_val

        st.subheader("📜 نتایج تحلیل")
        st.write(f"🔢 ارزش ابجدی نام شما و مادر: {abjad_total}")

        moon = get_moon_phase(dob)
        st.write(f"🌙 قمر ماه هنگام تولد: {moon}")

        # ---------------- فرزندان ----------------
        st.subheader("👶 فرزندان")
        child_names = [n.strip() for n in child_names_raw.split("\n") if n.strip()]
        child_dobs = [d.strip() for d in child_dobs_raw.split("\n") if d.strip()]

        if len(child_names) != len(child_dobs):
            st.warning("تعداد نام فرزندان با تعداد تاریخ تولدها یکسان نیست.")

        for i in range(min(len(child_names), len(child_dobs))):
            try:
                child_date = datetime.strptime(child_dobs[i], "%Y-%m-%d")
                child_moon = get_moon_phase(child_date)
                child_val = get_abjad_value(child_names[i])
                st.write(f"👧 {child_names[i]} | ابجد: {child_val} | قمر: {child_moon}")
            except ValueError:
                st.error(f"❗ فرمت تاریخ تولد برای {child_names[i]} اشتباه است.")