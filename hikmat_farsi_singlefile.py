import streamlit as st
import datetime
import math
from random import randint

st.set_page_config(page_title="خوانش ابراهیمی", layout="centered")
st.title("🧿 خوانش ابراهیمی | تحلیل ابجد، جفر، همسر روحی")

st.markdown("---")
st.markdown("لطفاً اطلاعات زیر را وارد نمایید:")

# فرم اصلی
with st.form("user_form"):
    full_name = st.text_input("نام کامل شما:")
    name_dob = st.date_input("تاریخ تولد شما:", value=datetime.date(1990, 1, 1),
                             min_value=datetime.date.today() - datetime.timedelta(days=365*100),
                             max_value=datetime.date.today())

    mother_name = st.text_input("نام مادر:")
    mother_dob = st.date_input("تاریخ تولد مادر:", value=datetime.date(1960, 1, 1))

    father_name = st.text_input("نام پدر:")
    father_dob = st.date_input("تاریخ تولد پدر:", value=datetime.date(1960, 1, 1))

    spouse_name = st.text_input("نام همسر:")
    spouse_mother = st.text_input("نام مادر همسر:")

    st.markdown("### 👨‍👩‍👧‍👦 فرزندان (حداکثر ۲)")
    child_1 = st.text_input("نام فرزند اول:")
    child_1_dob = st.date_input("تاریخ تولد فرزند اول:", value=datetime.date(2010, 1, 1))
    child_2 = st.text_input("نام فرزند دوم:")
    child_2_dob = st.date_input("تاریخ تولد فرزند دوم:", value=datetime.date(2012, 1, 1))

    submitted = st.form_submit_button("محاسبه و تحلیل")

# تابع محاسبه ابجد کبیر
def abjad(name):
    table = {
        'ا':1,'ب':2,'ج':3,'د':4,'ه':5,'و':6,'ز':7,'ح':8,'ط':9,
        'ی':10,'ک':20,'ل':30,'م':40,'ن':50,'س':60,'ع':70,'ف':80,'ص':90,
        'ق':100,'ر':200,'ش':300,'ت':400,'ث':500,'خ':600,'ذ':700,'ض':800,
        'ظ':900,'غ':1000,'ء':0,' ':0,'آ':1,'ة':400
    }
    return sum([table.get(ch, 0) for ch in name])

# فاز ماه
def moon_phase(d):
    diff = d - datetime.date(2001,1,1)
    days = diff.days % 29.53
    phase = round((days / 29.53) * 8)
    phases = ['🌑 محاق', '🌒 هلال', '🌓 تربیع اول', '🌔 قرص در حال افزایش', '🌕 بدر', '🌖 قرص در حال کاهش', '🌗 تربیع دوم', '🌘 پایان ماه']
    return phases[phase % 8]

# آیه
def get_verse(num):
    return f"سوره ۵، آیه {num}: «کُلُّ نَفْسٍ بِمَا كَسَبَتْ رَهِينَةٌ»"

# مرگ نفس
def soul_exit(dob):
    base = dob.year + randint(47, 63)
    return f"📅 زمان تقریبی مرگ نفس: سال {base}"

# تحلیل همسر روحی
def soulmate_analysis(your_name, your_mom, spouse, spouse_mom):
    if not spouse or not spouse_mom:
        return "🔻 اطلاعات ناقص برای تحلیل همسر روحی"

    total_you = abjad(your_name) + abjad(your_mom)
    total_spouse = abjad(spouse) + abjad(spouse_mom)

    diff = abs(total_you - total_spouse)
    closeness = 100 - (diff % 100)

    return f"""
    💞 تحلیل هماهنگی با همسر:
    - مجموع ابجد شما: {total_you}
    - مجموع ابجد همسر: {total_spouse}
    - درصد هماهنگی روحی: {closeness}٪
    - تفسیر: {"👫 هماهنگ و متعادل" if closeness >= 70 else "⚠️ نیازمند کار و درک بیشتر"}
    """

# اجرای تحلیل‌ها
if submitted:
    st.subheader("🔮 نتایج تحلیل:")

    val1 = abjad(full_name)
    val2 = abjad(mother_name)
    total_val = val1 + val2

    st.write(f"🔢 مجموع ابجد نام و مادر: {total_val}")
    st.write(f"🌙 فاز ماه تولد شما: {moon_phase(name_dob)}")
    st.write(get_verse(total_val % 120))
    st.write(soul_exit(name_dob))

    st.markdown("---")
    st.subheader("🧩 تحلیل همسر روحی")
    st.markdown(soulmate_analysis(full_name, mother_name, spouse_name, spouse_mother))

    st.markdown("---")
    st.subheader("👧 تحلیل فرزندان:")
    if child_1:
        st.write(f"{child_1} - ابجد: {abjad(child_1)} - فاز ماه: {moon_phase(child_1_dob)}")
    if child_2:
        st.write(f"{child_2} - ابجد: {abjad(child_2)} - فاز ماه: {moon_phase(child_2_dob)}")

    st.markdown("---")
    st.caption("🧿 این تحلیل صرفاً جهت الهام معنوی و شناخت شخصی است.")