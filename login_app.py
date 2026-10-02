
# from datetime import date
# import sqlite3
# import pandas as pd
# import streamlit as st
# import base64

# # Page Config
# st.set_page_config(
#     page_title="Youva Pahal - Free Coaching Centre", page_icon="🎓", layout="wide"
# )

# DB_NAME = "institute_management.db"

# # --- DATABASE SETUP & PERFORMANCE OPTIMIZATIONS ---
# def get_db_connection():
#   conn = sqlite3.connect(DB_NAME, check_same_thread=False, timeout=30)
#   conn.execute("PRAGMA journal_mode=WAL;")
#   conn.row_factory = sqlite3.Row
#   return conn

# def init_db():
#   conn = get_db_connection()
#   try:
#     cursor = conn.cursor()

#     # Users Table for Admin & Students
#     cursor.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 username TEXT PRIMARY KEY,
#                 password TEXT NOT NULL,
#                 role TEXT NOT NULL,
#                 name TEXT
#             )
#         """)
#     cursor.execute(
#         "INSERT OR IGNORE INTO users VALUES ('admin', 'admin123', 'Admin', 'Administrator')"
#     )

#     # Enrollments Table for Tracking Course Purchases
#     cursor.execute("""
#             CREATE TABLE IF NOT EXISTS enrollments (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 student_name TEXT,
#                 email TEXT,
#                 course_name TEXT,
#                 fees TEXT,
#                 purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#         """)

#     # Students Record Table
#     cursor.execute("""
#             CREATE TABLE IF NOT EXISTS students (
#                 roll_no TEXT PRIMARY KEY,
#                 name TEXT NOT NULL,
#                 fathers_name TEXT NOT NULL,
#                 dob TEXT NOT NULL,
#                 email TEXT NOT NULL,
#                 gender TEXT NOT NULL,
#                 class TEXT NOT NULL,
#                 section TEXT NOT NULL,
#                 contact TEXT NOT NULL,
#                 address TEXT NOT NULL
#             )
#         """)

#     # Courses Table
#     cursor.execute("""
#             CREATE TABLE IF NOT EXISTS courses (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 course_name TEXT,
#                 batch_time TEXT,
#                 fees TEXT,
#                 description TEXT
#             )
#         """)

#     # Public Posts & Batches Table
#     cursor.execute("""
#             CREATE TABLE IF NOT EXISTS public_posts (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 title TEXT,
#                 content TEXT,
#                 category TEXT,
#                 status TEXT,
#                 image BLOB,
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#         """)

#     # Attendance Table
#     cursor.execute("""
#             CREATE TABLE IF NOT EXISTS attendance (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 roll_no TEXT,
#                 student_name TEXT,
#                 class TEXT,
#                 date TEXT,
#                 status TEXT
#             )
#         """)

#     # Safe Migration: Image column check
#     try:
#       cursor.execute("ALTER TABLE public_posts ADD COLUMN image BLOB;")
#       conn.commit()
#     except sqlite3.OperationalError:
#       pass

#     # Default courses agar table khali ho
#     cursor.execute("SELECT COUNT(*) FROM courses")
#     if cursor.fetchone()[0] == 0:
#       cursor.executemany(
#           "INSERT INTO courses (course_name, batch_time, fees, description) VALUES (?, ?, ?, ?)",
#           [
#               (
#                   "Basic Mathematics (Nursery - 4th)",
#                   "Morning (8:00 AM - 9:00 AM)",
#                   "Free",
#                   "Fundamental mathematical concepts for young students completely free of cost.",
#               ),
#               (
#                   "Junior English & Grammar (5th - 8th)",
#                   "Evening (4:00 PM - 5:00 PM)",
#                   "Free",
#                   "Building strong English communication and grammar foundations.",
#               ),
#               (
#                   "General Science Basics",
#                   "Weekend (10:00 AM - 11:30 AM)",
#                   "Free",
#                   "Interactive science learning sessions for underprivileged children.",
#               ),
#           ],
#       )
#     conn.commit()
#   finally:
#     conn.close()

# # Run init_db only once using session state
# if "db_initialized" not in st.session_state:
#   init_db()
#   st.session_state.db_initialized = True

# # Cached data fetchers
# @st.cache_data(ttl=60)
# def fetch_all_courses():
#   conn = get_db_connection()
#   try:
#     df = pd.read_sql("SELECT * FROM courses", conn)
#   finally:
#     conn.close()
#   return df

# @st.cache_data(ttl=5)
# def fetch_all_students():
#   conn = get_db_connection()
#   try:
#     df = pd.read_sql("SELECT * FROM students", conn)
#   finally:
#     conn.close()
#   return df

# # Session States
# if "logged_in" not in st.session_state:
#   st.session_state.logged_in = False
# if "username" not in st.session_state:
#   st.session_state.username = ""
# if "role" not in st.session_state:
#   st.session_state.role = ""
# if "user_logged_in" not in st.session_state:
#   st.session_state.user_logged_in = False

# # --- SIDEBAR: ADMIN LOGIN LINK ---
# st.sidebar.title("🧭 Navigation")

# with st.sidebar.expander("🔒 Admin Portal Login"):
#   if not st.session_state.logged_in:
#     adm_user = st.text_input("Admin Username", key="adm_u")
#     adm_pass = st.text_input("Admin Password", type="password", key="adm_p")
#     if st.button("Login as Admin"):
#       conn = get_db_connection()
#       try:
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT role FROM users WHERE username=? AND password=? AND role='Admin'",
#             (adm_user, adm_pass),
#         )
#         res = cursor.fetchone()
#       finally:
#         conn.close()

#       if res:
#         st.session_state.logged_in = True
#         st.session_state.username = adm_user
#         st.session_state.role = "Admin"
#         st.success("Admin Login Successful!")
#         st.rerun()
#       else:
#         st.error("Invalid Admin Credentials!")
#   else:
#     st.write(f"Logged in as **{st.session_state.username}**")
#     if st.button("Admin Logout"):
#       st.session_state.logged_in = False
#       st.session_state.username = ""
#       st.session_state.role = ""
#       st.rerun()

# st.sidebar.markdown("---")

# # ==========================================
# # SCENARIO 1: ADMIN PANEL (Logged In)
# # ==========================================
# if st.session_state.logged_in and st.session_state.role == "Admin":
#   st.title("🛠 Admin Dashboard - Institute Management")
#   st.info("Aap yahan students ke records, courses aur attendance manage kar sakte hain.")

#   menu = st.sidebar.selectbox(
#       "Admin Menu",
#       [
#           "Manage Students Records",
#           "Search Students",
#           "Manage Courses",
#           "View Course Purchases",
#           "Manage Public Posts",
#           "Manage Attendance",
#       ],
#   )

#   if menu == "Manage Students Records":
#     st.subheader("📋 Student Records Database")
#     df = fetch_all_students()

#     selected_roll = ""
#     selected_data = None

#     if not df.empty:
#       df.columns = [
#           "Roll No",
#           "Name",
#           "Father's Name",
#           "D.O.B",
#           "Email",
#           "Gender",
#           "Class",
#           "Section",
#           "Contact",
#           "Address",
#       ]
#       st.write("👉 *Table me kisi bhi row par click karke select karein:*")
#       event = st.dataframe(
#           df,
#           use_container_width=True,
#           on_select="rerun",
#           selection_mode="single-row",
#       )
#       if event.selection.rows:
#         selected_row = df.iloc[event.selection.rows[0]]
#         selected_roll = selected_row["Roll No"]
#         conn = get_db_connection()
#         try:
#           cursor = conn.cursor()
#           cursor.execute(
#               "SELECT * FROM students WHERE roll_no = ?", (selected_roll,)
#           )
#           selected_data = cursor.fetchone()
#         finally:
#           conn.close()
#     else:
#       st.info("No student records found yet.")

