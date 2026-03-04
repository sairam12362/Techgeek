#!/usr/bin/env python3
"""
VidyāMitra AI Career Agent - Startup Script
Run this script to start the application
"""

import os
import sys
import uvicorn
import webbrowser
import time
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import openai
        import pydantic
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_vars():
    """Check if required environment variables are set"""
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  WARNING: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key to enable AI analysis features")
        print("Example: export OPENAI_API_KEY='your-api-key-here'")
        return False
    return True

def create_static_dirs():
    """Create necessary directories"""
    static_dir = Path("static")
    if not static_dir.exists():
        static_dir.mkdir()
        print("✅ Created static directory")
    
    return True

def main():
    print("🎯 VidyāMitra AI Career Agent")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Create directories
    create_static_dirs()
    
    # Check environment variables
    env_ok = check_env_vars()
    
    print("\n🚀 Starting server...")
    print("📱 Frontend: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("⚡ Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(2)
        webbrowser.open("http://localhost:8000")
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the server
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=["./"],
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")

if __name__ == "__main__":
    main()
