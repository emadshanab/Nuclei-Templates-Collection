import os

def get_all_files(dir_path):
    # Dict to store all templates names and their full paths
    all_files = {}

    # Traverse directory tree
    for dirpath, dirs, files in os.walk(dir_path):

        # Ignore .git directories
        dirs[:] = [d for d in dirs if d != '.git']

        # Add each template name and its path to the dict
        for filename in files:
            all_files[filename] = os.path.join(dirpath, filename)

    return all_files

community_path = 'community-templates'
nucleiTemplates_path = 'nuclei-templates'

community = get_all_files(community_path)
nucleiTemplates = get_all_files(nucleiTemplates_path)

# Find templates that are in the nuclei-templates directory but not the community-templates
diff_templates = set(community.keys()) - set(nucleiTemplates.keys())

# Find templates that are in both the community and nuclei templates directories
common_templates = set(community.keys()) & set(nucleiTemplates.keys())  # use intersection operation to find common files

print("Community templates: ", len(community))
print("Common templates: ", len(common_templates))

# Remove the common files from the community directory
for template in common_templates:
    os.remove(community[template])  # remove the file using its full path

# Recheck the community templates
community = get_all_files(community_path)
print("Community templates after removal: ", len(community))
