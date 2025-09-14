#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram Video Bot - Setup and Deployment Script
This script helps users set up their environment and deploy the bot automatically
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime

def check_python():
    """Check if Python is installed and version is compatible."""
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 7:
            print(f"✓ Python {version.major}.{version.minor}.{version.micro} is installed")
            return True
        else:
            print(f"✗ Python version is too old: {version.major}.{version.minor}.{version.micro}")
            print("  Please install Python 3.7 or higher")
            return False
    except Exception as e:
        print(f"✗ Error checking Python version: {e}")
        return False

def check_git():
    """Check if Git is installed."""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {result.stdout.strip()}")
            return True
        else:
            print("✗ Git is not installed")
            print("  Please install Git from https://git-scm.com/")
            return False
    except FileNotFoundError:
        print("✗ Git is not installed")
        print("  Please install Git from https://git-scm.com/")
        return False
    except Exception as e:
        print(f"✗ Error checking Git: {e}")
        return False

def check_pip():
    """Check if pip is installed."""
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ pip is installed")
            return True
        else:
            print("✗ pip is not installed")
            return False
    except Exception as e:
        print(f"✗ Error checking pip: {e}")
        return False

def setup_env_file():
    """Help user set up the .env file."""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    env_example_path = os.path.join(os.path.dirname(__file__), '.env.example')
    
    if os.path.exists(env_path):
        print("✓ .env file already exists")
        return True
    
    if not os.path.exists(env_example_path):
        print("✗ .env.example file not found")
        return False
    
    print("\nSetting up .env file...")
    print("To use the Telegram bot, you need a Telegram Bot Token.")
    print("1. Open Telegram and search for @BotFather")
    print("2. Start a conversation and send /newbot")
    print("3. Follow the instructions to create a new bot")
    print("4. Copy the bot token when it's provided")
    
    bot_token = input("\nEnter your Telegram Bot Token (or press Enter to skip): ").strip()
    
    if not bot_token:
        print("Skipping .env setup. You can manually create .env file later.")
        return True
    
    try:
        with open(env_example_path, 'r') as f:
            content = f.read()
        
        content = content.replace('YOUR_BOT_TOKEN_HERE', bot_token)
        
        with open(env_path, 'w') as f:
            f.write(content)
        
        print("✓ .env file created successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating .env file: {e}")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("\nInstalling dependencies...")
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Dependencies installed successfully")
            return True
        else:
            print("✗ Error installing dependencies:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"✗ Error installing dependencies: {e}")
        return False

def initialize_git():
    """Initialize Git repository if not already done."""
    try:
        # Check if this is already a Git repository
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Git repository already initialized")
            return True
        
        # Initialize Git repository
        result = subprocess.run(['git', 'init'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Git repository initialized")
            return True
        else:
            print("✗ Error initializing Git repository:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"✗ Error initializing Git: {e}")
        return False

def git_add_commit():
    """Add all files and create initial commit."""
    try:
        # Add all files
        result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
        if result.returncode != 0:
            print("✗ Error adding files to Git:")
            print(result.stderr)
            return False
        
        # Create commit
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Initial commit: Telegram Video Bot - {timestamp}"
        
        result = subprocess.run(['git', 'commit', '-m', commit_message], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Files committed to Git")
        else:
            # This might happen if there are no changes
            if "nothing to commit" in result.stderr:
                print("✓ No changes to commit (already up to date)")
            else:
                print("✗ Error committing files:")
                print(result.stderr)
                return False
        
        return True
    except Exception as e:
        print(f"✗ Error with Git operations: {e}")
        return False

def setup_remote_repository():
    """Help user set up remote repository."""
    try:
        # Check if remote is already set up
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        if result.returncode == 0 and 'origin' in result.stdout:
            print("✓ Remote repository already set up")
            return True
        
        print("\nSetting up remote repository...")
        print("To set up automatic deployment, you need a remote Git repository.")
        print("1. Go to GitHub (https://github.com) or GitLab (https://gitlab.com)")
        print("2. Create a new repository")
        print("3. Copy the repository URL")
        
        repo_url = input("\nEnter your repository URL (or press Enter to skip): ").strip()
        
        if not repo_url:
            print("Skipping remote repository setup. You can set it up later with:")
            print("  git remote add origin YOUR_REPOSITORY_URL")
            return True
        
        # Add remote repository
        result = subprocess.run(['git', 'remote', 'add', 'origin', repo_url], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Remote repository added")
            return True
        else:
            print("✗ Error adding remote repository:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Error setting up remote repository: {e}")
        return False

def push_to_remote():
    """Push to remote repository."""
    try:
        print("\nPushing to remote repository...")
        
        # Set upstream and push
        result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Successfully pushed to remote repository")
            return True
        else:
            # Try with master branch if main doesn't work
            result = subprocess.run(['git', 'push', '-u', 'origin', 'master'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Successfully pushed to remote repository")
                return True
            else:
                print("✗ Error pushing to remote repository:")
                print(result.stderr)
                return False
    except Exception as e:
        print(f"✗ Error pushing to remote: {e}")
        return False

def main():
    """Main function to run setup and deployment."""
    print("=" * 60)
    print("Telegram Video Bot - Setup and Deployment Script")
    print("=" * 60)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working directory: {script_dir}")
    
    # Check prerequisites
    print("\n1. Checking prerequisites...")
    prerequisites = [
        ("Python", check_python),
        ("Git", check_git),
        ("pip", check_pip)
    ]
    
    for name, check_func in prerequisites:
        print(f"  Checking {name}... ", end="")
        if not check_func():
            print(f"\n✗ {name} check failed. Please fix the issue and run this script again.")
            return False
    
    # Setup environment
    print("\n2. Setting up environment...")
    if not setup_env_file():
        print("✗ Environment setup failed")
        return False
    
    # Install dependencies
    print("\n3. Installing dependencies...")
    if not install_dependencies():
        print("✗ Dependency installation failed")
        return False
    
    # Git operations
    print("\n4. Setting up Git...")
    git_steps = [
        ("Initialize Git repository", initialize_git),
        ("Add and commit files", git_add_commit),
        ("Set up remote repository", setup_remote_repository),
        ("Push to remote", push_to_remote)
    ]
    
    for step_name, step_func in git_steps:
        print(f"  {step_name}... ", end="")
        if not step_func():
            print(f"✗ {step_name} failed")
            return False
        print("✓")
    
    print("\n" + "=" * 60)
    print("🎉 Setup and deployment completed successfully!")
    print("=" * 60)
    
    print("\nTo run the bot:")
    print("1. Make sure you have a .env file with your Telegram bot token")
    print("2. Run: python run_bot.py")
    
    print("\nFor automatic deployment in the future, simply run:")
    print("1. This script again, or")
    print("2. The auto_deploy.bat file (on Windows)")
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        if success:
            print("\n✅ All steps completed successfully!")
        else:
            print("\n❌ Some steps failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)