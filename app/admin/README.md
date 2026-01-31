# Portfolio Admin Panel

A secure, server-rendered admin panel for managing your portfolio data.

## Features

- 🔐 **Session-based Authentication** - Secure login with username/password
- 👤 **Personal Info Management** - Update your profile, bio, and social links
- 🎯 **Skills Management** - Add/delete skills with categories and proficiency levels
- 📜 **Certifications** - Manage your professional certifications
- 💼 **Projects** - Showcase personal and professional projects
- 👔 **Experience** - Document your work history and learnings
- 📧 **Contact Requests** - View messages from visitors (read-only)

## Tech Stack

- **FastAPI** - Web framework
- **Jinja2** - Server-side templating
- **Tailwind CSS** (CDN) - Styling
- **httpx** - Async HTTP client for API calls
- **itsdangerous** - Secure session tokens

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Add the following to your `.env` file:

```env
# Admin Panel Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password

# Session Security
SECRET_KEY=your-super-secret-key-change-in-production

# API Base URL (for internal API calls)
API_BASE_URL=http://localhost:8000
```

### 3. Run the Server

```bash
uvicorn app.main:app --reload
```

### 4. Access the Admin Panel

Open your browser and navigate to:

- **Login Page**: http://localhost:8000/admin/login
- **Dashboard**: http://localhost:8000/admin/dashboard (requires login)

## Admin Routes

| Route | Description |
|-------|-------------|
| `/admin/login` | Login page |
| `/admin/logout` | Logout (clears session) |
| `/admin/dashboard` | Main dashboard |
| `/admin/personal` | Manage personal info |
| `/admin/skills` | Manage skills |
| `/admin/certifications` | Manage certifications |
| `/admin/projects` | Manage projects |
| `/admin/experience` | Manage work experience |
| `/admin/contacts` | View contact requests |

## Architecture

```
app/admin/
├── __init__.py       # Module initialization
├── auth.py           # Authentication logic (session-based)
├── routes.py         # Admin panel routes
├── services.py       # API service layer (calls existing APIs)
├── templates/        # Jinja2 HTML templates
│   ├── base.html
│   ├── layout.html
│   ├── login.html
│   ├── dashboard.html
│   ├── personal.html
│   ├── skills.html
│   ├── certifications.html
│   ├── projects.html
│   ├── experience.html
│   └── contacts.html
└── static/           # Static assets (CSS, JS)
    └── admin.css
```

## Security Notes

1. **Change default credentials** in production
2. **Use a strong SECRET_KEY** for session security
3. **Use HTTPS** in production
4. Session tokens expire after 24 hours
5. All admin routes require authentication

## API Integration

The admin panel **never accesses the database directly**. It calls the existing REST APIs:

- `POST/PUT /api/v1/personal`
- `GET/POST/DELETE /api/v1/skills`
- `GET/POST/DELETE /api/v1/certifications`
- `GET/POST/DELETE /api/v1/projects`
- `GET/POST/DELETE /api/v1/experience`
- `GET /api/v1/contact` (read-only)

This ensures:
- Same validation rules
- Same data shape
- Zero code duplication
- Future-proof versioning

## Future Enhancements (v2)

- [ ] JWT authentication
- [ ] Role-based access control
- [ ] OAuth (Google/GitHub)
- [ ] File upload for images
- [ ] Edit/Update functionality for all entities
- [ ] Search and filtering
- [ ] Pagination for lists
