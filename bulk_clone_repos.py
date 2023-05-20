import os

# File containing repository URLs
repo_file = "templates-repos.txt"

# Directory to clone into
clone_dir = "community-templates"

# Read repository URLs from file
with open(repo_file, 'r') as file:
    repos = [line.strip() for line in file if line.strip()]

# Clone each repository
for repo in repos:
    os.system(f"git clone {repo} {clone_dir}/{os.path.basename(repo)}")