#     st.markdown("---")
#     st.subheader(
#         "✏️ Add / Update Student Form"
#         + (f" (Selected: {selected_roll})" if selected_roll else "")
#     )

#     def_roll = selected_data[0] if selected_data else ""
#     def_name = selected_data[1] if selected_data else ""
#     def_fname = selected_data[2] if selected_data else ""
#     def_dob = selected_data[3] if selected_data else ""
#     def_email = selected_data[4] if selected_data else ""
#     def_gender = selected_data[5] if selected_data else "Male"
#     def_cls = selected_data[6] if selected_data else ""
#     def_sec = selected_data[7] if selected_data else ""
#     def_contact = selected_data[8] if selected_data else ""
#     def_addr = selected_data[9] if selected_data else ""

#     gender_options = ["Male", "Female", "Other"]
#     gender_index = (
#         gender_options.index(def_gender) if def_gender in gender_options else 0
#     )

#     with st.form("admin_student_form"):
#       c1, c2, c3 = st.columns(3)
#       with c1:
#         roll = st.text_input("Roll No", value=def_roll)
#         name = st.text_input("Name", value=def_name)
#         fathers_name = st.text_input("Father's Name", value=def_fname)
#       with c2:
#         dob = st.text_input("D.O.B (DD/MM/YYYY)", value=def_dob)
#         email = st.text_input("Email", value=def_email)
#         gender = st.selectbox("Gender", gender_options, index=gender_index)
#       with c3:
#         cls = st.text_input("Class", value=def_cls)
#         section = st.text_input("Section", value=def_sec)
#         contact = st.text_input("Contact", value=def_contact)

#       address = st.text_area("Address", value=def_addr)

#       b1, b2, b3 = st.columns(3)
#       with b1:
#         add_b = st.form_submit_button("➕ Add Student")
#       with b2:
#         up_b = st.form_submit_button("🔄 Update Student")
#       with b3:
#         del_b = st.form_submit_button("🗑️ Delete Student")

#       if add_b:
#         if roll and name:
#           conn = get_db_connection()
#           try:
#             cursor = conn.cursor()
#             cursor.execute(
#                 "INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?)",
#                 (
#                     roll,
#                     name,
#                     fathers_name,
#                     dob,
#                     email,
#                     gender,
#                     cls,
#                     section,
#                     contact,
#                     address,
#                 ),
#             )
#             default_pass = contact if contact else "123456"
#             cursor.execute(
#                 "INSERT OR IGNORE INTO users VALUES (?, ?, 'Student', ?)",
#                 (email, default_pass, name),
#             )
#             conn.commit()
#             st.cache_data.clear()
#             st.success(
#                 f"Student added successfully! (Login Email: {email}, Default Password: {default_pass})"
#             )
#             st.rerun()
#           except sqlite3.IntegrityError:
#             st.error("Roll No ya Email pehle se exist karta hai!")
#           finally:
#             conn.close()
#         else:
#           st.warning("Fill required fields.")
#       if up_b:
#         if roll:
#           conn = get_db_connection()
#           try:
#             cursor = conn.cursor()
#             cursor.execute(
#                 """UPDATE students SET name=?, fathers_name=?, dob=?, email=?,
#                 gender=?, class=?, section=?, contact=?, address=? WHERE roll_no=?""",
#                 (
#                     name,
#                     fathers_name,
#                     dob,
#                     email,
#                     gender,
#                     cls,
#                     section,
#                     contact,
#                     address,
#                     roll,
#                 ),
#             )
#             conn.commit()
#             st.cache_data.clear()
#             st.success("Updated successfully!")
#             st.rerun()
#           finally:
#             conn.close()

#       if del_b:
#         if roll:
#           conn = get_db_connection()
#           try:
#             cursor = conn.cursor()
#             cursor.execute("DELETE FROM students WHERE roll_no=?", (roll,))
#             conn.commit()
#             st.cache_data.clear()
#             st.success("Deleted successfully!")
#             st.rerun()
#           finally:
#             conn.close()

#   elif menu == "Search Students":
#     st.subheader("🔍 Advanced Student Search Filter")
#     search_by = st.selectbox("Search By", ["Roll No", "Name", "Class", "Section"])
#     search_query = st.text_input("Search keyword enter karein")

#     if st.button("Search"):
#       col_map = {
#           "Roll No": "roll_no",
#           "Name": "name",
#           "Class": "class",
#           "Section": "section",
#       }
#       db_col = col_map[search_by]

#       conn = get_db_connection()
#       try:
#         cursor = conn.cursor()
#         cursor.execute(
#             f"SELECT * FROM students WHERE {db_col} LIKE ?",
#             ("%" + search_query + "%",),
#         )
#         results = cursor.fetchall()
#       finally:
#         conn.close()

#       if results:
#         df = pd.DataFrame(
#             results,
#             columns=[
#                 "Roll No",
#                 "Name",
#                 "Father's Name",
#                 "D.O.B",
#                 "Email",
#                 "Gender",
#                 "Class",
#                 "Section",
#                 "Contact",
#                 "Address",
#             ],
#         )
#         st.success(f"Total {len(results)} matching record(s) mile hain:")
#         st.dataframe(df, use_container_width=True)
#       else:
#         st.warning("Koi matching record nahi mila.")

#   elif menu == "Manage Courses":
#     st.subheader("📚 Add/Update Institute Courses")
#     with st.form("course_add_form"):
#       c_name = st.text_input("Course Name")
#       c_time = st.text_input("Batch Time (e.g., Morning 8 AM)")
#       c_fees = st.text_input("Fees (e.g., Free / ₹0)")
#       c_desc = st.text_area("Description")
#       submit_course = st.form_submit_button("Add Course")
#       if submit_course:
#         conn = get_db_connection()
#         try:
#           cursor = conn.cursor()
#           cursor.execute(
#               "INSERT INTO courses (course_name, batch_time, fees, description) VALUES (?, ?, ?, ?)",
#               (c_name, c_time, c_fees, c_desc),
#           )
#           conn.commit()
#           st.cache_data.clear()
#           st.success("Course added to website successfully!")
#           st.rerun()
#         finally:
#           conn.close()

#   elif menu == "View Course Purchases":
#     st.subheader("🛍️ Enrolled Students / Course Purchases List")
#     conn = get_db_connection()
#     try:
#       df_purchases = pd.read_sql(
#           "SELECT * FROM enrollments ORDER BY purchase_date DESC", conn
#       )
#     finally:
#       conn.close()

#     if not df_purchases.empty:
#       df_purchases.columns = [
#           "ID",
#           "Student Name",
#           "Email / Username",
#           "Course Name",
#           "Fees",
#           "Purchase Date",
#       ]
#       st.dataframe(df_purchases, use_container_width=True)
#     else:
#       st.info("Abhi tak kisi ne koi course enroll nahi kiya hai.")

#   elif menu == "Manage Public Posts":
#     st.subheader("📢 Manage Public Posts & Batches (with Image Support)")

