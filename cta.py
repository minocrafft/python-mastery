import sys
import tracemalloc
from collections import defaultdict, Counter

import reader

tracemalloc.start()

if False:
    # Part (b)
    rows = reader.read_csv_as_dicts(
        "Data/ctabus.csv", [sys.intern, sys.intern, sys.intern, int]
    )
else:
    # Part (d) - Challenge
    rows = reader.read_csv_as_columns(
        "Data/ctabus.csv", [sys.intern, sys.intern, sys.intern, int]
    )

# Q1
routes = set()
for row in rows:
    routes.add(row["route"])

print(len(routes))


# Q2
route_date = {(row["route"], row["date"]): row["rides"] for row in rows}
print("Rides on Route 22, February 2, 2011:", route_date["22", "02/02/2011"])


# Q3
total_rides = Counter()
for row in rows:
    total_rides[row["route"]] += row["rides"]

print(total_rides.most_common(5))


# Q4

rides_by_year = defaultdict(Counter)

for row in rows:
    rides_by_year[row["date"].split("/")[-1]][row["route"]] += row["rides"]

diffs = rides_by_year["2011"] - rides_by_year["2001"]
print(diffs.most_common(5))

print("Memory Use: Current %d, Peak %d" % tracemalloc.get_traced_memory())
