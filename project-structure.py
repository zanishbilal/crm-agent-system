import os

base = "app"

folders = [
    f"{base}/agents",
    f"{base}/tools",
    f"{base}/config"
]

files = [
    "requirements.txt",
    "README.md",
    f"{base}/main.py",
    f"{base}/__init__.py",
    f"{base}/config/config.json",
    f"{base}/tools/__init__.py",
    f"{base}/tools/hubspot_tools.py",
    f"{base}/tools/email_tools.py",
    f"{base}/agents/__init__.py",
    f"{base}/agents/orchestrator_agent.py"
]

def create_structure():
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"📁 Created folder: {folder}")
    
    for file in files:
        open(file, "a").close()
        print(f"📄 Created file: {file}")

if __name__ == "__main__":
    create_structure()
    print("\n✅ Clean structure created inside 'app/'. Now ready to start coding.")
