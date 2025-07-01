import streamlit as st
import datetime
import math

st.set_page_config(page_title="تحلیل عرفانی جامع", layout="centered")
st.title("📿 تحلیل ابجدی، سیمیا، فاز ماه و تولد فرزندان")

# ✅ محاسبه ابجد
def abjad_calc(name):
    table = {
        'ا': 1, 'ب': 2, 'پ': 2, 'ت': 400, 'ث': 500, 'ج': 3, 'چ': 3, 'ح': 8, 'خ': 600,
        'د': 4, 'ذ': 700, 'ر': 200, 'ز': 7, 'ژ': 7, 'س': 60, 'ش': 300, 'ص': 90, 'ض': 800,
        'ط': 9, 'ظ': 900, 'ع': 70, 'غ': 1000, 'ف': 80, 'ق': 100, 'ک': 20, 'ك': 20,
        'گ': 20, 'ل': 30, 'م': 40, 'ن': 50, 'و': 6, 'ه': 5, 'ی': 10, 'ي': 10, 'ئ': 10,
        'ء': 0, ' ': 0, 'أ': 1, 'إ': 1, 'آ': 1, 'ة': 5
    }
    return sum(table.get(ch, 0) for ch in name.strip())

# ✅ فاز ماه و تاریخ قمری
def moon_phase_and_hijri(date):
    ref = datetime.date(2000, 1, 6)
    days = (date - ref).days
    synodic = 29.53058867
    phase_day = days % synodic
    moon_index = int((phase_day / synodic) * 8) % 8
    phases = [
        "🌑 محاق", "🌒 هلال اول", "🌓 تربیع اول", "🌔 نیمه پر",
        "🌕 بدر کامل", "🌖 کاهنده", "🌗 تربیع دوم", "🌘 پایان ماه"
    ]
    hijri_day = (days % 354) % 30 + 1
    hijri_month = ((days % 354) // 30) + 1
    return phases[moon_index], f"{hijri_day} / {hijri_month}"

# ✅ تحلیل سیمیا ساده
def simiya_analysis(abjad_val):
    if abjad_val < 500:
        return "🌱 طبع خاک: شخصیت آرام و واقع‌گرا"
    elif abjad_val < 1000:
        return "🔥 طبع آتش: پرشور و پرحرارت"
    elif abjad_val < 1500:
        return "🌊 طبع آب: احساسی، لطیف، اسرارآمیز"
    else:
        return "🌪 طبع هوا: ذهنی، بلندپرواز، تجزیه‌گر"

# ✅ فرم اصلی
with st.form("form"):
    name = st.text_input("🧍 نام کامل")
    mother = st.text_input("👩‍👧‍👦 نام مادر")
    birth_date = st.date_input("📅 تاریخ تولد", datetime.date(1980,1,1),
                               min_value=datetime.date(1900,1,1), max_value=datetime.date(2100,1,1))
    father_birth = st.date_input("📅 تاریخ تولد پدر", datetime.date(1955,1,1))
    mother_birth = st.date_input("📅 تاریخ تولد مادر", datetime.date(1960,1,1))
    child_names = st.text_area("👶 نام فرزندان (هر خط یک نام)")
    child_dobs = st.text_area("📅 تاریخ تولد فرزندان (YYYY-MM-DD به ترتیب بالا)")

    submit = st.form_submit_button("🔍 تحلیل کن")

# ✅ پس از ارسال
if submit:
    if not name or not mother:
        st.error("⚠️ لطفا نام و نام مادر را وارد کنید.")
    else:
        abjad_sum = abjad_calc(name) + abjad_calc(mother)
        moon, hijri = moon_phase_and_hijri(birth_date)
        simiya = simiya_analysis(abjad_sum)

        st.subheader("📜 نتیجه نهایی:")
        st.markdown(f"🔢 **ارزش ابجدی:** {abjad_sum}")
        st.markdown(f"🌙 **فاز ماه تولد:** {moon}")
        st.markdown(f"🗓 **تاریخ تقریبی قمری:** {hijri}")
        st.markdown(f"🧠 **تحلیل سیمیا:** {simiya}")

        # 👶 تحلیل فرزندان
        if child_names.strip() and child_dobs.strip():
            names = child_names.splitlines()
            dobs = child_dobs.splitlines()
            if len(names) != len(dobs):
                st.warning("⚠️ تعداد نام‌ها با تاریخ‌ها برابر نیست.")
            else:
                st.markdown("👶 **فرزندان:**")
                for i in range(len(names)):
                    try:
                        dob = datetime.date.fromisoformat(dobs[i])
                        m, h = moon_phase_and_hijri(dob)
                        st.write(f"{names[i]} – {m} | قمری: {h}")
                    except:
                        st.error(f"❌ خطا در تاریخ {dobs[i]} برای {names[i]}")