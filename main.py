import os
from enum import Enum

import pandas

class Headers(str,Enum):
    race = "Race"
    name = "Name"
    drivers_involved = "Drivers Involved"
    ruling = "Ruling"
    drivers_at_fault = "Drivers At Fault"
    time_penalty = "Time Penalty"
    penalty_points = "Penalty Points"
    other_penalty = "Other Penalty"
    majority_opinion = "Majority Opinion"


def replace_semi_colon(string):
    return ', '.join(f"@{s}" for s in string.split(";"))


class Formatter:
    def __init__(self,df):
        self.df = df

    @property
    def location(self):
        return self.df[Headers.race][0]

    @property
    def header(self):
        return self.wrap(f"Beginning of {self.location}")

    @property
    def footer(self):
        return self.wrap(f"End of {self.location}")

    def wrap(self,string):
        return f"""
------------
{string}
------------"""

    def format(self):
        print(self.header)

        for i,row in self.df.iterrows():
            if pandas.isna(row[Headers.name]):
                break
            self.format_row(row)

        print(self.footer)

    def format_row(self,row):
        s = ""
        s += row[Headers.name]
        s+="\n"

        s = self.append_field(s,row,Headers.drivers_involved)
        s = self.append_field(s,row,Headers.ruling)

        s = self.append_optional_field(s,row,Headers.drivers_at_fault,"None")
        s = self.append_optional_field(s,row,Headers.time_penalty)
        s = self.append_optional_field(s,row,Headers.penalty_points)
        s = self.append_optional_field(s,row,Headers.other_penalty)
        s = self.append_optional_field(s,row,Headers.majority_opinion,"Nothing to see here")

        print(s)

    @staticmethod
    def append_field(string, row, field):
        if field in (Headers.drivers_at_fault, Headers.drivers_involved):
            row[field] = replace_semi_colon(row[field])
        string+= f"{field}: {row[field]}"
        string+="\n"
        return string

    @staticmethod
    def append_optional_field(s, row, field, default=None):
        if not pandas.isna(row[field]):
            if field in (Headers.drivers_at_fault,Headers.drivers_involved):
                row[field] = replace_semi_colon(row[field])
            s+= f"{field}: {row[field]}"
            s+='\n'
        elif default is not None:
            s+=f"{field}: {default}"
            s+="\n"
        return s


def main(url):
    import pandas as pd

    df = pd.read_csv(url)

    formatter = Formatter(df)

    formatter.format()


if __name__ == '__main__':
    URL = os.getenv("URL")
    csv_export_url = URL.replace('/edit#gid=', '/export?format=csv&gid=')
    main(csv_export_url)

