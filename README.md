# bevager-redux

A custom presentation of a bevager.com user's data via asynchronous import.

## Motivation
A www.bevager.com instance site, while appreciated, leaves quite a bit to be desired from a UI/UX perspective. Current grievances are:

 - No multi-column sorting (country + name, or price + name)
 - No filtering by signature status
 - Note column content makes table unusable

By exporting bevager data (from the rendered table) and rendering into html ourselves we can apply whatever custom visualizations we desire.


## Dependencies
As made apparent by the `requirements.txt` file, this app relies on underlying technologies of `MongoDB`, and `redis` as its primary datastore, and celery queue, respectively.
Installation of these dependencies is left as an exercise to the user.

## Usage
A top-level `credentials.yaml` file is expected to provide `username: password` mapping for use by the `BevagerClient` class in `bevager_cli.py`.

It is recommended to install dependencies within a virtualenvironment:
```
dnathe4th@~/bevager-redux: mkvirtualenv bevager
(bevager) dnathe4th@~/bevager-redux: pip install -r requirements.txt
```

The app can be started by invoking `python` with the `app.py` file as its argument:
```
(bevager) dnathe4th@~/bevager-redux: python app.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Similarly, the celery process can be started (in another window, or tmux pane) as such:
```
(bevager) dnathe4th@~/bevager-redux: celery -A tasks worker --loglevel=info
```

Once the app and celery workers are up and running, the initial dump of data can be loaded from bevager:
```
(bevager) dnathe4th@~/bevager-redux: python
>>> from tasks import load_rums
>>> load_rums.delay(user='<USER NAME PRESENT IN CREDENTIALS.YAML>')
```
This will trigger a single celery task to log into bevager and load the table of data, and then triggers independent celery tasks to upsert each rum listed into the datastore.

## Assumptions
Since the data import is done via [beautifulsoup] parsing of the html table on bevager.com, significant changes to the html will disrupt data import.
Current assumptions about the shape of the table are:

  - rows relating to rums are identified by presence of an `'item'` html class.
  - Country name is available from the first column, with whitespace stripped.
  - Rum name is available from the second column, with whitespace stripped.
  - Price is available from the third column, and is an integer after removing whitespace, leading dollar sign, and truncating decimal.
  - Signature status is available in the fourth column, and is indicated by the text 'REQ' (unrequested), a 'fa-check' class (requested), or otherwise (pending).
  - Notes are available in the fifth column, with whitespace stripped.
  - Availability is determined by the presence of a 'historic-item' class on the entire row.

## TODO's
 - Bevager data import is currently triggered by hand rather than scheduled as it should be.
 - Notes should be optionally rendered.
 - Rums should be selectable for more information to match bevager functionality.
 - Rums should be requesable with persistance back to bevager.
 - Notes should be submittable with persistance back to bevager.
 - Some form of authentication should exist.
 - Non-defaults for mongodb/redis should probably be used.
 - Better deployment than '[master] dnathe4th@~/Experimental/bevager: rsync -a -v --exclude=.git/ . 52.34.133.96:./bevager-redux/'
