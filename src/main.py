import pickle
import numpy as np
from scipy import spatial
from heapq import nlargest
import time
from src.stemmer import lyrics_to_bow
from src.search_yt import search_song_on_youtube
from tabulate import   tabulate

def load_database():
    """
    Function to load the database from a pickle file where all the processed data has been loaded.
    RETURN
        1)numpy array
    and 2)dictionary track id -> term frequency
    and 3)dictionary track id -> artist name , song title etc.
    """
    start = time.time()
    print("Loading database...")
    with open('src/dataset/processed_data.pkl', 'rb') as f:
        data = pickle.load(f)
    vocab = data[0]
    tf_idf_dict = data[1]
    idf = data[2]
    songinfo_dict = data[3]
    print("Done.", len(tf_idf_dict), "files loaded in", time.time()-start, "seconds.")
    return vocab, tf_idf_dict, idf, songinfo_dict

def query_to_tfidf(query):
    """
    Function to calculate the term frequency-inverse document frequency for the input query.
    INPUT
        song query as string as input by user.
    RETURN
        term frequency-inverse document frequency as a numpy array.
    """
    bow = lyrics_to_bow(query)
    tf = np.zeros(len(vocab))
    for term,count in bow.items():
        index = np.where(vocab == term)[0]
        if len(index>0):
            tf[index[0]] += count
    tf /= np.linalg.norm(tf)
    tf_idf = np.multiply(tf,idf)
    return tf_idf

def execute_query(query):
    """
    Function to compare the tf-idf of database and song query to get the top results regarding our query.
    INPUT
        Song query as string as input by user.
    RETURN
        The top results from Search.
    """
    start = time.time()
    query_tf_idf = query_to_tfidf(query)
    def get_scores():
        """
        Function to calculate and asign cosine similarities to the terms in database and input query.
        Each term in query gets a score using which we can asses the top tracks(documents) that have the the lyric in them.
        """
        for tid,tfidf in tf_idf_dict.items():
            score = 1 - spatial.distance.cosine(query_tf_idf, tfidf)
            yield [score,tid]
    results = nlargest(10, get_scores())
    print("Search results found in", time.time()-start, "seconds.\n")
    return results

def print_results(results):
    """
    Function to print the search resultsin a tabulated form.
    INPUT
        The top results from search.
    """
    table = []
    idx=0
    for track in results:
        idx+=1
        table.append([str(idx), track[1], track[0], songinfo_dict[track[1]][1], songinfo_dict[track[1]][3]])
    print(tabulate(table, headers=["#", "Track ID","Score", "Title", "Artist"]))


def play_song(results):
    """
    Function to play the selected song in youtube.
    INPUT
        top results from search.
    """
    print("\nSelect a song to play on youtube (Enter 0 to skip)")
    option = int(input()) -1
    if option == -1:
        return
    elif option > len(results):
        print("Invalid input")
        return
    print("\nPlaying song: ", songinfo_dict[results[option][1]][1])
    search_song_on_youtube(songinfo_dict[results[option][1]][1] + " " + songinfo_dict[results[option][1]][3])


vocab, tf_idf_dict, idf, songinfo_dict = load_database()
while True:
    query = input("\nEnter a search query (Enter 'exit' to exit program):\t")
    if query == "exit":
        break
    results = execute_query(query)
    print_results(results)
    play_song(results)
