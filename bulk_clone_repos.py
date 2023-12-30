import os
import subprocess

# File containing repository URLs
repo_file = "README.md"

# Directory to clone into
clone_dir = "community-templates"

# Ensure the clone directory exists
os.makedirs(clone_dir, exist_ok=True)

# Read repository URLs from file and remove duplicates
with open(repo_file, 'r') as file:
    urls = list(set(line.strip() for line in file if line.strip()))

# Process each repository
for url in urls:
    # Extract the owner and repo name from the URL
    parts = url.split('/')
    if len(parts) >= 2:
        owner, repo_name = parts[-2], parts[-1]
        target_dir = os.path.join(clone_dir, f"{owner}__{repo_name}".lower())
    else:
        continue  # Skip if the URL format is incorrect

    if os.path.isdir(target_dir):
        # If directory exists, pull changes
        print(f"Updating {repo_name} in {target_dir}")
        subprocess.run(["git", "-C", target_dir, "pull"])
    else:
        # If directory does not exist, clone repository
        print(f"Cloning {repo_name} into {target_dir}")
        subprocess.run(["git", "clone", url, target_dir])
