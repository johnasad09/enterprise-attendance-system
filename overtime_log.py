"""
Overtime Logging Module
Allows employees to log overtime hours with real-time pay calculation
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


def show_overtime_log(n8n_base_url):
    """
    Overtime Logging Page with Real-time Calculation
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
        .calculation-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
            text-align: center;
        }
        .pay-amount {
            font-size: 48px;
            font-weight: 700;
            margin: 15px 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='color: #333; font-size: 32px; margin-bottom: 10px;'>⏰ Overtime Log</h1>
        <p style='color: #666; font-size: 14px;'>Record Your Overtime Hours</p>
    </div>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("← Back to Check-in"):
        st.session_state.current_page = 'checkin'
        st.rerun()

    # Info Box
    st.markdown("""
    <div class='info-box'>
        <h4>📋 Overtime Policy:</h4>
        <p>
            • Overtime rate: 1.5x regular hourly rate<br>
            • Must be pre-approved by manager<br>
            • Maximum 8 hours per day<br>
            • Log within 24 hours of completion<br>
            • Requires justification and approval
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📝 Overtime Details")

    # Employee Information
    col1, col2 = st.columns(2)

    with col1:
        employee_id = st.text_input(
            "👤 Employee ID *",
            placeholder="E001",
            help="Your employee ID",
            key="emp_id"
        )

    with col2:
        employee_name = st.text_input(
            "📛 Full Name *",
            placeholder="John Doe",
            help="Your full name",
            key="emp_name"
        )

    # Date and Hours
    col1, col2 = st.columns(2)

    with col1:
        overtime_date = st.date_input(
            "📅 Overtime Date *",
            value=datetime.now(),
            max_value=datetime.now(),
            help="Date when overtime was performed",
            key="ot_date"
        )

    with col2:
        overtime_hours = st.number_input(
            "⏱️ Overtime Hours *",
            min_value=0.5,
            max_value=8.0,
            value=2.0,
            step=0.5,
            help="Number of overtime hours (0.5 - 8.0)",
            key="ot_hours"
        )

    # Regular Hours and Rate
    col1, col2 = st.columns(2)

    with col1:
        regular_hours = st.number_input(
            "🕐 Regular Hours",
            min_value=0,
            max_value=12,
            value=8,
            step=1,
            help="Regular working hours for the day",
            key="reg_hours"
        )

    with col2:
        hourly_rate = st.number_input(
            "💰 Hourly Rate ($) *",
            min_value=10.0,
            max_value=100.0,
            value=15.0,
            step=0.5,
            help="Your regular hourly rate",
            key="hr_rate"
        )

    # Calculate overtime pay in real-time
    overtime_rate = hourly_rate * 1.5
    overtime_pay = overtime_hours * overtime_rate

    # Display calculation in real-time (updates automatically with inputs)
    st.markdown(f"""
    <div class='calculation-box'>
        <div style='font-size: 16px; opacity: 0.9;'>Estimated Overtime Pay</div>
        <div class='pay-amount'>${overtime_pay:.2f}</div>
        <div style='font-size: 14px; opacity: 0.8;'>
            {overtime_hours} hours × ${overtime_rate:.2f}/hour (1.5x rate)
        </div>
        <div style='font-size: 12px; opacity: 0.7; margin-top: 10px;'>
            Regular Rate: ${hourly_rate:.2f}/hour | Overtime Rate: ${overtime_rate:.2f}/hour
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Reason for Overtime
    reason = st.text_area(
        "💬 Reason for Overtime *",
        placeholder="Please explain why overtime was necessary...",
        height=120,
        help="Provide detailed justification for overtime",
        key="ot_reason"
    )

    # Project/Task
    task_project = st.text_input(
        "📋 Project/Task",
        placeholder="e.g., Server Upgrade, Client Meeting, Emergency Fix",
        help="What task required overtime?",
        key="ot_task"
    )

    # Approved By (Manager)
    approved_by = st.text_input(
        "✅ Approved By",
        placeholder="Manager Name",
        help="Manager who pre-approved the overtime",
        key="ot_approver"
    )

    # Additional Notes
    notes = st.text_area(
        "📝 Additional Notes (Optional)",
        placeholder="Any additional information...",
        height=80,
        key="ot_notes"
    )

    # Submit Button
    if st.button("📤 Submit Overtime Log", use_container_width=True, type="primary"):
        # Validation
        if not employee_id or not employee_name:
            st.error("❌ Please enter Employee ID and Name!")
            return

        if overtime_hours <= 0:
            st.error("❌ Overtime hours must be greater than 0!")
            return

        if not reason or len(reason.strip()) < 10:
            st.error("❌ Please provide a detailed reason (at least 10 characters)!")
            return

        # Prepare overtime data with all required fields
        overtime_data = {
            "Employee ID": employee_id,
            "Employee Name": employee_name,
            "Date": overtime_date.strftime("%Y-%m-%d"),
            "Regular Hours": str(regular_hours),
            "Overtime Hours": str(overtime_hours),
            "Hourly Rate": str(hourly_rate),
            "Regular Rate": str(hourly_rate),
            "Overtime Rate": str(overtime_rate),
            "Overtime Pay": str(overtime_pay),
            "Reason": reason.strip(),
            "Task/Project": task_project if task_project else "N/A",
            "Approved By": approved_by if approved_by else "Pending",
            "Notes": notes.strip() if notes else "",
            "Logged At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Show loading
        with st.spinner("Logging your overtime..."):
            result = call_n8n_webhook(n8n_base_url, 'overtime/log', overtime_data)

            if result:
                st.success(f"""
                ✅ **Overtime Logged Successfully!**

                **Employee:** {employee_name} ({employee_id})  
                **Date:** {overtime_date.strftime('%B %d, %Y')}  
                **Hours:** {overtime_hours} hours  
                **Estimated Pay:** ${overtime_pay:.2f}  
                **Status:** {'Approved' if approved_by else 'Pending Approval'}  

                Your overtime has been recorded and will be included in your next payroll.
                """)

                st.balloons()

                # Show breakdown
                with st.expander("💰 Payment Breakdown"):
                    st.write(f"""
                    **Regular Rate:** ${hourly_rate:.2f}/hour  
                    **Overtime Rate (1.5x):** ${overtime_rate:.2f}/hour  
                    **Overtime Hours:** {overtime_hours} hours  
                    **Total Overtime Pay:** ${overtime_pay:.2f}  

                    ---

                    *Note: This is an estimate. Final amount may vary based on tax deductions and company policy.*
                    """)

    # Overtime History Section
    st.markdown("---")
    st.subheader("📊 This Month's Overtime Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Hours", "12.5 hrs", "+2.5")

    with col2:
        st.metric("Estimated Pay", "$281.25", "+56.25")

    with col3:
        st.metric("Days Logged", "5 days", "+1")

    with col4:
        st.metric("Pending Approval", "2 logs", "0")

    # Recent Overtime Logs
    st.markdown("---")
    st.subheader("📜 Recent Overtime Logs")

    st.info("Enter your Employee ID above and submit a log to see your overtime history here.")

    # Tips Section
    st.markdown("---")
    st.subheader("💡 Overtime Tips")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Before Logging:**
        - ✅ Get manager pre-approval
        - ✅ Document the reason clearly
        - ✅ Log within 24 hours
        - ✅ Include project/task details
        """)

    with col2:
        st.markdown("""
        **Payment Information:**
        - 💰 Overtime rate: 1.5x regular rate
        - 📅 Paid in next payroll cycle
        - 🧾 Subject to standard deductions
        - 📊 View in payroll reports
        """)


if __name__ == "__main__":
    # For testing standalone
    st.set_page_config(
        page_title="Overtime Log",
        page_icon="⏰",
        layout="centered"
    )

    show_overtime_log("http://localhost:5678/webhook")
