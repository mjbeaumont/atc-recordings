from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import requests


def __download_file(location):
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    response = requests.get(location['url'], stream=True, headers=headers)
    response.raise_for_status()

    tqdm.write(f"Downloading {location['url']}:")
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
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(__download_file, loc): loc for loc in locations
        }

        for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading Files"):
            try:
                future.result()  # To raise exceptions if any occurred
            except Exception as e:
                tqdm.write(f"Error downloading file: {e}")
