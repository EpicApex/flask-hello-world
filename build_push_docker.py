import subprocess
import sys
import re
import argparse
import os
import yaml

def read_current_version(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def increment_version(version, component):
    major, minor, patch = map(int, version.split('.'))
    
    if component == 'major':
        major += 1
    elif component == 'minor':
        minor += 1
    elif component == 'patch':
        patch += 1
    
    return f"{major}.{minor}.{patch}"

def build_docker_image(repo, version):
    tag = f"{repo}:{version}"
    subprocess.run(['docker', 'build', '-t', tag, '.'], check=True)
    return tag

def push_docker_image(tag):
    subprocess.run(['docker', 'push', tag], check=True)

def update_version_file(file_path, version):
    with open(file_path, 'w') as file:
        file.write(version)

def update_k8s_manifest(manifest_file, image_tag):
    with open(manifest_file, 'r') as file:
        # Load all documents from the YAML file
        documents = list(yaml.safe_load_all(file))

    for doc in documents:
        # Check if the document is a Deployment and has the specified name
        if doc.get('kind', '') == 'Deployment':
            # Update the image in the manifest
            container = doc['spec']['template']['spec']['containers'][0]  # First container
            current_image = container['image']
            new_image = f"{current_image.split(':')[0]}:{image_tag}"
            container['image'] = new_image

    # Write the updated documents back to the file
    with open(manifest_file, 'w') as file:
        yaml.dump_all(documents, file)

def main(repo, component, manifest_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    version_file_path = os.path.join(script_dir, "current_flask_app_version.txt")

    current_version = read_current_version(version_file_path)
    new_version = increment_version(current_version, component)
    tag = build_docker_image(repo, new_version)
    push_docker_image(tag)
    update_version_file(version_file_path, new_version)
    update_k8s_manifest(manifest_file, new_version)

    print(f"Successfully built and pushed {tag}. Updated version to {new_version} in {manifest_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Increment and update the version of a Docker image and Kubernetes manifest.')
    parser.add_argument('dockerhub_repo', type=str)
    parser.add_argument('component', choices=['major', 'minor', 'patch'])
    parser.add_argument('manifest_file', type=str)
    args = parser.parse_args()
    
    main(args.dockerhub_repo, args.component, args.manifest_file)
