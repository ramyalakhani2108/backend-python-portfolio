-- Portfolio Database Schema
-- PostgreSQL v14+
-- Generated for Portfolio Backend v1

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- 1. PERSONAL INFO TABLE
-- ============================================
CREATE TABLE personal_info (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    place VARCHAR(255),
    country VARCHAR(100),
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50),
    bio TEXT,
    profile_image_url VARCHAR(500),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for auto-updating updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_personal_info_updated_at
    BEFORE UPDATE ON personal_info
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 2. TAGS TABLE
-- ============================================
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    label VARCHAR(100) NOT NULL UNIQUE
);

-- ============================================
-- 3. SKILLS TABLE
-- ============================================
CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('backend', 'frontend', 'devops', 'other')),
    proficiency_level INTEGER CHECK (proficiency_level >= 1 AND proficiency_level <= 100),
    is_hobby BOOLEAN DEFAULT FALSE
);

CREATE INDEX ix_skills_category ON skills(category);

-- ============================================
-- 4. CERTIFICATIONS TABLE
-- ============================================
CREATE TABLE certifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    issuer VARCHAR(255) NOT NULL,
    issue_date TIMESTAMP,
    credential_url VARCHAR(500)
);

-- ============================================
-- 5. PROJECTS TABLE
-- ============================================
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    tech_stack VARCHAR[] DEFAULT '{}',
    github_url VARCHAR(500),
    live_url VARCHAR(500),
    project_type VARCHAR(50) DEFAULT 'personal' CHECK (project_type IN ('personal', 'professional')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_projects_project_type ON projects(project_type);

-- ============================================
-- 6. EXPERIENCE TABLE
-- ============================================
CREATE TABLE experience (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    description TEXT,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    learnings TEXT
);

CREATE INDEX ix_experience_start_date ON experience(start_date DESC);

-- ============================================
-- 7. CONTACT REQUESTS TABLE
-- ============================================
CREATE TABLE contact_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_contact_requests_created_at ON contact_requests(created_at DESC);

-- ============================================
-- 8. AI CONTEXT LOGS TABLE
-- ============================================
CREATE TABLE ai_context_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_question TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    used_context JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_ai_context_logs_created_at ON ai_context_logs(created_at DESC);

-- ============================================
-- SAMPLE DATA (Optional - for testing)
-- ============================================

-- Insert sample personal info
-- INSERT INTO personal_info (name, place, country, email, bio)
-- VALUES (
--     'Ramya',
--     'Bangalore',
--     'India',
--     'ramya@example.com',
--     'Full-stack developer passionate about building scalable applications with modern technologies.'
-- );

-- Insert sample skills
-- INSERT INTO skills (name, category, proficiency_level, is_hobby) VALUES
-- ('Python', 'backend', 90, false),
-- ('FastAPI', 'backend', 85, false),
-- ('Flutter', 'frontend', 80, false),
-- ('PostgreSQL', 'backend', 85, false),
-- ('Docker', 'devops', 75, false),
-- ('AWS', 'devops', 70, false);

-- Insert sample certifications
-- INSERT INTO certifications (title, issuer, issue_date, credential_url) VALUES
-- ('AWS Solutions Architect', 'Amazon Web Services', '2024-06-15', 'https://aws.amazon.com/verification/12345');

-- Insert sample projects
-- INSERT INTO projects (title, description, tech_stack, github_url, project_type) VALUES
-- ('Portfolio App', 'Personal portfolio application with AI assistant', ARRAY['Flutter', 'FastAPI', 'PostgreSQL', 'Gemini AI'], 'https://github.com/ramya/portfolio', 'personal');
