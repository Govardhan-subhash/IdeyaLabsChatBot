import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_all_website_links(url):
    """
    Extracts all unique internal links from a given URL.
    """
    urls = set()
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue

        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # Reconstruct url without fragment to avoid duplicates, but KEEP query params
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if parsed_href.query:
            href += "?" + parsed_href.query

        if not is_valid(href, domain_name):
            continue

        urls.add(href)
    return urls

def is_valid(url, domain_name):
    """
    Checks whether `url` is a valid URL and belongs to the same domain.
    """
    parsed = urlparse(url)
    is_same_domain = bool(parsed.netloc) and bool(parsed.scheme) and domain_name in parsed.netloc
    
    # Filter out common non-html extensions
    ignored_extensions = [
        '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.ico', 
        '.pdf', '.zip', '.tar', '.gz', '.rar', '.mp4', '.mp3', '.avi', '.css', '.js', '.json', '.xml'
    ]
    path = parsed.path.lower()
    is_valid_ext = not any(path.endswith(ext) for ext in ignored_extensions)
    
    return is_same_domain and is_valid_ext

def scrape_website_recursively(url, max_depth=2):
    """
    Recursively scrapes content from all pages of a website up to a certain depth.
    """
    scraped_data = {}
    visited_urls = set()
    urls_to_visit = [(url, 0)]  # (url, current_depth)

    while urls_to_visit:
        current_url, current_depth = urls_to_visit.pop(0)

        if current_url in visited_urls or current_depth > max_depth:
            continue

        print(f"Scraping: {current_url} (Depth: {current_depth})")
        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.content, "html.parser")
            text_content = soup.get_text(separator=" ", strip=True)
            scraped_data[current_url] = text_content
            visited_urls.add(current_url)

            if current_depth < max_depth:
                links = get_all_website_links(current_url)
                for link in links:
                    if link not in visited_urls:
                        urls_to_visit.append((link, current_depth + 1))

        except Exception as e:
            print(f"Error scraping {current_url}: {e}")

    return scraped_data

def scrape_and_chunk(url, max_depth=2):
    """
    Scrapes website and splits content into chunks.
    """
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    
    raw_data = scrape_website_recursively(url, max_depth)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    
    chunked_documents = []
    
    for url, content in raw_data.items():
        chunks = text_splitter.split_text(content)
        for i, chunk in enumerate(chunks):
            chunked_documents.append({
                "page_content": chunk,
                "metadata": {"source": url, "chunk_id": i}
            })
            
    return chunked_documents

if __name__ == "__main__":
    start_url = "https://ideyalabs.com/"
    scraped_content = scrape_website_recursively(start_url, max_depth=1) # Set max_depth to 1 for initial testing
    for url, content in scraped_content.items():
        print(f"URL: {url}\nContent: {content[:500]}\n---")
