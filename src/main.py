from typing import Optional
from filename_generator import FilenameGenerator
from  filemanager import FileManager
import typer
from typing_extensions import Annotated


def main(
        airport: Annotated[str, typer.Argument(help='4-letter ICAO code')],
        start: Annotated[str, typer.Argument(help='YYYY-mm-dd H:I (in UTC)', prompt=True)],
        feed: Annotated[Optional[str], typer.Option(help='Defaults to airport if not provided', prompt=True)],
        number_of_periods: Annotated[Optional[int], typer.Option(help='How many 30 minute periods to include')] = 4
    ):
    feed_name = feed if feed else airport.upper()

    fg = FilenameGenerator(
        airport.lower(),
        feed_name,
        start,
        number_of_periods
    )
    urls = fg.generate_filenames()
    combined_filename = fg.generate_combined_filename()

    fm = FileManager(urls, combined_filename)
    fm.process_recordings()


if __name__ == "__main__":
    typer.run(main)
