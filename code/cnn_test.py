import librosa, librosa.display
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import euclidean
from sklearn.metrics.pairwise import euclidean_distances
from numpy import genfromtxt

def oti_func(original_features, cover_features):
    profile1 = np.sum(original_features.T, axis = 1)
    profile2 = np.sum(cover_features.T, axis = 1)
    oti = [0] * 12
    for i in range(profile2.shape[0]):
        oti[i] = np.dot(profile1, np.roll(profile2, i))
    oti.sort(reverse=True)
    newmusic = np.roll(cover_features.T, int(oti[0]))
    return newmusic.T

def extract_features(signal):
    return librosa.feature.chroma_stft(signal)[:12, :180].T

def sim_matrix(original_features, cover_features):
    similarity_matrix = []
    for each in original_features:
        sm = []
        for beach in cover_features:
            sm.append(euclidean(each, beach))
        similarity_matrix.append(sm)
    return np.array(similarity_matrix)

original_song = "../data/test_data/take_on_me.mp3"
cover_song = "../data/test_data/take_on_me_cover.mp3"

original_signal = librosa.load(original_song)[0]
cover_signal = librosa.load(cover_song)[0]

original_features = extract_features(original_signal)
cover_features = extract_features(cover_signal)

oti_cover_features = oti_func(original_features, cover_features)

mat = sim_matrix(original_features, oti_cover_features)
plt.imshow(mat, cmap='hot', interpolation='nearest')
plt.show()
