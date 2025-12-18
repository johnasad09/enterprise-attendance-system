# 🏢 Enterprise Attendance Management System

A complete attendance management system built with Streamlit, n8n, and Google Sheets.
### NOTE: This is a test project for the AI/ML Facebook Community.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.29.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Security](#security)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### Admin Features
- 📊 **Dashboard** - Real-time attendance statistics
- 👥 **Employee Management** - Register and manage employees
- ✅ **Leave Approval** - Approve/reject leave requests
- 💰 **Payroll Generation** - Automated monthly payroll
- 🚨 **Alert System** - Track late arrivals and absences

### Employee Features
- 📸 **Photo Check-in** - Attendance with camera capture
- 🏖️ **Leave Requests** - Submit leave applications
- ⏰ **Overtime Logging** - Log overtime with real-time pay calculation

### Technical Features
- 🔐 **Secure** - Environment-based configuration
- ☁️ **Cloud Ready** - Deploy to Streamlit Cloud
- 🔗 **n8n Integration** - All data via webhooks
- 📊 **Google Sheets** - Data storage and management

---

## 🎥 Demo

**Live Demo:**
URL will be provided on Demand

**Screenshots:**
<img width="1920" height="1548" alt="image" src="https://github.com/user-attachments/assets/19821cfd-a781-4624-9e11-dab1a2a1fedc" />
<img width="1920" height="1280" alt="image" src="https://github.com/user-attachments/assets/2a77d4fb-8beb-4bec-936d-e9df43522f32" />
<img width="1920" height="1755" alt="image" src="https://github.com/user-attachments/assets/e07f6278-c9a8-460c-a4bf-f09b9ffed480" />
<img width="1920" height="2231" alt="image" src="https://github.com/user-attachments/assets/27b32e2f-bc58-4f06-96a9-bdb7b76da628" />
<img width="1920" height="2686" alt="image" src="https://github.com/user-attachments/assets/f3bfd935-d025-40bf-8e30-971a1da90ce8" />


---

## 📦 Prerequisites

Before you begin, ensure you have:

1. **Python 3.8+** installed
2. **n8n instance** (self-hosted or cloud)
3. **Google Sheet** for data storage
4. **GitHub account** (for deployment)
5. **Streamlit Cloud account** (free tier available)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Step 1: Configure n8n

1. **Set up n8n workflows:**
   - Import workflows from `n8n_workflows/` folder
   - Update Google Sheets credentials in each workflow
   - Activate all workflows
   - Note your n8n webhook base URL

2. **Your n8n base URL format:**
   ```
   https://your-n8n-domain.com/webhook
   ```

### Step 2: Configure Google Sheet

1. **Create a Google Sheet** with these tabs:
   - Attendance
   - Leave_Requests
   - Overtime Sheet
   - Employees
   - Alerts
   - Payroll

2. **Get your Sheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/[THIS_IS_YOUR_SHEET_ID]/edit
   ```

### Step 3: Local Configuration

**Option A: Edit config.py (Not Recommended for Public Repos)**

```python
# In config.py, replace:
N8N_BASE_URL = "https://your-n8n-domain.com/webhook"
GOOGLE_SHEET_ID = "your-sheet-id-here"
```

**Option B: Use Environment Variables (Recommended)**

```bash
# Windows (PowerShell)
$env:N8N_BASE_URL="https://your-n8n-domain.com/webhook"

# Mac/Linux
export N8N_BASE_URL="https://your-n8n-domain.com/webhook"
```

**Option C: Use Streamlit Secrets (Best for Production)**

1. Create `.streamlit/secrets.toml`:
   ```bash
   mkdir .streamlit
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. Edit `.streamlit/secrets.toml`:
   ```toml
   [n8n]
   base_url = "https://your-n8n-domain.com/webhook"
   
   [google_sheets]
   sheet_id = "your-sheet-id-here"
   ```

### Step 4: Run Locally

```bash
streamlit run main.py
```

Visit: `http://localhost:8501`

---

## 🌐 Deployment to Streamlit Cloud

### Step 1: Prepare Repository

1. **Create `.gitignore`:**
   ```bash
   # Copy from .gitignore file in this repo
   ```

2. **IMPORTANT: Never commit these files:**
   - `.streamlit/secrets.toml`
   - Any file with actual n8n URLs
   - Environment files with credentials

3. **Verify config.py has placeholders:**
   ```python
   N8N_BASE_URL = "YOUR_N8N_URL_HERE"  # ✅ Good - placeholder
   # NOT:
   N8N_BASE_URL = "https://n8n.myserver.com"  # ❌ Bad - actual URL
   ```

### Step 2: Push to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository
4. Set main file: `main.py`
5. Click "Advanced settings"
6. Add secrets:

```toml
[n8n]
base_url = "https://your-n8n-domain.com/webhook"

[google_sheets]
sheet_id = "your-sheet-id-here"
```

