import os
import shutil

workspace = os.getcwd()

# Folders to create
scripts_dir = os.path.join(workspace, 'scripts')
data_dir = os.path.join(workspace, 'data')

os.makedirs(scripts_dir, exist_ok=True)
os.makedirs(data_dir, exist_ok=True)

# Important core files to keep in root:
core_files = {
    'README.md',
    'agents.md',
    'AGENTS.md',
    'Sensebar_AI_Agent_Videos_Full_Version.md',
    'sensebar_urls_for_notebooklm.txt',
    'sensebar_ai_agent_videos.md',
    '.gitignore',
    '.git',
    '有用資料',
    'scripts',
    'data',
    'organize_workspace.py'
}

all_items = os.listdir(workspace)

moved_scripts = []
moved_data = []
deleted_temp = []

for item in all_items:
    if item in core_files:
        continue

    item_path = os.path.join(workspace, item)
    
    if os.path.isfile(item_path):
        # Temporary test/dump files to delete
        if item.startswith('test_') or item.startswith('inspect_') or item.startswith('verify_'):
            try:
                os.remove(item_path)
                deleted_temp.append(item)
            except Exception as e:
                print(f"Error removing {item}: {e}")
        # Data JSON files
        elif item.endswith('.json'):
            try:
                shutil.move(item_path, os.path.join(data_dir, item))
                moved_data.append(item)
            except Exception as e:
                print(f"Error moving {item}: {e}")
        # Helper Python scripts
        elif item.endswith('.py'):
            try:
                shutil.move(item_path, os.path.join(scripts_dir, item))
                moved_scripts.append(item)
            except Exception as e:
                print(f"Error moving {item}: {e}")

print(f"Moved {len(moved_scripts)} python scripts to scripts/")
print(f"Moved {len(moved_data)} JSON data files to data/")
print(f"Cleaned up {len(deleted_temp)} temporary test files.")
