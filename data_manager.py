from pandas import ExcelWriter, read_excel, read_html, DataFrame
from requests import get
from re import sub
from datetime import datetime


class ExcelManager:

    def __init__(
            self,
            outfile_name: str
    ):
        now = datetime.now()
        month = now.month
        day = now.day
        year = now.year
        self.outfile = f"{month}_{day}_{year}_{outfile_name}.xlsx"
        self.writer = ExcelWriter(
            self.outfile,
            engine='xlsxwriter'
        )
        # datasource : dataframe
        self.dataframes = {}
        # sheet name: {column : dataframe}
        self.frames_to_write = {}
        # sheet name: {chart name: dataframe}
        self.charts_to_write = {}

    def read_local(
            self,
            filepath: str,
            sheetname: str,
            name: str = None
    ) -> None:
        if name is None:
            name = sheetname
        print(f"Reading data locally from: \n{filepath} . . .")
        self.dataframes[name] = read_excel(
            filepath,
            sheetname
        )
        print("\tSuccess!")

    def read_online(
            self,
            url: str,
            name: str,
            username: str = None,
            password: str = None
    ) -> None:
        print(f"Reading data from: \n{url} . . .")
        self.dataframes[name] = self.get_dataframe_from_url(
            url,
            username=username,
            password=password
        )
        print("\tSuccess!")

    def write_charts(
            self,
            type: str,
    ):
        for sheet in self.charts_to_write:
            for chart_name in self.charts_to_write[sheet]:

                if sheet not in self.writer.sheets:
                    self.writer.sheets[sheet] = self.writer.book.add_worksheet(sheet)

                chart = self.writer.book.add_chart({"type": type})
                chart.add_series(
                    {
                        'name': f"{chart_name}",
                        'categories': f'={sheet}!$A$3:$A${self.charts_to_write[sheet][chart_name].shape[0]+2}',
                        'values': f'={sheet}!$B$3:$B${self.charts_to_write[sheet][chart_name].shape[0]+2}'
                    }
                )
                self.writer.sheets[sheet].insert_chart('D2', chart)

    def write_dataframes(
            self,
            index: bool = False
    ) -> None:
        for sheet in self.frames_to_write:
            if isinstance(self.frames_to_write[sheet], dict):
                if sheet not in self.writer.sheets:
                    self.writer.sheets[sheet] = self.writer.book.add_worksheet(sheet)
                col = 0
                for column in self.frames_to_write[sheet]:
                    row = 0
                    frames = list(self.frames_to_write[sheet][column].keys())
                    for frame in frames:
                        self.writer.sheets[sheet].write_string(
                            row, col,
                            frame
                        )
                        self.frames_to_write[sheet][column][frame].to_excel(
                            self.writer,
                            sheet,
                            startrow=row+1,
                            startcol=col,
                            index=index
                        )
                        row += self.frames_to_write[sheet][column][frame].shape[0]+3
                    if isinstance(self.frames_to_write[sheet][column][frames[0]], DataFrame):
                        col += self.frames_to_write[sheet][column][frames[0]].shape[1]+3
                    else:
                        col += 3
            else:
                self.frames_to_write[sheet].to_excel(
                    self.writer,
                    sheet,
                    index=index
                )

    def save_close(self):
        self.writer.save()
        self.writer.close()

    # retrieve a Dataframe from a url
    def get_dataframe_from_url(
            self,
            url: str,
            username: str = None,
            password: str = None
    ) -> DataFrame:
        if username and password:
            prefix = r"https://"
            suffix = sub(prefix, '', url)
            prefix += f"{username}:{password}@"
            url = prefix + suffix
        processed_url = get(
            url,
            verify=False
        )
        return read_html(processed_url.content)[0]
