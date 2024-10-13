from filename_generator import FilenameGenerator
from  filemanager import FileManager

fg = FilenameGenerator('kcdw', 'KCDW', '2024-10-10 1200', 4) 
urls = fg.generate_filenames()
combined_filename = fg.generate_combined_filename()

fm = FileManager(urls, combined_filename)
fm.process_recordings()
