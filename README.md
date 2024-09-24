# LinkedIn AutoConnect

This script automates the process of sending connection requests on LinkedIn, helping you expand your professional network more efficiently.

## Features

- Automatically sends connection requests to targeted LinkedIn profiles
- Customizable connection message
- Rate limiting to avoid triggering LinkedIn's anti-automation measures
- Detailed logging of actions and results

## Prerequisites

- Python 3.7+
- Selenium WebDriver
- Chrome or Firefox browser

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/linkedin-connection-script.git
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Download the appropriate WebDriver for your browser and add it to your system PATH.

## Usage

1. Configure the script by editing `config.py`:

   - Set your LinkedIn credentials
   - Customize your search criteria and connection message

2. Run the script:

   ```
   python linkedin_connector.py
   ```

3. Monitor the console output and log file for progress and results.
