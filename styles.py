"""
Custom Styling Module for Enterprise Attendance System
Contains all CSS styles, colors, and theme configurations
"""

import streamlit as st

# Color Palette
COLORS = {
    'primary': '#667eea',
    'primary_dark': '#764ba2',
    'secondary': '#48bb78',
    'warning': '#ed8936',
    'danger': '#f56565',
    'info': '#4299e1',
    'success': '#48bb78',
    'light_bg': '#f0f2f5',
    'white': '#ffffff',
    'text_dark': '#333333',
    'text_light': '#666666',
    'border': '#e2e8f0',
}


def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app"""
    st.markdown(f"""
    <style>
        /* Global Styles */
        .main {{
            background-color: {COLORS['light_bg']};
        }}

        /* Header Gradient */
        .gradient-header {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            color: white;
        }}

        /* Metric Cards */
        .stMetric {{
            background-color: {COLORS['white']};
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border-left: 4px solid {COLORS['primary']};
        }}

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
            background-color: {COLORS['white']};
            padding: 10px;
            border-radius: 10px 10px 0 0;
        }}

        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            white-space: pre-wrap;
            background-color: {COLORS['light_bg']};
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            color: {COLORS['text_light']};
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }}

        .stTabs [data-baseweb="tab"]:hover {{
            background-color: {COLORS['border']};
            border-color: {COLORS['primary']};
            transform: translateY(-2px);
        }}

        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
            color: white !important;
            border-color: {COLORS['primary']};
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }}

        /* Button Styling */
        .stButton > button {{
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }}

        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}

        /* Primary Button */
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
            color: white;
        }}

        /* Secondary Button */
        .stButton > button[kind="secondary"] {{
            background-color: {COLORS['white']};
            color: {COLORS['primary']};
            border-color: {COLORS['primary']};
        }}

        .stButton > button[kind="secondary"]:hover {{
            background-color: {COLORS['primary']};
            color: white;
        }}

        /* Info Box */
        .info-box {{
            background: #edf2f7;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 25px;
            border-left: 4px solid {COLORS['primary']};
        }}

        .info-box h4 {{
            color: {COLORS['text_dark']};
            margin-bottom: 8px;
            font-size: 14px;
        }}

        .info-box p {{
            color: {COLORS['text_light']};
            font-size: 13px;
            line-height: 1.5;
            margin: 0;
        }}

        /* Success Box */
        .success-box {{
            background: #c6f6d5;
            color: #22543d;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid {COLORS['success']};
            margin: 10px 0;
        }}

        /* Warning Box */
        .warning-box {{
            background: #feebc8;
            color: #7c2d12;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid {COLORS['warning']};
            margin: 10px 0;
        }}

        /* Danger Box */
        .danger-box {{
            background: #fed7d7;
            color: #742a2a;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid {COLORS['danger']};
            margin: 10px 0;
        }}

        /* Status Badges */
        .badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            display: inline-block;
        }}

        .badge-present {{
            background-color: #c6f6d5;
            color: #22543d;
        }}

        .badge-absent {{
            background-color: #fed7d7;
            color: #742a2a;
        }}

        .badge-late {{
            background-color: #feebc8;
            color: #7c2d12;
        }}

        .badge-pending {{
            background-color: #feebc8;
            color: #7c2d12;
        }}

        .badge-approved {{
            background-color: #c6f6d5;
            color: #22543d;
        }}

        .badge-rejected {{
            background-color: #fed7d7;
            color: #742a2a;
        }}

        /* Preview ID */
        .preview-id {{
            background: #f7fafc;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
            border: 2px solid {COLORS['border']};
        }}

        .generated-id {{
            font-size: 24px;
            font-weight: 700;
            color: {COLORS['primary']};
            margin-top: 5px;
        }}

        /* Time Display */
        .time-display {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }}

        .time-display .time {{
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 10px;
        }}

        .time-display .date {{
            font-size: 18px;
            opacity: 0.9;
        }}

        /* Calculation Box */
        .calculation-box {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
            text-align: center;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }}

        .pay-amount {{
            font-size: 48px;
            font-weight: 700;
            margin: 15px 0;
        }}

        /* Leave Summary */
        .leave-summary {{
            background: #f7fafc;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border: 2px solid {COLORS['border']};
        }}

        /* Alert Cards */
        .alert-card {{
            background-color: white;
            padding: 15px;
            border-left: 4px solid;
            margin-bottom: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}

        .alert-card:hover {{
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}

        .alert-card.high {{
            border-left-color: {COLORS['danger']};
            background-color: #fed7d7;
        }}

        .alert-card.medium {{
            border-left-color: {COLORS['warning']};
            background-color: #feebc8;
        }}

        .alert-card.low {{
            border-left-color: {COLORS['info']};
            background-color: #e6fffa;
        }}

        /* Activity Feed */
        .activity-item {{
            background-color: #f7fafc;
            padding: 15px;
            border-left: 3px solid {COLORS['primary']};
            margin-bottom: 10px;
            border-radius: 5px;
            transition: all 0.3s ease;
        }}

        .activity-item:hover {{
            background-color: #e2e8f0;
            transform: translateX(5px);
        }}

        /* Success Animation */
        .success-animation {{
            text-align: center;
            padding: 30px;
            font-size: 64px;
            animation: bounce 0.5s ease;
        }}

        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-20px); }}
        }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background-color: #ffffff;
            border-right: 2px solid {COLORS['border']};
        }}

        section[data-testid="stSidebar"] .stButton > button {{
            width: 100%;
            text-align: left;
            justify-content: flex-start;
            margin-bottom: 5px;
        }}

        /* Form Styling */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {{
            border-radius: 8px;
            border: 2px solid {COLORS['border']};
            transition: all 0.3s ease;
        }}

        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stTextArea > div > div > textarea:focus,
        .stNumberInput > div > div > input:focus {{
            border-color: {COLORS['primary']};
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}

        /* DataFrames */
        .stDataFrame {{
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}

        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Responsive Design */
        @media (max-width: 768px) {{
            .time-display .time {{
                font-size: 32px;
            }}

            .pay-amount {{
                font-size: 32px;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)


def create_colored_metric(label, value, icon="", color="primary"):
    """Create a colored metric card"""
    bg_color = {
        'primary': '#667eea',
        'success': '#48bb78',
        'warning': '#ed8936',
        'danger': '#f56565',
        'info': '#4299e1',
    }.get(color, '#667eea')

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {bg_color} 0%, {bg_color}dd 100%);
                color: white; padding: 20px; border-radius: 10px; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
        <div style='font-size: 14px; opacity: 0.9; margin-bottom: 5px;'>{icon} {label}</div>
        <div style='font-size: 36px; font-weight: 700;'>{value}</div>
    </div>
    """, unsafe_allow_html=True)


def create_status_badge(status, text=None):
    """Create a colored status badge"""
    status_map = {
        'present': ('badge-present', '✅'),
        'absent': ('badge-absent', '❌'),
        'late': ('badge-late', '⚠️'),
        'pending': ('badge-pending', '⏳'),
        'approved': ('badge-approved', '✅'),
        'rejected': ('badge-rejected', '❌'),
    }

    badge_class, icon = status_map.get(status.lower(), ('badge-pending', ''))
    display_text = text if text else status.capitalize()

    return f'<span class="badge {badge_class}">{icon} {display_text}</span>'


def create_gradient_button(text, icon="", key=None):
    """Create a gradient-styled button"""
    return st.button(f"{icon} {text}", key=key, use_container_width=True)