7. Click "Deploy"

### Step 4: Verify Deployment

1. Wait for deployment (2-5 minutes)
2. Visit your app URL
3. Test check-in feature
4. Verify data appears in Google Sheet

---

## 🔐 Security Best Practices

### ✅ DO:
- ✅ Use Streamlit Secrets for sensitive data
- ✅ Keep `.streamlit/secrets.toml` in `.gitignore`
- ✅ Use environment variables for local development
- ✅ Use HTTPS for n8n webhooks
- ✅ Rotate credentials regularly
- ✅ Use strong passwords
- ✅ Keep dependencies updated

### ❌ DON'T:
- ❌ Commit actual n8n URLs to GitHub
- ❌ Share secrets.toml file publicly
- ❌ Use HTTP (non-secure) webhooks
- ❌ Hardcode credentials in code
- ❌ Use default passwords
- ❌ Share API keys publicly

### Security Checklist:

- [ ] `.gitignore` includes `secrets.toml`
- [ ] `config.py` has placeholder values
- [ ] n8n webhooks use HTTPS
- [ ] Streamlit secrets configured
- [ ] Google Sheet has proper permissions
- [ ] No credentials in code files
- [ ] Repository secrets are set

---

## 📖 Usage

### For Administrators

1. **Access Admin Dashboard:**
   - Navigate to the app
   - Click "Admin Dashboard" in sidebar

2. **Register New Employee:**
   - Click "Register Employee"
   - Fill in details
   - Employee ID auto-generated

3. **Approve Leave Requests:**
   - Go to "Leave Management" tab
   - Click ✅ Approve or ❌ Reject

4. **Generate Payroll:**
   - Go to "System Actions" tab
   - Click "Generate Monthly Payroll"

### For Employees

1. **Check-in:**
   - Enter Employee ID and Name
   - Click "Check In Now"
   - Take photo
   - Confirm and submit

2. **Request Leave:**
   - Click "Request Leave" in sidebar
   - Fill leave details
   - Submit request

3. **Log Overtime:**
   - Click "Log Overtime"
   - Enter hours and rate
   - See real-time pay calculation
   - Submit log

---

## 🗂️ Project Structure

```
attendance-system/
├── .streamlit/
│   ├── secrets.toml.example    # Example secrets file
│   └── config.toml             # Streamlit config
├── main.py                     # Main application
├── config.py                   # Configuration (with placeholders)
├── styles.py                   # Custom CSS styling
├── attendance_checkin.py       # Check-in module
├── leave_request.py            # Leave request module
├── overtime_log.py             # Overtime module
├── employee_registration.py    # Registration module
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore file
├── README.md                   # This file
└── LICENSE                     # License file
```

---

## 🔧 Troubleshooting

### Issue: "Cannot connect to n8n"

**Solution:**
1. Check n8n URL is correct
2. Verify n8n workflows are active
3. Check n8n is accessible from internet
4. Verify secrets are set in Streamlit Cloud

### Issue: "Google Sheet not updating"

**Solution:**
1. Verify Sheet ID is correct
2. Check n8n has Google Sheets credentials
3. Verify sheet tab names match exactly
4. Check n8n workflow execution logs

### Issue: "Camera not working"

**Solution:**
1. Allow camera permissions in browser
2. Use HTTPS (required for camera access)
3. Check browser compatibility
4. Try different browser

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

**Please do not:**
- Commit any actual credentials
- Include your n8n URLs
- Share sensitive data

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/johnasad09)
- Email: johnasad09@gmail[dot]com

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Automation with [n8n](https://n8n.io/)
- Data storage with [Google Sheets](https://sheets.google.com/)

---

## 📞 Support

If you have questions or need help:

1. **Check the documentation** in this README
2. **Search existing issues** on GitHub
3. **Open a new issue** with details
4. **Include error messages** and steps to reproduce

---

## 🗺️ Roadmap

- [ ] Add email notifications
- [ ] Implement user authentication
- [ ] Add mobile app support
- [ ] Create admin analytics dashboard
- [ ] Add export to PDF feature
- [ ] Implement shift management
- [ ] Add multi-language support

---

## ⚠️ Important Notes for GitHub Users

### If You Clone This Repository:

1. **Don't use the example n8n URL** - You must set up your own n8n instance
2. **Create your own Google Sheet** - Structure it according to the documentation
3. **Set up Streamlit Secrets** - Never commit actual credentials
4. **Import n8n workflows** - Found in `n8n_workflows/` folder
5. **Customize for your needs** - Departments, rates, policies, etc.

### Security Reminder:

**This repository is PUBLIC**. Anyone can see the code. Make sure:
- ✅ No real URLs in code
- ✅ No credentials in files
- ✅ Use secrets/environment variables
- ✅ `.gitignore` is properly configured

---

**⭐ If you find this useful, please star the repository!**

---

*Last Updated: December 2025*
