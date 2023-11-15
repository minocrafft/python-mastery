from .formatter import TableFormatter, print_table
from .formats.text import TextTableFormatter
from .formats.csv import CSVTableFormatter
from .formats.html import HTMLTableFormatter


__all__ = ["print_table", "create_formatter"]


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