#     with st.expander(
#         "➕ Add New Public Post / Batch with Thumbnail/Image", expanded=True
#     ):
#       with st.form("add_post_form"):
#         p_title = st.text_input("Title (e.g., Nursery & Primary Free Batch)")
#         p_content = st.text_area("Details / Description / Timings")
#         p_category = st.selectbox(
#             "Category", ["Batch", "Announcement", "Notice"]
#         )
#         p_status = st.selectbox("Status", ["Active", "Expired/Timeout"])

#         p_image_file = st.file_uploader(
#             "Upload Thumbnail / Poster Image (Optional)",
#             type=["jpg", "png", "jpeg"],
#         )

#         submit_post = st.form_submit_button("Publish to Public View")
#         if submit_post:
#           if p_title and p_content:
#             image_bytes = (
#                 p_image_file.read() if p_image_file is not None else None
#             )

#             conn = get_db_connection()
#             cursor = conn.cursor()
#             cursor.execute(
#                 "INSERT INTO public_posts (title, content, category, status, image) VALUES (?, ?, ?, ?, ?)",
#                 (p_title, p_content, p_category, p_status, image_bytes),
#             )
#             conn.commit()
#             conn.close()
#             st.success("Successfully public view me image ke sath add ho gaya!")
#             st.rerun()
#           else:
#             st.warning("Please title aur content bharein.")

#     st.markdown("---")
#     st.subheader("📋 Existing Public Posts & Batches (Update / Delete)")

#     conn = get_db_connection()
#     df_posts = pd.read_sql(
#         "SELECT id, title, content, category, status FROM public_posts ORDER BY id DESC",
#         conn,
#     )
#     conn.close()

#     if not df_posts.empty:
#       for index, row in df_posts.iterrows():
#         with st.container():
#           col1, col2, col3 = st.columns([3, 1, 1])
#           with col1:
#             st.markdown(
#                 f"**[{row['category']}] {row['title']}** (Status: `{row['status']}`)"
#             )
#             st.write(row["content"])
#           with col2:
#             new_status = st.selectbox(
#                 "Change Status",
#                 ["Active", "Expired/Timeout"],
#                 index=0 if row["status"] == "Active" else 1,
#                 key=f"status_{row['id']}",
#             )
#             if st.button("Update Status", key=f"up_btn_{row['id']}"):
#               conn = get_db_connection()
#               cursor = conn.cursor()
#               cursor.execute(
#                   "UPDATE public_posts SET status = ? WHERE id = ?",
#                   (new_status, row["id"]),
#               )
#               conn.commit()
#               conn.close()
#               st.success("Updated!")
#               st.rerun()
#           with col3:
#             st.write("")
#             if st.button("🗑️ Delete", key=f"del_post_{row['id']}"):
#               conn = get_db_connection()
#               cursor = conn.cursor()
#               cursor.execute(
#                   "DELETE FROM public_posts WHERE id = ?", (row["id"],)
#               )
#               conn.commit()
#               conn.close()
#               st.success("Deleted from public view!")
#               st.rerun()
#           st.divider()
#     else:
#       st.info("Koi public post ya batch available nahi hai.")

#   elif menu == "Manage Attendance":
#     st.subheader("📊 Online Attendance Management System")

#     tab_mark, tab_report = st.tabs(
#         ["📝 Mark Attendance", "📈 View Attendance Reports & Counts"]
#     )

#     with tab_mark:
#       st.write("👉 **Date aur Class select karke bachho ki attendance lagayein:**")

#       conn = get_db_connection()
#       classes_df = pd.read_sql("SELECT DISTINCT class FROM students", conn)
#       conn.close()

#       if not classes_df.empty:
#         class_list = classes_df["class"].tolist()
#         selected_class = st.selectbox(
#             "Select Class / Batch", class_list, key="att_class"
#         )
#         selected_date = st.date_input(
#             "Attendance Date", value=date.today(), key="att_date"
#         )

#         conn = get_db_connection()
#         students_in_class = pd.read_sql(
#             "SELECT roll_no, name FROM students WHERE class = ?",
#             conn,
#             params=(selected_class,),
#         )
#         conn.close()

#         if not students_in_class.empty:
#           st.info(
#               f"Total Students in Class {selected_class}: {len(students_in_class)}"
#           )

#           with st.form("attendance_form"):
#             st.markdown("---")
#             col_h1, col_h2, col_h3 = st.columns([1, 2, 1])
#             col_h1.markdown("**Roll No**")
#             col_h2.markdown("**Student Name**")
#             col_h3.markdown("**Status (Present/Absent)**")
#             st.markdown("---")

#             attendance_status = {}
#             for idx, s_row in students_in_class.iterrows():
#               r_no = s_row["roll_no"]
#               s_name = s_row["name"]

#               c1, c2, c3 = st.columns([1, 2, 1])
#               c1.write(f"`{r_no}`")
#               c2.write(f"**{s_name}**")

#               status = c3.radio(
#                   "Status",
#                   ["Present", "Absent"],
#                   key=f"status_{r_no}",
#                   horizontal=True,
#                   label_visibility="collapsed",
#               )
#               attendance_status[r_no] = (s_name, status)

#             st.markdown("---")
#             submitted_attendance = st.form_submit_button("💾 Save Attendance")

#             if submitted_attendance:
#               date_str = str(selected_date)
#               conn = get_db_connection()
#               cursor = conn.cursor()

#               for r_no, (s_name, status) in attendance_status.items():
#                 cursor.execute(
#                     "DELETE FROM attendance WHERE roll_no = ? AND class = ? AND date = ?",
#                     (r_no, selected_class, date_str),
#                 )
#                 cursor.execute(
#                     "INSERT INTO attendance (roll_no, student_name, class, date, status) VALUES (?, ?, ?, ?, ?)",
#                     (r_no, s_name, selected_class, date_str, status),
#                 )
#               conn.commit()
#               conn.close()
#               st.success(
#                   f"🎉 Date {date_str} ki attendance successfully save ho gayi hai!"
#               )
#         else:
#           st.warning("Is class me koi student registered nahi hai.")
#       else:
#         st.warning(
#             "Pehle 'Manage Students Records' se students add karein aur unhe class assign karein."
#         )

#     with tab_report:
#       st.subheader("📈 Automatic Attendance Counter & Reports")
#       conn = get_db_connection()
#       att_df = pd.read_sql("SELECT * FROM attendance", conn)
#       conn.close()

#       if not att_df.empty:
#         summary_data = []
#         grouped = att_df.groupby(["roll_no", "student_name", "class"])

#         for (r_no, s_name, s_class), group in grouped:
#           total_classes = len(group)
#           total_present = len(group[group["status"] == "Present"])
#           total_absent = len(group[group["status"] == "Absent"])
#           percentage = (
#               round((total_present / total_classes) * 100, 2)
#               if total_classes > 0
#               else 0
#           )

#           summary_data.append({
#               "Roll No": r_no,
#               "Student Name": s_name,
#               "Class": s_class,
#               "Total Classes": total_classes,
#               "Present Days": total_present,
#               "Absent Days": total_absent,
#               "Attendance %": f"{percentage}%",
#           })

#         summary_df = pd.DataFrame(summary_data)
#         st.dataframe(summary_df, use_container_width=True)

#         with st.expander("🔍 View Detailed Date-wise Attendance History"):
#           selected_r_no = st.text_input(
#               "Roll Number enter karein student ki history dekhne ke liye:"
#           )
#           if selected_r_no:
#             conn = get_db_connection()
#             hist_df = pd.read_sql(
#                 "SELECT date, status FROM attendance WHERE roll_no = ? ORDER BY date DESC",
#                 conn,
#                 params=(selected_r_no,),
#             )
#             conn.close()
#             if not hist_df.empty:
#               st.write(f"Attendance history for Roll No: `{selected_r_no}`")
#               st.dataframe(hist_df, use_container_width=True)
#             else:
#               st.warning("Is roll number ka koi record nahi mila.")
#       else:
#         st.info("Abhi tak koi attendance record nahi banaya gaya hai.")

