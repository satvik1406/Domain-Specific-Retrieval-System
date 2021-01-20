import pickle
import math
import numpy as np
import time

print("Processing data...")
start = time.time()


def load_dataset():
    """
    Function to load the two datasets.
    Two text files are the datasets:
      1) mxm_779k_matches.txt : which has information regarding track id,artist name,song title etc.
      2) mxm_dataset_train.txt : Which has a list of all top unique words and their frequency with respect to track id.
    RETURN
        1)numpy array
    and 2)dictionary track id -> term frequency
    and 3)dictionary track id -> artist name , song title etc.
    """
    vocab = []
    tf_dict = {}
    songinfo_dict = {}

    with open('src/dataset/mxm_779k_matches.txt', 'r', encoding="utf-8") as f:
        out = f.readlines()
        for line in out:
            line = line.strip('\n')
            if line[0] != '#':
                info = line.split("<SEP>")
                track_id = info[0]
                songinfo_dict[track_id] = info[1:]

    with open('src/dataset/mxm_dataset_train.txt', 'r') as f:
            out = f.readlines()
            for line in out:
                    line = line.strip('\n')
                    if line[0] != '#':
                            if line[0] == '%':
                                vocab = line[1:].split(',')
                            else:
                                tf = np.zeros(len(vocab))
                                track = line.split(',')
                                tid = track[0]
                                for term in track[2:]:
                                    word_count = term.split(':')
                                    index = int(word_count[0])-1
                                    count = int(word_count[1])
                                    tf[index] = count
                                tf /= np.linalg.norm(tf)
                                tf_dict[tid] = tf

    return np.array(vocab), tf_dict, songinfo_dict

def calculate_idf(vocab, tf_dict):
    """
    Function to calculate the inverse-document frequency.
    INPUT
        1)Unique words as a list.
        2)dictionary track id -> term frequency.
    RETURN
        inverse document frequency as a numpy array.
    """
    df = np.zeros(len(vocab))
    for tf in tf_dict.values():
        df = np.add(df,np.where(tf>0, 1, tf))
    idf = np.log2(len(tf_dict)*np.reciprocal(df))
    return idf

def calculate_tfidf(tf_dict, idf):
    """
    Function to calculte the tf-idf value of the track.
    INPUT
        1)dictionary track id -> term frequency
        2)inverse document frequency as a numpy array.
    RETURN
        dictionary track id -> inverse document frequency.
    """
    tf_idf_dict = {}
    for tid,tf in tf_dict.items():
        tf_idf_dict[tid] = np.multiply(tf,idf)
    return tf_idf_dict

def data_to_pickle(data):
    """
    Function to create and dump all data into a pickle file.
    INPUT
        all data tobe stored.
    """
    with open('src/dataset/processed_data.pkl', 'wb') as f:
            pickle.dump(data, f)


vocab, tf_dict, songinfo_dict = load_dataset()
idf = calculate_idf(vocab, tf_dict)
tf_idf_dict = calculate_tfidf(tf_dict, idf)
data_to_pickle([vocab, tf_idf_dict, idf, songinfo_dict])

print("Done.", len(tf_idf_dict), "files processed in", time.time()-start, "seconds.")
