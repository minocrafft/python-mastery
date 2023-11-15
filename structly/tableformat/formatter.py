from abc import ABC, abstractmethod


class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers):
        raise NotImplementedError

    @abstractmethod
    def row(self, rowdata):
        raise NotImplementedError


class ColumnFormatMixin:
    formats = []

    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)


class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])


def print_table(records, fields, formatter):
    if not isinstance(formatter, TableFormatter):
        raise TypeError(f"Expected a TableFormatter")

    formatter.headings(fields)
    for record in records:
        rowdata = [getattr(record, fieldname) for fieldname in fields]
        formatter.row(rowdata)
