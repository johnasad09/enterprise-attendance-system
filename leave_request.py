"""
Leave Request Module
Allows employees to submit leave requests
"""

import streamlit as st
import requests
from datetime import datetime, timedelta
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


def calculate_working_days(start_date, end_date):
    """Calculate number of working days between two dates (excluding weekends)"""
    days = 0
    current = start_date
    while current <= end_date:
        # 0-4 = Monday-Friday, 5-6 = Saturday-Sunday
        if current.weekday() < 5:
            days += 1
        current += timedelta(days=1)
    return days


def show_leave_request(n8n_base_url):
    """
    Leave Request Submission Page
    """

    # Custom CSS
    st.markdown("""
    <style>
        .info-box {
            background: #edf2f7;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 25px;
            border-left: 4px solid #667eea;
        }
        .leave-summary {
            background: #f7fafc;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border: 2px solid #e2e8f0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='color: #333; font-size: 32px; margin-bottom: 10px;'>🏖️ Leave Request</h1>
        <p style='color: #666; font-size: 14px;'>Submit Your Leave Application</p>
    </div>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("← Back to Check-in"):
        st.session_state.current_page = 'checkin'
        st.rerun()

    # Info Box
    st.markdown("""
    <div class='info-box'>
        <h4>📋 Leave Request Guidelines:</h4>
        <p>
            • Submit requests at least 3 days in advance<br>
            • Annual leave: 15 days per year<br>
            • Sick leave: With medical certificate<br>
            • Emergency leave: Notify immediately<br>
            • All requests require manager approval
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Leave Request Form
    with st.form("leave_request_form"):
        st.subheader("📝 Leave Details")

        # Employee Information
        col1, col2 = st.columns(2)

        with col1:
            employee_id = st.text_input(
                "👤 Employee ID *",
                placeholder="E001",
                help="Your employee ID"
            )

        with col2:
            employee_name = st.text_input(
                "📛 Full Name *",
                placeholder="John Doe",
                help="Your full name"
            )

        # Leave Type
        leave_type = st.selectbox(
            "📋 Leave Type *",
            [
                "-- Select Leave Type --",
                "Annual Leave",
                "Sick Leave",
                "Emergency Leave",
                "Maternity Leave",
                "Paternity Leave",
                "Unpaid Leave",
                "Compensatory Leave"
            ],
            help="Select the type of leave"
        )

        # Date Range
        col1, col2 = st.columns(2)

        with col1:
            start_date = st.date_input(
                "📅 Start Date *",
                value=datetime.now() + timedelta(days=3),
                min_value=datetime.now(),
                help="First day of leave"
            )

        with col2:
            end_date = st.date_input(
                "📅 End Date *",
                value=datetime.now() + timedelta(days=3),
                min_value=datetime.now(),
                help="Last day of leave"
            )

        # Calculate days
        if start_date and end_date:
            if end_date >= start_date:
                total_days = (end_date - start_date).days + 1
                working_days = calculate_working_days(start_date, end_date)

                st.markdown(f"""
                <div class='leave-summary'>
                    <h4 style='color: #667eea; margin-bottom: 10px;'>📊 Leave Summary</h4>
                    <p style='margin: 5px 0;'><strong>Total Days:</strong> {total_days} days</p>
                    <p style='margin: 5px 0;'><strong>Working Days:</strong> {working_days} days</p>
                    <p style='margin: 5px 0;'><strong>Weekend Days:</strong> {total_days - working_days} days</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ End date must be after or equal to start date!")
                working_days = 0
        else:
            working_days = 0

        # Reason
        reason = st.text_area(
            "💬 Reason for Leave *",
            placeholder="Please provide a detailed reason for your leave request...",
            height=150,
            help="Explain why you need leave"
        )

        # Emergency Contact (optional)
        emergency_contact = st.text_input(
            "📱 Emergency Contact (Optional)",
            placeholder="+1 (555) 123-4567",
            help="Contact number during leave"
        )

        # Submit Button
        submitted = st.form_submit_button("📤 Submit Leave Request", use_container_width=True)

    # Handle Form Submission
    if submitted:
        # Validation
        if not employee_id or not employee_name:
            st.error("❌ Please enter Employee ID and Name!")
            return

        if leave_type == "-- Select Leave Type --":
            st.error("❌ Please select a leave type!")
            return

        if not start_date or not end_date:
            st.error("❌ Please select start and end dates!")
            return

        if end_date < start_date:
            st.error("❌ End date must be after or equal to start date!")
            return

        if not reason or len(reason.strip()) < 10:
            st.error("❌ Please provide a detailed reason (at least 10 characters)!")
            return

        # Generate Leave ID
        leave_id = f"L{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Prepare leave request data
        leave_data = {
            "Leave ID": leave_id,
            "Employee ID": employee_id,
            "Employee Name": employee_name,
            "Leave Type": leave_type,
            "Start Date": start_date.strftime("%Y-%m-%d"),
            "End Date": end_date.strftime("%Y-%m-%d"),
            "Days": working_days,
            "Reason": reason.strip(),
            "Status": "Pending",
            "Approved By": "",
            "Approved Date": "",
            "Submitted Date": datetime.now().strftime("%Y-%m-%d"),
            "Emergency Contact": emergency_contact if emergency_contact else "N/A"
        }

        # Show loading
        with st.spinner("Submitting your leave request..."):
            result = call_n8n_webhook(n8n_base_url, 'leave/request', leave_data)

            if result:
                st.success(f"""
                ✅ **Leave Request Submitted Successfully!**

                **Request ID:** {leave_id}  
                **Employee:** {employee_name} ({employee_id})  
                **Leave Type:** {leave_type}  
                **Duration:** {start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')}  
                **Working Days:** {working_days}  
                **Status:** Pending Approval  

                Your request has been forwarded to your manager for approval.  
                You will be notified once it's reviewed.
                """)

                st.balloons()

                # Show next steps
                st.info("""
                📌 **Next Steps:**
                1. Wait for manager approval (typically 1-2 business days)
                2. Check your email for approval notification
                3. You can view request status in the admin dashboard
                """)

    # My Leave History Section
    st.markdown("---")
    st.subheader("📜 Recent Leave Requests")

    col1, col2 = st.columns([3, 1])

    with col1:
        emp_id_search = st.text_input("Enter your Employee ID to view history", "")

    with col2:
        if st.button("🔍 Search", use_container_width=True):
            if emp_id_search:
                st.info("Fetching your leave history...")
                # Here you can fetch from n8n and display the history
            else:
                st.warning("Please enter Employee ID")

    # Leave Balance Card
    st.markdown("---")
    st.subheader("📊 Leave Balance (Example)")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Annual Leave", "12 days", "3 used")

    with col2:
        st.metric("Sick Leave", "8 days", "2 used")

    with col3:
        st.metric("Emergency", "3 days", "0 used")

    with col4:
        st.metric("Total Balance", "23 days", "-5")


if __name__ == "__main__":
    # For testing standalone
    st.set_page_config(
        page_title="Leave Request",
        page_icon="🏖️",
        layout="centered"
    )

    show_leave_request("http://localhost:5678/webhook")
