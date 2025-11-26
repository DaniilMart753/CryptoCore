# fix_structure.py
import os
import shutil
from pathlib import Path

def fix_structure():
    """Fix the repository structure"""
    base_dir = Path(".")
    
    print("Fixing repository structure...")
    
    # Create correct directory structure
    directories = [
        "milestones/ml1/src",
        "milestones/ml1/tests",
        "milestones/ml2/src", 
        "milestones/ml2/tests",
        "milestones/ml3/src",
        "milestones/ml3/tests",
        "tests",
        "docs",
        "scripts"
    ]
    
    for directory in directories:
        (base_dir / directory).mkdir(parents=True, exist_ok=True)
        print(f"Created {directory}")
    
    # Copy current files to milestones/ml3
    src_files = ["main.py", "cli.py", "crypto.py", "modes.py", "csprng.py", "file_utils.py", "utils.py"]
    
    for file in src_files:
        src_path = base_dir / "src" / file
        if src_path.exists():
            dst_path = base_dir / "milestones/ml3/src" / file
            shutil.copy2(src_path, dst_path)
            print(f"Copied {file} to milestones/ml3/src/")
    
    print("Structure fixed successfully!")

if __name__ == "__main__":
    fix_structure()