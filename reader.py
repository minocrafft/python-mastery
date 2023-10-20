import csv
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Callable


class DataCollection:
    def __init__(self, columns):
        self.names = list(columns)
        self.values = list(columns.values())

    def __len__(self):
        return len(self.values[0])

    def __getitem__(self, index):
        return dict(zip(self.names, (col[index] for col in self.values)))


class CSVParser(ABC):
    def parse(self, filename):
        records = []
        with open(filename) as f:
            rows = csv.reader(f)
            headers = next(rows)
            for row in rows:
                record = self.make_record(headers, row)
                records.append(record)
        return records

    @abstractmethod
    def make_record(self, headers, row):
        pass


class DictCSVParser(CSVParser):
    def __init__(self, types):
        self.types = types

    def make_record(self, headers, row):
        return {name: func(val) for name, func, val in zip(headers, self.types, row)}


class InstanceCSVParser(CSVParser):
    def __init__(self, cls):
        self.cls = cls

    def make_record(self, headers, row):
        return self.cls.from_row(row)


def read_csv_as_dicts(filename, types: list[Callable] = [str, int, float]):
    """Read the bus ride data as a list of dicts"""
    parser = DictCSVParser(types)
    return parser.parse(filename)


def read_csv_as_columns(filename, types: list[Callable]):
    """
    Read the bus ride data into 4 lists, representing columns
    """
    datas = defaultdict(list)
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)  # Skip headers

        for row in rows:
            for name, func, val in zip(headers, types, row):
                datas[name].append(func(val))

    return DataCollection(datas)


def read_csv_as_instances(filename, cls):
    """Read a CSV file into a list of instances"""
    parser = InstanceCSVParser(cls)
    return parser.parse(filename)


if __name__ == "__main__":
    import tracemalloc
    from sys import intern

    tracemalloc.start()
    data = read_csv_as_columns("Data/ctabus.csv", [intern, intern, intern, int])
    print(tracemalloc.get_traced_memory())