# # ==========================================
# # SCENARIO 2: PUBLIC WEBSITE (Normal User / Student)
# # ==========================================
# else:
#   st.title("🌟 Yuva Pahal - Free Coaching Centre")
#   st.markdown(
#       "### *Empowering Underprivileged Children Through Free Education Up to Class 8th*"
#   )

#   st.image(
#       "https://images.unsplash.com/photo-1523240795612-9a054b0db644?q=80&w=1200&auto=format&fit=crop",
#       caption="Education is a right, not a privilege",
#       use_container_width=True,
#   )

#   # --- Coaching Address Section on Public Page ---
#   st.markdown("---")
#   st.markdown("## 📍 Coaching Centre Address & Location")
#   st.markdown("""
#         <div style="padding: 15px; border-radius: 10px; background-color: #f8f9fa; border-left: 5px solid #1f77b4; border: 1px solid #e0e0e0;">
#             <p style="margin: 0; font-size: 16px; color: #333333;">
#                 <b>Village Bari, Post Shahajana</b><br>
#                 Pihani, Hardoi, Uttar Pradesh – <b>241407</b>
#             </p>
#         </div>
#     """, unsafe_allow_html=True)

#   # --- About Coaching Section ---
#   st.markdown("---")
#   st.markdown("## 📖 About Our Free Coaching Centre")
#   st.markdown("""
#     Our coaching centre is dedicated to providing **100% free education** to children from underprivileged and needy families who are unable to afford quality learning due to financial constraints. 
#     This noble initiative is founded and managed by **Ramesh Singh** with the mission to build a brighter future, instil confidence, and provide strong foundational learning for every child.
    
#     * **Target Group:** Students from Nursery up to **Class 8th**
#     * **Founder & Director:** Ramesh Singh
#     * **Fee Structure:** Completely Free (No charges)
#     * **Mission:** Ensuring that no child is left behind due to a lack of resources.
#     """)

#   # --- Display Dynamic Active Public Posts / Batches & Images on Website ---
#   conn = get_db_connection()
#   cursor = conn.cursor()
#   cursor.execute(
#       "SELECT title, content, category, image FROM public_posts WHERE status = 'Active'"
#   )
#   active_posts = cursor.fetchall()
#   conn.close()

#   if active_posts:
#     st.markdown("---")
#     st.header("📢 Latest Announcements & Active Batches")
#     for title, content, category, img_blob in active_posts:
#       with st.container():
#         cols_p = st.columns([2, 1] if img_blob else [1])
#         with cols_p[0]:
#           st.markdown(f"### 📌 [{category}] {title}")
#           st.write(content)
#         if img_blob and len(cols_p) > 1:
#           with cols_p[1]:
#             st.image(img_blob, caption=title, use_container_width=True)
#         st.markdown("---")

#   st.header("🚀 Available Batches & Courses")

#   courses_df = fetch_all_courses()

#   cols = st.columns(3)
#   for index, row in courses_df.iterrows():
#     c_id, c_name, c_time, c_fees, c_desc = (
#         row["id"],
#         row["course_name"],
#         row["batch_time"],
#         row["fees"],
#         row["description"],
#     )
#     with cols[index % 3]:
#       st.subheader(c_name)
#       st.write(f"**🕒 Timing:** {c_time}")
#       st.write(f"**💰 Fees:** {c_fees}")
#       st.write(f"*{c_desc}*")

#       if st.button(f"Enroll Free", key=f"course_{c_id}"):
#         st.session_state.selected_course = c_name
#         st.session_state.selected_fees = c_fees
#         st.session_state.show_checkout = True

#   if "show_checkout" in st.session_state and st.session_state.show_checkout:
#     st.markdown("---")
#     st.subheader(
#         f"🛒 Free Registration: Enrolling in '{st.session_state.selected_course}'"
#     )
#     st.info(f"Fee Amount: **{st.session_state.selected_fees}**")

#     if not st.session_state.user_logged_in:
#       st.warning(
#           "Registration complete karne ke liye pehle login ya account create karein!"
#       )

#       tab1, tab2 = st.tabs(["Login", "Register"])

#       with tab1:
#         with st.form("user_login_form"):
#           u_name = st.text_input("Username / Email")
#           u_pass = st.text_input("Password", type="password")
#           u_sub = st.form_submit_button("Login to Proceed")
#           if u_sub:
#             conn = get_db_connection()
#             try:
#               cursor = conn.cursor()
#               cursor.execute(
#                   "SELECT * FROM users WHERE username=? AND password=?",
#                   (u_name, u_pass),
#               )
#               user_res = cursor.fetchone()
#             finally:
#               conn.close()

#             if user_res:
#               st.session_state.user_logged_in = True
#               st.session_state.logged_user_name = u_name
#               st.success("Login Successful!")
#               st.rerun()
#             else:
#               st.error("Invalid credentials!")

#       with tab2:
#         with st.form("user_reg_form"):
#           r_name = st.text_input("Student / Parent Full Name")
#           r_user = st.text_input("Email / Username")
#           r_pass = st.text_input("Create Password", type="password")
#           r_sub = st.form_submit_button("Register Account")
#           if r_sub:
#             file_conn = get_db_connection()
#             try:
#               cursor = file_conn.cursor()
#               cursor.execute(
#                   "INSERT INTO users VALUES (?, ?, 'Student', ?)",
#                   (r_user, r_pass, r_name),
#               )
#               file_conn.commit()
#               st.session_state.user_logged_in = True
#               st.session_state.logged_user_name = r_user
#               st.success("Account created & logged in successfully!")
#               st.rerun()
#             except sqlite3.IntegrityError:
#               st.error("Username already exists!")
#             finally:
#               file_conn.close()
#     else:
#       st.success(
#           f"Aap logged in hain as **{st.session_state.logged_user_name}**!"
#       )
#       if st.button("Confirm Free Enrollment"):
#         conn = get_db_connection()
#         try:
#           cursor = conn.cursor()
#           cursor.execute(
#               "INSERT INTO enrollments (student_name, email, course_name, fees) VALUES (?, ?, ?, ?)",
#               (
#                   st.session_state.logged_user_name,
#                   st.session_state.logged_user_name,
#                   st.session_state.selected_course,
#                   st.session_state.selected_fees,
#               ),
#           )
#           conn.commit()
#           st.success("Successfully Enrolled in the Course!")
#           st.session_state.show_checkout = False
#           st.rerun()
#         finally:
#           conn.close()

#   # ==========================================
#   # PROFESSIONAL CIRCULAR FOOTER (STRICTLY FOR PUBLIC PAGE ONLY)
#   # ==========================================
#   st.markdown("<br><br>", unsafe_allow_html=True)
#   st.markdown("---")

#   def get_img_b64(path):
#     try:
#       with open(path, "rb") as f:
#         return base64.b64encode(f.read()).decode()
#     except Exception:
#       return ""

#   img_data = get_img_b64("image_bdace0.png")

