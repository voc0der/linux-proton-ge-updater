# GE-Proton Updater

This repository provides a Python script to automate the process of downloading, extracting, and configuring the latest release of GE-Proton for use with Steam.

## Features
- Fetches the latest GE-Proton release from the [GitHub releases page](https://github.com/GloriousEggroll/proton-ge-custom/releases).
- Automatically extracts the release to `~/.steam/root/compatibilitytools.d/`.
- Removes any existing GE-Proton installations to avoid conflicts.
- Updates the `config.vdf` file to ensure all apps using GE-Proton are set to the latest version.
- Simplifies the setup process for GE-Proton on Linux systems.

## Requirements
- Python 3.6+
- Dependencies:
  - `requests`
  - `BeautifulSoup4`
  - `psutil`

Install the required dependencies using pip:
```bash
pip install requests beautifulsoup4 psutil
```

## Installation
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Make the script executable:
   ```bash
   chmod +x update-ge-proton.py
   ```

## Usage
1. Ensure Steam is not running.
2. Run the script:
   ```bash
   python3 update-ge-proton.py
   ```
3. The script will:
   - Fetch the latest tag from the [Tags page](https://github.com/GloriousEggroll/proton-ge-custom/tags).
   - Download the corresponding `.tar.gz` file.
   - Extract it into `~/.steam/root/compatibilitytools.d/`.
   - Update the `config.vdf` file to point to the new version.
4. Restart Steam and select the latest GE-Proton version under Steam Play settings.

## Troubleshooting
- **FileNotFoundError:** Ensure the `~/.steam/root/compatibilitytools.d/` directory exists and has the proper permissions.
- **No `.tar.gz` file found:** Confirm that the latest release has an associated `.tar.gz` file.
- **Permissions issues:** Run the script with `sudo` if necessary, but it is recommended to adjust permissions instead.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to improve the script.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- Thanks to GloriousEggroll for maintaining GE-Proton.
- Inspired by the needs of Linux gamers to simplify Proton configuration for Steam.

