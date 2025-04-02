import os
import subprocess

# Step 1: Remove existing database
if os.path.exists("library.db"):
    os.remove("library.db")
    print("🗑️ Existing library.db deleted.")
else:
    print("✅ No previous database found. Fresh start!")

# Step 2: Recreate schema
print("📐 Creating schema...")
subprocess.run(["python", "schema.py"])

# Step 3: Populate data
print("📊 Populating database...")
subprocess.run(["python", "data.py"])

# Step 4: Create triggers
print("🔄 Creating triggers...")
subprocess.run(["python", "triggers.py"])

# Step 5: Success message
print("\n🎉 All done! Your library system is ready.")
print("▶️ To start, run one of the following:")
print("   python library_app.py   # for command-line interface")
print("   python library_gui.py   # for GUI")