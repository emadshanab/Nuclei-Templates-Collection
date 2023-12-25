"""
Filename: remove_duplicated_templates.py

This Python script is designed to identify and delete common templates across two directories, 'community-templates' and 'nuclei-templates'. 
It ensures that only unique templates remain in the 'community-templates' directory, reducing redundancy and saving storage space.

Workflow:
1. The script initially defines two directory paths, 'community-templates' and 'nuclei-templates'.
2. It calls the `get_all_files(dir_path)` function for each directory to retrieve all file names along with their full paths.
3. It finds the templates that exist in the 'nuclei-templates' directory but not in the 'community-templates' directory. 
   These are the templates unique to 'nuclei-templates'.
4. It also finds the templates that exist in both directories by performing an intersection operation on the template names.
5. The script prints the total number of templates in the 'community-templates' directory and the number of common templates between the two directories.
6. The script then removes all common templates from the 'community-templates' directory using their full paths stored in the dictionary.
7. After the deletion operation, it rechecks the 'community-templates' directory and prints the updated count of templates.

Dependencies: This script requires Python's built-in `os` module.
"""

import os

def get_all_yaml_files(dir_path):
    """
    This function takes a directory path as input and returns a dictionary containing the names of all YAML files in the directory
    (including subdirectories) as keys, with their corresponding full paths as values.
    """
    all_yaml_files = {}  # Dict to store all YAML file names and their full paths

    for dirpath, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d != '.git']  # Ignore .git directories
        for filename in files:
            if filename.endswith(".yml") or filename.endswith(".yaml"):
                all_yaml_files[filename] = os.path.join(dirpath, filename)  # Add each YAML file and its path to the dict

    return all_yaml_files

def get_file_size(file_path):
    # Function to get the size of a file in bytes
    return os.path.getsize(file_path)

community_path = 'community-templates'
nucleiTemplates_path = os.path.expanduser('~/.local/nuclei-templates')

community = get_all_yaml_files(community_path)
nucleiTemplates = get_all_yaml_files(nucleiTemplates_path)

# Find templates that are in the nuclei-templates directory but not in the community-templates
diff_templates = set(community.keys()) - set(nucleiTemplates.keys())

# Find templates that are in both the community and nuclei templates directories
common_templates = set(community.keys()) & set(nucleiTemplates.keys())

print("Community templates: ", len(community))
print("Common templates: ", len(common_templates))

# Create a log file to track duplicate files
log_file_path = "duplicate_files.log"

with open(log_file_path, "w") as log_file:
    log_file.write("Duplicate File\tCommunity Path\tCommunity Size\tNucleiTemplates Size\tNucleiTemplates Path\n")

    # Compare file sizes and rename or delete accordingly
    for template in common_templates:
        community_path = community[template]
        nucleiTemplates_path = nucleiTemplates[template]

        community_size = get_file_size(community_path)
        nucleiTemplates_size = get_file_size(nucleiTemplates_path)

        log_file.write(f"{template}\t{community_path}\t{community_size}\t{nucleiTemplates_size}\t{nucleiTemplates_path}\n")

        if community_size == nucleiTemplates_size:
            # Log duplicate file and delete the community template
            os.remove(community_path)
            print(f"Deleted duplicate: {template}")
        else:
            # Rename the community template with a prefix
            new_name = f"_dup__{template}"
            os.rename(community_path, os.path.join(os.path.dirname(community_path), new_name))
            print(f"Renamed: {template} to {new_name}")

# Recheck the community templates
community = get_all_yaml_files(community_path)
print("Community templates after removal and renaming: ", len(community))
