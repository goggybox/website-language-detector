# Website Language Detector
A simple tool written in Python that detects the language of a webpage using [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) and [adbar/py3langid](https://github.com/adbar/py3langid).

This tool scrapes webpage text using **BeautifulSoup** and detects the language using **py3langid**. It accepts as input a single URL or a file of URLs (one per line), and optionally outputs to a file.

## Features
- Detect language for a single URL or multiple URLs from a `.txt` or `.csv` file.
- Webpages that are too short to detect are defaulted to English.
- Automatically adds `http://` to any URL provided without a scheme.
- Provides a `--lang` option to specify a default language (in ISO 639-1 format) for websites that redirect based on language preferences.
- If an `HTTP` URL is provided, but the website requires an `HTTPS` connection, the tool automatically retries with `HTTPS`.
- Save results to an output CSV file with headers: `domain,language`.
- Simple CLI interface using `web-lang`.

## Installation

### 1. Clone the repository
```
git clone https://github.com/goggybox/website-language-detector.git
cd website-language-detector
```

### 2. Run the installation script
```
./install.sh
```
This will create a virtual environment, install dependencies, and set up the CLI.

## Usage

### Activating the virtual environment
The CLI depends on the Python virtual environment established during installation, so it must be activated before using the program.
```
source venv/bin/activate
```

### Single URLs
The program can be used to detect the language of a single URL:
```
> web-lang -u google.co.uk
Detecting language for URL 'google.co.uk'...
http://google.co.uk: en
```

### Multiple URLs from a file
The program can be used to detect multiple URLs at a time. The URLs must be given in a `.txt` or `.csv` file with one domain per line, e.g.:
```
google.co.uk
github.com
```
The language of each website can then be detected as follows:
```
> web-lang -f file.txt
Detecting language for each URL in 'file.txt'...
http://google.co.uk: en
http://github.com: en
```

### Output to CSV
The program can output the detected languages to a `.txt` or `.csv` file:
```
> web-lang -f file.txt -o results.csv
```
Which produces a file of the format:
```
domain,language
http://google.co.uk,en
http://github.com,en
```

### Optional arguments
- `-l` - preferred language for websites with multiple language redirects (if not provided, defaults to `en`).
- `-h` - shows the help message.

### Help menu
The help menu can be used to display all features available.
```
> web-lang -h
usage: web-lang [-h] [-u URL] [-f FILE] [-o OUTPUT] [-l LANG]

Detect the language of a webpage using BeautifulSoup and adbar/py3langid

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Analyse a single URL
  -f FILE, --file FILE  Analyse multiple URLs from .csv/.txt file (one
                        per line)
  -o OUTPUT, --output OUTPUT
                        Optional path to save the results
  -l LANG, --lang LANG  Preferred language for websites with multiple
                        language redirects.
```

## Dependencies
All dependencies are listed in `requirements.txt`, and are automatically installed with the `install.sh` script.
- Python 3.9+ (not tested with earlier versions)
- [py3langid](https://github.com/adbar/py3langid)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [requests](https://pypi.org/project/requests/)

## License
This project is released under the GNU General Public License v3.0.
