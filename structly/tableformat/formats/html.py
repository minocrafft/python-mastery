from ..formatter import TableFormatter


class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        headers = [f"<th>{header}</th>" for header in headers]
        print(f"<tr> {' '.join('%10s' % h for h in headers)} </tr>")

    def row(self, rowdata):
        rowdata = [f"<th>{row}</th>" for row in rowdata]
        print(f"<tr> {' '.join('%10s' % d for d in rowdata)} </tr>")
