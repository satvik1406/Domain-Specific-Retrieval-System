import urllib.request
import urllib.parse
import re
import webbrowser

def search_song_on_youtube(query):
    """
    Function to play the song given out as output in youtube.
    INPUT
        Song name as selected by the user.
    RETURN
        Redirects user to the youtube video link.
    or  Displays "Video not found" if such a song does not exist in youtube.
    """
    query_string = urllib.parse.urlencode({"search_query" : query})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'\"\/watch\?v=(.{11})', html_content.read().decode())
    if not search_results:
        print("Video not found")
    else:
        webbrowser.open_new("http://www.youtube.com/watch?v=" + search_results[0])
