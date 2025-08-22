
import os
import shutil

project_name = "insurance"
folders = [".venv", "static", "templates", "data"]
files = {
    ".gitignore": """# Virtual environment
.venv/
__pycache__/
*.pyc

# Streamlit cache
.streamlit/

# OS files
.DS_Store
""",
    "requirements.txt": "streamlit\npandas\n",
    "showmydepends.txt": """Dependencies for Insurance App:
- streamlit: Web app framework
- pandas: Data handling (optional, for dependents list)
""",
    "README.md": """# Insurance Application

This is a simple **insurance cost estimation web app** built with [Streamlit](https://streamlit.io/).

## Features
- Collects user details: name, age, employment info.
- Select known health issues via checkboxes.
- Add multiple dependents under 18 years old.
- Displays estimated insurance cost dynamically.

## Installation
```bash
git clone <repo-url>
cd insurance
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```
""",

}
if __name__ == "__main__":
    # Create folders
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Create files
    for filename, content in files.items():
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    # Copy uploaded file if it exists
    uploaded_file = "/mnt/data/7aaa5542-2f88-49a3-a940-a0e47d9d6d62.csv"  # path in this session
    destination_file = os.path.join("data", "insurance_data.csv")
    if os.path.exists(uploaded_file):
        shutil.copy(uploaded_file, destination_file)