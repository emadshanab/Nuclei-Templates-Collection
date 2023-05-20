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

def get_all_files(dir_path):
    """
    This function takes a directory path as input and returns a dictionary containing the names of all files in the directory 
    (including subdirectories) as keys, with their corresponding full paths as values.
    """
    all_files = {}  # Dict to store all templates names and their full paths

    for dirpath, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d != '.git']  # Ignore .git directories
        for filename in files:
            all_files[filename] = os.path.join(dirpath, filename)  # Add each template name and its path to the dict

    return all_files

community_path = 'community-templates'
nucleiTemplates_path = 'nuclei-templates'

community = get_all_files(community_path)
nucleiTemplates = get_all_files(nucleiTemplates_path)

# Find templates that are in the nuclei-templates directory but not the community-templates
diff_templates = set(community.keys()) - set(nucleiTemplates.keys())

# Find templates that are in both the community and nuclei templates directories
common_templates = set(community.keys()) & set(nucleiTemplates.keys())  # use intersection operation to find common templates

print("Community templates: ", len(community))
print("Common templates: ", len(common_templates))

# Remove the common files from the community directory
for template in common_templates:
    os.remove(community[template])  # remove the template using its full path

# Recheck the community templates
community = get_all_files(community_path)
print("Community templates after removal: ", len(community))
