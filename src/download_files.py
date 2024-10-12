from pathlib import Path
import concurrent.futures
from tqdm import tqdm
import requests


def __download_file(location):
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    response = requests.get(location['url'], stream=True, headers=headers)
    response.raise_for_status()

    print(f"Downloading {location['url']}:")
    total_size = int(response.headers.get("content-length", 0))
    chunk_size = 8192

    filepath = 'tmp/'
    Path(filepath).mkdir(parents=True, exist_ok=True)

    with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
        with open(f"{filepath}{location['filename']}", 'wb') as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                progress_bar.update(len(chunk))
                file.write(chunk)


def download_files(locations):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(__download_file, locations)
