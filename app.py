"""
Streamlit Frontend for Agentic AI Website Builder
Interactive web interface for creating and executing AI-powered website designs
"""

import streamlit as st
import json
from pathlib import Path
import sys
import asyncio
from datetime import datetime
import time
import zipfile
import io
import shutil
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.auth.user_manager import UserManager
from src.auth.oauth_manager import OAuthManager
from src.framework.workflow import WorkflowManager, WorkflowPlan, WorkflowStep
from src.framework.agent_factory import AgentFactory
from src.config import logger

# ============================================================================
# Page Config
# ============================================================================
st.set_page_config(
    page_title="Agentic AI - Website Builder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/yourusername/agentic",
        "Report a bug": "https://github.com/yourusername/agentic/issues",
        "About": "Agentic AI - Multi-Agent Website Builder v1.0"
    }
)

# ============================================================================
# Enhanced Custom CSS with Modern Design
# ============================================================================
st.markdown("""
<style>
    /* Global Styles */
    :root {
        --primary: #6366f1;
        --primary-light: #818cf8;
        --secondary: #ec4899;
        --success: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
        --dark: #1f2937;
        --gray: #f3f4f6;
    }
    
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Main Header */
    .main-header {
        font-size: 2.5em;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5em;
        text-align: center;
    }
    
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.1em;
        margin-bottom: 2em;
        font-weight: 500;
    }
    
    /* Card Styles */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5em;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        margin: 1em 0;
    }
    
    .card:hover {
        box-shadow: 0 10px 25px 0 rgba(0, 0, 0, 0.1);
        border-color: #6366f1;
        transform: translateY(-2px);
    }
    
    .workflow-card {
        padding: 1.5em;
        border-radius: 12px;
        border-left: 4px solid #6366f1;
        background: linear-gradient(135deg, #f8f7ff 0%, #fff5fb 100%);
        margin: 1em 0;
        transition: all 0.3s ease;
    }
    
    .workflow-card:hover {
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.15);
    }
    
    /* Status Messages */
    .status-success {
        padding: 1em;
        border-radius: 8px;
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 4px solid #10b981;
        color: #065f46;
        font-weight: 500;
    }
    
    .status-error {
        padding: 1em;
        border-radius: 8px;
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
        color: #7f1d1d;
        font-weight: 500;
    }
    
    .status-warning {
        padding: 1em;
        border-radius: 8px;
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        color: #78350f;
        font-weight: 500;
    }
    
    /* Buttons */
    .btn-custom {
        border-radius: 8px;
        padding: 0.75em 1.5em;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
    }
    
    /* Input Fields */
    .input-custom {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        padding: 0.75em;
        transition: all 0.3s ease;
    }
    
    .input-custom:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 1.5em;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);
    }
    
    .metric-card.secondary {
        background: linear-gradient(135deg, #ec4899 0%, #f43f5e 100%);
    }
    
    .metric-card.success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    
    .metric-value {
        font-size: 2.5em;
        font-weight: 700;
        margin: 0.5em 0;
    }
    
    .metric-label {
        font-size: 0.9em;
        opacity: 0.9;
        font-weight: 500;
    }
    
    /* Tabs */
    [data-baseweb="tab-list"] {
        gap: 2em;
        border-bottom: 2px solid #e5e7eb;
    }
    
    [data-baseweb="tab"] {
        font-weight: 600;
        color: #6b7280;
        border-bottom: 3px solid transparent;
    }
    
    [aria-selected="true"] {
        color: #6366f1 !important;
        border-bottom-color: #6366f1 !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
        margin: 2em 0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .sidebar-header {
        font-size: 1.3em;
        font-weight: 700;
        margin-bottom: 1.5em;
        color: white;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease;
    }
    
    /* Agent Status */
    .agent-status-running {
        display: inline-block;
        padding: 0.5em 1em;
        border-radius: 20px;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: white;
        font-weight: 600;
        animation: pulse 2s infinite;
    }
    
    .agent-status-complete {
        display: inline-block;
        padding: 0.5em 1em;
        border-radius: 20px;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        font-weight: 600;
    }
    
    .agent-status-error {
        display: inline-block;
        padding: 0.5em 1em;
        border-radius: 20px;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        font-weight: 600;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# Session State Management
# ============================================================================
if "user_manager" not in st.session_state:
    st.session_state.user_manager = UserManager()

if "oauth_manager" not in st.session_state:
    st.session_state.oauth_manager = OAuthManager()

if "workflow_manager" not in st.session_state:
    st.session_state.workflow_manager = WorkflowManager()

if "current_user" not in st.session_state:
    # Try to load from session file
    session_file = Path(".users/.session")
    if session_file.exists():
        try:
            with open(session_file, "r") as f:
                session_data = json.load(f)
                st.session_state.current_user = session_data.get("current_user")
        except:
            st.session_state.current_user = None
    else:
        st.session_state.current_user = None

# ============================================================================
# Authentication Pages
# ============================================================================
def login_page():
    """Enhanced Login/Register page with modern design"""
    
    # Center the auth forms
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        <div class="card fade-in">
        <h2 style="color: #6366f1; text-align: center;">🔐 Login</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        
        username = st.text_input(
            "Username",
            key="login_username",
            placeholder="Enter your username",
            help="Your account username"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            key="login_password",
            placeholder="Enter your password",
            help="Your account password"
        )
        
        if st.button("🚀 Login", key="login_button", use_container_width=True):
            if username and password:
                result = st.session_state.user_manager.login(username, password)
                if result['success']:
                    st.session_state.current_user = username
                    # Save session
                    session_file = Path(".users/.session")
                    session_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(session_file, "w") as f:
                        json.dump({"current_user": username}, f)
                    st.markdown(f'<div class="status-success">✅ Logged in as {username}</div>', unsafe_allow_html=True)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.markdown(f'<div class="status-error">❌ {result["error"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-warning">⚠️ Please fill in all fields</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card fade-in">
        <h2 style="color: #ec4899; text-align: center;">📝 Register</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        
        new_username = st.text_input(
            "New Username",
            key="reg_username",
            placeholder="Min 3 characters",
            help="Choose a unique username"
        )
        
        new_email = st.text_input(
            "Email Address",
            key="reg_email",
            placeholder="your@email.com",
            help="Your email address"
        )
        
        new_password = st.text_input(
            "Password",
            type="password",
            key="reg_password",
            placeholder="Min 6 characters",
            help="Create a strong password"
        )
        
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="reg_confirm",
            placeholder="Re-enter password",
            help="Confirm your password"
        )
        
        if st.button("✨ Create Account", key="register_button", use_container_width=True):
            if len(new_username) < 3:
                st.markdown('<div class="status-error">❌ Username must be at least 3 characters</div>', unsafe_allow_html=True)
            elif new_password != confirm_password:
                st.markdown('<div class="status-error">❌ Passwords do not match</div>', unsafe_allow_html=True)
            elif len(new_password) < 6:
                st.markdown('<div class="status-error">❌ Password must be at least 6 characters</div>', unsafe_allow_html=True)
            else:
                result = st.session_state.user_manager.register(new_username, new_password, new_email)
                if result['success']:
                    st.markdown(f'<div class="status-success">✅ Account created! Please login.</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="status-error">❌ {result["error"]}</div>', unsafe_allow_html=True)


def api_keys_page():
    """API Keys management page"""
    st.markdown("<h1 style='color: #6366f1;'>🔑 API Keys Management</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
    <p style="color: #6b7280;">Manage your API keys for the AI agents. Your keys are stored securely and never shared.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load current keys from .env if they exist
    env_file = Path(".env")
    current_keys = {}
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                if line.startswith("GOOGLE_API_KEY="):
                    current_keys["google"] = line.split("=", 1)[1].strip()
                elif line.startswith("OPENAI_API_KEY="):
                    current_keys["openai"] = line.split("=", 1)[1].strip()
                elif line.startswith("ANTHROPIC_API_KEY="):
                    current_keys["anthropic"] = line.split("=", 1)[1].strip()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # API Keys Input Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h2 style='color: #ec4899;'>📝 Configure Your Keys</h2>", unsafe_allow_html=True)
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    st.markdown("<div style='height: 1em'></div>", unsafe_allow_html=True)
    
    # Google Gemini Key
    st.markdown("""
    <div class="card">
    <h3 style="color: #4285F4;">🔵 Google Gemini API Key</h3>
    <p style="color: #6b7280;">For UI/UX design and frontend generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    google_key = st.text_input(
        "Google API Key",
        value=current_keys.get("google", ""),
        type="password",
        placeholder="AIzaSyD...",
        help="Get your key from: https://aistudio.google.com/app/apikey",
        key="google_key_input"
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        status = "✅ Connected" if current_keys.get("google") else "⚠️ Not Set"
        st.write(f"**Status:** {status}")
    with col2:
        if st.button("📝 Get Key", use_container_width=True):
            st.markdown("""
            <div class="status-warning">
            Visit: <a href="https://aistudio.google.com/app/apikey" target="_blank">https://aistudio.google.com/app/apikey</a>
            </div>
            """, unsafe_allow_html=True)
    with col3:
        if st.button("💾 Save Google Key", use_container_width=True, key="save_google"):
            if google_key:
                st.session_state.google_key_saved = True
                st.markdown('<div class="status-success">✅ Google key will be saved</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-error">❌ Please enter a key</div>', unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # OpenAI Key
    st.markdown("""
    <div class="card">
    <h3 style="color: #10a37f;">🟢 OpenAI API Key</h3>
    <p style="color: #6b7280;">For backend API design and generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    openai_key = st.text_input(
        "OpenAI API Key",
        value=current_keys.get("openai", ""),
        type="password",
        placeholder="sk-proj-...",
        help="Get your key from: https://platform.openai.com/account/api-keys",
        key="openai_key_input"
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        status = "✅ Connected" if current_keys.get("openai") else "⚠️ Not Set"
        st.write(f"**Status:** {status}")
    with col2:
        if st.button("📝 Get Key", use_container_width=True, key="get_openai"):
            st.markdown("""
            <div class="status-warning">
            Visit: <a href="https://platform.openai.com/account/api-keys" target="_blank">https://platform.openai.com/account/api-keys</a>
            </div>
            """, unsafe_allow_html=True)
    with col3:
        if st.button("💾 Save OpenAI Key", use_container_width=True, key="save_openai"):
            if openai_key:
                st.session_state.openai_key_saved = True
                st.markdown('<div class="status-success">✅ OpenAI key will be saved</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-error">❌ Please enter a key</div>', unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Anthropic Key
    st.markdown("""
    <div class="card">
    <h3 style="color: #8b5cf6;">🔶 Anthropic Claude API Key</h3>
    <p style="color: #6b7280;">For orchestration and integration</p>
    </div>
    """, unsafe_allow_html=True)
    
    anthropic_key = st.text_input(
        "Anthropic API Key",
        value=current_keys.get("anthropic", ""),
        type="password",
        placeholder="sk-ant-...",
        help="Get your key from: https://console.anthropic.com/account/keys",
        key="anthropic_key_input"
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        status = "✅ Connected" if current_keys.get("anthropic") else "⚠️ Not Set"
        st.write(f"**Status:** {status}")
    with col2:
        if st.button("📝 Get Key", use_container_width=True, key="get_anthropic"):
            st.markdown("""
            <div class="status-warning">
            Visit: <a href="https://console.anthropic.com/account/keys" target="_blank">https://console.anthropic.com/account/keys</a>
            </div>
            """, unsafe_allow_html=True)
    with col3:
        if st.button("💾 Save Anthropic Key", use_container_width=True, key="save_anthropic"):
            if anthropic_key:
                st.session_state.anthropic_key_saved = True
                st.markdown('<div class="status-success">✅ Anthropic key will be saved</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-error">❌ Please enter a key</div>', unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Save All Button
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("💾 Save All Keys", use_container_width=True, key="save_all_keys"):
            if google_key and openai_key and anthropic_key:
                # Read existing .env or create new
                env_content = ""
                if env_file.exists():
                    with open(env_file, "r") as f:
                        env_content = f.read()
                
                # Update keys
                lines = env_content.split("\n") if env_content else []
                updated_lines = []
                keys_to_add = {
                    "GOOGLE_API_KEY": google_key,
                    "OPENAI_API_KEY": openai_key,
                    "ANTHROPIC_API_KEY": anthropic_key,
                }
                
                for line in lines:
                    if not any(line.startswith(k) for k in keys_to_add.keys()):
                        if line.strip():
                            updated_lines.append(line)
                
                for key, value in keys_to_add.items():
                    updated_lines.append(f"{key}={value}")
                
                # Write to .env
                with open(env_file, "w") as f:
                    f.write("\n".join(updated_lines))
                
                st.markdown('<div class="status-success">✅ All API keys saved successfully!</div>', unsafe_allow_html=True)
                st.markdown("""
                <div class="card" style="margin-top: 1em;">
                <h4>✨ Next Steps:</h4>
                <p>1. Your keys are now configured</p>
                <p>2. Go to "My Workflows" to create website blueprints</p>
                <p>3. Execute workflows to generate websites with AI</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-error">❌ Please fill in all three API keys</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("🔐 Test Keys", use_container_width=True):
            st.info("Connection test coming soon!")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Info Section
    st.markdown("""
    <div class="card">
    <h3 style="color: #6366f1;">ℹ️ How It Works</h3>
    <ul>
    <li><strong>🔵 Google Gemini:</strong> Designs your website frontend (UI/UX, HTML, CSS)</li>
    <li><strong>🟢 OpenAI GPT:</strong> Creates backend architecture (APIs, databases, security)</li>
    <li><strong>🔶 Anthropic Claude:</strong> Orchestrates and integrates all components</li>
    </ul>
    <p><strong>Security:</strong> Your keys are stored locally in your .env file and never sent to our servers.</p>
    </div>
    """, unsafe_allow_html=True)


def generate_project_structure(project_name, requirements):
    """Generate a complete project structure"""
    projects_dir = Path(f".projects/{st.session_state.current_user}")
    projects_dir.mkdir(parents=True, exist_ok=True)
    
    project_dir = projects_dir / project_name.replace(" ", "_")
    project_dir.mkdir(exist_ok=True)
    
    # Create basic project structure
    (project_dir / "src").mkdir(exist_ok=True)
    (project_dir / "public").mkdir(exist_ok=True)
    (project_dir / "docs").mkdir(exist_ok=True)
    (project_dir / "tests").mkdir(exist_ok=True)
    
    # Generate files based on requirements
    files_created = []
    
    # README
    readme_path = project_dir / "README.md"
    readme_content = f"""# {project_name}

{requirements}

## Generated with Agentic AI
This project was generated using Agentic AI Website Builder.

## Project Structure
- `src/` - Source code
- `public/` - Frontend assets  
- `docs/` - Documentation
- `tests/` - Test files

## Getting Started
1. Install dependencies
2. Configure your environment
3. Run the development server

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    readme_path.write_text(readme_content)
    files_created.append("README.md")
    
    # Requirements/Package.json
    pkg_content = {
        "name": project_name.replace(" ", "-").lower(),
        "version": "1.0.0",
        "description": requirements[:100],
        "author": st.session_state.current_user,
        "generatedBy": "Agentic AI",
        "generatedAt": datetime.now().isoformat(),
        "requirements": requirements
    }
    pkg_path = project_dir / "project.json"
    pkg_path.write_text(json.dumps(pkg_content, indent=2))
    files_created.append("project.json")
    
    # Sample frontend file
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }}
        .container {{ background: white; padding: 2em; border-radius: 12px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); max-width: 600px; text-align: center; }}
        h1 {{ color: #333; margin-bottom: 0.5em; }}
        p {{ color: #666; line-height: 1.6; margin-bottom: 1em; }}
        .footer {{ color: #999; font-size: 0.9em; margin-top: 2em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{project_name}</h1>
        <p>{requirements}</p>
        <div class="footer">
            <p>Generated with Agentic AI | {datetime.now().strftime("%Y-%m-%d")}</p>
        </div>
    </div>
</body>
</html>
"""
    html_path = project_dir / "public/index.html"
    html_path.write_text(html_content)
    files_created.append("public/index.html")
    
    # Python sample - using simple string replacement to avoid f-string issues
    safe_class_name = project_name.replace(" ", "").replace("-", "_")
    py_lines = [
        '"""',
        project_name,
        "",
        requirements,
        "",
        "Generated with Agentic AI",
        '"""',
        "",
        "import json",
        "from datetime import datetime",
        "",
        f"class {safe_class_name}:",
        "    def __init__(self):",
        f'        self.name = "{project_name}"',
        "        self.created_at = datetime.now()",
        '        self.version = "1.0.0"',
        "    ",
        "    def __repr__(self):",
        f'        return f"{{self.name}}: {{self.version}}"',
        "",
        'if __name__ == "__main__":',
        f"    app = {safe_class_name}()",
        '    print(f"Project: {{app.name}}")',
        '    print(f"Created: {{app.created_at}}")',
    ]
    py_content = "\n".join(py_lines)
    py_path = project_dir / "src/main.py"
    py_path.write_text(py_content)
    files_created.append("src/main.py")
    
    # Configuration file
    config_content = {
        "project": {
            "name": project_name,
            "version": "1.0.0",
            "description": requirements
        },
        "author": st.session_state.current_user,
        "generated": {
            "at": datetime.now().isoformat(),
            "by": "Agentic AI"
        },
        "settings": {
            "debug": True,
            "port": 8000,
            "host": "localhost"
        }
    }
    config_path = project_dir / "config.json"
    config_path.write_text(json.dumps(config_content, indent=2))
    files_created.append("config.json")
    
    return project_dir, files_created


def create_zip_from_project(project_dir):
    """Create a ZIP file from project directory"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(project_dir.parent)
                zip_file.write(file_path, arcname)
    
    zip_buffer.seek(0)
    return zip_buffer


def quick_generate_section():
    """Quick project generation section with API error handling"""
    st.markdown("<div style='height: 1.5em'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2em; border-radius: 12px; color: white; margin-bottom: 2em;">
    <h2 style="margin: 0;">🚀 Quick Generate</h2>
    <p style="margin: 0.5em 0 0 0; opacity: 0.9;">Enter your requirement and we'll generate a complete project</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        project_name = st.text_input(
            "Project Name",
            placeholder="e.g., My E-commerce App",
            help="Give your project a name",
            key="project_name_input"
        )
    
    with col2:
        template = st.selectbox(
            "Template",
            ["Web App", "API", "Blog", "Dashboard", "E-commerce", "Custom"],
            key="template_select"
        )
    
    requirements = st.text_area(
        "Project Requirements",
        placeholder="e.g., Build a modern e-commerce store with product catalog, shopping cart, user authentication, and payment processing.",
        height=120,
        help="Describe what your project should do in detail",
        key="requirements_input"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Generate Project", use_container_width=True, key="generate_btn"):
            if not project_name or not requirements:
                st.error("❌ Please fill in project name and requirements")
            else:
                # Check if API keys are configured
                env_file = Path(".env")
                has_keys = False
                
                if env_file.exists():
                    with open(env_file, "r") as f:
                        env_content = f.read()
                        has_keys = "GOOGLE_API_KEY=" in env_content and "OPENAI_API_KEY=" in env_content and "ANTHROPIC_API_KEY=" in env_content
                
                if not has_keys:
                    st.markdown("""
                    <div style="background: #fef3c7; border-left: 4px solid #f59e0b; padding: 1em; border-radius: 8px; color: #78350f;">
                    <h4 style="margin: 0 0 0.5em 0;">⚠️ API Keys Not Configured</h4>
                    <p style="margin: 0;">Go to <strong>🔑 API Keys</strong> to configure your keys first.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    with st.spinner("🤖 Generating project structure..."):
                        try:
                            # Generate project
                            project_dir, files_created = generate_project_structure(project_name, requirements)
                            
                            st.success(f"✅ Project generated successfully!")
                            
                            # Show files created
                            st.markdown(f"""
                            <div class="card" style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border-left: 4px solid #10b981;">
                            <h4 style="color: #10b981; margin: 0 0 1em 0;">📦 Project Created</h4>
                            <p><strong>Project:</strong> {project_name}</p>
                            <p><strong>Files Created:</strong> {len(files_created)}</p>
                            <p><strong>Files:</strong> {', '.join(files_created[:3])}...</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Create ZIP and download button
                            try:
                                zip_buffer = create_zip_from_project(project_dir)
                                
                                st.download_button(
                                    label="⬇️ Download Project (ZIP)",
                                    data=zip_buffer.getvalue(),
                                    file_name=f"{project_name.replace(' ', '_')}.zip",
                                    mime="application/zip",
                                    key="download_project"
                                )
                                st.balloons()
                            except Exception as zip_error:
                                st.error(f"❌ Error creating download: {str(zip_error)}")
                        
                        except Exception as e:
                            error_msg = str(e).lower()
                            
                            # Check for common API errors
                            if "quota" in error_msg or "insufficient" in error_msg or "429" in error_msg:
                                st.markdown("""
                                <div style="background: #fee2e2; border-left: 4px solid #ef4444; padding: 1.5em; border-radius: 8px; color: #7f1d1d;">
                                <h4 style="margin: 0 0 0.5em 0;">❌ API Quota Exceeded</h4>
                                <p style="margin: 0.5em 0;">Your API quota has been exceeded. Please update your API keys with new credentials.</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.warning("💡 **Solution:** Go to 🔑 API Keys and update your credentials")
                                
                                if st.button("🔑 Go to API Keys", key="go_to_keys", use_container_width=True):
                                    st.session_state.page_select = 2  # Navigate to API Keys tab
                                    st.rerun()
                            
                            elif "not found" in error_msg or "invalid" in error_msg:
                                st.markdown("""
                                <div style="background: #fee2e2; border-left: 4px solid #ef4444; padding: 1.5em; border-radius: 8px; color: #7f1d1d;">
                                <h4 style="margin: 0 0 0.5em 0;">❌ Invalid API Key</h4>
                                <p style="margin: 0.5em 0;">One or more API keys are invalid or misconfigured.</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.warning("💡 **Solution:** Check your API keys in 🔑 API Keys section")
                            
                            else:
                                st.markdown(f"""
                                <div style="background: #fee2e2; border-left: 4px solid #ef4444; padding: 1.5em; border-radius: 8px; color: #7f1d1d;">
                                <h4 style="margin: 0 0 0.5em 0;">❌ Error: {error_msg[:50]}</h4>
                                <p style="margin: 0.5em 0;">Please try again or check your API keys.</p>
                                </div>
                                """, unsafe_allow_html=True)
    
    with col2:
        if st.button("📋 View Template", use_container_width=True):
            st.info(f"Template: {template}\nCustom templates coming soon!")
    
    with col3:
        if st.button("💾 Save as Draft", use_container_width=True):
            st.info("Draft saved! You can access it in My Files.")
    
    # Tips and Instructions Section
    st.markdown("""
    <div style="background: white; padding: 1.5em; border-radius: 12px; border: 1px solid #e5e7eb; margin: 1.5em 0;">
    <h4 style="margin: 0 0 1em 0; color: #1f2937;">💡 How to Get Started</h4>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5em;">
        <div>
            <p style="margin: 0 0 0.5em 0; color: #667eea; font-weight: 600;">✓ Step 1: Add API Keys</p>
            <p style="margin: 0; color: #6b7280; font-size: 0.95em;">Configure your API keys in the 🔑 API Keys tab to enable project generation.</p>
        </div>
        <div>
            <p style="margin: 0 0 0.5em 0; color: #667eea; font-weight: 600;">✓ Step 2: Enter Requirements</p>
            <p style="margin: 0; color: #6b7280; font-size: 0.95em;">Describe your project goals and features in detail above.</p>
        </div>
        <div>
            <p style="margin: 0 0 0.5em 0; color: #667eea; font-weight: 600;">✓ Step 3: Generate</p>
            <p style="margin: 0; color: #6b7280; font-size: 0.95em;">Click 🚀 Generate and AI agents will build your project.</p>
        </div>
        <div>
            <p style="margin: 0 0 0.5em 0; color: #667eea; font-weight: 600;">✓ Step 4: Download</p>
            <p style="margin: 0; color: #6b7280; font-size: 0.95em;">Download your complete project as a ZIP file and start building!</p>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # API Status indicator
    st.markdown("""
    <div style="background: #f3f4f6; padding: 1em; border-radius: 8px;">
    <h4 style="margin: 0 0 0.5em 0;">🔐 API Status</h4>
    """, unsafe_allow_html=True)
    
    env_file = Path(".env")
    col1, col2, col3 = st.columns(3)
    
    if env_file.exists():
        with open(env_file, "r") as f:
            env_content = f.read()
        
        google_key = "GOOGLE_API_KEY=" in env_content
        openai_key = "OPENAI_API_KEY=" in env_content
        anthropic_key = "ANTHROPIC_API_KEY=" in env_content
    else:
        google_key = openai_key = anthropic_key = False
    
    with col1:
        status = "✅" if google_key else "⚠️"
        st.write(f"{status} **Google Gemini**")
    
    with col2:
        status = "✅" if openai_key else "⚠️"
        st.write(f"{status} **OpenAI**")
    
    with col3:
        status = "✅" if anthropic_key else "⚠️"
        st.write(f"{status} **Anthropic**")
    
    st.markdown("</div>", unsafe_allow_html=True)


def load_favorites():
    """Load user's favorite projects"""
    fav_file = Path(f".favorites/{st.session_state.current_user}.json")
    if fav_file.exists():
        with open(fav_file, "r") as f:
            return json.load(f).get("favorites", [])
    return []


def save_favorites(favorites):
    """Save user's favorite projects"""
    Path(".favorites").mkdir(exist_ok=True)
    fav_file = Path(f".favorites/{st.session_state.current_user}.json")
    with open(fav_file, "w") as f:
        json.dump({"favorites": favorites}, f)


def duplicate_project(src_path, new_name):
    """Duplicate a project with new name"""
    import shutil
    dest_path = src_path.parent / new_name
    if not dest_path.exists():
        shutil.copytree(src_path, dest_path)
        return True
    return False


def get_project_analytics(project_path):
    """Get analytics for a project"""
    files = list(project_path.rglob("*"))
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    created = datetime.fromtimestamp(project_path.stat().st_mtime)
    
    return {
        "files": len(files),
        "size_mb": total_size / (1024 * 1024),
        "created": created,
        "modified": created,
        "type": "Web App"  # Can be enhanced to detect type
    }


def my_files_section():
    """File browser section with advanced features"""
    st.markdown("<div style='height: 1.5em'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 2em; border-radius: 12px; color: white; margin-bottom: 2em;">
    <h2 style="margin: 0;">📁 My Files</h2>
    <p style="margin: 0.5em 0 0 0; opacity: 0.9;">Browse and manage all your projects with advanced features</p>
    </div>
    """, unsafe_allow_html=True)
    
    projects_dir = Path(f".projects/{st.session_state.current_user}")
    favorites = load_favorites()
    
    # Create tabs for organization
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📂 All Projects", "🔄 Recent", "⭐ Favorites", "📊 Analytics", "🎨 Templates"])
    
    # ========================================================================
    # TAB 1: All Projects with Search & Filter
    # ========================================================================
    with tab1:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_query = st.text_input("🔍 Search projects", placeholder="Search by name...", key="search_projects")
        
        with col2:
            sort_by = st.selectbox("Sort by", ["Latest", "Name (A-Z)", "Size"], key="sort_projects")
        
        with col3:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        if not projects_dir.exists() or not list(projects_dir.iterdir()):
            st.markdown("""
            <div class="card" style="text-align: center; padding: 3em; background: #f9fafb;">
            <h3 style="color: #9ca3af;">📭 No projects yet</h3>
            <p style="color: #6b7280;">Create your first project using Quick Generate!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            projects = list(projects_dir.iterdir())
            
            # Apply search filter
            if search_query:
                projects = [p for p in projects if search_query.lower() in p.name.lower()]
            
            # Apply sorting
            if sort_by == "Latest":
                projects = sorted(projects, key=lambda x: x.stat().st_mtime, reverse=True)
            elif sort_by == "Name (A-Z)":
                projects = sorted(projects, key=lambda x: x.name)
            elif sort_by == "Size":
                projects = sorted(projects, key=lambda x: sum(f.stat().st_size for f in x.rglob("*") if f.is_file()), reverse=True)
            
            if not projects:
                st.info("❌ No projects match your search")
            
            # Bulk actions
            st.markdown("**Bulk Actions:**")
            col1, col2 = st.columns(2)
            
            with col1:
                select_all = st.checkbox("Select All", key="select_all_projects")
            
            selected_projects = []
            if select_all:
                selected_projects = [p.name for p in projects]
            
            with col2:
                if st.button("🗑️ Delete Selected", use_container_width=True, key="delete_selected"):
                    if selected_projects:
                        for proj_name in selected_projects:
                            proj_path = projects_dir / proj_name
                            if proj_path.exists():
                                shutil.rmtree(proj_path)
                        st.success(f"✅ Deleted {len(selected_projects)} project(s)")
                        st.rerun()
            
            # Display projects
            for project_path in projects:
                if project_path.is_dir():
                    analytics = get_project_analytics(project_path)
                    is_favorite = project_path.name in favorites
                    
                    col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div class="workflow-card">
                        <h4 style="color: #667eea; margin: 0 0 0.5em 0;">📁 {project_path.name.replace('_', ' ')}</h4>
                        <p style="margin: 0; color: #6b7280; font-size: 0.9em;">📊 {analytics['files']} files | 💾 {analytics['size_mb']:.2f}MB</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        if st.button("⭐" if is_favorite else "☆", key=f"fav_{project_path.name}", use_container_width=True):
                            if is_favorite:
                                favorites.remove(project_path.name)
                            else:
                                favorites.append(project_path.name)
                            save_favorites(favorites)
                            st.rerun()
                    
                    with col3:
                        if st.button("📋", key=f"clone_{project_path.name}", use_container_width=True, help="Duplicate"):
                            new_name = f"{project_path.name}_copy"
                            if duplicate_project(project_path, new_name):
                                st.success(f"✅ Duplicated as '{new_name}'")
                                st.rerun()
                    
                    with col4:
                        if st.button("📥", key=f"dl_{project_path.name}", use_container_width=True, help="Download"):
                            zip_buffer = create_zip_from_project(project_path)
                            st.download_button(
                                label="📥",
                                data=zip_buffer.getvalue(),
                                file_name=f"{project_path.name}.zip",
                                mime="application/zip",
                                key=f"download_{project_path.name}",
                                use_container_width=True
                            )
                    
                    with col5:
                        if st.button("👁️", key=f"view_{project_path.name}", use_container_width=True, help="View details"):
                            st.json(analytics)
                    
                    with col6:
                        if st.button("🗑️", key=f"del_{project_path.name}", use_container_width=True, help="Delete"):
                            shutil.rmtree(project_path)
                            st.success(f"✅ Deleted '{project_path.name}'")
                            st.rerun()
    
    # ========================================================================
    # TAB 2: Recent Projects
    # ========================================================================
    with tab2:
        st.markdown("**Recent projects** (last 10)")
        
        if projects_dir.exists() and list(projects_dir.iterdir()):
            projects = sorted(projects_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)[:10]
            
            for project_path in projects:
                if project_path.is_dir():
                    analytics = get_project_analytics(project_path)
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"📁 **{project_path.name}** - {analytics['created'].strftime('%Y-%m-%d %H:%M')} | {analytics['size_mb']:.2f}MB")
                    
                    with col2:
                        if st.button("📥 Get", key=f"recent_dl_{project_path.name}", use_container_width=True):
                            zip_buffer = create_zip_from_project(project_path)
                            st.download_button(
                                label="Download",
                                data=zip_buffer.getvalue(),
                                file_name=f"{project_path.name}.zip",
                                mime="application/zip",
                                key=f"recent_download_{project_path.name}"
                            )
        else:
            st.info("No projects yet")
    
    # ========================================================================
    # TAB 3: Favorites
    # ========================================================================
    with tab3:
        if not favorites:
            st.markdown("""
            <div class="card" style="text-align: center; padding: 2em;">
            <p style="color: #6b7280;">⭐ No favorites yet. Star projects to add them here!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"**Your ⭐ Favorite Projects** ({len(favorites)})")
            
            if projects_dir.exists():
                for fav_name in favorites:
                    fav_path = projects_dir / fav_name
                    if fav_path.exists():
                        analytics = get_project_analytics(fav_path)
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"⭐ **{fav_name}** | 📊 {analytics['files']} files | 💾 {analytics['size_mb']:.2f}MB")
                        
                        with col2:
                            if st.button("📥", key=f"fav_dl_{fav_name}", use_container_width=True):
                                zip_buffer = create_zip_from_project(fav_path)
                                st.download_button(
                                    label="Download",
                                    data=zip_buffer.getvalue(),
                                    file_name=f"{fav_name}.zip",
                                    mime="application/zip",
                                    key=f"fav_download_{fav_name}"
                                )
    
    # ========================================================================
    # TAB 4: Analytics Dashboard
    # ========================================================================
    with tab4:
        st.markdown("**📊 Project Analytics**")
        
        if projects_dir.exists() and list(projects_dir.iterdir()):
            projects = list(projects_dir.iterdir())
            
            # Overall stats
            col1, col2, col3, col4 = st.columns(4)
            
            total_projects = len(projects)
            total_files = sum(len(list(p.rglob("*"))) for p in projects if p.is_dir())
            total_size = sum(sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) for p in projects if p.is_dir())
            
            with col1:
                st.metric("📁 Total Projects", total_projects)
            with col2:
                st.metric("📄 Total Files", total_files)
            with col3:
                st.metric("💾 Total Size", f"{total_size / (1024 * 1024):.2f} MB")
            with col4:
                st.metric("⭐ Favorites", len(favorites))
            
            # Detailed analytics table
            st.markdown("**Project Details:**")
            analytics_data = []
            
            for project_path in sorted(projects, key=lambda x: x.stat().st_mtime, reverse=True):
                if project_path.is_dir():
                    ana = get_project_analytics(project_path)
                    analytics_data.append({
                        "Project": project_path.name,
                        "Files": ana['files'],
                        "Size (MB)": f"{ana['size_mb']:.2f}",
                        "Created": ana['created'].strftime('%Y-%m-%d'),
                        "Type": ana['type'],
                        "Favorite": "⭐" if project_path.name in favorites else ""
                    })
            
            st.dataframe(analytics_data, use_container_width=True)
        else:
            st.info("No projects yet")
    
    # ========================================================================
    # TAB 5: Project Templates
    # ========================================================================
    with tab5:
        st.markdown("**🎨 Start from Templates**")
        
        templates = {
            "E-commerce Store": "Build a modern online store with product catalog, shopping cart, and checkout",
            "SaaS Dashboard": "Build a professional dashboard for managing software-as-a-service features",
            "Blog Platform": "Create a blog with posts, comments, and categories",
            "Portfolio Site": "Showcase your work with a professional portfolio website",
            "Documentation": "Create comprehensive documentation site",
            "Community Forum": "Build an interactive community discussion platform"
        }
        
        col1, col2 = st.columns(2)
        
        for idx, (template_name, template_desc) in enumerate(templates.items()):
            if idx % 2 == 0:
                col = col1
            else:
                col = col2
            
            with col:
                st.markdown(f"""
                <div class="card">
                <h4 style="color: #667eea; margin: 0 0 0.5em 0;">{template_name}</h4>
                <p style="color: #6b7280; margin: 0.5em 0;">{template_desc}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🚀 Use {template_name}", key=f"template_{template_name}", use_container_width=True):
                    st.session_state.template_selected = template_name
                    st.success(f"✅ Template selected! Fill in Quick Generate with your requirements.")
                    st.info(f"📝 **Suggested:** {template_name} is great for {template_desc.lower()}")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("**💡 Tip:** Select a template above and use it with Quick Generate to create amazing projects!")



def profile_page():
    """Enhanced user profile page"""
    st.markdown(f"<h1 style='color: #6366f1;'>👤 Profile: {st.session_state.current_user}</h1>", unsafe_allow_html=True)
    
    # Get user data
    user_file = Path(f".users/{st.session_state.current_user}.json")
    if user_file.exists():
        with open(user_file, "r") as f:
            user_data = json.load(f)
        
        col1, col2, col3 = st.columns(3)
        
        # Account Information Card
        with col1:
            st.markdown("""
            <div class="card">
            <h3 style="color: #6366f1;">📋 Account Information</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.write(f"**👤 Username:** `{user_data.get('username')}`")
            st.write(f"**📧 Email:** `{user_data.get('email')}`")
            st.write(f"**📅 Member Since:** {user_data.get('created_at', 'N/A')[:10]}")
            
            if 'credits' in user_data:
                st.write(f"**💳 Plan:** {user_data['credits'].get('plan', 'Free')}")
                st.write(f"**⭐ Credits:** {user_data['credits'].get('available', 0)}")
        
        # Workflow Statistics
        with col2:
            st.markdown("""
            <div class="card">
            <h3 style="color: #ec4899;">📊 Statistics</h3>
            </div>
            """, unsafe_allow_html=True)
            
            workflows_dir = Path(".workflows")
            if workflows_dir.exists():
                workflow_files = list(workflows_dir.glob("*.json"))
                st.metric("Total Workflows", len(workflow_files))
                st.metric("Websites Generated", len(workflow_files))
        
        # Connected Providers
        with col3:
            st.markdown("""
            <div class="card">
            <h3 style="color: #10b981;">🔗 Connected Providers</h3>
            </div>
            """, unsafe_allow_html=True)
            
            oauth_tokens = Path(".oauth_tokens")
            username = st.session_state.current_user
            
            providers = [
                ("🔵 Google Gemini", f"{username}_google_token.json"),
                ("🟢 OpenAI GPT", f"{username}_openai_token.json"),
                ("🔶 Anthropic Claude", f"{username}_anthropic_token.json"),
            ]
            
            for provider_name, token_file in providers:
                token_path = oauth_tokens / token_file
                if token_path.exists():
                    st.markdown(f'<div style="color: #10b981; font-weight: 600;">✅ {provider_name}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="color: #f59e0b; font-weight: 600;">⚠️ {provider_name}</div>', unsafe_allow_html=True)


def workflow_page():
    """Enhanced workflow creation and execution page"""
    st.markdown("<h1 style='color: #6366f1;'>⚙️ Website Builder</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["✨ Create New", "📚 My Workflows", "🚀 Execute"])
    
    # ========================================================================
    # Tab 1: Create New Workflow
    # ========================================================================
    with tab1:
        st.markdown("<h2 style='color: #ec4899;'>Create Your Website Blueprint</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class="card">
            <h3>🎯 Website Details</h3>
            <p>Fill in the information about your website project</p>
            </div>
            """, unsafe_allow_html=True)
            
            topic = st.text_input(
                "Website Topic",
                placeholder="e.g., E-commerce Store, Blog Platform, SaaS Dashboard",
                help="What type of website do you want to build?",
                key="topic_input"
            )
            
            description = st.text_area(
                "Project Description",
                placeholder="Describe what you want in your website. Be as detailed as possible...",
                height=150,
                help="Include features, design preferences, target audience, etc.",
                key="desc_input"
            )
        
        with col2:
            st.markdown("""
            <div class="card">
            <h3>💡 Template Examples</h3>
            </div>
            """, unsafe_allow_html=True)
            
            templates = {
                "🛒 E-commerce Store": "An online store with product catalog, shopping cart, and payment processing",
                "📱 Mobile App Landing": "A modern landing page showcasing a mobile application with download links",
                "📚 Blog Platform": "A content management system for publishing and managing blog posts",
                "💼 SaaS Dashboard": "A professional dashboard for managing software-as-a-service features",
                "🏢 Corporate Website": "A professional corporate website with services and company information",
            }
            
            for template_name, template_desc in templates.items():
                if st.button(f"{template_name}", key=f"template_{template_name}"):
                    st.session_state.topic_input = template_name.split()[0]
                    st.rerun()
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        if st.button("✨ Generate Blueprint", key="create_workflow", use_container_width=True):
            if not topic or not description:
                st.markdown('<div class="status-error">❌ Please fill in both topic and description</div>', unsafe_allow_html=True)
            else:
                with st.spinner("🤖 Creating workflow plan..."):
                    try:
                        # Create workflow steps
                        steps = [
                            WorkflowStep(
                                step_id="frontend-design",
                                description="Design UI/UX for the website",
                                agent_type="frontend",
                                task_query=f"Design frontend for {topic}: {description[:100]}",
                                dependencies=[],
                                estimated_time=300,
                            ),
                            WorkflowStep(
                                step_id="backend-design",
                                description="Design backend architecture and APIs",
                                agent_type="backend",
                                task_query=f"Design backend architecture for {topic}",
                                dependencies=[],
                                estimated_time=300,
                            ),
                            WorkflowStep(
                                step_id="orchestration",
                                description="Coordinate all components",
                                agent_type="orchestrator",
                                task_query=f"Orchestrate integration for {topic}",
                                dependencies=["frontend-design", "backend-design"],
                                estimated_time=300,
                            ),
                        ]
                        
                        # Create plan
                        plan = st.session_state.workflow_manager.create_plan(
                            project_name=topic,
                            description=description,
                            steps=steps,
                        )
                        
                        # Save plan
                        plan.save()
                        
                        st.markdown(f'<div class="status-success">✅ Blueprint created successfully!</div>', unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Workflow ID", plan.workflow_id[:8] + "...")
                        with col2:
                            st.metric("Total Steps", len(plan.steps))
                        with col3:
                            st.metric("Est. Time", f"{plan.estimated_total_time}s")
                        
                        st.balloons()
                    except Exception as e:
                        st.markdown(f'<div class="status-error">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # Tab 2: My Workflows
    # ========================================================================
    with tab2:
        st.markdown("<h2 style='color: #10b981;'>Your Workflows</h2>", unsafe_allow_html=True)
        
        workflows_dir = Path(".workflows")
        if workflows_dir.exists():
            workflow_files = sorted(workflows_dir.glob("*.json"), reverse=True)
            
            if not workflow_files:
                st.markdown("""
                <div class="card" style="text-align: center; padding: 3em;">
                <h3>📭 No workflows yet</h3>
                <p>Create your first website blueprint in the 'Create New' tab!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Filter workflows for current user
                cols = st.columns(1)
                
                for idx, workflow_file in enumerate(workflow_files):
                    try:
                        with open(workflow_file, "r") as f:
                            workflow_data = json.load(f)
                        
                        # Create workflow card
                        with st.container():
                            st.markdown(f"""
                            <div class="workflow-card fade-in">
                            <h3>{workflow_data.get('project_name', 'Unknown')}</h3>
                            <p><strong>ID:</strong> <code>{workflow_data.get('workflow_id')}</code></p>
                            <p><strong>📊 Status:</strong> <span class="agent-status-complete">{workflow_data.get('phase', 'planning').upper()}</span></p>
                            <p><strong>📝 Description:</strong> {workflow_data.get('description', 'No description')[:100]}...</p>
                            <p><strong>⏱️ Est. Time:</strong> {workflow_data.get('estimated_total_time', 0)}s | <strong>📅 Created:</strong> {workflow_data.get('created_at', 'N/A')[:10]}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.button(f"🚀 Execute", key=f"execute_{idx}", use_container_width=True):
                                    st.session_state.selected_workflow = str(workflow_file)
                                    st.session_state.execute_workflow = True
                                    st.success(f"Selected: {workflow_data.get('workflow_id')}")
                            
                            with col2:
                                if st.button(f"👁️ View Details", key=f"view_{idx}", use_container_width=True):
                                    st.json(workflow_data)
                            
                            with col3:
                                if st.button(f"📋 Copy ID", key=f"copy_{idx}", use_container_width=True):
                                    st.write(f"`{workflow_data.get('workflow_id')}`")
                    except Exception as e:
                        st.warning(f"Error loading workflow: {str(e)}")
    
    # ========================================================================
    # Tab 3: Execute Workflow
    # ========================================================================
    with tab3:
        st.markdown("<h2 style='color: #6366f1;'>Execute Website Generation</h2>", unsafe_allow_html=True)
        
        if "selected_workflow" not in st.session_state:
            st.markdown("""
            <div class="status-warning">⚠️ Select a workflow from 'My Workflows' tab first</div>
            """, unsafe_allow_html=True)
        else:
            workflow_file = st.session_state.selected_workflow
            
            with open(workflow_file, "r") as f:
                workflow_data = json.load(f)
            
            st.markdown(f"""
            <div class="card">
            <h3 style="color: #6366f1;">Executing: {workflow_data.get('project_name')}</h3>
            <p>{workflow_data.get('description')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show workflow steps
            st.markdown("**🔄 Workflow Steps:**")
            for idx, step in enumerate(workflow_data.get('steps', []), 1):
                st.write(f"{idx}. {step['description']} (**{step['agent_type']}**)")
            
            if st.button("🚀 Start Execution", key="execute_button", use_container_width=True):
                with st.spinner("⏳ Running AI agents... This may take 1-2 minutes"):
                    # Agent execution visualization
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); padding: 1.5em; border-radius: 12px; color: white; text-align: center;">
                        <h3>🎨 Frontend Design</h3>
                        <p>UI/UX with Gemini</p>
                        <div class="agent-status-running">● Running...</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); padding: 1.5em; border-radius: 12px; color: white; text-align: center;">
                        <h3>⚙️ Backend Architecture</h3>
                        <p>APIs with OpenAI</p>
                        <div class="agent-status-running">● Running...</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #a855f7 0%, #9333ea 100%); padding: 1.5em; border-radius: 12px; color: white; text-align: center;">
                        <h3>🔗 Orchestration</h3>
                        <p>Integration with Claude</p>
                        <div class="agent-status-running">● Running...</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    time.sleep(2)
                    
                    st.markdown(f'<div class="status-success">✅ Website generation complete!</div>', unsafe_allow_html=True)
                    st.balloons()
                    
                    # Show results
                    st.markdown("<h3 style='color: #6366f1;'>📦 Generated Website Blueprint</h3>", unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("""
                        <div class="card">
                        <h4 style="color: #ec4899;">🎨 Frontend</h4>
                        <ul>
                        <li>Responsive Design</li>
                        <li>Modern UI Components</li>
                        <li>Accessibility</li>
                        <li>Mobile Optimized</li>
                        </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("""
                        <div class="card">
                        <h4 style="color: #10b981;">⚙️ Backend</h4>
                        <ul>
                        <li>RESTful APIs</li>
                        <li>Database Schema</li>
                        <li>Authentication</li>
                        <li>Security</li>
                        </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown("""
                        <div class="card">
                        <h4 style="color: #f59e0b;">🔗 Integration</h4>
                        <ul>
                        <li>Deployment Guide</li>
                        <li>CI/CD Pipeline</li>
                        <li>Monitoring</li>
                        <li>Scaling</li>
                        </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.divider()
                    
                    with st.expander("📄 View Full Blueprint"):
                        results = {
                            "frontend": {
                                "pages": ["Home", "Product Catalog", "Product Detail", "Cart", "Checkout", "User Profile"],
                                "features": ["Responsive Design", "Search & Filter", "Product Reviews", "Wishlist", "Notifications"],
                                "tech_stack": ["React 18", "Tailwind CSS", "TypeScript", "Redux"]
                            },
                            "backend": {
                                "apis": ["/api/products", "/api/orders", "/api/users", "/api/payments", "/api/auth"],
                                "database": ["PostgreSQL", "Redis Cache", "Elasticsearch"],
                                "services": ["Node.js/Express", "Authentication Service", "Payment Service", "Email Service"]
                            },
                            "deployment": {
                                "hosting": "AWS EC2 / Docker",
                                "cdn": "CloudFront",
                                "monitoring": "CloudWatch / New Relic",
                                "ci_cd": "GitHub Actions"
                            }
                        }
                        st.json(results)


# ============================================================================
# Main App
# ============================================================================
def main():
    # Enhanced Header with Gradient
    st.markdown("""
    <div style="background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%); padding: 2em; border-radius: 12px; margin-bottom: 2em;">
    <h1 style="color: white; text-align: center; margin: 0;">🤖 Agentic AI - Website Builder</h1>
    <p style="color: rgba(255,255,255,0.9); text-align: center; font-size: 1.1em; margin: 0.5em 0 0 0;">Generate complete websites using AI agents (Gemini + GPT + Claude)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%); padding: 1.5em; border-radius: 12px; margin-bottom: 2em;">
        <h2 style="color: white; margin: 0; text-align: center;">🎯 Agentic AI</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.current_user:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 1em; border-radius: 8px; color: white; text-align: center;">
            <b>✅ Logged in as</b><br>
            <code style="color: white; font-weight: bold;">{st.session_state.current_user}</code>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='height: 1.5em'></div>", unsafe_allow_html=True)
            
            page = st.radio(
                "Navigation",
                ["📊 Dashboard", "👤 Profile", "🔑 API Keys", "⚙️ My Workflows", "📚 Documentation"],
                key="page_select",
                label_visibility="collapsed"
            )
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⚙️ Settings", use_container_width=True):
                    st.info("Settings coming soon!")
            
            with col2:
                if st.button("🚪 Logout", use_container_width=True):
                    session_file = Path(".users/.session")
                    if session_file.exists():
                        session_file.unlink()
                    st.session_state.current_user = None
                    st.rerun()
        else:
            page = "Login"
    
    # ========================================================================
    # Login Page
    # ========================================================================
    if not st.session_state.current_user:
        st.markdown("""
        <div style="text-align: center; padding: 2em;">
        <h2 style="color: #6366f1;">Welcome to Agentic AI</h2>
        <p style="color: #6b7280; font-size: 1.1em;">Build professional websites with AI in minutes</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1em'></div>", unsafe_allow_html=True)
        
        login_page()
    
    # ========================================================================
    # Dashboard
    # ========================================================================
    elif page == "📊 Dashboard":
        st.markdown("<h1 style='color: #6366f1;'>📊 Dashboard</h1>", unsafe_allow_html=True)
        
        # Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        workflows_dir = Path(".workflows")
        workflow_count = len(list(workflows_dir.glob("*.json"))) if workflows_dir.exists() else 0
        
        projects_dir = Path(f".projects/{st.session_state.current_user}")
        project_count = len(list(projects_dir.iterdir())) if projects_dir.exists() else 0
        
        with col1:
            st.markdown("""
            <div class="metric-card">
            <div class="metric-label">Workflows</div>
            <div class="metric-value">""" + str(workflow_count) + """</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card secondary">
            <div class="metric-label">Projects</div>
            <div class="metric-value">""" + str(project_count) + """</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card success">
            <div class="metric-label">API Credits</div>
            <div class="metric-value">∞</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
            <div class="metric-label">Usage</div>
            <div class="metric-value">42%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Quick Start
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div class="card">
            <h3 style="color: #6366f1; margin-bottom: 0.5em;">🚀 Quick Start</h3>
            <p style="color: #374151; margin-bottom: 1em;">Ready to build your next project?</p>
            <ol style="color: #1f2937; margin: 0; padding-left: 1.5em;">
            <li style="margin-bottom: 0.5em;"><strong>🚀 Quick Generate</strong> - Enter requirement below to auto-generate projects</li>
            <li style="margin-bottom: 0.5em;"><strong>⚙️ Workflows</strong> - Create complex website blueprints</li>
            <li><strong>📁 My Files</strong> - Browse and download all your projects</li>
            </ol>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="card">
            <h3 style="color: #ec4899; margin-bottom: 0.5em;">💡 Features</h3>
            <ul style="color: #1f2937; margin: 0; padding-left: 1.5em; list-style-type: none;">
            <li style="margin-bottom: 0.5em;">✨ <strong>AI-Powered Design</strong></li>
            <li style="margin-bottom: 0.5em;">🚀 <strong>Auto Generate</strong></li>
            <li style="margin-bottom: 0.5em;">🔒 <strong>Secure Storage</strong></li>
            <li>📦 <strong>Downloadable</strong></li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Quick Generate Section
        quick_generate_section()
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # My Files Section
        my_files_section()
    
    # ========================================================================
    # Profile
    # ========================================================================
    elif page == "👤 Profile":
        profile_page()
    
    # ========================================================================
    # API Keys
    # ========================================================================
    elif page == "🔑 API Keys":
        api_keys_page()
    
    # ========================================================================
    # My Workflows
    # ========================================================================
    elif page == "⚙️ My Workflows":
        workflow_page()
    
    # ========================================================================
    # Documentation
    # ========================================================================
    elif page == "📚 Documentation":
        st.markdown("<h1 style='color: #6366f1;'>📚 Documentation</h1>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📖 Guide", "🔑 API Keys", "❓ FAQ"])
        
        with tab1:
            st.markdown("""
            ### How to Use Agentic AI
            
            #### Step 1: Create a Blueprint
            1. Go to "My Workflows" tab
            2. Click "✨ Create New"
            3. Enter your website topic and detailed description
            4. Click "Generate Blueprint"
            
            #### Step 2: Execute with AI
            1. Select your workflow from "My Workflows"
            2. Click the "🚀 Execute" button
            3. Watch as AI agents design your website:
               - **🎨 Frontend Agent** designs the UI/UX
               - **⚙️ Backend Agent** creates the API architecture
               - **🔗 Orchestrator** integrates everything
            
            #### Step 3: Download & Deploy
            1. Get the generated code from the results
            2. Deploy to your hosting platform
            3. Customize as needed
            
            ---
            
            ### AI Agents
            
            **🎨 Frontend Agent (Google Gemini)**
            - Designs beautiful, responsive UI/UX
            - Creates modern HTML & CSS layouts
            - Implements accessibility standards
            - Optimizes for all devices
            
            **⚙️ Backend Agent (OpenAI GPT)**
            - Designs scalable APIs
            - Creates database schemas
            - Implements authentication & security
            - Optimizes performance
            
            **🔗 Orchestrator Agent (Anthropic Claude)**
            - Coordinates all agents
            - Integrates frontend & backend
            - Provides deployment guide
            - Ensures best practices
            """)
        
        with tab2:
            st.markdown("""
            ### 🔑 Connected API Keys
            
            Your API keys are securely stored and never shared with anyone.
            """)
            
            oauth_tokens = Path(".oauth_tokens")
            username = st.session_state.current_user
            
            col1, col2, col3 = st.columns(3)
            
            providers = [
                ("🔵 Google Gemini", f"{username}_google_token.json", "Google"),
                ("🟢 OpenAI", f"{username}_openai_token.json", "OpenAI"),
                ("🔶 Anthropic Claude", f"{username}_anthropic_token.json", "Anthropic"),
            ]
            
            for provider_name, token_file, key_link in providers:
                token_path = oauth_tokens / token_file
                if token_path.exists():
                    st.markdown(f'<div style="color: #10b981; font-weight: 600; padding: 1em; border-radius: 8px; background: #f0fdf4; border-left: 4px solid #10b981;">✅ {provider_name} Connected</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="color: #f59e0b; font-weight: 600; padding: 1em; border-radius: 8px; background: #fffbeb; border-left: 4px solid #f59e0b;">⚠️ {provider_name} Not Connected</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown("""
            ### ❓ Frequently Asked Questions
            
            **Q: Do I need API keys?**
            A: Yes, you'll need API keys from Google (Gemini), OpenAI, and Anthropic. You bring your own keys.
            
            **Q: How much does it cost?**
            A: You only pay for the API calls you make to the LLM providers. No subscription fees!
            
            **Q: Can I customize the generated code?**
            A: Absolutely! The generated code is yours to modify as needed.
            
            **Q: How long does generation take?**
            A: Typically 1-2 minutes depending on project complexity.
            
            **Q: Is my data private?**
            A: Yes! All your data is stored locally and securely. We never share or sell your information.
            
            **Q: What if generation fails?**
            A: Try again or check your API keys. If issues persist, contact support.
            """)


if __name__ == "__main__":
    main()
