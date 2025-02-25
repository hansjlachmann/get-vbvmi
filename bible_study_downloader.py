import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin

def create_download_directory():
    """Create a directory to store downloads if it doesn't exist"""
    if not os.path.exists("colossians"):
        os.makedirs("colossians")

def download_file(url, filename):
    """Download a file from URL and save it with given filename"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filename, 'wb') as file:
            print(f"Downloading: {filename}")
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        print(f"Successfully downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Error downloading {filename}: {str(e)}")
        return False

def main():
    # Create download directory
    create_download_directory()
    
    # URL of the Bible study
    url = "https://versebyverseministry.org/bible-studies/the-book-of-colossians"
    
    try:
        # Get the webpage content
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all lesson links - updated pattern for Colossians
        lessons = soup.find_all('a', href=re.compile(r'/bible-studies/the-book-of-colossians/.*'))
        
        for lesson in lessons:
            lesson_url = urljoin(url, lesson.get('href'))
            
            # Get the lesson page
            lesson_response = requests.get(lesson_url)
            lesson_soup = BeautifulSoup(lesson_response.text, 'html.parser')
            
            # Find MP3 download link
            mp3_link = lesson_soup.find('a', href=re.compile(r'.*\.mp3$'))
            
            if mp3_link:
                mp3_url = mp3_link['href']
                # Create filename from the lesson title
                clean_title = lesson.text.strip().replace(':', '-').replace('/', '-')
                filename = f"colossians/{clean_title}.mp3"
                download_file(mp3_url, filename)
            
            print(f"Processed lesson: {lesson.text.strip()}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print("Starting Bible Study MP3 downloader...")
    main()
    print("Download process completed!") 