from datetime import datetime, timedelta
import sys


class FilenameGenerator:
    """
        Used to generate a list of filenames to download from liveatc.net, and
        to generate the name of the final outputted recording
    """

    TIME_FORMAT = '%H%M'
    INPUT_FORMAT = f'%Y-%m-%d {TIME_FORMAT}'
    OUTPUT_DATE_FORMAT = '%b-%d-%Y'
    OUTPUT_FORMAT = f'{OUTPUT_DATE_FORMAT}-{TIME_FORMAT}Z'
    MAIN_URL = 'https://archive.liveatc.net'
    """
        Class constants. Used to match the format of feed archive files
        at liveatc.net

        eg. https://archive.liveatc.net/kcdw/KCDW-Oct-10-2024-1000Z.mp3
    """

    def __init__(self, airport, feed, start, num):
        self.airport = airport
        self.feed = feed
        self.num = num
        self.start = self.__set_start(start)

    def __set_start(self, start_input):
        try:
            return datetime.strptime(start_input, self.INPUT_FORMAT)
        except ValueError:
            print(
                f'{start_input} does not match the format {self.INPUT_FORMAT}'
            )
            sys.exit(1)

    def __get_datetime_string(self, dt, fmt):
        return dt.strftime(fmt)

    def __format_datetime(self, dt):
        return self.__get_datetime_string(dt, self.OUTPUT_FORMAT)

    def __format_date(self, dt):
        return self.__get_datetime_string(dt, self.OUTPUT_DATE_FORMAT)

    def __format_time(self, dt):
        return self.__get_datetime_string(dt, self.TIME_FORMAT)

    def __generate_times(self):
        times = []
        times.append(self.start)
        time_delta = timedelta(minutes=30)
        for _ in range(1, self.num):
            next_time = times[-1] + time_delta
            times.append(next_time)
        return times

    def __generate_filename_datecomponent(self):
        times = self.__generate_times()
        return list(map(self.__format_datetime, times))

    def generate_filenames(self):
        """
            Generate a list of URLs to download from liveatc.net using
            the class' airport, feed name, date & time
        """
        dates = self.__generate_filename_datecomponent()
        files = []
        for date in dates:
            data = {
                'date': date,
                'airport': self.airport.lower(),
                'feed': self.feed
            }
            filename = f"{data['feed']}-{data['date']}.mp3"
            url = f"{self.MAIN_URL}/{data['airport']}/{filename}"
            files.append(url)
        return files

    def generate_combined_filename(self):
        """
            Using the airport, feed name, date, and list of times,
            output a filename that contains the correct time range
        """
        times = self.__generate_times()
        feed = self.feed
        date = self.__format_date(times[0])
        start_time = self.__format_time(times[0])
        end_time = self.__format_time(times[-1])
        return f'{feed}-{date}-{start_time}-{end_time}Z-combined.mp3'
