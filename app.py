import json
import os
import uuid
from datetime import date

import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AttendPro | Student Attendance",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# APPLICATION SETTINGS
# ============================================================

DATA_FILE = "attendance.json"

BRANCHES = [
    "CSE",
    "ECE",
    "EEE",
    "MECH",
    "CIVIL",
    "AI & ML",
    "IT",
    "Other",
]

YEARS = [
    "1st Year",
    "2nd Year",
    "3rd Year",
    "4th Year",
]

SECTIONS = [
    "A",
    "B",
    "C",
    "D",
]


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #111827 0%,
        #0f172a 100%
    );
}

.hero {
    padding: 28px 30px;
    border-radius: 22px;
    background: linear-gradient(
        135deg,
        #4f46e5 0%,
        #7c3aed 100%
    );
    color: white;
    margin-bottom: 24px;
    box-shadow: 0 15px 40px rgba(79,70,229,.25);
}

.hero h1 {
    margin: 0;
    font-size: 2.35rem;
    font-weight: 900;
}

.hero p {
    margin: 8px 0 0;
    color: #e0e7ff;
    font-weight: 600;
}

.section-title {
    font-size: 1.35rem;
    font-weight: 850;
    margin: 8px 0 16px;
}

.footer {
    margin-top: 30px;
    padding: 20px;
    border: 1px solid rgba(148,163,184,.18);
    border-radius: 18px;
    text-align: center;
    color: #94a3b8;
    font-weight: 600;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# JSON FUNCTIONS
# ============================================================

def empty_data():
    return {
        "students": [],
        "attendance": []
    }


def ensure_data_file():
    if not os.path.exists(DATA_FILE):
        save_data(empty_data())


def load_data():

    ensure_data_file()

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, dict):
            return empty_data()

        students_data = data.get(
            "students",
            []
        )

        attendance_data = data.get(
            "attendance",
            []
        )

        if not isinstance(
            students_data,
            list
        ):
            students_data = []

        if not isinstance(
            attendance_data,
            list
        ):
            attendance_data = []

        return {
            "students": students_data,
            "attendance": attendance_data
        }

    except (
        json.JSONDecodeError,
        OSError
    ):

        return empty_data()


def save_data(data):

    try:

        temporary_file = DATA_FILE + ".tmp"

        with open(
            temporary_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        os.replace(
            temporary_file,
            DATA_FILE
        )

        return True

    except OSError as error:

        st.error(
            f"Could not save attendance.json: {error}"
        )

        return False


# ============================================================
# SESSION STATE
# ============================================================

if "data" not in st.session_state:

    st.session_state.data = load_data()


if "edit_student_id" not in st.session_state:

    st.session_state.edit_student_id = None


if "delete_student_id" not in st.session_state:

    st.session_state.delete_student_id = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def students():
    return st.session_state.data["students"]


def attendance():
    return st.session_state.data["attendance"]


def get_student(student_id):

    return next(
        (
            student
            for student in students()
            if student["id"] == student_id
        ),
        None
    )


def student_stats(student_id):

    records = [
        item
        for item in attendance()
        if item.get("student_id") == student_id
    ]

    total = len(records)

    present = sum(
        item.get("status") == "Present"
        for item in records
    )

    absent = sum(
        item.get("status") == "Absent"
        for item in records
    )

    percentage = (
        present / total * 100
        if total
        else 0.0
    )

    return (
        total,
        present,
        absent,
        percentage
    )


def class_sessions():

    return {
        (
            item.get("date", ""),
            item.get(
                "subject",
                ""
            ).strip().lower()
        )
        for item in attendance()
    }


def student_label(student):

    return (
        f"{student['roll_no']} • "
        f"{student['name']}"
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🎓 AttendPro"
    )

    st.caption(
        "Student Attendance Management"
    )

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "📊 Dashboard",
            "👨‍🎓 Students",
            "📝 Record Attendance",
            "📈 Reports",
        ],
        key="navigation_page"
    )

    st.divider()

    st.markdown(
        "### 👨‍💻 Developer"
    )

    st.markdown(
        "**Sheik Mohammad Riyaaz**"
    )

    st.caption(
        "B.Tech CSE • 3rd Year"
    )


