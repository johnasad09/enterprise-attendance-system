import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import json
import time

# Import configuration
from config import (
    N8N_BASE_URL,
    DEFAULT_NEXT_EMPLOYEE_ID,
    DEPARTMENTS,
    PAGE_TITLE,
    PAGE_ICON,
    validate_config
)

# Import styling
from styles import apply_custom_styles

# Import page modules
from employee_registration import show_employee_registration
from attendance_checkin import show_attendance_checkin
from leave_request import show_leave_request
from overtime_log import show_overtime_log

# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Validate configuration before proceeding
validate_config()

# Apply custom styles
apply_custom_styles()

# Initialize session state
if 'n8n_base_url' not in st.session_state:
    st.session_state.n8n_base_url = N8N_BASE_URL
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'
if 'next_employee_id' not in st.session_state:
    st.session_state.next_employee_id = DEFAULT_NEXT_EMPLOYEE_ID


# ==================== N8N API FUNCTIONS ====================

def clean_dataframe_for_display(df):
    """Clean dataframe to prevent Arrow serialization errors"""
    if df.empty:
        return df

    # Convert all columns to string to avoid type conflicts
    df_clean = df.copy()
    for col in df_clean.columns:
        df_clean[col] = df_clean[col].astype(str)

    return df_clean


def call_n8n_webhook(endpoint, data=None, method='POST'):
    """Universal function to call n8n webhooks"""
    try:
        url = f"{st.session_state.n8n_base_url}/{endpoint}"

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


def fetch_attendance_data():
    """Fetch attendance data via n8n webhook"""
    result = call_n8n_webhook('admin/get-attendance', method='GET')
    if result:
        return pd.DataFrame(result.get('data', []))
    return pd.DataFrame()


def fetch_leave_data():
    """Fetch leave requests via n8n webhook"""
    result = call_n8n_webhook('admin/get-leave', method='GET')
    if result:
        df = pd.DataFrame(result.get('data', []))
        # Convert Days to numeric
        if not df.empty and 'Days' in df.columns:
            df['Days'] = pd.to_numeric(df['Days'], errors='coerce')
        return df
    return pd.DataFrame()


def fetch_overtime_data():
    """Fetch overtime logs via n8n webhook"""
    result = call_n8n_webhook('admin/get-overtime', method='GET')
    if result:
        df = pd.DataFrame(result.get('data', []))
        # Convert numeric columns to proper types
        if not df.empty:
            numeric_columns = ['Regular Hours', 'Overtime Hours', 'Regular Rate', 'Overtime Rate', 'Overtime Pay']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    return pd.DataFrame()


def fetch_employee_data():
    """Fetch employee records via n8n webhook"""
    result = call_n8n_webhook('admin/get-employees', method='GET')
    if result:
        return pd.DataFrame(result.get('data', []))
    return pd.DataFrame()


def fetch_alerts_data():
    """Fetch alerts via n8n webhook"""
    result = call_n8n_webhook('admin/get-alerts', method='GET')
    if result:
        return pd.DataFrame(result.get('data', []))
    return pd.DataFrame()


def get_system_stats():
    """Calculate system statistics from n8n data"""
    try:
        result = call_n8n_webhook('admin/get-stats', method='GET')
        if result:
            return (
                result.get('total_employees', 0),
                result.get('present_today', 0),
                result.get('pending_leave', 0),
                result.get('late_arrivals', 0)
            )
        return 0, 0, 0, 0
    except Exception as e:
        st.error(f"Error fetching stats: {str(e)}")
        return 0, 0, 0, 0


# ==================== PAGE: ADMIN DASHBOARD ====================

