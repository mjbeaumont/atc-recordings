from filename_generator import FilenameGenerator
from download_files import download_files

fg = FilenameGenerator('kcdw', 'KCDW', '2024-10-10 1200', 10)
locations = fg.generate_filenames()

download_files(locations)