#   st.markdown(f"""
#       <div style="display: flex; align-items: center; justify-content: center; gap: 25px; padding: 15px; background: rgba(255, 255, 255, 0.03); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);">
#           <div>
#               <img src="data:image/png;base64,{img_data}" style="width: 95px; height: 95px; border-radius: 50%; object-fit: cover; border: 3px solid #1f77b4; box-shadow: 0px 4px 10px rgba(0,0,0,0.4);">
#           </div>
#           <div>
#               <p style="margin: 0 0 6px 0; font-size: 17px; font-weight: bold; color: #ffffff;">
#                   Website Developed by: Dileep Kumar Rathaur
#               </p>
#               <p style="margin: 0; font-size: 15px; color: #cccccc;">
#                   📞 <b>Mobile:</b> 8874549203 &nbsp;|&nbsp; 📸 <b>Instagram:</b> <a href="https://instagram.com/royal_dk700" target="_blank" style="color: #4dabf7; text-decoration: none;">@royal_dk700</a>
#               </p>
#               <p style="margin: 0; font-size: 15px; color: #cccccc;">
#                 🐱<b>GitHub:</b> <a href="https://github.com/dk-coder149" target="_blank" style="color: #4dabf7; text-decoration: none;">dk-coder149</a> &nbsp;|&nbsp; 🌐 <b>LinkedIn:</b> <a href="https://www.linkedin.com/in/dileep-kumar-rathaur-25a3ab383" target="_blank" style="color: #4dabf7; text-decoration: none;">dileep-kumar-rathaur-25a3ab383</a>
#                 </p>
#           </div>
#       </div>
#       <p style='text-align: center; font-size: 13px; color: #888888; margin-top: 15px;'>
#           © 2026 Youva Pahal Free Coaching Centre | All Rights Reserved.
#       </p>
#   """, unsafe_allow_html=True)
























from datetime import date
import mysql.connector
import pandas as pd
import streamlit as st
import base64
import certifi
# Page Config
st.set_page_config(
    page_title="Youva Pahal - Free Coaching Centre", page_icon="🎓", layout="wide"
)

# --- TIDB CLOUD DATABASE CONNECTION SETUP ---
import certifi

# --- TIDB CLOUD DATABASE CONNECTION SETUP ---
def get_db_connection():
    return mysql.connector.connect(
        host=st.secrets["tidb"]["host"],
        port=int(st.secrets["tidb"]["port"]),
        user=st.secrets["tidb"]["user"],
        password=st.secrets["tidb"]["password"],
        database=st.secrets["tidb"]["database"],
        ssl_ca=certifi.where(),
        ssl_verify_cert=True
  )

def init_db():
  # TiDB Cloud mein database pehle se created hota hai ya hum connection ke baad tables check/create karte hain
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
  except Exception as e:
    st.error(f"TiDB Cloud Connection Error: {e}")
    return

  # Users Table for Admin & Students
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(255) PRIMARY KEY,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL,
            name VARCHAR(255)
        )
    """)
  
  # Check if admin exists before inserting
  cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
  if cursor.fetchone()[0] == 0:
    cursor.execute("""
            INSERT INTO users (username, password, role, name) 
            VALUES ('admin', 'admin123', 'Admin', 'Administrator')
        """)

  # Enrollments Table for Tracking Course Purchases
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_name VARCHAR(255),
            email VARCHAR(255),
            course_name VARCHAR(255),
            fees VARCHAR(50),
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

  # Students Record Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll_no VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            fathers_name VARCHAR(255) NOT NULL,
            dob VARCHAR(50) NOT NULL,
            email VARCHAR(255) NOT NULL,
            gender VARCHAR(50) NOT NULL,
            class VARCHAR(50) NOT NULL,
            section VARCHAR(50) NOT NULL,
            contact VARCHAR(50) NOT NULL,
            address TEXT
        )
    """)

  # Courses Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            course_name VARCHAR(255),
            batch_time VARCHAR(255),
            fees VARCHAR(50),
            description TEXT
        )
    """)

  # Public Posts & Batches Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS public_posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            content TEXT,
            category VARCHAR(100),
            status VARCHAR(50),
            image LONGBLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

  # Attendance Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            roll_no VARCHAR(50),
            student_name VARCHAR(255),
            class VARCHAR(50),
            date VARCHAR(50),
            status VARCHAR(50)
        )
    """)

  # Default courses agar table khali ho
  cursor.execute("SELECT COUNT(*) FROM courses")
  count = cursor.fetchone()[0]
  if count == 0:
    cursor.executemany(
        "INSERT INTO courses (course_name, batch_time, fees, description) VALUES (%s, %s, %s, %s)",
        [
            (
                "Basic Mathematics (Nursery - 4th)",
                "Morning (8:00 AM - 9:00 AM)",
                "Free",
                "Fundamental mathematical concepts for young students completely free of cost.",
            ),
            (
                "Junior English & Grammar (5th - 8th)",
                "Evening (4:00 PM - 5:00 PM)",
                "Free",
                "Building strong English communication and grammar foundations.",
            ),
            (
                "General Science Basics",
                "Weekend (10:00 AM - 11:30 AM)",
                "Free",
                "Interactive science learning sessions for underprivileged children.",
            ),
        ],
    )
  conn.commit()
  cursor.close()
  conn.close()

# Run init_db only once using session state
if "db_initialized" not in st.session_state:
  init_db()
  st.session_state.db_initialized = True

# Data fetchers using dictionary cursor for Pandas
def fetch_all_courses():
  conn = get_db_connection()
  cursor = conn.cursor(dictionary=True)
  cursor.execute("SELECT * FROM courses")
  result = cursor.fetchall()
  cursor.close()
  conn.close()
  return pd.DataFrame(result)

def fetch_all_students():
  conn = get_db_connection()
  cursor = conn.cursor(dictionary=True)
  cursor.execute("SELECT * FROM students")
  result = cursor.fetchall()
  cursor.close()
  conn.close()
  return pd.DataFrame(result)

# Session States
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "username" not in st.session_state:
  st.session_state.username = ""
if "role" not in st.session_state:
  st.session_state.role = ""
if "user_logged_in" not in st.session_state:
  st.session_state.user_logged_in = False

# --- SIDEBAR: ADMIN LOGIN LINK ---
st.sidebar.title("🧭 Navigation")

with st.sidebar.expander("🔒 Admin Portal Login"):
  if not st.session_state.logged_in:
    adm_user = st.text_input("Admin Username", key="adm_u")
    adm_pass = st.text_input("Admin Password", type="password", key="adm_p")
    if st.button("Login as Admin"):
      conn = get_db_connection()
      cursor = conn.cursor(dictionary=True)
      cursor.execute(
          "SELECT role FROM users WHERE username=%s AND password=%s AND role='Admin'",
          (adm_user, adm_pass),
      )
      res = cursor.fetchone()
      cursor.close()
      conn.close()

      if res:
        st.session_state.logged_in = True
        st.session_state.username = adm_user
        st.session_state.role = "Admin"
        st.success("Admin Login Successful!")
        st.rerun()
      else:
        st.error("Invalid Admin Credentials!")
  else:
    st.write(f"Logged in as **{st.session_state.username}**")
    if st.button("Admin Logout"):
      st.session_state.logged_in = False
      st.session_state.username = ""
      st.session_state.role = ""
      st.rerun()

st.sidebar.markdown("---")