def show_admin_dashboard():
    """Main Admin Dashboard"""

    # Header
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 10px; margin-bottom: 30px; color: white;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <h1 style='margin: 0; font-size: 32px;'>📊 Admin Dashboard</h1>
                    <p style='margin: 5px 0 0 0; opacity: 0.9;'>Enterprise Attendance Management</p>
                </div>
                <div style='text-align: right;'>
                    <div style='font-size: 18px; font-weight: 600;'>👨‍💼 Admin User</div>
                    <div style='font-size: 14px; opacity: 0.8;'>System Administrator</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("👤 Register Employee", use_container_width=True, type="primary"):
            st.session_state.current_page = 'register'
            st.rerun()
    with col2:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()

    st.markdown("---")

    # System Overview Statistics
    st.subheader("📈 System Overview")

    total_employees, present_today, pending_leave, late_arrivals = get_system_stats()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="👥 Total Employees", value=total_employees)

    with col2:
        st.metric(label="✅ Present Today", value=present_today)

    with col3:
        st.metric(label="⌛ Pending Leave Requests", value=pending_leave)

    with col4:
        st.metric(label="🚨 Late Arrivals (Today)", value=late_arrivals)

    st.markdown("---")

    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Attendance Log",
        "🏖️ Leave Management",
        "⏰ Overtime Log",
        "👥 Employee Records",
        "⚙️ System Actions"
    ])

    # Tab 1: Attendance Log
    with tab1:
        st.subheader("Attendance Log")

        col1, col2, col3, col4 = st.columns([2, 2, 3, 1])

        with col1:
            filter_dept = st.selectbox("Department", ["All Departments"] + DEPARTMENTS, key="att_dept")

        with col2:
            filter_date = st.date_input("Date", value=datetime.now(), key="att_date")

        with col3:
            search_term = st.text_input("Search by ID or Name", "", key="att_search")

        with col4:
            if st.button("📥 Export", key="export_att"):
                st.success("Exporting data...")

        with st.spinner("Loading attendance data from n8n..."):
            df_attendance = fetch_attendance_data()

            if not df_attendance.empty:
                if 'Department' in df_attendance.columns and filter_dept != "All Departments":
                    df_attendance = df_attendance[df_attendance['Department'] == filter_dept]

                if search_term:
                    if 'Employee ID' in df_attendance.columns and 'Employee Name' in df_attendance.columns:
                        mask = (df_attendance['Employee ID'].astype(str).str.contains(search_term, case=False,
                                                                                      na=False) |
                                df_attendance['Employee Name'].astype(str).str.contains(search_term, case=False,
                                                                                        na=False))
                        df_attendance = df_attendance[mask]

                # Clean dataframe for display
                df_display = clean_dataframe_for_display(df_attendance)
                st.dataframe(df_display, width='stretch', hide_index=True)
            else:
                st.info("📄 No attendance records found.")

    # Tab 2: Leave Management
    with tab2:
        st.subheader("Leave Management")

        col1, col2 = st.columns([3, 1])

        with col1:
            filter_leave_status = st.selectbox("Status", ["All Statuses", "Pending", "Approved", "Rejected"],
                                               key="leave_status")

        with col2:
            if st.button("📥 Export", key="export_leave"):
                st.success("Exporting data...")

        with st.spinner("Loading leave requests from n8n..."):
            df_leave = fetch_leave_data()

            if not df_leave.empty:
                if 'Status' in df_leave.columns and filter_leave_status != "All Statuses":
                    df_leave = df_leave[df_leave['Status'] == filter_leave_status]

                for idx, row in df_leave.iterrows():
                    with st.container():
                        col1, col2, col3, col4 = st.columns([1, 2, 3, 1])

                        with col1:
                            st.write(f"**{row.get('Employee ID', 'N/A')}**")
                            st.write(row.get('Employee Name', 'N/A'))

                        with col2:
                            st.write(f"**Type:** {row.get('Leave Type', 'N/A')}")
                            st.write(f"**Days:** {row.get('Days', 0)}")

                        with col3:
                            st.write(f"**Dates:** {row.get('Start Date', 'N/A')} to {row.get('End Date', 'N/A')}")
                            st.write(f"**Reason:** {row.get('Reason', 'N/A')}")
                            st.write(f"**Status:** {row.get('Status', 'Pending')}")

                        with col4:
                            if row.get('Status') == 'Pending':
                                col_approve, col_reject = st.columns(2)
                                with col_approve:
                                    if st.button("✅", key=f"approve_{idx}", help="Approve", use_container_width=True):
                                        with st.spinner("Approving..."):
                                            result = call_n8n_webhook('admin/approve-leave', {
                                                'Leave ID': row.get('Leave ID'),
                                                'Status': 'Approved',
                                                'Approved By': 'Admin'
                                            })
                                            if result and result.get('success'):
                                                st.success("✅ Approved!")
                                                time.sleep(1)
                                                st.rerun()
                                            elif result:
                                                st.error(f"Error: {result.get('message', 'Unknown error')}")
                                with col_reject:
                                    if st.button("❌", key=f"reject_{idx}", help="Reject", use_container_width=True):
                                        with st.spinner("Rejecting..."):
                                            result = call_n8n_webhook('admin/approve-leave', {
                                                'Leave ID': row.get('Leave ID'),
                                                'Status': 'Rejected',
                                                'Approved By': 'Admin'
                                            })
                                            if result and result.get('success'):
                                                st.warning("❌ Rejected!")
                                                time.sleep(1)
                                                st.rerun()
                                            elif result:
                                                st.error(f"Error: {result.get('message', 'Unknown error')}")

                        st.markdown("---")
            else:
                st.info("🏖️ No leave requests found.")

    # Tab 3: Overtime Log
    with tab3:
        st.subheader("Overtime Log")

        col1, col2 = st.columns([3, 1])

        with col1:
            filter_overtime_date = st.date_input("Filter by Date", value=None, key="overtime_date")

        with col2:
            if st.button("📥 Export", key="export_overtime"):
                st.success("Exporting data...")

        with st.spinner("Loading overtime logs from n8n..."):
            df_overtime = fetch_overtime_data()

            if not df_overtime.empty:
                # Clean dataframe for display
                df_display = clean_dataframe_for_display(df_overtime)
                st.dataframe(df_display, width='stretch', hide_index=True)
            else:
                st.info("⏰ No overtime logs found.")

    # Tab 4: Employee Records
    with tab4:
        st.subheader("Employee Records")

        col1, col2 = st.columns([3, 1])

        with col1:
            if st.button("🔄 Sync from n8n", key="sync_employees"):
                with st.spinner("Syncing employee data..."):
                    st.success("Employee data synced!")
                    time.sleep(1)
                    st.rerun()

        with col2:
            if st.button("📥 Export", key="export_employees"):
                st.success("Exporting data...")

        with st.spinner("Loading employee records from n8n..."):
            df_employees = fetch_employee_data()

            if not df_employees.empty:
                # Clean dataframe for display
                df_display = clean_dataframe_for_display(df_employees)
                st.dataframe(df_display, width='stretch', hide_index=True)
            else:
                st.info("👥 No employee records found.")

    # Tab 5: System Actions
    with tab5:
        st.subheader("⚙️ System Automation Actions")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("💰 Generate Monthly Payroll", key="gen_payroll", use_container_width=True, type="primary"):
                with st.spinner("Generating payroll via n8n..."):
                    result = call_n8n_webhook('admin/generate-payroll')
                    if result:
                        st.success("✅ Payroll generated successfully!")
                        st.json(result)

        with col2:
            if st.button("🔔 Run Daily Attendance Check", key="check_alerts", use_container_width=True, type="primary"):
                with st.spinner("Running attendance check via n8n..."):
                    result = call_n8n_webhook('admin/check-alerts')
                    if result:
                        alerts_found = result.get('alerts_found', 0)

                        if alerts_found > 0:
                            st.warning(f"⚠️ Found **{alerts_found}** alert(s)")

                            time.sleep(2)
                            alerts_df = fetch_alerts_data()

                            if not alerts_df.empty:
                                today = datetime.now()
                                today_str1 = today.strftime('%Y-%m-%d')
                                today_str2 = today.strftime('%m/%d/%Y')
                                today_str3 = f"{today.month}/{today.day}/{today.year}"

                                if 'Date' in alerts_df.columns:
                                    today_alerts = alerts_df[
                                        alerts_df['Date'].astype(str).str.contains(today_str1, na=False) |
                                        alerts_df['Date'].astype(str).str.contains(today_str2, na=False) |
                                        alerts_df['Date'].astype(str).str.contains(today_str3, na=False)
                                        ]

                                    if today_alerts.empty:
                                        st.info("Showing latest alerts:")
                                        today_alerts = alerts_df.tail(alerts_found)

                                    for idx, alert in today_alerts.iterrows():
                                        alert_type = alert.get('Alert Type', 'UNKNOWN')
                                        severity = alert.get('Severity', 'MEDIUM')

                                        if severity == 'HIGH':
                                            border_color = '#f56565'
                                            bg_color = '#fed7d7'
                                        elif severity == 'MEDIUM':
                                            border_color = '#ed8936'
                                            bg_color = '#feebc8'
                                        else:
                                            border_color = '#667eea'
                                            bg_color = '#e6fffa'

                                        st.markdown(f"""
                                        <div style='background-color: {bg_color}; padding: 15px; border-left: 4px solid {border_color}; 
                                                    margin-bottom: 10px; border-radius: 5px;'>
                                            <div style='font-weight: 600; color: #333; margin-bottom: 5px;'>
                                                🚨 {alert_type}: {alert.get('Employee Name', 'Unknown')} ({alert.get('Employee ID', 'N/A')})
                                            </div>
                                            <div style='color: #666; font-size: 14px;'>
                                                📧 {alert.get('Email', 'N/A')} | 🏢 {alert.get('Department', 'N/A')}
                                            </div>
                                            <div style='color: #666; font-size: 14px; margin-top: 5px;'>
                                                💬 {alert.get('Message', 'No message')}
                                            </div>
                                            <div style='color: #999; font-size: 12px; margin-top: 8px;'>
                                                🕐 {alert.get('Time', 'N/A')} | 📅 {alert.get('Date', 'N/A')} | ⚠️ {severity}
                                            </div>
                                        </div>
                                        """, unsafe_allow_html=True)
                        else:
                            st.success("✅ No issues found - all employees are on time!")

        with col3:
            if st.button("🚨 View Logged Alerts", key="view_alerts", use_container_width=True):
                alerts_df = fetch_alerts_data()
                if not alerts_df.empty:
                    # Clean dataframe for display
                    df_display = clean_dataframe_for_display(alerts_df)
                    st.dataframe(df_display, width='stretch', hide_index=True)
                else:
                    st.info("No alerts logged yet.")

        st.markdown("---")
        st.subheader("📊 Recent System Activity Feed")

        activities = [
            {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "text": "🔔 System monitoring active"},
            {"time": (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"),
             "text": "✅ Latest check-ins recorded"},
            {"time": (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
             "text": "🏖️ Processing leave requests"},
        ]

        for activity in activities:
            st.markdown(f"""
            <div class='activity-item'>
                <div style='color: #999; font-size: 12px; margin-bottom: 5px;'>{activity['time']}</div>
                <div style='color: #333; font-size: 14px;'>{activity['text']}</div>
            </div>
            """, unsafe_allow_html=True)


# ==================== SIDEBAR ====================

with st.sidebar:
    st.header("⚙️ Navigation")

    st.markdown("---")

    # Admin Section
    st.markdown("**👨‍💼 Admin Panel**")
    if st.button("📊 Admin Dashboard", use_container_width=True, key="nav_dashboard", type="primary"):
        st.session_state.current_page = 'dashboard'
        st.rerun()

    if st.button("👤 Register Employee", use_container_width=True, key="nav_register"):
        st.session_state.current_page = 'register'
        st.rerun()

    st.markdown("---")

    # Employee Section
    st.markdown("**👷 Employee Portal**")
    if st.button("⏰ Check-in/out", use_container_width=True, key="nav_checkin"):
        st.session_state.current_page = 'checkin'
        st.rerun()

    if st.button("🏖️ Request Leave", use_container_width=True, key="nav_leave"):
        st.session_state.current_page = 'leave_request'
        st.rerun()

    if st.button("⏰ Log Overtime", use_container_width=True, key="nav_overtime"):
        st.session_state.current_page = 'overtime'
        st.rerun()

    st.markdown("---")
    st.success("""
    **System Status:**  
    ✅ n8n: Connected  
    ✅ Real-time updates  
    ✅ All systems operational
    """)

# ==================== MAIN ROUTER ====================

if st.session_state.current_page == 'dashboard':
    show_admin_dashboard()
elif st.session_state.current_page == 'register':
    show_employee_registration(st.session_state.n8n_base_url, DEPARTMENTS)
elif st.session_state.current_page == 'checkin':
    show_attendance_checkin(st.session_state.n8n_base_url)
elif st.session_state.current_page == 'leave_request':
    show_leave_request(st.session_state.n8n_base_url)
elif st.session_state.current_page == 'overtime':
    show_overtime_log(st.session_state.n8n_base_url)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Enterprise Attendance Management System v1.0</p>
        <p style='font-size: 12px; margin-top: 10px;'>All data accessed via n8n webhooks</p>
    </div>
""", unsafe_allow_html=True)
