import json
import urllib2
import webbrowser
from feedback import Feedback

_HOST = "http://localhost:5050"
_APIKEY = "YOUR API KEY"


def url():
    return _HOST + "/api/" + _APIKEY + "/"


def get_data(method_name):
    req = urllib2.Request(url() + method_name)
    req.add_header("Accept", "application/json")
    try:
        res = urllib2.urlopen(req)
    except urllib2.URLError:
        print "Connection timed out"
        raise SystemExit()

    return json.loads(res.read())


def open_browser():
    webbrowser.open(_HOST)


def isRunning():
    data = get_data("app.available")
    success = data['success']
    if success:
        return True
    else:
        return False


def get_version():
    if isRunning():
        data = get_data("app.version")
        print data['version']
    else:
        print "CouchPotato is not running"

def ping():
    if isRunning():
        print "CouchPotato is running!"
    else:
        print "CouchPotato is not running"


def add_movie_by_id(identifier):
    data = get_data("movie.add?identifier=" + identifier)

    added = data['added']
    if added:
        print "Movie added to wanted list"
    else:
        print "Movie not found!"

def search_movie(query):
    data = get_data("movie.search" + "?q=" + query)
    fb = Feedback()
    for movie in data['movies']:
        movieTitle = movie['titles'][0]
        movieYear = str(movie['year'])
        identifier = movie['imdb']
        fb.add_item(movieTitle, movieYear, identifier)
    print fb


def forced_search():
    if isRunning():
        data = get_data("searcher.full_search")
        success = data['success']
        if success:
            print "Searching for movies..."
        else:
            print "Error - Can't search right now"
    else:
        print "CouchPotato is not running"


def update():
    if isRunning():
        data = get_data("updater.check")
        update_avail = data['update_available']
        if update_avail:
            print "Update available - Updating.."
        else:
            print "No update available"
    else:
        print "CouchPotato is not running"


def restart():
    if isRunning():
        data = get_data("app.restart")
        message = data['restart']
        if message:
            print message.title()
        else:
            print "Error - Can't restart right now"
    else:
        print "CouchPotato is not running"


def shutdown():
    if isRunning():
        get_data("app.shutdown")
        print "CouchPotato is shutting down"
    else:
        print "CouchPotato is not running"
