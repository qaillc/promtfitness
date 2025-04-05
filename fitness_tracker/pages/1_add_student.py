"""
Page for adding new students to the system.
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path to import services
sys.path.append(str(Path(__file__).parent.parent))
from services.student_service import StudentService

st.set_page_config(page_title="Add Student", page_icon="➕")

st.title("Add Student")
st.write("Enter the student details below to add them to the system.")

# Create a form for better mobile experience
with st.form("add_student_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=100, value=16)
        grade = st.text_input("Grade")
    
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        fitness_level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
        height_cm = st.number_input("Height (cm)", min_value=0.0, value=170.0, step=0.1)
    
    submitted = st.form_submit_button("Add Student")
    
    if submitted:
        success, message = StudentService.add_student(name, age, grade, gender, fitness_level, height_cm)
        if success:
            st.success(message)
            
            # Add gamification points for adding a new student
            if 'points' in st.session_state:
                st.session_state.points += 5
                st.success("You earned 5 points for adding a new student!")
        else:
            st.error(message)

# Display existing students in a table with search functionality
st.subheader("Existing Students")

# Add a search box
search_term = st.text_input("Search students by name", "")

students = StudentService.get_all_students()
if students:
    # Filter students by search term if provided
    if search_term:
        filtered_students = [s for s in students if search_term.lower() in s.name.lower()]
    else:
        filtered_students = students
    
    # Convert to a list of dictionaries for display
    students_data = [
        {
            "ID": s.id,
            "Name": s.name,
            "Age": s.age,
            "Grade": s.grade,
            "Gender": s.gender,
            "Fitness Level": s.fitness_level
        }
        for s in filtered_students
    ]
    
    st.dataframe(students_data, use_container_width=True)
else:
    st.info("No students found in the system. Add your first student above!")

# Mobile-friendly tip
st.markdown("""
<div style="background-color:#F0F2F6; padding: 10px; border-radius: 5px;">
<strong>💡 Tip:</strong> On mobile devices, scroll horizontally to see all student data in the table.
</div>
""", unsafe_allow_html=True)