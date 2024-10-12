from src.filename_generator import FilenameGenerator
import pytest


@pytest.fixture
def test_data():
    fg = FilenameGenerator('KJFK', 'KJFK-Gnd', '2024-10-05 12:00', 4, )
    yield fg


def test_invalid_date_format(capsys):
    fg = FilenameGenerator('KJFK', 'KJFK-Gnd', '2024-13-13 1:00PM', 4)
    with pytest.raises(SystemExit) as sys_error:
        fg.generate_filenames()
        out = capsys.readouterr()
        assert "2024-13-13 1:00PM" in out


def test_generate_filenames(test_data):
    expected_result = [
        {
            'filename': 'KJFK-Gnd-Oct-05-2024-12:00Z.mp3',
            'url': 'https://archive.liveatc.net/kjfk/KJFK-Gnd-Oct-05-2024-12:00Z.mp3'
        },
        {
            'filename': 'KJFK-Gnd-Oct-05-2024-12:30Z.mp3',
            'url': 'https://archive.liveatc.net/kjfk/KJFK-Gnd-Oct-05-2024-12:30Z.mp3'
        },
        {
            'filename': 'KJFK-Gnd-Oct-05-2024-13:00Z.mp3',
            'url': 'https://archive.liveatc.net/kjfk/KJFK-Gnd-Oct-05-2024-13:00Z.mp3'
        },
        {
            'filename': 'KJFK-Gnd-Oct-05-2024-13:30Z.mp3',
            'url': 'https://archive.liveatc.net/kjfk/KJFK-Gnd-Oct-05-2024-13:30Z.mp3'
        },

    ]
    result = test_data.generate_filenames()
    assert result == expected_result


def test_generate_combined_filename(test_data):
    result = test_data.generate_combined_filename()
    assert result == 'KJFK-Gnd-Oct-05-2024-12:00-13:30Z-combined.mp3'

