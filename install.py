#!/usr/bin/env python3
"""
PROJECT NIV - Installation Script
Installs all required dependencies and verifies installation
"""

import os
import sys
import subprocess
import importlib

def print_banner():
    """Print installation banner"""
    print("=" * 60)
    print("🚀 PROJECT NIV - Installation Script")
    print("📦 Installing Dependencies")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python and try again")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    # Check if requirement.txt exists
    if os.path.exists('requirement.txt'):
        print("📄 Found requirement.txt, installing from file...")
        try:
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirement.txt'
            ], capture_output=True, text=True, check=True)
            print("✅ Dependencies installed successfully from requirement.txt")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing from requirement.txt: {e}")
            print("Trying individual package installation...")
    
    # Install packages individually
    packages = [
        'pandas>=1.3.0',
        'numpy>=1.20.0', 
        'matplotlib>=3.3.0',
        'flask>=2.0.0',
        'openpyxl>=3.0.0',
        'jinja2>=3.0.0',
        'schedule>=1.1.0'
    ]
    
    print("📦 Installing packages individually...")
    for package in packages:
        try:
            print(f"   Installing {package}...")
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', package
            ], capture_output=True, text=True, check=True)
            print(f"   ✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}: {e}")
            return False
    
    print("✅ All dependencies installed successfully")
    return True

def verify_installation():
    """Verify that all required packages are installed"""
    print("\n🔍 Verifying installation...")
    
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'flask', 
        'openpyxl', 'jinja2', 'schedule'
    ]
    
    all_installed = True
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NOT INSTALLED")
            all_installed = False
    
    if all_installed:
        print("\n🎉 All dependencies are properly installed!")
        return True
    else:
        print("\n❌ Some dependencies failed to install")
        print("Please try running: pip install -r requirement.txt")
        return False

def test_imports():
    """Test importing project modules"""
    print("\n🧪 Testing project modules...")
    
    try:
        from etl_processor import ETLProcessor
        print("   ✅ ETL Processor")
    except ImportError as e:
        print(f"   ❌ ETL Processor: {e}")
        return False
    
    try:
        from web_server import app
        print("   ✅ Web Server")
    except ImportError as e:
        print(f"   ❌ Web Server: {e}")
        return False
    
    try:
        from data_processor import generate_report
        print("   ✅ Data Processor")
    except ImportError as e:
        print(f"   ❌ Data Processor: {e}")
        return False
    
    print("✅ All project modules imported successfully")
    return True

def create_sample_data():
    """Create sample data for testing"""
    print("\n📁 Creating sample data...")
    
    sample_data = """Date,Product,Category,Sales,Quantity,Region,Profit
2024-01-01,Widget A,Electronics,1500,10,North,300
2024-01-02,Widget B,Electronics,2200,15,South,440
2024-01-03,Gadget X,Electronics,1800,12,East,360
2024-01-04,Tool Y,Hardware,1200,8,West,240
2024-01-05,Widget A,Electronics,1600,11,North,320
2024-01-06,Gadget Z,Electronics,2500,18,South,500
2024-01-07,Tool X,Hardware,900,6,East,180
2024-01-08,Widget C,Electronics,1900,13,West,380
2024-01-09,Gadget Y,Electronics,2100,14,North,420
2024-01-10,Tool Z,Hardware,1100,7,South,220"""
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    sample_file = 'data/sample_detailed.csv'
    with open(sample_file, 'w') as f:
        f.write(sample_data)
    
    print(f"   ✅ Created {sample_file}")
    
    # Create reports directory
    os.makedirs('reports', exist_ok=True)
    print("   ✅ Created reports directory")
    
    return True

def main():
    """Main installation function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Verify installation
    if not verify_installation():
        return False
    
    # Test project imports
    if not test_imports():
        return False
    
    # Create sample data
    if not create_sample_data():
        return False
    
    print("\n" + "=" * 60)
    print("🎉 INSTALLATION COMPLETE!")
    print("=" * 60)
    print("✅ All dependencies installed")
    print("✅ Project modules verified")
    print("✅ Sample data created")
    print("\n🚀 You can now run PROJECT NIV:")
    print("   python3 run_once.py --interactive")
    print("   python3 run_once.py --csv data/sample_detailed.csv --web")
    print("   python3 main.py --mode etl --csv data/sample_detailed.csv")
    print("\n📚 Read the guide: STEP_BY_STEP_GUIDE.md")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)