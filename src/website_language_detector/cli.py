import argparse
from pathlib import Path
from urllib.parse import urlparse

try:
    from .detector import fetch_text_from_url, detect_language, normalise_url
except ModuleNotFoundError as e:
    missing = str(e).split("'")[1]
    print(f"ERROR: Missing required module: {missing}\n")
    print(f"It looks like some dependencies are not installed. You")
    print(f"may need to activate the virtual environment:")
    print(f"    source venv/bin/activate\n")
    print(f"If no virtual environment exists, please ensure you have")
    print(f"correctly setup the program as detailed in the README.")
    raise SystemExit(1)

def prepare_output_file(output_file: str):
    """
    if the output file exists, ask for confirmation to overwrite.
    creates a new file with header "domain,language,confidence"
    :return: True if file is ready to write, False if user declined.
    """
    output_path = Path(output_file)
    if output_path.exists():
        confirmation = input(f"Output file '{output_file}' already exists. Overwrite it? [y/N]: ").strip().lower()
        if confirmation != "y":
            print("Aborting writing to output file.")
            return False

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("domain,language,confidence\n")
    return True

def process_url(url: str, lang: str, output_file=None):
    url = normalise_url(url)

    def attempt(u, lang):
        # attempt to get the (lang, confidence) for u.
        text = fetch_text_from_url(u, lang)
        lang = detect_language(text)
        print(f"{u}: {lang}")
        if output_file:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"{u},{lang}\n")

    try:
        attempt(url, lang)
    except Exception as e:
        # if the attempt failed, it *could* be because http:// was used,
        # but the website demands https://. If we used http://, try https:// instead.
        u = urlparse(url)
        parsed_scheme = u.scheme
        if parsed_scheme == "http":
            https_url = "https://" + u.netloc + u.path
            print(f"{url}: HTTP failed, retrying with HTTPs...")

            try:
                attempt(https_url, lang)
                return
            except Exception as e2:
                e2 = str(e2)
                print(f"{https_url}: ERROR - {e2[:17]+"..." if len(e2) > 20 else e2}")
                return

        # the attempt failed and was not http, give up
        e = str(e)
        print(f"{url}: ERROR - {e[:17]+"..." if len(e) > 20 else e}")

def main():
    parser = argparse.ArgumentParser(
        description="Detect the language of a webpage using BeautifulSoup and adbar/py3langid"
    )
    parser.add_argument("-u", "--url", help="Analyse a single URL")
    parser.add_argument("-f", "--file", help="Analyse multiple URLs from .csv/.txt file (one per line)")
    parser.add_argument("-o", "--output", help="Optional path to save the results")
    parser.add_argument("-l", "--lang", default="en", help="Preferred language for websites with multiple language redirects.")

    args = parser.parse_args()

    if not args.url and not args.file:
        parser.error("You must provide --url or --file")

    output_file = args.output
    if output_file:
        ready = prepare_output_file(output_file)
        if not ready:
            output_file = None

    if args.url:
        print(f"Detecting language for URL '{args.url}'...")
        process_url(args.url, args.lang, output_file)

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"ERROR: File not found: {file_path}")
            return

        print(f"Detecting language for each URL in '{file_path}'...")
        urls = [line.strip() for line in file_path.read_text().splitlines() if line.strip()]
        for url in urls:
            process_url(url, args.lang, output_file)

        if output_file:
            print(f"\nOutput saved to file '{output_file}'")

if __name__ == "__main__":
    main()