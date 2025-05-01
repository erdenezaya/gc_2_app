import os, glob, shutil

# locate project root and paths
root       = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
backups    = os.path.join(root, "backups", "*.db")
live_db    = os.path.join(root, "app", "app.db")

# pick latest
candidates = glob.glob(backups)
latest     = max(candidates, key=os.path.getmtime)

# overwrite
shutil.copy2(latest, live_db)
print(f"Restored {latest} → {live_db}")
