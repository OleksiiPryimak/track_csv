# python (location)/track_csv.py (location)/track.csv

from csv import DictReader
from typing import Dict, List

import click


class Entry:
    def __init__(self, description: str, time: int, tags: List[str]):
        self.description = description
        self.time = time
        self.tags = tags

    
    def __repr__(self):
        return f"Entry(description={self.description!r}, time{self.time!r}, tags={self.tags!r})"
    

    def __str__(self):
        tags = [f'#{t}' for t in self.tags]
        tags = " ".join(tags)
        return f"{self.description} ({self.time} min) {tags}"
    

def build_entry_from_dict(row: dict) -> Entry:
    tags = row['tags'].split(' ')
    tags = [t.strip() for t in tags]
    entry = Entry(
        description=row['desc'].strip(),
        time=int(row['time'].strip()),
        tags=tags,
    )
    return entry


def load_entries(csv_file: str) -> list[Entry]:
    with open(csv_file) as stream:
        reader = DictReader(stream)
        entries = [build_entry_from_dict(row) for row in reader]
    return entries


def compute_total_time_by_tags(entries: List[Entry]) -> Dict[str, int]:
    tags = {t for e in entries for t in e.tags}
    report = {}
    for tag in tags:
        total = sum([e.time for e in entries if tag in e.tags])
        report[tag] = total
    return report


def display_report_by_tags(time_by_tags: Dict[str, int]) -> None:
    print('TOTAL-Time   Tag')
    for tag, time in time_by_tags.items():
        print(f'{time:10} #{tag}')


@click.command()
@click.argument('csv_file')
def main(csv_file: str):
    entries = load_entries(csv_file)
    report = compute_total_time_by_tags(entries)
    display_report_by_tags(report)


if __name__ == "__main__":
    main()