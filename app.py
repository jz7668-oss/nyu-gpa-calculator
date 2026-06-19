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

st.markdown("""
<style>
/* Tighten page top */
.block-container { padding-top: 1rem; padding-bottom: 0.5rem; }

/* Shrink title */
h1 { margin-bottom: 0 !important; font-size: 1.6rem !important; }

/* Remove form card border and padding */
[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
    background: transparent !important;
}

/* Tighten vertical gaps between all blocks */
[data-testid="stVerticalBlock"] > div { gap: 0.3rem; }

/* Compact input labels */
label { font-size: 0.8rem !important; margin-bottom: 0 !important; }

/* Compact metric labels and values */
[data-testid="stMetric"] { padding: 0.2rem 0 !important; }
[data-testid="stMetricLabel"] { font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { font-size: 1.1rem !important; }

/* Remove button text wrapping */
button[kind="secondary"], button[kind="primary"] {
    white-space: nowrap !important;
}

/* Tighten divider margin */
hr { margin: 0.4rem 0 !important; }

/* Compact expander header */
[data-testid="stExpander"] { margin-top: 0.2rem; }
</style>
""", unsafe_allow_html=True)

st.title("NYU GPA Calculator")
st.caption("Track grades and credit hours — GPA updates instantly.")

if "courses" not in st.session_state:
    st.session_state.courses = []

with st.form("add_course_form", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
    with col1:
        course_code = st.text_input("Course Code", placeholder="e.g. CSCI-UA 101")
    with col2:
        grade = st.selectbox("Letter Grade", list(GRADE_POINTS.keys()))
    with col3:
        credits = st.number_input("Credit Hours", min_value=0.5, max_value=6.0, value=3.0, step=0.5)
    with col4:
        st.markdown("<div style='padding-top:1.45rem'>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Add Course", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

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
    total_credits = sum(c["Credits"] for c in st.session_state.courses)
    total_quality = sum(c["Quality Points"] * c["Credits"] for c in st.session_state.courses)
    gpa = total_quality / total_credits

    col1, col2, col3, col4 = st.columns([2, 2, 3, 2])
    col1.metric("GPA", f"{gpa:.3f}")
    col2.metric("Total Credits", f"{total_credits:g}")
    col3.metric("Total Quality Points", f"{total_quality:.3f}")
    with col4:
        st.markdown("<div style='padding-top:1.45rem'>", unsafe_allow_html=True)
        if st.button("Reset", use_container_width=True):
            st.session_state.courses = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

COL_WIDTHS = [3, 1, 2, 1, 2, 1]
HEADERS = ["Course", "Grade", "Grade Points", "Credits", "Quality Points", ""]

header_cols = st.columns(COL_WIDTHS)
for col, label in zip(header_cols, HEADERS):
    col.markdown(f"<small><strong>{label}</strong></small>", unsafe_allow_html=True)

for i, course in enumerate(st.session_state.courses):
    c1, c2, c3, c4, c5, c6 = st.columns(COL_WIDTHS)
    c1.markdown(f"<small>{course['Course']}</small>", unsafe_allow_html=True)
    c2.markdown(f"<small>{course['Grade']}</small>", unsafe_allow_html=True)
    c3.markdown(f"<small>{course['Quality Points']:.3f}</small>", unsafe_allow_html=True)
    c4.markdown(f"<small>{course['Credits']:g}</small>", unsafe_allow_html=True)
    c5.markdown(f"<small>{course['Quality Points'] * course['Credits']:.3f}</small>", unsafe_allow_html=True)
    if c6.button("Remove", key=f"remove_{i}"):
        st.session_state.courses.pop(i)
        st.rerun()

st.divider()

with st.expander("How it works"):
    st.markdown(
        "- **Grade Points** come from the selected letter grade (e.g. A = 4.000)\n"
        "- **Quality Points** = Grade Points × Credit Hours\n"
        "- **GPA** = Total Quality Points ÷ Total Credits"
    )

with st.expander("Future improvements"):
    st.markdown(
        "- Student profile support\n"
        "- Optional NYU email login\n"
        "- Automatic course import"
    )
