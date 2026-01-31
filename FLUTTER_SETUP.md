# Portfolio Backend - Running Instructions

## Server is now configured to accept connections from Flutter app

### Current Configuration:
- **Host**: 0.0.0.0 (accessible from network)
- **Port**: 8000
- **CORS**: Enabled for all origins (["*"])

### To start the server:
```bash
cd D:\portfolio-application\backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Find your local IP address:
```powershell
# Windows PowerShell
Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.*' }
```

Or simply check in Command Prompt:
```cmd
ipconfig
```
Look for "IPv4 Address" under your active network adapter (Wi-Fi or Ethernet).

### Flutter App Configuration:

Update your Flutter app's API base URL to use your machine's local IP address:

**For Android Emulator:**
- Use `http://10.0.2.2:8000` (emulator's special alias for host machine)

**For Physical Device or iOS Simulator:**
- Use `http://YOUR_LOCAL_IP:8000` (e.g., `http://192.168.1.100:8000`)

**For Web:**
- Use `http://localhost:8000`

### Testing the connection:
1. Make sure both devices are on the same WiFi network
2. Open your Flutter app
3. The app should now connect to the backend API

### API Endpoints Available:
- Health check: http://YOUR_IP:8000/health
- Admin panel: http://YOUR_IP:8000/admin/login
- API docs: http://YOUR_IP:8000/docs
- API v1: http://YOUR_IP:8000/api/v1/

### Admin Panel Credentials:
- Username: admin  
- Password: adminn@gmail12312

### Notes:
- Make sure Windows Firewall allows incoming connections on port 8000
- The server logs will show all incoming requests
- CORS is currently set to allow all origins for development
