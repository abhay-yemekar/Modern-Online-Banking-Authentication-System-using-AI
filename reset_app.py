import os
import shutil

files_to_delete = ["users.db", "face.db", "trainingdata.yml"]
folders_to_delete = ["data"]

for f in files_to_delete:
    if os.path.exists(f):
        os.remove(f)
        print(f"Deleted {f}")

for folder in folders_to_delete:
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"Deleted folder {folder}")

print("✅ App reset complete. Fresh start ready.")