# ==========================================
# SCENARIO 1: ADMIN PANEL (Logged In)
# ==========================================
if st.session_state.logged_in and st.session_state.role == "Admin":
  st.title("🛠 Admin Dashboard - Institute Management")
  st.info("Aap yahan students ke records, courses aur attendance manage kar sakte hain.")

  menu = st.sidebar.selectbox(
      "Admin Menu",
      [
          "Manage Students Records",
          "Search Students",
          "Manage Courses",
          "View Course Purchases",
          "Manage Public Posts",
          "Manage Attendance",
      ],
  )

  if menu == "Manage Students Records":
    st.subheader("📋 Student Records Database")
    df = fetch_all_students()

    selected_roll = ""
    selected_data = None

    if not df.empty:
      df.columns = [
          "Roll No",
          "Name",
          "Father's Name",
          "D.O.B",
          "Email",
          "Gender",
          "Class",
          "Section",
          "Contact",
          "Address",
      ]
      st.write("👉 *Table me kisi bhi row par click karke select karein:*")
      event = st.dataframe(
          df,
          use_container_width=True,
          on_select="rerun",
          selection_mode="single-row",
      )
      if event.selection.rows:
        selected_row = df.iloc[event.selection.rows[0]]
        selected_roll = selected_row["Roll No"]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE roll_no = %s", (selected_roll,))
        selected_data = cursor.fetchone()
        cursor.close()
        conn.close()
    else:
      st.info("No student records found yet.")

    st.markdown("---")
    st.subheader(
        "✏️ Add / Update Student Form"
        + (f" (Selected: {selected_roll})" if selected_roll else "")
    )

    def_roll = selected_data[0] if selected_data else ""
    def_name = selected_data[1] if selected_data else ""
    def_fname = selected_data[2] if selected_data else ""
    def_dob = selected_data[3] if selected_data else ""
    def_email = selected_data[4] if selected_data else ""
    def_gender = selected_data[5] if selected_data else "Male"
    def_cls = selected_data[6] if selected_data else ""
    def_sec = selected_data[7] if selected_data else ""
    def_contact = selected_data[8] if selected_data else ""
    def_addr = selected_data[9] if selected_data else ""

    gender_options = ["Male", "Female", "Other"]
    gender_index = (
        gender_options.index(def_gender) if def_gender in gender_options else 0
    )

    with st.form("admin_student_form"):
      c1, c2, c3 = st.columns(3)
      with c1:
        roll = st.text_input("Roll No", value=def_roll)
        name = st.text_input("Name", value=def_name)
        fathers_name = st.text_input("Father's Name", value=def_fname)
      with c2:
        dob = st.text_input("D.O.B (DD/MM/YYYY)", value=def_dob)
        email = st.text_input("Email", value=def_email)
        gender = st.selectbox("Gender", gender_options, index=gender_index)
      with c3:
        cls = st.text_input("Class", value=def_cls)
        section = st.text_input("Section", value=def_sec)
        contact = st.text_input("Contact", value=def_contact)

      address = st.text_area("Address", value=def_addr)

      b1, b2, b3 = st.columns(3)
      with b1:
        add_b = st.form_submit_button("➕ Add Student")
      with b2:
        up_b = st.form_submit_button("🔄 Update Student")
      with b3:
        del_b = st.form_submit_button("🗑️ Delete Student")

      if add_b:
        if roll and name:
          conn = get_db_connection()
          try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    roll,
                    name,
                    fathers_name,
                    dob,
                    email,
                    gender,
                    cls,
                    section,
                    contact,
                    address,
                ),
            )
            default_pass = contact if contact else "123456"
            
            # Check if user already exists
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (email,))
            if cursor.fetchone()[0] == 0:
              cursor.execute(
                  "INSERT INTO users (username, password, role, name) VALUES (%s, %s, 'Student', %s)",
                  (email, default_pass, name),
              )
            conn.commit()
            cursor.close()
            conn.close()
            st.success(
                f"Student added successfully! (Login Email: {email}, Default Password: {default_pass})"
            )
            st.rerun()
          except Exception as err:
            st.error(f"Error: Roll No ya Email pehle se exist karta hai! ({err})")
        else:
          st.warning("Fill required fields.")
      if up_b:
        if roll:
          conn = get_db_connection()
          cursor = conn.cursor()
          cursor.execute(
              """UPDATE students SET name=%s, fathers_name=%s, dob=%s, email=%s,
              gender=%s, class=%s, section=%s, contact=%s, address=%s WHERE roll_no=%s""",
              (
                  name,
                  fathers_name,
                  dob,
                  email,
                  gender,
                  cls,
                  section,
                  contact,
                  address,
                  roll,
              ),
          )
          conn.commit()
          cursor.close()
          conn.close()
          st.success("Updated successfully!")
          st.rerun()

      if del_b:
        if roll:
          conn = get_db_connection()
          cursor = conn.cursor()
          cursor.execute("DELETE FROM students WHERE roll_no=%s", (roll,))
          conn.commit()
          cursor.close()
          conn.close()
          st.success("Deleted successfully!")
          st.rerun()

  elif menu == "Search Students":
    st.subheader("🔍 Advanced Student Search Filter")
    search_by = st.selectbox("Search By", ["Roll No", "Name", "Class", "Section"])
    search_query = st.text_input("Search keyword enter karein")

    if st.button("Search"):
      col_map = {
          "Roll No": "roll_no",
          "Name": "name",
          "Class": "class",
          "Section": "section",
      }
      db_col = col_map[search_by]

      conn = get_db_connection()
      cursor = conn.cursor(dictionary=True)
      cursor.execute(
          f"SELECT * FROM students WHERE {db_col} LIKE %s",
          ("%" + search_query + "%",),
      )
      results = cursor.fetchall()
      cursor.close()
      conn.close()

      if results:
        df = pd.DataFrame(results)
        df.columns = [
            "Roll No",
            "Name",
            "Father's Name",
            "D.O.B",
            "Email",
            "Gender",
            "Class",
            "Section",
            "Contact",
            "Address",
        ]
        st.success(f"Total {len(results)} matching record(s) mile hain:")
        st.dataframe(df, use_container_width=True)
      else:
        st.warning("Koi matching record nahi mila.")

  elif menu == "Manage Courses":
    st.subheader("📚 Add/Update Institute Courses")
    with st.form("course_add_form"):
      c_name = st.text_input("Course Name")
      c_time = st.text_input("Batch Time (e.g., Morning 8 AM)")
      c_fees = st.text_input("Fees (e.g., Free / ₹0)")
      c_desc = st.text_area("Description")
      submit_course = st.form_submit_button("Add Course")
      if submit_course:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO courses (course_name, batch_time, fees, description) VALUES (%s, %s, %s, %s)",
            (c_name, c_time, c_fees, c_desc),
        )
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Course added to website successfully!")
        st.rerun()

  elif menu == "View Course Purchases":
    st.subheader("🛍️ Enrolled Students / Course Purchases List")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM enrollments ORDER BY purchase_date DESC")
    res_enroll = cursor.fetchall()
    cursor.close()
    conn.close()
    df_purchases = pd.DataFrame(res_enroll)

    if not df_purchases.empty:
      df_purchases.columns = [
          "ID",
          "Student Name",
          "Email / Username",
          "Course Name",
          "Fees",
          "Purchase Date",
      ]
      st.dataframe(df_purchases, use_container_width=True)
    else:
      st.info("Abhi tak kisi ne koi course enroll nahi kiya hai.")

  elif menu == "Manage Public Posts":
    st.subheader("📢 Manage Public Posts & Batches (with Image Support)")

    with st.expander(
        "➕ Add New Public Post / Batch with Thumbnail/Image", expanded=True
    ):
      with st.form("add_post_form"):
        p_title = st.text_input("Title (e.g., Nursery & Primary Free Batch)")
        p_content = st.text_area("Details / Description / Timings")
        p_category = st.selectbox(
            "Category", ["Batch", "Announcement", "Notice"]
        )
        p_status = st.selectbox("Status", ["Active", "Expired/Timeout"])

        p_image_file = st.file_uploader(
            "Upload Thumbnail / Poster Image (Optional)",
            type=["jpg", "png", "jpeg"],
        )

        submit_post = st.form_submit_button("Publish to Public View")
        if submit_post:
          if p_title and p_content:
            image_bytes = (
                p_image_file.read() if p_image_file is not None else None
            )

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO public_posts (title, content, category, status, image) VALUES (%s, %s, %s, %s, %s)",
                (p_title, p_content, p_category, p_status, image_bytes),
            )
            conn.commit()
            cursor.close()
            conn.close()
            st.success("Successfully public view me image ke sath add ho gaya!")
            st.rerun()
          else:
            st.warning("Please title aur content bharein.")

    st.markdown("---")
    st.subheader("📋 Existing Public Posts & Batches (Update / Delete)")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, title, content, category, status FROM public_posts ORDER BY id DESC"
    )
    df_posts = pd.DataFrame(cursor.fetchall())
    cursor.close()
    conn.close()

    if not df_posts.empty:
      for index, row in df_posts.iterrows():
        with st.container():
          col1, col2, col3 = st.columns([3, 1, 1])
          with col1:
            st.markdown(
                f"**[{row['category']}] {row['title']}** (Status: `{row['status']}`)"
            )
            st.write(row["content"])
          with col2:
            new_status = st.selectbox(
                "Change Status",
                ["Active", "Expired/Timeout"],
                index=0 if row["status"] == "Active" else 1,
                key=f"status_{row['id']}",
            )
            if st.button("Update Status", key=f"up_btn_{row['id']}"):
              conn = get_db_connection()
              cursor = conn.cursor()
              cursor.execute(
                  "UPDATE public_posts SET status = %s WHERE id = %s",
                  (new_status, row["id"]),
              )
              conn.commit()
              cursor.close()
              conn.close()
              st.success("Updated!")
              st.rerun()
          with col3:
            st.write("")
            if st.button("🗑️ Delete", key=f"del_post_{row['id']}"):
              conn = get_db_connection()
              cursor = conn.cursor()
              cursor.execute("DELETE FROM public_posts WHERE id = %s", (row["id"],))
              conn.commit()
              cursor.close()
              conn.close()
              st.success("Deleted from public view!")
              st.rerun()
          st.divider()
    else:
      st.info("Koi public post ya batch available nahi hai.")

  elif menu == "Manage Attendance":
    st.subheader("📊 Online Attendance Management System")

    tab_mark, tab_report = st.tabs(
        ["📝 Mark Attendance", "📈 View Attendance Reports & Counts"]
    )

    with tab_mark:
      st.write("👉 **Date aur Class select karke bachho ki attendance lagayein:**")

      conn = get_db_connection()
      cursor = conn.cursor(dictionary=True)
      cursor.execute("SELECT DISTINCT class FROM students")
      classes_df = pd.DataFrame(cursor.fetchall())
      cursor.close()
      conn.close()

      if not classes_df.empty:
        class_list = classes_df["class"].tolist()
        selected_class = st.selectbox(
            "Select Class / Batch", class_list, key="att_class"
        )
        selected_date = st.date_input(
            "Attendance Date", value=date.today(), key="att_date"
        )

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT roll_no, name FROM students WHERE class = %s",
            (selected_class,),
        )
        students_in_class = pd.DataFrame(cursor.fetchall())
        cursor.close()
        conn.close()

        if not students_in_class.empty:
          st.info(
              f"Total Students in Class {selected_class}: {len(students_in_class)}"
          )

          with st.form("attendance_form"):
            st.markdown("---")
            col_h1, col_h2, col_h3 = st.columns([1, 2, 1])
            col_h1.markdown("**Roll No**")
            col_h2.markdown("**Student Name**")
            col_h3.markdown("**Status (Present/Absent)**")
            st.markdown("---")

            attendance_status = {}
            for idx, s_row in students_in_class.iterrows():
              r_no = s_row["roll_no"]
              s_name = s_row["name"]

              c1, c2, c3 = st.columns([1, 2, 1])
              c1.write(f"`{r_no}`")
              c2.write(f"**{s_name}**")

              status = c3.radio(
                  "Status",
                  ["Present", "Absent"],
                  key=f"status_{r_no}",
                  horizontal=True,
                  label_visibility="collapsed",
              )
              attendance_status[r_no] = (s_name, status)

            st.markdown("---")
            submitted_attendance = st.form_submit_button("💾 Save Attendance")

            if submitted_attendance:
              date_str = str(selected_date)
              conn = get_db_connection()
              cursor = conn.cursor()

              for r_no, (s_name, status) in attendance_status.items():
                cursor.execute(
                    "DELETE FROM attendance WHERE roll_no = %s AND class = %s AND date = %s",
                    (r_no, selected_class, date_str),
                )
                cursor.execute(
                    "INSERT INTO attendance (roll_no, student_name, class, date, status) VALUES (%s, %s, %s, %s, %s)",
                    (r_no, s_name, selected_class, date_str, status),
                )
              conn.commit()
              cursor.close()
              conn.close()
              st.success(
                  f"🎉 Date {date_str} ki attendance successfully save ho gayi hai!"
              )
        else:
          st.warning("Is class me koi student registered nahi hai.")
      else:
        st.warning(
            "Pehle 'Manage Students Records' se students add karein aur unhe class assign karein."
        )

    with tab_report:
      st.subheader("📈 Automatic Attendance Counter & Reports")
      conn = get_db_connection()
      cursor = conn.cursor(dictionary=True)
      cursor.execute("SELECT * FROM attendance")
      att_df = pd.DataFrame(cursor.fetchall())
      cursor.close()
      conn.close()

      if not att_df.empty:
        summary_data = []
        grouped = att_df.groupby(["roll_no", "student_name", "class"])

        for (r_no, s_name, s_class), group in grouped:
          total_classes = len(group)
          total_present = len(group[group["status"] == "Present"])
          total_absent = len(group[group["status"] == "Absent"])
          percentage = (
              round((total_present / total_classes) * 100, 2)
              if total_classes > 0
              else 0
          )

          summary_data.append({
              "Roll No": r_no,
              "Student Name": s_name,
              "Class": s_class,
              "Total Classes": total_classes,
              "Present Days": total_present,
              "Absent Days": total_absent,
              "Attendance %": f"{percentage}%",
          })

        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True)

        with st.expander("🔍 View Detailed Date-wise Attendance History"):
          selected_r_no = st.text_input(
              "Roll Number enter karein student ki history dekhne ke liye:"
          )
          if selected_r_no:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT date, status FROM attendance WHERE roll_no = %s ORDER BY date DESC",
                (selected_r_no,),
            )
            hist_df = pd.DataFrame(cursor.fetchall())
            cursor.close()
            conn.close()
            if not hist_df.empty:
              st.write(f"Attendance history for Roll No: `{selected_r_no}`")
              st.dataframe(hist_df, use_container_width=True)
            else:
              st.warning("Is roll number ka koi record nahi mila.")
      else:
        st.info("Abhi tak koi attendance record nahi banaya gaya hai.")

