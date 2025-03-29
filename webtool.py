import urllib.request
from bs4 import BeautifulSoup
import re
import chardet

def clean_text(text):
    # Remove non-printable characters using regex
    return re.sub(r'[^\x20-\x7E]', '', text)

def get_info_from_website(url):
    # Create a request object with a User-Agent
    req = urllib.request.Request(url, headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
})

    # Make the request and read the response
    with urllib.request.urlopen(req) as response:
        html_bytes = response.read()

    # Detect encoding using chardet
        result = chardet.detect(html_bytes)
        encoding = result['encoding']

    # Decode the HTML content using the detected encoding
    # Try decoding using detected encoding first
    try:
        html = html_bytes.decode(encoding)
    except (UnicodeDecodeError, TypeError, LookupError):
        # Fallback to encodings that support Hebrew
        for fallback_encoding in ['utf-8', 'windows-1255', 'iso-8859-8']:
            try:
                html = html_bytes.decode(fallback_encoding)
                break
            except (UnicodeDecodeError, LookupError):
                continue
        else:
            # If all decoding attempts fail, print an error message
            print("Failed to decode the response with Hebrew-compatible encodings.")
            return ""
    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Remove all HTML tags; you can customize this to format as Markdown
    text = []
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'li']):
        cleaned_text = element.get_text()  # Clean the text here
        text.append(cleaned_text)

    # Join the text into a single string, converting it to Markdown format
    markdown_content = '\n\n'.join(text)  # Separate sections by new lines

    return markdown_content


# Example usage
if __name__ == "__main__":
    url = "https://www.10dakot.co.il/recipe/%D7%A4%D7%90%D7%93-%D7%AA%D7%90%D7%99/"
    markdown_content = get_info_from_website(url)
    if markdown_content:
        print("Content fetched successfully:")
        print(markdown_content)