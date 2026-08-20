# ==========================================
# CareerPilot AI Configuration
# ==========================================

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000"
API_BASE_URL = f"{BACKEND_URL}/api/v1"

# API Endpoints
LOGIN_ENDPOINT = "/auth/login"
REGISTER_ENDPOINT = "/auth/register"
CURRENT_USER_ENDPOINT = "/users/me"

# Request Timeout (seconds)
REQUEST_TIMEOUT = 30

# Application
APP_NAME = "CareerPilot AI"
APP_VERSION = "1.0.0"

# Session Keys
TOKEN_KEY = "access_token"
USER_KEY = "current_user"
LOGGED_IN_KEY = "logged_in"