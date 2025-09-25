#!/usr/bin/env python3
"""
Car Advisor Setup Script
Automated setup and installation script for the Car Advisor application
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_step(step_num, total_steps, description):
    """Print formatted step information"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}/{total_steps}: {description}")
    print(f"{'='*60}")

def run_command(command, description=""):
    """Run a system command with error handling"""
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error {description}: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported.")
        print("✅ Please install Python 3.8 or later.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible.")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "upgrading pip"):
        return False
    
    # Install from requirements.txt
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "installing dependencies"):
        print("⚠️ Some dependencies failed to install. Trying individual installation...")
        
        # Core dependencies
        core_deps = [
            "streamlit>=1.28.0",
            "openai>=1.3.0", 
            "python-dotenv>=1.0.0",
            "pandas>=2.1.0",
            "plotly>=5.17.0",
            "streamlit-option-menu>=0.3.6",
            "reportlab>=4.0.4",
            "Pillow>=10.0.0",
            "requests>=2.31.0"
        ]
        
        failed_deps = []
        for dep in core_deps:
            if not run_command(f"{sys.executable} -m pip install {dep}", f"installing {dep}"):
                failed_deps.append(dep)
        
        if failed_deps:
            print(f"❌ Failed to install: {', '.join(failed_deps)}")
            return False
    
    print("✅ All dependencies installed successfully!")
    return True

def setup_environment_file():
    """Setup .env file from template"""
    env_template = ".env.template"
    env_file = ".env"
    
    if not os.path.exists(env_template):
        print(f"❌ Template file {env_template} not found!")
        return False
    
    if os.path.exists(env_file):
        print(f"⚠️ {env_file} already exists. Backing up as {env_file}.backup")
        shutil.copy(env_file, f"{env_file}.backup")
    
    # Copy template to .env
    shutil.copy(env_template, env_file)
    print(f"✅ Created {env_file} from template.")
    
    # Prompt for API key
    print("\n🔑 OpenAI API Key Setup:")
    print("You need an OpenAI API key to use the AI features.")
    print("Get your API key from: https://platform.openai.com/api-keys")
    
    api_key = input("\nEnter your OpenAI API key (or press Enter to set up later): ").strip()
    
    if api_key:
        # Update the .env file
        with open(env_file, 'r') as f:
            content = f.read()
        
        content = content.replace('your_openai_api_key_here', api_key)
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ OpenAI API key configured!")
    else:
        print("⚠️ You can set up the API key later by editing the .env file")
    
    return True

def verify_installation():
    """Verify that the installation was successful"""
    print("🔍 Verifying installation...")
    
    try:
        import streamlit
        import openai
        import pandas
        import plotly
        from dotenv import load_dotenv
        print("✅ All core modules can be imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def create_run_scripts():
    """Create convenient run scripts"""
    
    # Create run script for Unix/Mac
    run_script_unix = """#!/bin/bash
# Car Advisor Run Script

echo "🚗 Starting Car Advisor..."
echo "📱 The app will open in your default browser"
echo "🛑 Press Ctrl+C to stop the application"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Run the application
streamlit run app.py

echo "👋 Car Advisor stopped. Thank you for using our app!"
"""
    
    # Create run script for Windows
    run_script_windows = """@echo off
rem Car Advisor Run Script

echo 🚗 Starting Car Advisor...
echo 📱 The app will open in your default browser
echo 🛑 Press Ctrl+C to stop the application
echo.

rem Activate virtual environment if it exists
if exist "venv\\Scripts\\activate.bat" (
    call venv\\Scripts\\activate.bat
    echo ✅ Virtual environment activated
)

rem Run the application
streamlit run app.py

echo 👋 Car Advisor stopped. Thank you for using our app!
pause
"""
    
    # Write scripts
    with open("run_app.sh", "w") as f:
        f.write(run_script_unix)
    
    with open("run_app.bat", "w") as f:
        f.write(run_script_windows)
    
    # Make Unix script executable
    if os.name != 'nt':  # Not Windows
        os.chmod("run_app.sh", 0o755)
    
    print("✅ Created run scripts: run_app.sh (Mac/Linux) and run_app.bat (Windows)")

def main():
    """Main setup function"""
    print("🚗 Car Advisor Setup")
    print("=" * 40)
    print("Welcome to the Car Advisor setup assistant!")
    print("This script will help you set up the application.")
    
    total_steps = 6
    current_step = 0
    
    # Step 1: Check Python version
    current_step += 1
    print_step(current_step, total_steps, "Checking Python version")
    if not check_python_version():
        print("\n❌ Setup failed. Please install a compatible Python version and try again.")
        sys.exit(1)
    
    # Step 2: Install dependencies
    current_step += 1
    print_step(current_step, total_steps, "Installing dependencies")
    if not install_dependencies():
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
    
    # Step 3: Setup environment file
    current_step += 1
    print_step(current_step, total_steps, "Setting up environment file")
    if not setup_environment_file():
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
    
    # Step 4: Verify installation
    current_step += 1
    print_step(current_step, total_steps, "Verifying installation")
    if not verify_installation():
        print("\n❌ Setup failed. Some dependencies are not working correctly.")
        sys.exit(1)
    
    # Step 5: Create run scripts
    current_step += 1
    print_step(current_step, total_steps, "Creating run scripts")
    create_run_scripts()
    
    # Step 6: Final instructions
    current_step += 1
    print_step(current_step, total_steps, "Setup complete!")
    
    print("""
✅ Car Advisor setup completed successfully!

🚀 To start the application:

   Option 1 (Recommended):
   • Mac/Linux: ./run_app.sh
   • Windows: run_app.bat

   Option 2 (Manual):
   • streamlit run app.py

📋 Next Steps:
   1. If you haven't set up your OpenAI API key, edit the .env file
   2. Run the application using one of the methods above
   3. Open your browser to the URL shown (usually http://localhost:8501)
   4. Login with the password: senior_car_guide_2024

🔧 Configuration:
   • Environment variables: .env file
   • Application settings: Check the sidebar in the app

💡 Need Help?
   • Check README.md for detailed instructions
   • Visit the app's help section
   • Contact support for technical issues

🎉 Enjoy using Car Advisor!
""")

if __name__ == "__main__":
    main()