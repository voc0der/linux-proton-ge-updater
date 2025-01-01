import os
import requests
import shutil
import subprocess
import tarfile
import psutil
from bs4 import BeautifulSoup

def close_steam():
    """Closes Steam if it's running."""
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'] == 'steam':
            print("Closing Steam...")
            process.terminate()
            process.wait()


def get_latest_release():
    """Fetches the latest release tarball URL by navigating from the Tags page and constructing the download link."""
    tags_url = "https://github.com/GloriousEggroll/proton-ge-custom/tags"
    print(f"Fetching the tags page: {tags_url}")
    response = requests.get(tags_url)
    print(f"HTTP status code: {response.status_code}")
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the latest tag (first matching tag link)
    tags = soup.find_all('a', href=True)
    for tag in tags:
        href = tag['href']
        if href.startswith("/GloriousEggroll/proton-ge-custom/releases/tag/"):
            latest_tag = href.split('/')[-1]  # Extract the tag name (e.g., GE-Proton9-22)
            print(f"Latest tag: {latest_tag}")

            # Construct the direct download URL for the .tar.gz file
            tarball_url = f"https://github.com/GloriousEggroll/proton-ge-custom/releases/download/{latest_tag}/{latest_tag}.tar.gz"
            print(f"Constructed tarball URL: {tarball_url}")
            return tarball_url, latest_tag

    raise RuntimeError("Could not find the latest release tag.")


def download_and_extract(url, extract_path):
    """Downloads and extracts the latest GE-Proton release."""
    filename = url.split("/")[-1]
    download_path = os.path.join("/tmp", filename)

    print(f"Downloading {url}...")
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(download_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)

    print(f"Extracting {download_path} to {extract_path}...")
    # Simplified extraction command
    subprocess.run(["tar", "-xf", download_path, "-C", extract_path], check=True)

    os.remove(download_path)
    print(f"Extraction complete. Installed to {extract_path}.")


def clean_old_ge_proton(directory):
    """Removes old GE-Proton directories."""
    for item in os.listdir(directory):
        if item.startswith("GE-Proton"):
            old_path = os.path.join(directory, item)
            print(f"Removing old GE-Proton folder: {old_path}")
            shutil.rmtree(old_path)


def update_config_vdf(config_path, new_version):
    """Updates the config.vdf file to use the new GE-Proton version."""
    with open(config_path, 'r') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        if '"name"' in line and 'GE-Proton' in line:
            line = line.split('"name"')[0] + f'"name"\t\t"{new_version}"\n'
        updated_lines.append(line)

    with open(config_path, 'w') as file:
        file.writelines(updated_lines)

    print("Updated config.vdf with the new GE-Proton version.")


def main():
    steam_root = os.path.expanduser("~/.steam/root")
    compatibility_dir = os.path.join(steam_root, "compatibilitytools.d")
    config_vdf_path = os.path.join(steam_root, "config/config.vdf")

    # Ensure the compatibility tools directory exists
    os.makedirs(compatibility_dir, exist_ok=True)

    # Step 1: Close Steam
    close_steam()

    # Step 2: Get the latest GE-Proton release
    latest_release_url, tag_name = get_latest_release()

    # Step 3: Clean old GE-Proton directories
    clean_old_ge_proton(compatibility_dir)

    # Step 4: Download and extract the new GE-Proton version
    download_and_extract(latest_release_url, compatibility_dir)

    # Step 5: Update config.vdf
    if os.path.exists(config_vdf_path):
        update_config_vdf(config_vdf_path, tag_name)
    else:
        print("config.vdf not found. Skipping configuration update.")

    print("All done! You can now restart Steam.")

if __name__ == "__main__":
    main()
