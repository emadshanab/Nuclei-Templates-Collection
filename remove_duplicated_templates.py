#!/usr/bin/env python3
# This shebang line specifies the Python 3 interpreter to use for executing this script.

import os
import shutil
import hashlib

category_map = {
    "wordpress": ["wp", "wordpress"],
    "xss": ["xss"],
    "sql_injection": ["sqli", "sql_injection"],
    "local_file_inclusion": ["lfi"],
    "remote_code_execution": ["rce"],
    "cross_site_request_forgery": ["csrf"],
    "xml_external_entity": ["xxe"],
    "cve": ["cve", "cnvd", "cnnvd", "cnnvd"],
    "open_redirect": ["redirect", "open_redirect"],
    "ssrf": ["ssrf", "server_side_request_forgery"],
    "subdomain_takeover": ["subdomain_takeover", "takeover"],
    "template_injection": ["template_injection", "ssti"],
    "crlf_injection": ["crlf_injection", "crlf"],
    "directory_listing": ["directory_listing", "traversal"],
    "exposed": ["exposed", "disclosure", "sensitive", "exposure"],
    "adobe": [
        "adobe",
        "aem",
    ],
    "coldfusion": ["coldfusion", "cfm"],
    "drupal": ["drupal"],
    "joomla": ["joomla"],
    "magento": ["magento"],
    "php": ["php"],
    "airflow": ["airflow"],
    "aws": ["aws", "amazon", "ec2", "s3", "lambda", "cloudfront", "cloudfront"],
    "apache": ["apache"],
    "cpanel": ["cpanel"],
    "docker": ["docker", "container", "kubernetes"],
    "git": ["git"],
    "jenkins": ["jenkins"],
    "cisco": ["cisco"],
    "api": ["api"],
    "upload": ["upload"],
    "sensitive": ["sensitive"],
    "debug": ["debug"],
    "backup": ["backup"],
    "auth": [
        "auth",
        "login",
        "signin",
        "sign_in",
        "sign-in",
        "oauth",
        "sso",
        "register",
        "signup",
        "sign_up",
        "sign-up",
        "password",
        "pwd",
        "passwd",
        "secret",
        "token",
        "credential",
        "cred",
        "jwt",
        "cookie",
        "session",
        "remember",
        "keycloak",
        "key",
    ],
    "atlassian": ["atlassian", "jira", "confluence", "bitbucket", "bamboo"],
    "config": ["config", "conf", "configuration"],
    "mysql": ["mysql", "mariadb"],
    "sql": ["sql", "database", "db"],
    "default": ["default"],
    "detect": ["detect"],
    "extract": ["extract"],
    "fuzz": ["fuzz"],
    "graphql": ["graphql"],
    "http": ["http"],
    "social": [
        "social",
        "social_media",
        "facebook",
        "twitter",
        "instagram",
        "linkedin",
    ],
    "favicon": ["favicon"],
    "python": ["python", "flask", "django"],
    "ftp": ["ftp"],
    "gcloud": ["gcloud", "google_cloud", "gcp"],
    "google": ["google"],
    "graphite": ["graphite"],
    "header": ["header"],
    "injection": ["injection"],
    "ibm": ["ibm"],
    "search": ["search"],
    "ldap": ["ldap"],
    "microsoft": ["microsoft", "ms"],
    "mongodb": ["mongodb", "mongo"],
    "netlify": ["netlify"],
    "oracle": ["oracle"],
    "java": [
        "java",
        "jsp",
        "jsf",
        "j2ee",
        "j2se",
        "j2me",
        "jvm",
        "jre",
        "jdk",
        "jboss",
        "tomcat",
        "glassfish",
        "wildfly",
        "jetty",
        "websphere",
        "weblogic",
        "spring",
        "struts",
        "hibernate",
        "mybatis",
        "shiro",
    ],
    "javascript": ["javascript", "js"],
    "elk": ["elk", "elasticsearch", "kibana", "logstash"],
    "kafka": ["kafka"],
    "kong": ["kong"],
    "laravel": ["laravel"],
    "nginx": ["nginx"],
    "nodejs": ["nodejs", "node", "express", "npm"],
    "perl": ["perl"],
    "postgres": ["postgres", "postgresql"],
    "rabbitmq": ["rabbitmq"],
    "redis": ["redis"],
    "ruby": ["ruby", "rails"],
    "samba": ["samba"],
    "sharepoint": ["sharepoint"],
    "smtp": ["smtp"],
    "sap": ["sap"],
    "shopify": ["shopify"],
    "ssh": ["ssh"],
    "vmware": ["vmware"],
    "web": ["web"],
}


def get_all_yaml_files(dir_path):
    """
    Returns a dictionary of all YAML files in the directory, including subdirectories.
    The keys are filenames, and values are their full paths.
    """
    all_yaml_files = {}
    for dirpath, dirs, files in os.walk(dir_path):
        dirs[:] = [
            d for d in dirs if d != ".git" and d != "projectdiscovery__nuclei-templates"
        ]  # Ignore .git and source of truth directories
        for filename in files:
            if filename.endswith(".yml") or filename.endswith(".yaml"):
                all_yaml_files[filename] = os.path.join(dirpath, filename)
    return all_yaml_files


def categorize_file(file_name, category_map):
    """
    Determines the categories of a file based on its name and the category map.
    Returns a list of all matching categories.
    """
    categories = []
    for category, keywords in category_map.items():
        if any(keyword in file_name.lower() for keyword in keywords):
            categories.append(category)
    return (
        categories if categories else ["other"]
    )  # Return "other" category if no match is found


def file_hash(file_path):
    """Calculate the MD5 hash of a file's contents."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def copy_file_to_categories(
    file_path, base_dir, category_map, category_counts, file_hashes
):
    """
    Copies the file to directories based on its vulnerability categories.
    Avoids duplicates within the same category based on file hash.
    Updates category_counts and file_hashes dictionaries.
    """
    categories = categorize_file(os.path.basename(file_path), category_map)
    file_hash_value = file_hash(file_path)
    for category in categories:
        target_dir = os.path.join(base_dir, category)
        os.makedirs(target_dir, exist_ok=True)

        # Check for duplicate file hash in the same category
        if file_hash_value not in file_hashes.get(category, set()):
            shutil.copy(
                file_path, os.path.join(target_dir, os.path.basename(file_path))
            )
            category_counts[category] = category_counts.get(category, 0) + 1
            file_hashes.setdefault(category, set()).add(file_hash_value)


def get_file_size(file_path):
    """
    Returns the size of a file in bytes.
    """
    return os.path.getsize(file_path)


community_path = "community-templates"
source_of_truth = "community-templates/projectdiscovery__nuclei-templates"
output_path = "categorized_templates"

community = get_all_yaml_files(community_path)
nucleiTemplates = get_all_yaml_files(source_of_truth)

common_templates = set(community.keys()) & set(nucleiTemplates.keys())

# Category count and file hash dictionaries
category_counts = {}
file_hashes = {}

# Process all community templates
for template, community_file in community.items():
    if template in common_templates and get_file_size(community_file) == get_file_size(
        nucleiTemplates[template]
    ):
        os.remove(community_file)  # Delete duplicate
        continue

    copy_file_to_categories(
        community_file, output_path, category_map, category_counts, file_hashes
    )

# Output category counts
print("Number of files in each category after processing:")
for category, count in category_counts.items():
    print(f"{category}: {count}")