# ==========================================
# SCENARIO 2: PUBLIC WEBSITE (Normal User / Student)
# ==========================================
else:
  st.title("🌟 Youva Pahal - Free Coaching Centre")
  st.markdown(
      "### *Empowering Underprivileged Children Through Free Education Up to Class 8th*"
  )

  st.image(
      "https://images.unsplash.com/photo-1523240795612-9a054b0db644?q=80&w=1200&auto=format&fit=crop",
      caption="Education is a right, not a privilege",
      use_container_width=True,
  )

  # --- Coaching Address Section on Public Page ---
  st.markdown("---")
  st.markdown("## 📍 Coaching Centre Address & Location")
  st.markdown("""
        <div style="padding: 15px; border-radius: 10px; background-color: #f8f9fa; border-left: 5px solid #1f77b4; border: 1px solid #e0e0e0;">
            <p style="margin: 0; font-size: 16px; color: #333333;">
                <b>Village Bari, Post Shahajana</b><br>
                Pihani, Hardoi, Uttar Pradesh – <b>241407</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

  # --- About Coaching Section ---
  st.markdown("---")
  st.markdown("## 📖 About Our Free Coaching Centre")
  st.markdown("""
    Our coaching centre is dedicated to providing **100% free education** to children from underprivileged and needy families who are unable to afford quality learning due to financial constraints. 
    This noble initiative is founded and managed by **Ramesh Singh** with the mission to build a brighter future, instil confidence, and provide strong foundational learning for every child.
    
    * **Target Group:** Students from Nursery up to **Class 8th**
    * **Founder & Director:** Ramesh Singh
    * **Fee Structure:** Completely Free (No charges)
    * **Mission:** Ensuring that no child is left behind due to a lack of resources.
    """)

  # --- Display Dynamic Active Public Posts / Batches & Images on Website ---
  conn = get_db_connection()
  cursor = conn.cursor(dictionary=True)
  cursor.execute(
      "SELECT title, content, category, image FROM public_posts WHERE status = 'Active'"
  )
  active_posts = cursor.fetchall()
  cursor.close()
  conn.close()

  if active_posts:
    st.markdown("---")
    st.header("📢 Latest Announcements & Active Batches")
    for post in active_posts:
      title, content, category, img_blob = (
          post["title"],
          post["content"],
          post["category"],
          post["image"],
      )
      with st.container():
        cols_p = st.columns([2, 1] if img_blob else [1])
        with cols_p[0]:
          st.markdown(f"### 📌 [{category}] {title}")
          st.write(content)
        if img_blob and len(cols_p) > 1:
          with cols_p[1]:
            st.image(img_blob, caption=title, use_container_width=True)
        st.markdown("---")

  st.header("🚀 Available Batches & Courses")

  courses_df = fetch_all_courses()

  cols = st.columns(3)
  for index, row in courses_df.iterrows():
    c_id, c_name, c_time, c_fees, c_desc = (
        row["id"],
        row["course_name"],
        row["batch_time"],
        row["fees"],
        row["description"],
    )
    with cols[index % 3]:
      st.subheader(c_name)
      st.write(f"**🕒 Timing:** {c_time}")
      st.write(f"**💰 Fees:** {c_fees}")
      st.write(f"*{c_desc}*")

      if st.button(f"Enroll Free", key=f"course_{c_id}"):
        st.session_state.selected_course = c_name
        st.session_state.selected_fees = c_fees
        st.session_state.show_checkout = True

  if "show_checkout" in st.session_state and st.session_state.show_checkout:
    st.markdown("---")
    st.subheader(
        f"🛒 Free Registration: Enrolling in '{st.session_state.selected_course}'"
    )
    st.info(f"Fee Amount: **{st.session_state.selected_fees}**")

    if not st.session_state.user_logged_in:
      st.warning(
          "Registration complete karne ke liye pehle login ya account create karein!"
      )

      tab1, tab2 = st.tabs(["Login", "Register"])

      with tab1:
        with st.form("user_login_form"):
          u_name = st.text_input("Username / Email")
          u_pass = st.text_input("Password", type="password")
          u_sub = st.form_submit_button("Login to Proceed")
          if u_sub:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (u_name, u_pass),
            )
            user_res = cursor.fetchone()
            cursor.close()
            conn.close()

            if user_res:
              st.session_state.user_logged_in = True
              st.session_state.logged_user_name = u_name
              st.success("Login Successful!")
              st.rerun()
            else:
              st.error("Invalid credentials!")

      with tab2:
        with st.form("user_reg_form"):
          r_name = st.text_input("Student / Parent Full Name")
          r_user = st.text_input("Email / Username")
          r_pass = st.text_input("Create Password", type="password")
          r_sub = st.form_submit_button("Register Account")
          if r_sub:
            file_conn = get_db_connection()
            try:
              cursor = file_conn.cursor()
              cursor.execute(
                  "INSERT INTO users (username, password, role, name) VALUES (%s, %s, 'Student', %s)",
                  (r_user, r_pass, r_name),
              )
              file_conn.commit()
              cursor.close()
              file_conn.close()
              st.session_state.user_logged_in = True
              st.session_state.logged_user_name = r_user
              st.success("Account created & logged in successfully!")
              st.rerun()
            except Exception:
              st.error("Username already exists!")
    else:
      st.success(
          f"Aap logged in hain as **{st.session_state.logged_user_name}**!"
      )
      if st.button("Confirm Free Enrollment"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO enrollments (student_name, email, course_name, fees) VALUES (%s, %s, %s, %s)",
            (
                st.session_state.logged_user_name,
                st.session_state.logged_user_name,
                st.session_state.selected_course,
                st.session_state.selected_fees,
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Successfully Enrolled in the Course!")
        st.session_state.show_checkout = False
        st.rerun()

  # ==========================================
  # PROFESSIONAL CIRCULAR FOOTER (STRICTLY FOR PUBLIC PAGE ONLY)
  # ==========================================
  st.markdown("<br><br>", unsafe_allow_html=True)
  st.markdown("---")

  def get_img_b64(path):
    try:
      with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    except Exception:
      return ""

  img_data = get_img_b64("image_bdace0.png")

  st.markdown(f"""
      <div style="display: flex; align-items: center; justify-content: center; gap: 20px; padding: 15px; background: rgba(255, 255, 255, 0.03); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1); flex-wrap: wrap;">
          <div>
              <img src="data:image/png;base64,{img_data}" style="width: 95px; height: 95px; border-radius: 50%; object-fit: cover; border: 3px solid #1f77b4; box-shadow: 0px 4px 10px rgba(0,0,0,0.4);">
          </div>
          <div>
              <p style="margin: 0 0 6px 0; font-size: 17px; font-weight: bold; color: #ffffff;">
                  Website Developed by: Dileep Kumar Rathaur
              </p>
              <p style="margin: 0; font-size: 14px; color: #cccccc; line-height: 1.8;">
                  📞 <b>Mobile:</b> 8874549203 &nbsp;|&nbsp; 
                  📸 <b>Instagram:</b> <a href="https://instagram.com/royal_dk700" target="_blank" style="color: #4dabf7; text-decoration: none;">@royal_dk700</a><br>
                  🐙 <b>GitHub:</b> <a href="https://github.com/" target="_blank" style="color: #4dabf7; text-decoration: none;">GitHub</a> &nbsp;|&nbsp; 
                  💼 <b>LinkedIn:</b> <a href="https://linkedin.com/" target="_blank" style="color: #4dabf7; text-decoration: none;">LinkedIn</a>
              </p>
          </div>
      </div>
      <p style='text-align: center; font-size: 13px; color: #888888; margin-top: 15px;'>
          © 2026 Youva Pahal Free Coaching Centre | All Rights Reserved.
      </p>
  """, unsafe_allow_html=True)