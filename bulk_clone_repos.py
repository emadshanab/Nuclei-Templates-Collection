import os
import hashlib

# File containing repository URLs
repo_file = "README.md"

# Directory to clone into
clone_dir = "community-templates"

# Read repository URLs from file and remove duplicates
with open(repo_file, 'r') as file:
    urls = list(set(line.strip() for line in file if line.strip()))

# Clone each repository
for url in urls:
    # Hash the URL to create a unique directory name
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:10]
    
    # Create a unique directory name with the separator
    target_dir = os.path.join(clone_dir, f"{os.path.basename(url)}__{url_hash}")

    os.system(f"git clone {url} {target_dir}")