# ============================================================
# DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.markdown(
        '<div class="hero">'
        '<h1>🎓 Attendance Dashboard</h1>'
        '<p>Monitor students, classes and attendance performance in one place.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    total_students = len(
        students()
    )

    total_sessions = len(
        class_sessions()
    )

    total_present = sum(
        item.get("status") == "Present"
        for item in attendance()
    )

    total_absent = sum(
        item.get("status") == "Absent"
        for item in attendance()
    )

    total_records = (
        total_present +
        total_absent
    )

    overall = (
        total_present /
        total_records *
        100
        if total_records
        else 0
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "👨‍🎓 Students",
            total_students
        )

    with c2:
        st.metric(
            "📚 Classes",
            total_sessions
        )

    with c3:
        st.metric(
            "✅ Present",
            total_present
        )

    with c4:
        st.metric(
            "❌ Absent",
            total_absent
        )

    with c5:
        st.metric(
            "📊 Overall",
            f"{overall:.1f}%"
        )

    st.divider()

    if not students():

        st.info(
            "No students yet. "
            "Open Students and add your first student."
        )

    elif not attendance():

        st.warning(
            "Students are ready. "
            "Record the first attendance session."
        )

    else:

        rows = []

        for student in students():

            total, present, absent, percentage = (
                student_stats(
                    student["id"]
                )
            )

            rows.append(
                {
                    "Roll No": student["roll_no"],
                    "Student": student["name"],
                    "Branch": student["branch"],
                    "Year": student["year"],
                    "Present": present,
                    "Absent": absent,
                    "Total": total,
                    "Attendance %": round(
                        percentage,
                        2
                    ),
                }
            )

        dashboard_df = pd.DataFrame(
            rows
        )

        st.markdown(
            '<div class="section-title">'
            '📋 Student Overview'
            '</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            dashboard_df,
            use_container_width=True,
            hide_index=True
        )

        left, right = st.columns(2)

        with left:

            st.markdown(
                "#### 📈 Attendance by Student"
            )

            chart_df = (
                dashboard_df[
                    [
                        "Student",
                        "Attendance %"
                    ]
                ]
                .set_index("Student")
            )

            st.bar_chart(
                chart_df
            )

        with right:

            st.markdown(
                "#### 📊 Present vs Absent"
            )

            status_df = pd.DataFrame(
                {
                    "Count": [
                        total_present,
                        total_absent
                    ]
                },
                index=[
                    "Present",
                    "Absent"
                ]
            )

            st.bar_chart(
                status_df
            )

        low_df = dashboard_df[
            dashboard_df["Attendance %"] < 75
        ]

        st.markdown(
            "#### ⚠️ Attendance Monitoring"
        )

        if low_df.empty:

            st.success(
                "No student is below 75% attendance."
            )

        else:

            st.warning(
                f"{len(low_df)} student(s) "
                "are below 75% attendance."
            )

            st.dataframe(
                low_df,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# STUDENT MANAGEMENT
# ============================================================

elif page == "👨‍🎓 Students":

    st.markdown(
        '<div class="section-title">'
        '👨‍🎓 Student Management'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Create, view, edit, search and delete student records."
    )

    # --------------------------------------------------------
    # ADD STUDENT
    # --------------------------------------------------------

    with st.form(
        "add_student_form",
        clear_on_submit=True
    ):

        st.markdown(
            "#### ➕ Add New Student"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            roll_no = st.text_input(
                "Roll Number",
                placeholder="23CSE001"
            )

            name = st.text_input(
                "Student Name",
                placeholder="Full name"
            )

        with col2:

            branch = st.selectbox(
                "Branch",
                BRANCHES
            )

            year = st.selectbox(
                "Year",
                YEARS,
                index=2
            )

        with col3:

            section = st.selectbox(
                "Section",
                SECTIONS
            )

            submitted = st.form_submit_button(
                "➕ Add Student",
                use_container_width=True
            )

        if submitted:

            clean_roll = roll_no.strip()

            clean_name = name.strip()

            if (
                not clean_roll
                or not clean_name
            ):

                st.error(
                    "Roll number and student name are required."
                )

            elif any(
                student["roll_no"]
                .strip()
                .lower()
                == clean_roll.lower()
                for student in students()
            ):

                st.error(
                    "A student with this roll number already exists."
                )

            else:

                new_student = {
                    "id": str(
                        uuid.uuid4()
                    ),
                    "roll_no": clean_roll,
                    "name": clean_name,
                    "branch": branch,
                    "year": year,
                    "section": section
                }

                st.session_state.data[
                    "students"
                ].append(
                    new_student
                )

                if save_data(
                    st.session_state.data
                ):

                    st.success(
                        "Student added successfully."
                    )

                    st.rerun()

    st.divider()

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    st.markdown(
        "#### 🔎 Search & Filter"
    )

    f1, f2, f3 = st.columns(3)

    with f1:

        search = st.text_input(
            "Search name / roll number",
            key="students_search"
        )

    with f2:

        branch_filter = st.selectbox(
            "Branch filter",
            ["All"] + BRANCHES,
            key="students_branch_filter"
        )

    with f3:

        year_filter = st.selectbox(
            "Year filter",
            ["All"] + YEARS,
            key="students_year_filter"
        )

    filtered = students()

    if search.strip():

        term = search.strip().lower()

        filtered = [
            student
            for student in filtered
            if (
                term in student["name"].lower()
                or
                term in student["roll_no"].lower()
            )
        ]

    if branch_filter != "All":

        filtered = [
            student
            for student in filtered
            if student["branch"]
            == branch_filter
        ]

    if year_filter != "All":

        filtered = [
            student
            for student in filtered
            if student["year"]
            == year_filter
        ]

    if filtered:

        table_rows = []

        for student in filtered:

            total, present, absent, percentage = (
                student_stats(
                    student["id"]
                )
            )

            table_rows.append(
                {
                    "Roll No": student["roll_no"],
                    "Name": student["name"],
                    "Branch": student["branch"],
                    "Year": student["year"],
                    "Section": student["section"],
                    "Present": present,
                    "Absent": absent,
                    "Attendance %": (
                        f"{percentage:.2f}%"
                    ),
                }
            )

        st.dataframe(
            pd.DataFrame(table_rows),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No students match your search or filters."
        )

    # --------------------------------------------------------
    # EDIT / DELETE
    # --------------------------------------------------------

    if students():

        st.divider()

        st.markdown(
            "#### ⚙️ Manage Existing Student"
        )

        options = {
            student_label(student):
            student["id"]
            for student in students()
        }

        selected_label = st.selectbox(
            "Select student",
            list(options.keys()),
            key="manage_student_select"
        )

        selected_id = options[
            selected_label
        ]

        b1, b2 = st.columns(2)

        with b1:

            if st.button(
                "✏️ Edit Student",
                use_container_width=True,
                key="edit_student_action"
            ):

                st.session_state.edit_student_id = (
                    selected_id
                )

                st.session_state.delete_student_id = None

                st.rerun()

        with b2:

            if st.button(
                "🗑️ Delete Student",
                use_container_width=True,
                key="delete_student_action"
            ):

                st.session_state.delete_student_id = (
                    selected_id
                )

                st.session_state.edit_student_id = None

                st.rerun()

    # --------------------------------------------------------
    # EDIT FORM
    # --------------------------------------------------------

    if st.session_state.edit_student_id:

        student = get_student(
            st.session_state.edit_student_id
        )

        if student:

            st.divider()

            st.markdown(
                "#### ✏️ Edit Student"
            )

            with st.form(
                "edit_student_form"
            ):

                e1, e2 = st.columns(2)

                with e1:

                    edit_roll = st.text_input(
                        "Roll Number",
                        value=student["roll_no"]
                    )

                    edit_name = st.text_input(
                        "Student Name",
                        value=student["name"]
                    )

                    edit_branch = st.selectbox(
                        "Branch",
                        BRANCHES,
                        index=(
                            BRANCHES.index(
                                student["branch"]
                            )
                            if student["branch"]
                            in BRANCHES
                            else 0
                        )
                    )

                with e2:

                    edit_year = st.selectbox(
                        "Year",
                        YEARS,
                        index=(
                            YEARS.index(
                                student["year"]
                            )
                            if student["year"]
                            in YEARS
                            else 0
                        )
                    )

                    edit_section = st.selectbox(
                        "Section",
                        SECTIONS,
                        index=(
                            SECTIONS.index(
                                student["section"]
                            )
                            if student["section"]
                            in SECTIONS
                            else 0
                        )
                    )

                ec1, ec2 = st.columns(2)

                with ec1:

                    update_button = (
                        st.form_submit_button(
                            "💾 Save Changes",
                            use_container_width=True
                        )
                    )

                with ec2:

                    cancel_button = (
                        st.form_submit_button(
                            "❌ Cancel",
                            use_container_width=True
                        )
                    )

                if update_button:

                    clean_roll = (
                        edit_roll.strip()
                    )

                    clean_name = (
                        edit_name.strip()
                    )

                    duplicate = any(
                        other["id"]
                        != student["id"]
                        and
                        other["roll_no"]
                        .strip()
                        .lower()
                        == clean_roll.lower()
                        for other in students()
                    )

                    if (
                        not clean_roll
                        or not clean_name
                    ):

                        st.error(
                            "Roll number and student name are required."
                        )

                    elif duplicate:

                        st.error(
                            "Another student already uses this roll number."
                        )

                    else:

                        student.update(
                            {
                                "roll_no": clean_roll,
                                "name": clean_name,
                                "branch": edit_branch,
                                "year": edit_year,
                                "section": edit_section,
                            }
                        )

                        if save_data(
                            st.session_state.data
                        ):

                            st.session_state.edit_student_id = None

                            st.success(
                                "Student updated successfully."
                            )

                            st.rerun()

                if cancel_button:

                    st.session_state.edit_student_id = None

                    st.rerun()

    # --------------------------------------------------------
    # DELETE CONFIRMATION
    # --------------------------------------------------------

    if st.session_state.delete_student_id:

        student = get_student(
            st.session_state.delete_student_id
        )

        if student:

            st.divider()

            st.warning(
                f"Delete **{student['name']} "
                f"({student['roll_no']})**? "
                "Their attendance records will also be removed."
            )

            d1, d2 = st.columns(2)

            with d1:

                if st.button(
                    "✅ Confirm Delete",
                    use_container_width=True,
                    key="confirm_delete_action"
                ):

                    deleted_id = student["id"]

                    st.session_state.data[
                        "students"
                    ] = [
                        item
                        for item in students()
                        if item["id"]
                        != deleted_id
                    ]

                    st.session_state.data[
                        "attendance"
                    ] = [
                        item
                        for item in attendance()
                        if item.get(
                            "student_id"
                        )
                        != deleted_id
                    ]

                    if save_data(
                        st.session_state.data
                    ):

                        st.session_state.delete_student_id = None

                        st.success(
                            "Student deleted successfully."
                        )

                        st.rerun()

            with d2:

                if st.button(
                    "❌ Cancel Delete",
                    use_container_width=True,
                    key="cancel_delete_action"
                ):

                    st.session_state.delete_student_id = None

                    st.rerun()


# ============================================================
# RECORD ATTENDANCE
# ============================================================

elif page == "📝 Record Attendance":

    st.markdown(
        '<div class="section-title">'
        '📝 Record Attendance'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Choose one date and subject, then mark every student."
    )

    if not students():

        st.info(
            "Add students first from the Students section."
        )

    else:

        with st.form(
            "record_attendance_form"
        ):

            c1, c2 = st.columns(2)

            with c1:

                attendance_date = st.date_input(
                    "Date",
                    value=date.today()
                )

            with c2:

                subject = st.text_input(
                    "Subject",
                    placeholder="DBMS"
                )

            st.markdown(
                "#### 👨‍🎓 Mark Students"
            )

            statuses = {}

            for index, student in enumerate(
                students()
            ):

                st.markdown(
                    f"**{student['roll_no']} — "
                    f"{student['name']}**"
                )

                statuses[
                    student["id"]
                ] = st.radio(
                    "Attendance status",
                    [
                        "Present",
                        "Absent"
                    ],
                    index=0,
                    horizontal=True,
                    key=(
                        f"attendance_"
                        f"{student['id']}_"
                        f"{index}"
                    ),
                    label_visibility="collapsed"
                )

            save_attendance = (
                st.form_submit_button(
                    "💾 Save Attendance",
                    use_container_width=True
                )
            )

            if save_attendance:

                clean_subject = (
                    subject.strip()
                )

                session_key = (
                    attendance_date.isoformat(),
                    clean_subject.lower()
                )

                if not clean_subject:

                    st.error(
                        "Subject is required."
                    )

                elif session_key in class_sessions():

                    st.error(
                        "Attendance for this date and subject already exists."
                    )

                else:

                    for student in students():

                        st.session_state.data[
                            "attendance"
                        ].append(
                            {
                                "id": str(
                                    uuid.uuid4()
                                ),
                                "student_id":
                                    student["id"],
                                "date":
                                    attendance_date.isoformat(),
                                "subject":
                                    clean_subject,
                                "status":
                                    statuses[
                                        student["id"]
                                    ],
                            }
                        )

                    if save_data(
                        st.session_state.data
                    ):

                        st.success(
                            "Attendance saved successfully."
                        )

                        st.rerun()


# ============================================================
# REPORTS
# ============================================================

elif page == "📈 Reports":

    st.markdown(
        '<div class="section-title">'
        '📈 Attendance Reports'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Search students and view detailed attendance history."
    )

    if not students():

        st.info(
            "Add students first."
        )

    else:

        r1, r2, r3 = st.columns(3)

        with r1:

            report_search = st.text_input(
                "Search",
                key="report_search"
            )

        with r2:

            report_branch = st.selectbox(
                "Branch",
                ["All"] + BRANCHES,
                key="report_branch"
            )

        with r3:

            report_year = st.selectbox(
                "Year",
                ["All"] + YEARS,
                key="report_year"
            )

        report_students = students()

        if report_search.strip():

            term = (
                report_search
                .strip()
                .lower()
            )

            report_students = [
                student
                for student in report_students
                if (
                    term
                    in student["name"].lower()
                    or
                    term
                    in student["roll_no"].lower()
                )
            ]

        if report_branch != "All":

            report_students = [
                student
                for student in report_students
                if student["branch"]
                == report_branch
            ]

        if report_year != "All":

            report_students = [
                student
                for student in report_students
                if student["year"]
                == report_year
            ]

        report_rows = []

        for student in report_students:

            total, present, absent, percentage = (
                student_stats(
                    student["id"]
                )
            )

            report_rows.append(
                {
                    "Roll No": student["roll_no"],
                    "Student": student["name"],
                    "Branch": student["branch"],
                    "Present": present,
                    "Absent": absent,
                    "Total Classes": total,
                    "Attendance %": round(
                        percentage,
                        2
                    ),
                }
            )

        if not report_rows:

            st.info(
                "No students match your filters."
            )

        else:

            report_df = pd.DataFrame(
                report_rows
            )

            st.dataframe(
                report_df,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            st.markdown(
                "#### 🔍 Individual Student"
            )

            options = {
                student_label(student):
                student["id"]
                for student in report_students
            }

            selected_label = st.selectbox(
                "Select student",
                list(options.keys()),
                key="report_student_select"
            )

            selected_id = options[
                selected_label
            ]

            total, present, absent, percentage = (
                student_stats(
                    selected_id
                )
            )

            a, b, c, d = st.columns(4)

            with a:
                st.metric(
                    "Total Classes",
                    total
                )

            with b:
                st.metric(
                    "Present",
                    present
                )

            with c:
                st.metric(
                    "Absent",
                    absent
                )

            with d:
                st.metric(
                    "Attendance",
                    f"{percentage:.2f}%"
                )

            records = [
                item
                for item in attendance()
                if item.get("student_id")
                == selected_id
            ]

            if records:

                detail_df = pd.DataFrame(
                    [
                        {
                            "Date": item.get(
                                "date",
                                ""
                            ),
                            "Subject": item.get(
                                "subject",
                                ""
                            ),
                            "Status": item.get(
                                "status",
                                ""
                            ),
                        }
                        for item in sorted(
                            records,
                            key=lambda item:
                            item.get(
                                "date",
                                ""
                            ),
                            reverse=True
                        )
                    ]
                )

                st.dataframe(
                    detail_df,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "No attendance records for this student yet."
                )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    '🎓 AttendPro • Python + Streamlit + JSON'
    '<br>'
    'Developed by <b>Sheik Mohammad Riyaaz</b>'
    '</div>',
    unsafe_allow_html=True
)