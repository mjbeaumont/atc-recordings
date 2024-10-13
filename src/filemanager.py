from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from shutil import rmtree
from tqdm import tqdm
import requests
import ffmpeg

class FileManager:

    WORKING_DIRECTORY = 'tmp/'

    def __init__(self, urls, combined_url):
        self.urls = urls
        self.combined_url = combined_url
        self.output_directory = self.__set_output_directory(combined_url)

    def __create_working_directory(self):
        Path(self.WORKING_DIRECTORY).mkdir(parents=True, exist_ok=True)

    def __create_output_directory(self):
        Path(self.output_directory).mkdir(parents=True, exist_ok=True)

    def __create_directories(self):
        self.__create_working_directory()
        self.__create_output_directory()

    def __cleanup(self):
        rmtree(self.WORKING_DIRECTORY, ignore_errors=True)

    def __set_output_directory(self, combined_url):
        return f'{combined_url.split('.')[0]}/'

    def __generate_filename_from_url(self, url):
        return url.split('/')[-1]

    def __download_file(self, url):
        headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))

        with tqdm(total=total_size, unit="B", unit_scale=True, desc=url) as progress_bar:
            filename = self.__generate_filename_from_url(url)
            output_filename = f"{self.WORKING_DIRECTORY}{filename}"
            with open(output_filename, 'wb') as file:
                for chunk in response.iter_content():
                    progress_bar.update(len(chunk))
                    file.write(chunk)

    def __download_files(self):
        max_workers = 3
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.__download_file, url): url for url in self.urls
            }

            for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading Files"):
                try:
                    future.result()  # To raise exceptions if any occurred
                except Exception as e:
                    tqdm.write(f"Error downloading file: {e}")

    def __get_downloaded_files(self):
        return list(Path().glob(f'{self.WORKING_DIRECTORY}/*.mp3'))

    def __process_audio_files(self):
        downloaded_files = self.__get_downloaded_files()
        ffmpeg_input = map(ffmpeg.input, downloaded_files)
        (
            ffmpeg
            .concat(*ffmpeg_input, v=0, a=1)
            .filter('silenceremove', stop_periods=-1, stop_duration=1, stop_threshold='-20dB')
            .output(f'{self.output_directory}{self.combined_url}')
            .run()
        )

    def process_recordings(self):
        self.__create_directories()
        self.__download_files()
        self.__process_audio_files()
        self.__cleanup()
