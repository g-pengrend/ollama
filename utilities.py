import re, os, requests, magic, ollama, string, configparser
from pdfminer.high_level import extract_text
from urllib.parse import unquote, urlparse
from bs4 import BeautifulSoup

def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename="([^"]+)"', cd)
    if len(fname) == 0:
        return None
    fname = fname[0]
    if fname.lower().startswith(("utf-8''", "utf-8'")):
        fname = fname.split("'")[-1]
    return unquote(fname)

def download_file(url):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        cd = r.headers.get('content-disposition')
        filename = get_filename_from_cd(cd)
        if not filename:
            # Use the URL to create a filename if no content-disposition header is present
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = parsed_url.netloc.replace('.', '_')
        filename = 'content/' + filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return filename

def readtext(path):
    path = path.rstrip().replace(' \n', '').replace('%0A', '')
    if re.match(r'^https?://', path):
        filename = download_file(path)
    else:
        filename = os.path.abspath(path)
    
    filetype = magic.from_file(filename, mime=True)
    print(f"\nEmbedding {filename} as {filetype}")
    
    text = ""
    if filetype == 'application/pdf':
        text = extract_text(filename)
        text = text.encode('utf-8', errors='ignore').decode('utf-8')
    if filetype == 'text/plain':
        with open(filename, 'rb') as f:
            text = f.read().decode('utf-8')    
    if filetype == 'text/html':
        with open(filename, 'rb') as f:
            soup = BeautifulSoup(f, 'html.parser')
            text = soup.get_text()
    
    if os.path.exists(filename) and 'content/' in filename:
        os.remove(filename)
    
    return text

def getconfig():
  config = configparser.ConfigParser()
  config.read('config.ini')
  return dict(config.items("main"))