import csv
import logging
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Callable

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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


def convert_csv(lines, converter, *, headers=None):
    rows = csv.reader(lines)
    if headers is None:
        headers = next(rows)

    records = []
    for i, row in enumerate(rows, 1):
        try:
            records.append(converter(headers, row))
        except ValueError as e:
            logger.warning(f"Row {i}: Bad row: {row}")
            logger.debug(f"Row {i}: Reason: {e}")

    return records


def csv_as_dicts(lines, types, *, headers=None):
    return convert_csv(
        lines,
        lambda headers, row: {
            name: func(val) for name, func, val in zip(headers, types, row)
        },
    )


def csv_as_instances(lines, cls, *, headers=None):
    return convert_csv(lines, lambda headers, row: cls.from_row(row))


def read_csv_as_dicts(filename, types, *, headers=None):
    """
    Read CSV data into a list of dictionaries with optional type conversion
    """
    with open(filename) as file:
        return csv_as_dicts(file, types, headers=headers)


def read_csv_as_instances(filename, cls, *, headers=None):
    """
    Read CSV data into a list of instances
    """
    with open(filename) as file:
        return csv_as_instances(file, cls, headers=headers)


if __name__ == "__main__":
    port = read_csv_as_dicts("Data/missing.csv", types=[str, int, float])
