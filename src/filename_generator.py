from datetime import datetime, timedelta


class FilenameGenerator:

    INPUT_FORMAT = '%Y-%m-%d %H:%M'
    OUTPUT_FORMAT = '%b-%d-%Y-%H%MZ'
    MAIN_URL = 'https://archive.liveatc.net'

    def __init__(self, airport, start, num):
        self.airport = airport
        self.start = start
        self.num = num

    def __format_timestamp(self, dt):
        return dt.strftime(self.OUTPUT_FORMAT)

    def __generate_timestamps(self):
        dates = []
        try:
            initial_time = datetime.strptime(self.start, self.INPUT_FORMAT)
            dates.append(initial_time)
            time_delta = timedelta(minutes=30)
            for _ in range(self.num):
                next_time = dates[-1] + time_delta
                dates.append(next_time)
            return list(map(self.__format_timestamp, dates))
        except ValueError:
            print('Invalid date string given as starting point')

    def generate_filenames(self):
        dates = self.__generate_timestamps()
        files = []
        for date in dates:
            data = {
                'date': date,
                'airport_path': self.airport.lower(),
                'airport_filename': self.airport.upper()
            }
            filename = f"{self.MAIN_URL}/{data['airport_path']}/{data['airport_filename']}-{data['date']}.mp3"
            files.append(filename)
        return files
