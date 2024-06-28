import json
from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from icalendar import Calendar, Event


def convert_event(json_event: dict) -> Event:
    start = (
        datetime.strptime(json_event["start"], "%Y-%m-%dT%H:%M:%S%z")
        .astimezone(timezone.utc)
        .strftime("%Y%m%dT%H%M%SZ")
    )
    summary = json_event["title"]
    description = json_event.get("website_url", "")
    dtstart = start
    duration = f"PT{json_event['duration']}M"
    dtstamp = start
    uid = str(uuid4())
    location = ", ".join(json_event["rooms"])

    return Event(
        summary=summary,
        description=description,
        dtstart=dtstart,
        duration=duration,
        dtstamp=dtstamp,
        uid=uid,
        location=location,
    )


def create_calendar() -> Calendar:
    cal = Calendar()
    cal.add("prodid", "-//Erik//Europython2024Calendar//EN")
    cal.add("version", "2.0")
    return cal


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-j",
        "--json-files",
        help="Path to the json file to process, supports globs in the filename",
    )
    args = parser.parse_args()

    calendar = create_calendar()
    path = Path(args.json_files)
    json_files = Path(path.parent).expanduser().glob(path.name)

    for json_file in json_files:
        with open(json_file, "r") as fp:
            events = json.load(fp)

        for json_event in events["events"]:
            event = convert_event(json_event)
            calendar.add_component(event)

    with open("calendar.ics", "wb") as fp:
        fp.write(calendar.to_ical())


if __name__ == "__main__":
    main()
