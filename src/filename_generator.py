from datetime import datetime, timedelta


class FilenameGenerator:

    TIME_FORMAT = '%H:%M'
    INPUT_FORMAT = f'%Y-%m-%d {TIME_FORMAT}'
    OUTPUT_DATE_FORMAT = '%b-%d-%Y'
    OUTPUT_FORMAT = f'{OUTPUT_DATE_FORMAT}-{TIME_FORMAT}Z'
    MAIN_URL = 'https://archive.liveatc.net'

    def __init__(self, airport, feed, start, num):
        self.airport = airport
        self.feed = feed
        self.start = start
        self.num = num

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
        try:
            initial_time = datetime.strptime(self.start, self.INPUT_FORMAT)
            times.append(initial_time)
            time_delta = timedelta(minutes=30)
            for _ in range(1, self.num):
                next_time = times[-1] + time_delta
                times.append(next_time)
        except ValueError:
            print(
                f'{self.start} does not match the format {self.INPUT_FORMAT}'
            )
        return times

    def __generate_filename_datecomponent(self):
        times = self.__generate_times()
        return list(map(self.__format_datetime, times))

    def generate_filenames(self):
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
            files.append({"filename": filename, "url": url})
        return files

    def generate_combined_filename(self):
        times = self.__generate_times()
        feed = self.feed
        date = self.__format_date(times[0])
        start_time = self.__format_time(times[0])
        end_time = self.__format_time(times[-1])
        return f'{feed}-{date}-{start_time}-{end_time}Z-combined.mp3'
