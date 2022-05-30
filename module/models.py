from cmath import log
from unittest import result
import numpy 
import librosa, librosa.display
import glob
import pandas as pd
import csv
from .helpers import freq_from_fft


class Rindik:

    expected_bilah = ""
    audio_path = ""

    def __init__(self, expected_bilah, audio_path):
        self.expected_bilah = expected_bilah
        self.audio_path = audio_path

    def predict_bilah(self):
        data_set=pd.read_csv('content/Dataset_123.csv', index_col=False)
        data_set=data_set[data_set.columns[1:2]]
        number_of_rows,number_of_cols = data_set.shape

        data_nama=pd.read_csv('content/Dataset_123.csv', index_col=False)
        data_nama=data_nama[data_nama.columns[2:3]]
        number_of_rows,number_of_cols = data_nama.shape

        data_nama_value=numpy.array(data_nama)
        dataset_value = numpy.array(data_set)

        # main
        # databaru ini nantinya berisikan path dari android inputan user
        databaru = glob.glob(self.audio_path)

        hasil_freq = []
        value_fft = float()

        for a in databaru:
            x, sr = librosa.load(a)

            X = numpy.fft.fft(x)
            X_mag = numpy.absolute(X)
            f = numpy.linspace(0, sr, len(X_mag))

            value = freq_from_fft(x,sr)
            value_fft = value

        klasifikasi = []

        for j in dataset_value:
            coba = abs(float(j)-float(value_fft))
            klasifikasi.append(coba)
        
        pilihan_terbaik = klasifikasi.index(min(klasifikasi))
        jawaban = data_nama_value[pilihan_terbaik]
        

        return str(jawaban).replace('\'', '').replace('[', '').replace(']', '')