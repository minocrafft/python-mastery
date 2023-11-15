from abc import ABC, abstractmethod


class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers):
        raise NotImplementedError

    @abstractmethod
    def row(self, rowdata):
        raise NotImplementedError


class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        print(" ".join("%10s" % h for h in headers))
        print(("-" * 10 + " ") * len(headers))

    def row(self, rowdata):
        print(" ".join("%10s" % d for d in rowdata))


class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        print(",".join(headers))

    def row(self, rowdata):
        print(",".join(str(d) for d in rowdata))


class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        headers = [f"<th>{header}</th>" for header in headers]
        print(f"<tr> {' '.join('%10s' % h for h in headers)} </tr>")

    def row(self, rowdata):
        rowdata = [f"<th>{row}</th>" for row in rowdata]
        print(f"<tr> {' '.join('%10s' % d for d in rowdata)} </tr>")


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


def create_formatter(types: str, column_formats=None, upper_headers=False):
    if types.lower() == "text":
        formatter = TextTableFormatter
    elif types.lower() == "csv":
        formatter = CSVTableFormatter
    elif types.lower() == "html":
        formatter = HTMLTableFormatter
    else:
        raise RuntimeError(f"Unknown format {types}")

    if column_formats:

        class formatter(ColumnFormatMixin, formatter):
            formats = column_formats

    if upper_headers:

        class formatter(UpperHeadersMixin, formatter):
            pass

    return formatter()
