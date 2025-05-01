# scripts/backup_db.py
import os, shutil, datetime

# 1) find the project root ("habit_tracker")
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 2) point to the real DB under app/
db_path = os.path.join(project_root, "app", "app.db")

# 3) ensure backups/ exists alongside scripts/
backups_dir = os.path.join(project_root, "backups")
os.makedirs(backups_dir, exist_ok=True)

# 4) timestamp and copy
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
dst = os.path.join(backups_dir, f"app_{timestamp}.db")
shutil.copy2(db_path, dst)

print(f"Backed up DB from\n  {db_path}\n→\n  {dst}")
print("Backup complete!")