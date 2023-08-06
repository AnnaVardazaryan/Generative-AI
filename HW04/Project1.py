"""This project is dedicated to the creation of a streamlined download manager capable of simultaneously downloading
multiple files. Leveraging both threading and multiprocessing, the download manager deftly handles URLs from both HTTP and FTP protocols."""

import threading
import requests
import ftplib
import os
from urllib.parse import urlparse

def download_content(url: str) -> bytes:
    """
    Downloads content from a given URL, supporting both HTTP and FTP protocols.

    Parameters:
        url (str): The URL of the file to download.
    Returns:
        bytes: The content of the downloaded file.
    """
    if url.startswith("http"):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            return b''
    elif url.startswith("ftp"):
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        with ftplib.FTP(parsed_url.hostname) as ftp:
            ftp.login(parsed_url.username, parsed_url.password)
            ftp.cwd(os.path.dirname(parsed_url.path))
            content = b''
            with open(filename, "wb") as f:
                def callback(data):
                    f.write(data)
                ftp.retrbinary("RETR " + filename, callback)
        with open(filename, "rb") as f:
            content = f.read()
        os.remove(filename)
        return content
    else:
        raise ValueError("Unsupported URL protocol")

class Download:
    """
    Base class representing a downloadable file.
    """
    def __init__(self, url, filename):
        """
        Initializes a Download object with URL and destination filename.
        """
        self.url = url
        self.filename = filename

    def start_download(self):
        """
        Starts the download process using a separate thread.
        """
        thread = threading.Thread(target=self._download_file)
        thread.start()
        return thread

    def _download_file(self):
        """
        Private method to handle the download process.
        """
        content = download_content(self.url)
        self.save_file(content)
        self.download_complete()

    def save_file(self, content: bytes):
        """
        Saves the downloaded content to the specified filename.
        """
        with open(self.filename, "wb") as f:
            f.write(content)

    def download_complete(self):
        """
        Signals that the download is complete.
        """
        print(f"Download from {self.url} is complete.")

class ThreadingDownloader(Download):
    """
    Class representing a threaded download.
    """
    def download_complete(self):
        """
        Signals that the download using threading is complete.
        """
        print(f"Download from {self.url} using threading is complete.")

class DownloadManager:
    """
    Manages multiple downloads using threading.
    """
    def __init__(self, max_threads=3):
        """
        Initializes the DownloadManager with the specified maximum number of threads.
        """
        self.max_threads = max_threads
        self.downloads = []

    def download(self, url: str, filename: str):
        """
        Adds a new download to the manager.
        """
        download = ThreadingDownloader(url, filename)
        self.downloads.append(download)

    def start(self):
        """
        Starts all downloads simultaneously.
        """
        threads = []
        for download in self.downloads:
            thread = download.start_download()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def wait(self) -> None:
        """
        Waits for all downloads to complete.
        """
        for download_thread in self.downloads:
            download_thread.join()

if __name__ == "__main__":
    download_manager = DownloadManager(max_threads=3)

    download_manager.download("http://example.com/file1.txt", "file1.txt")
    download_manager.download("ftp://example.com/file2.txt", "file2.txt")
    download_manager.download("http://example.com/file3.txt", "file3.txt")

    download_manager.start()

    print("All downloads completed!")

