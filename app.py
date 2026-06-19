import streamlit as st

GRADE_POINTS = {
    "A":  4.000,
    "A-": 3.667,
    "B+": 3.333,
    "B":  3.000,
    "B-": 2.667,
    "C+": 2.333,
    "C":  2.000,
    "F":  0.000,
}

st.title("NYU GPA Calculator")

if "courses" not in st.session_state:
    st.session_state.courses = []

with st.form("add_course_form", clear_on_submit=True):
    st.subheader("Add a Course")
    col1, col2, col3 = st.columns(3)
    with col1:
        course_code = st.text_input("Course Code", placeholder="e.g. CSCI-UA 101")
    with col2:
        grade = st.selectbox("Letter Grade", list(GRADE_POINTS.keys()))
    with col3:
        credits = st.number_input("Credit Hours", min_value=0.5, max_value=6.0, value=3.0, step=0.5)
    submitted = st.form_submit_button("Add Course")

if submitted:
    if not course_code.strip():
        st.warning("Please enter a course code.")
    else:
        st.session_state.courses.append({
            "Course": course_code.strip(),
            "Grade": grade,
            "Credits": credits,
            "Quality Points": GRADE_POINTS[grade],
        })

if st.session_state.courses:
    st.subheader("Your Courses")

    header = st.columns([3, 1, 1, 2, 1])
    for col, label in zip(header, ["Course", "Grade", "Credits", "Quality Points", "Action"]):
        col.markdown(f"**{label}**")

    for i, course in enumerate(st.session_state.courses):
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 2, 1])
        col1.write(course["Course"])
        col2.write(course["Grade"])
        col3.write(f'{course["Credits"]:g}')
        col4.write(f'{course["Quality Points"] * course["Credits"]:.3f}')
        if col5.button("Remove", key=f"remove_{i}"):
            st.session_state.courses.pop(i)
            st.rerun()

    total_credits = sum(c["Credits"] for c in st.session_state.courses)
    total_quality = sum(c["Quality Points"] * c["Credits"] for c in st.session_state.courses)
    gpa = total_quality / total_credits

    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Credits", f"{total_credits:g}")
    col2.metric("Total Quality Points", f"{total_quality:.3f}")
    col3.metric("GPA", f"{gpa:.3f}")

    if st.button("Reset"):
        st.session_state.courses = []
        st.rerun()
