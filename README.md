Eventor
=======

A simple tool to convert EuroPython's json files to an ICS file.

Clone EuroPython's [website repo](https://github.com/EuroPython/website/).
Then install and use this tool:

```bash
python3 -m venv venv
source venv/bin/activate
pip install ./eventor
eventor -j '~/path/to/europython/website/src/content/days/*.json'
```

This will write a calendar.ics file in the current directory that you can then import to your favorite calendar app.
