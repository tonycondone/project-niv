# 🚀 PROJECT NIV - Setup & Run Guide

## ❌ **Common Error Fix**

If you're getting npm errors like "Missing script: backend", it's because **PROJECT NIV is a Python project**, not a Node.js project!

## ✅ **Correct Way to Run PROJECT NIV**

### **Option 1: Direct Python Commands (Recommended)**
```bash
# 1. Install Python dependencies
pip install -r requirement.txt

# 2. Run the production system
python production_main.py

# 3. Or run the flexibility demo
python demo_flexibility.py
```

### **Option 2: Using npm (Now Fixed)**
```bash
# Install dependencies
npm run install

# Run the backend (calls Python)
npm run backend

# Run demo
npm run demo

# Run dashboard demo
npm run dashboard
```

### **Option 3: Easy Start Scripts**

**Windows:**
```cmd
# Double-click or run:
start.bat
```

**Linux/Mac:**
```bash
# Run:
./start.sh
```

**Cross-platform:**
```bash
python run.py
```

---

## 🎯 **What Each Command Does**

| Command | Description | What It Runs |
|---------|-------------|--------------|
| `python production_main.py` | **Main production system** - works with any CSV | Interactive dashboard system |
| `python demo_flexibility.py` | **Flexibility demo** - shows system adapting to 5 different datasets | Comprehensive demonstration |
| `python dashboard_demo.py` | **Dashboard demo** - standalone KPI dashboard | Single dashboard generation |
| `python main.py` | **Original enhanced system** - with rich terminal UI | Original workflow with enhancements |
| `npm run backend` | **Run via npm** - calls Python production system | Same as `python production_main.py` |

---

## 📋 **Prerequisites**

### **Required:**
- **Python 3.8+** (Download from [python.org](https://python.org))
- **pip** (Usually comes with Python)

### **Optional:**
- **Node.js 16+** (Only if you want to use npm commands)

---

## 🔧 **Installation Steps**

### **Step 1: Verify Python Installation**
```bash
python --version
# Should show Python 3.8 or higher
```

### **Step 2: Install Dependencies**
```bash
pip install -r requirement.txt
```

### **Step 3: Test the System**
```bash
# Quick test with sample data
python production_main.py --dataset data/sample.csv

# Or run the comprehensive demo
python demo_flexibility.py
```

---

## 🎨 **What You'll See**

### **Beautiful Terminal Interface:**
```
🚀 PROJECT NIV - PRODUCTION DASHBOARD SYSTEM

📊 Dataset Overview
┌─────────────────┬─────────────────┐
│ Metric          │ Value           │
├─────────────────┼─────────────────┤
│ Rows            │ 4               │
│ Columns         │ 2               │
│ Detected Type   │ Sales Data      │
│ Confidence      │ 14.3%           │
│ Data Quality    │ 100.0% complete │
└─────────────────┴─────────────────┘
```

### **Professional Dashboards:**
- Tableau-style KPI cards
- Adaptive visualizations
- Business intelligence insights
- Export-ready charts

---

## 🎯 **Sample Datasets Included**

The system comes with 5 sample datasets to demonstrate flexibility:

1. **`data/sample.csv`** - Sales data
2. **`data/customer_data.csv`** - Customer analytics
3. **`data/financial_data.csv`** - Financial statements
4. **`data/inventory_data.csv`** - Inventory management
5. **`data/web_analytics.csv`** - Web analytics

---

## 🚀 **Quick Start Examples**

### **Analyze Your Own Data:**
```bash
python production_main.py --dataset /path/to/your/data.csv
```

### **Batch Process Multiple Files:**
```bash
python production_main.py --batch /path/to/data/directory
```

### **See System Flexibility:**
```bash
python demo_flexibility.py
```

---

## ❓ **Troubleshooting**

### **Error: "Missing script: backend"**
- **Problem:** You're trying to run a Python project with npm
- **Solution:** Use `python production_main.py` instead

### **Error: "No module named 'pandas'"**
- **Problem:** Dependencies not installed
- **Solution:** Run `pip install -r requirement.txt`

### **Error: "python: command not found"**
- **Problem:** Python not installed or not in PATH
- **Solution:** Install Python from [python.org](https://python.org)

### **Error: "Permission denied"**
- **Problem:** Script not executable (Linux/Mac)
- **Solution:** Run `chmod +x start.sh`

---

## 🎉 **Success Indicators**

You'll know it's working when you see:
- ✅ Beautiful colored terminal output
- ✅ Progress bars and spinners
- ✅ Professional KPI cards
- ✅ Generated dashboard files in `reports/` folder
- ✅ Business intelligence insights

---

## 📞 **Need Help?**

1. **Check this guide first** - Most issues are covered here
2. **Run the demo** - `python demo_flexibility.py` shows if everything works
3. **Check dependencies** - `python run.py --check`
4. **Use the helper script** - `python run.py` for interactive setup

---

**PROJECT NIV is ready to analyze any CSV dataset and create professional dashboards!** 🚀📊