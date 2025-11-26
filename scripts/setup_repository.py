import os
import shutil
from pathlib import Path

def setup_repository_structure():
    """Setup perfect GitHub repository structure"""
    
    base_dir = Path(".")
    
    # Create directories
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
        print(f"Created directory: {directory}")
    
    # Copy current src files to milestones/ml3
    src_files = [
        "main.py", "cli.py", "crypto.py", "modes.py", 
        "csprng.py", "file_utils.py", "utils.py"
    ]
    
    for file in src_files:
        src_path = base_dir / "src" / file
        if src_path.exists():
            # Copy to ml3 (current version)
            shutil.copy2(src_path, base_dir / "milestones/ml3/src" / file)
            print(f"Copied {file} to milestones/ml3/src/")
    
    # Copy test files
    test_files = ["test_csprng.py", "test_modes.py", "test_crypto.py"]
    for test_file in test_files:
        src_path = base_dir / "tests" / test_file
        if src_path.exists():
            shutil.copy2(src_path, base_dir / "milestones/ml3/tests" / test_file)
            print(f"Copied {test_file} to milestones/ml3/tests/")
    
    # Create requirements files
    requirements_content = "pycryptodome==3.19.0\n"
    
    for ml in ["ml1", "ml2", "ml3"]:
        req_path = base_dir / "milestones" / ml / "requirements.txt"
        with open(req_path, "w", encoding="utf-8") as f:
            f.write(requirements_content)
        print(f"Created milestones/{ml}/requirements.txt")
    
    print("Repository structure setup completed!")

if __name__ == "__main__":
    setup_repository_structure()