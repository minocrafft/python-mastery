from abc import ABC, abstractmethod


def print_table(records, fields, formatter):
    formatter.headings(fields)
    for record in records:
        rowdata = [getattr(record, fieldname) for fieldname in fields]
        formatter.row(rowdata)


def create_formatter(types: str = "text"):
    if types.lower() == "text":
        return TextTableFormatter()
    elif types.lower() == "csv":
        return CSVTableFormatter()
    elif types.lower() == "html":
        return HTMLTableFormatter()
    else:
        raise RuntimeError(f"Unknown format {types}")


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
