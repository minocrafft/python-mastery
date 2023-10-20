def print_table(records, fields):
    print(" ".join(f"{field:>10s}" for field in fields))
    print(f"{'-'*10} " * len(fields))

    for record in records:
        print(" ".join(f"{getattr(record, key):>10}" for key in fields))
