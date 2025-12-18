"""
Employee Registration Module
Allows admins to register new employees
"""

import streamlit as st
import requests
from datetime import datetime
import time


def call_n8n_webhook(n8n_base_url, endpoint, data=None, method='POST'):
    """Call n8n webhook"""
    try:
        url = f"{n8n_base_url}/{endpoint}"

        if method == 'POST':
            response = requests.post(url, json=data, timeout=10)
        else:
            response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"n8n Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to n8n. Make sure n8n is running!")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None


def show_employee_registration(n8n_base_url, departments):
    """
    Employee Registration Page
    """

    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='color: #333; font-size: 32px; margin-bottom: 10px;'>👤 Employee Registration</h1>
        <p style='color: #666; font-size: 14px;'>Add New Employee to the System</p>
    </div>
    """, unsafe_allow_html=True)

    # Back button - OUTSIDE THE FORM
    if st.button("← Back to Dashboard"):
        st.session_state.current_page = 'dashboard'
        st.rerun()

    st.markdown("""
    <div class='info-box'>
        <h4>📋 Registration Information:</h4>
        <p>
            Fill in all required fields to register a new employee.<br>
            Employee ID will be auto-generated based on current count.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Form
    with st.form("employee_registration_form"):
        employee_name = st.text_input("👤 Full Name *", placeholder="Enter employee's full name")

        col1, col2 = st.columns(2)
        with col1:
            department = st.selectbox("🏢 Department *",
                                      ["-- Select Department --"] + departments
                                      )
        with col2:
            hire_date = st.date_input("📅 Hire Date *", value=datetime.now())

        email = st.text_input("📧 Email Address *", placeholder="employee@company.com")
        phone = st.text_input("📱 Phone Number", placeholder="+1 (555) 123-4567")
        hourly_rate = st.number_input("💰 Hourly Rate ($) *", min_value=0.0, value=15.0, step=0.01, format="%.2f")

        if employee_name:
            emp_id = f"E{str(st.session_state.next_employee_id).zfill(3)}"
            st.markdown(f"""
            <div class='preview-id'>
                <div style='font-size: 12px; color: #666;'>Auto-Generated Employee ID:</div>
                <div class='generated-id'>{emp_id}</div>
            </div>
            """, unsafe_allow_html=True)

        submitted = st.form_submit_button("✅ Register Employee", use_container_width=True)

    # Handle form submission - OUTSIDE THE FORM
    if submitted:
        if not employee_name or department == "-- Select Department --" or not email or hourly_rate <= 0:
            st.error("❌ Please fill in all required fields!")
        else:
            emp_id = f"E{str(st.session_state.next_employee_id).zfill(3)}"

            employee_data = {
                "Employee ID": emp_id,
                "Employee Name": employee_name,
                "Department": department,
                "Email": email,
                "Phone": phone if phone else "N/A",
                "Hire Date": hire_date.strftime("%Y-%m-%d"),
                "Hourly Rate": f"{hourly_rate:.2f}"
            }

            with st.spinner("Registering employee via n8n..."):
                result = call_n8n_webhook(n8n_base_url, 'employee/register', employee_data)

                if result:
                    st.success(f"✅ SUCCESS! Employee {employee_name} ({emp_id}) registered!")
                    st.balloons()
                    st.session_state.next_employee_id += 1
                    st.info("Redirecting to dashboard in 2 seconds...")

                    time.sleep(2)
                    st.session_state.current_page = 'dashboard'
                    st.rerun()


if __name__ == "__main__":
    # For testing standalone
    st.set_page_config(
        page_title="Employee Registration",
        page_icon="👤",
        layout="centered"
    )

    from config import DEPARTMENTS

    show_employee_registration("http://localhost:5678/webhook", DEPARTMENTS)
