import streamlit as st
import datetime

st.set_page_config(page_title="تحلیل اَبجد و قمری - نسخه ساده", layout="centered")
st.title("🔮 تحلیل ابجدی، قمری و فرزندان")

def calculate_abjad(name):
    abjad_dict = {
        'ا': 1, 'ب': 2, 'پ': 2, 'ت': 400, 'ث': 500, 'ج': 3, 'چ': 3, 'ح': 8, 'خ': 600,
        'د': 4, 'ذ': 700, 'ر': 200, 'ز': 7, 'ژ': 7, 'س': 60, 'ش': 300, 'ص': 90, 'ض': 800,
        'ط': 9, 'ظ': 900, 'ع': 70, 'غ': 1000, 'ف': 80, 'ق': 100, 'ک': 20, 'ك': 20,
        'گ': 20, 'ل': 30, 'م': 40, 'ن': 50, 'و': 6, 'ه': 5, 'ی': 10, 'ئ': 10, 'ي': 10,
        'ء': 0, ' ': 0, '.': 0
    }
    return sum(abjad_dict.get(ch, 0) for ch in name.strip())

def get_moon_phase(date):
    synodic_month = 29.53
    new_moon = datetime.date(2000, 1, 6)
    delta_days = (date - new_moon).days % synodic_month
    phase = int((delta_days / synodic_month) * 8) % 8
    phases = ["🌑 محاق", "🌒 هلال اول", "🌓 تربیع اول", "🌔 بدر ناقص", "🌕 بدر کامل", 
              "🌖 بدر کاهنده", "🌗 تربیع دوم", "🌘 هلال آخر"]
    return phases[phase]

with st.form("form"):
    name = st.text_input("نام کامل شما")
    mother = st.text_input("نام مادر شما")
    birth_date = st.date_input("تاریخ تولد شما", datetime.date(1990,1,1),
                               min_value=datetime.date(1900,1,1), max_value=datetime.date(2100,1,1))
    
    father_birth = st.date_input("تاریخ تولد پدر", datetime.date(1960,1,1),
                                 min_value=datetime.date(1900,1,1), max_value=datetime.date(2100,1,1))
    mother_birth = st.date_input("تاریخ تولد مادر", datetime.date(1965,1,1),
                                 min_value=datetime.date(1900,1,1), max_value=datetime.date(2100,1,1))
    
    child_names = st.text_area("نام فرزندان (هر نام در یک خط)")
    child_dobs = st.text_area("تاریخ تولد فرزندان (مطابق ترتیب بالا، فرمت YYYY-MM-DD)")
    
    submit = st.form_submit_button("🔍 تحلیل کن")

if submit:
    if not name or not mother:
        st.error("❌ لطفاً نام کامل و نام مادر را وارد کنید.")
    else:
        abjad_value = calculate_abjad(name) + calculate_abjad(mother)
        st.subheader("📜 نتایج تحلیل")
        st.write(f"ارزش ابجدی نام شما و مادرتان: {abjad_value}")
        st.write(f"فاز ماه هنگام تولد شما: {get_moon_phase(birth_date)}")

        if child_names.strip() and child_dobs.strip():
            names = [n.strip() for n in child_names.splitlines()]
            dobs = [d.strip() for d in child_dobs.splitlines()]
            if len(names) != len(dobs):
                st.warning("⚠️ تعداد نام‌ها و تاریخ‌ها با هم تطابق ندارند.")
            else:
                for i in range(len(names)):
                    try:
                        dob = datetime.date.fromisoformat(dobs[i])
                        moon = get_moon_phase(dob)
                        st.write(f"👶 {names[i]} – فاز ماه هنگام تولد: {moon}")
                    except ValueError:
                        st.error(f"❌ تاریخ '{dobs[i]}' برای فرزند '{names[i]}' معتبر نیست.")