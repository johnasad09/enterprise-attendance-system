"""
Employee Attendance Check-in Module
Allows employees to check in/out for attendance with automatic image capture
"""

import streamlit as st
import requests
from datetime import datetime
import time
import base64
from io import BytesIO
from PIL import Image


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


def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    # Resize to reasonable size
    max_size = (400, 300)
    image.thumbnail(max_size, Image.Resampling.LANCZOS)

    buffered = BytesIO()
    image.save(buffered, format="JPEG", quality=80)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


def show_attendance_checkin(n8n_base_url):
    """
    Employee Attendance Check-in Page with Automatic Image Capture
    """

    # Custom CSS
    st.markdown("""
    <style>
        .camera-compact {
            max-width: 400px;
            margin: 0 auto;
        }
        .camera-compact img {
            max-width: 100%;
            border-radius: 10px;
        }
        .success-animation {
            text-align: center;
            padding: 30px;
            font-size: 64px;
            animation: bounce 0.5s ease;
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        .time-display {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
        }
        .time-display .time {
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .time-display .date {
            font-size: 18px;
            opacity: 0.9;
        }
        .stCameraInput {
            max-width: 400px !important;
            margin: 0 auto;
        }
        .stCameraInput > label {
            max-width: 400px !important;
        }
        .stCameraInput video {
            max-width: 400px !important;
            max-height: 300px !important;
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='color: #333; font-size: 32px; margin-bottom: 10px;'>⏰ Attendance Check-in</h1>
        <p style='color: #666; font-size: 14px;'>Mark Your Attendance for Today</p>
    </div>
    """, unsafe_allow_html=True)

    # Current Time Display
    current_time = datetime.now()
    st.markdown(f"""
    <div class='time-display'>
        <div class='time'>{current_time.strftime('%I:%M:%S %p')}</div>
        <div class='date'>{current_time.strftime('%A, %B %d, %Y')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Info Box
    st.markdown("""
    <div class='info-box'>
        <h4>📋 Check-in Instructions:</h4>
        <p>
            1. Enter your Employee ID and Name<br>
            2. Click "Check In Now" button<br>
            3. Allow camera access when prompted<br>
            4. Photo will be captured automatically<br>
            5. Your attendance will be recorded with photo
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'camera_ready' not in st.session_state:
        st.session_state.camera_ready = False
    if 'show_camera' not in st.session_state:
        st.session_state.show_camera = False
    if 'captured_image' not in st.session_state:
        st.session_state.captured_image = None
    if 'check_in_clicked' not in st.session_state:
        st.session_state.check_in_clicked = False

    # Employee Details Form
    st.subheader("📝 Enter Your Details")

    col1, col2 = st.columns(2)

    with col1:
        employee_id = st.text_input(
            "👤 Employee ID *",
            placeholder="E001",
            help="Enter your employee ID (e.g., E001)",
            key="emp_id_input"
        )

    with col2:
        employee_name = st.text_input(
            "📛 Full Name *",
            placeholder="John Doe",
            help="Enter your full name",
            key="emp_name_input"
        )

    # Department (optional for verification)
    department = st.selectbox(
        "🏢 Department (Optional)",
        ["Not Specified", "IT", "HR", "Finance", "Marketing", "Sales", "Operations", "Customer Service"],
        key="dept_input"
    )

    # Check In Button
    if st.button("📸 Check In Now", use_container_width=True, type="primary", key="checkin_btn"):
        if not employee_id or not employee_name:
            st.error("❌ Please fill in both Employee ID and Name!")
        else:
            st.session_state.check_in_clicked = True
            st.session_state.show_camera = True
            st.rerun()

    # Show Camera if check-in clicked
    if st.session_state.show_camera:
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; margin: 20px 0;'>
            <h3 style='color: #667eea;'>📸 Capture Your Photo</h3>
            <p style='color: #666;'>Allow camera access and take your photo</p>
        </div>
        """, unsafe_allow_html=True)

        # Camera input in centered container
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            camera_photo = st.camera_input("Take your photo", key="camera_input")

            if camera_photo is not None:
                # Image captured
                image = Image.open(camera_photo)
                st.session_state.captured_image = image
                st.session_state.camera_ready = True

                # Show preview
                st.image(image, caption="Captured Photo", width=400)
                st.success("✅ Photo captured successfully!")

                # Process check-in
                if st.button("✅ Confirm and Submit", use_container_width=True, type="primary", key="submit_btn"):
                    # Determine status based on time
                    current_hour = current_time.hour
                    current_minute = current_time.minute

                    # Late if after 9:30 AM
                    if current_hour > 9 or (current_hour == 9 and current_minute > 30):
                        status = "Late"
                        status_icon = "⚠️"
                        status_color = "warning"
                    else:
                        status = "Present"
                        status_icon = "✅"
                        status_color = "success"

                    # Convert image to base64
                    image_base64 = image_to_base64(st.session_state.captured_image)

                    # Prepare attendance data
                    attendance_data = {
                        "Employee ID": employee_id,
                        "Employee Name": employee_name,
                        "Department": department if department != "Not Specified" else "N/A",
                        "Date": current_time.strftime("%Y-%m-%d"),
                        "Time": current_time.strftime("%I:%M %p"),
                        "Status": status,
                        "Image": f"data:image/jpeg;base64,{image_base64}"
                    }

                    # Show loading
                    with st.spinner("Recording your attendance..."):
                        result = call_n8n_webhook(n8n_base_url, 'attendance', attendance_data)

                        if result:
                            # Success Animation
                            st.markdown(f"""
                            <div class='success-animation'>
                                {status_icon}
                            </div>
                            """, unsafe_allow_html=True)

                            if status_color == "success":
                                st.success(f"""
                                ✅ **Attendance Recorded Successfully!**

                                **Employee:** {employee_name} ({employee_id})  
                                **Time:** {current_time.strftime('%I:%M %p')}  
                                **Status:** {status}  
                                **Photo:** Captured and saved

                                Have a great day at work! 🎉
                                """)
                            else:
                                st.warning(f"""
                                ⚠️ **Attendance Recorded - Late Arrival**

                                **Employee:** {employee_name} ({employee_id})  
                                **Time:** {current_time.strftime('%I:%M %p')}  
                                **Status:** {status}  
                                **Photo:** Captured and saved

                                Please ensure to arrive on time tomorrow.
                                """)

                            st.balloons()

                            # Reset states
                            st.session_state.show_camera = False
                            st.session_state.check_in_clicked = False
                            st.session_state.captured_image = None
                            st.session_state.camera_ready = False

                            time.sleep(2)
                            st.rerun()
            else:
                # Camera access instructions
                st.info("""
                📷 **Camera Access Required**

                If camera doesn't appear:
                1. Click the camera icon above
                2. Allow camera access in browser
                3. Wait for camera to activate
                4. Take your photo
                """)

    # Statistics Section
    st.markdown("---")
    st.subheader("📊 Today's Attendance Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Check-ins", "18", "2")

    with col2:
        st.metric("On Time", "15", "1")

    with col3:
        st.metric("Late Arrivals", "3", "1")

    # Quick Links
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center;'>
        <h4 style='color: #666; margin-bottom: 15px;'>Quick Links</h4>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📅 View My Attendance", use_container_width=True, key="view_att"):
            st.info("Feature coming soon!")

    with col2:
        if st.button("🏖️ Request Leave", use_container_width=True, key="req_leave"):
            st.session_state.current_page = 'leave_request'
            st.rerun()

    with col3:
        if st.button("⏰ Log Overtime", use_container_width=True, key="log_ot"):
            st.session_state.current_page = 'overtime'
            st.rerun()


if __name__ == "__main__":
    # For testing standalone
    st.set_page_config(
        page_title="Employee Check-in",
        page_icon="⏰",
        layout="centered"
    )

    show_attendance_checkin("http://localhost:5678/webhook")
