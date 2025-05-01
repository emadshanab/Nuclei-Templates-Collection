#!/usr/bin/env python3

import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

repo_file = "README.txt"
clone_dir = "community-templates"
max_threads = 10  # Adjust based on your system/network capability

# Ensure the clone directory exists
os.makedirs(clone_dir, exist_ok=True)

# Read repository URLs and remove duplicates
with open(repo_file, 'r') as file:
    urls = list(set(line.strip() for line in file if line.strip()))

def process_repo(url):
    parts = url.split('/')
    if len(parts) < 2:
        return f"❌ Invalid URL format: {url}"

    owner, repo_name = parts[-2], parts[-1]
    target_dir = os.path.join(clone_dir, f"{owner}__{repo_name}".lower())

    if os.path.isdir(target_dir):
        try:
            subprocess.run(
                ["git", "-C", target_dir, "pull"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            return f"🔄 Updated: {repo_name}"
        except subprocess.CalledProcessError:
            return f"⚠️ Failed to update: {repo_name}"
    else:
        try:
            subprocess.run(
                ["git", "clone", url, target_dir],
                env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            return f"✅ Cloned: {repo_name}"
        except subprocess.CalledProcessError:
            return f"❌ Skipped (private or error): {url}"

# Run cloning/updating in parallel
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    futures = [executor.submit(process_repo, url) for url in urls]

    for future in as_completed(futures):
        print(future.result())
