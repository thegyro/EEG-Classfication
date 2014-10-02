import numpy
from scipy.stats import kurtosis

import pickle
import os
import glob
import sys
from  filter_eeg import butter_bandpass_filter
from util import mapminmax

class FeatureExtractor:
    def __init__(self,sample_freq,duration,channels,train_dir,classes):
        self.sample_freq = sample_freq
        self.duration = duration
        self.train_dir = train_dir
        self.channels = channels
        self.classes = classes


    def combine_data(self,reject):
        reject_samples = reject*self.sample_freq
        eeg_class_data  = {}

        no_train_samples = len(glob.glob(self.classes[0] + '/EEG*'))
        total_len = self.sample_freq * (self.duration - reject) * no_train_samples

        #net_eeg_data = numpy.ndarray((total_len,len(self.channels) + 1))
        for klass in self.classes:
            train_files = glob.glob(klass + '/EEG*')
            file_path = self.train_dir + '/'
            try:
                with open(file_path + train_files[0]) as eeg:
                    eeg_data1 = pickle.load(eeg)
                    eeg_data1 = eeg_data1.astype(numpy.int64)

                with open(file_path + train_files[1]) as eeg:
                    eeg_data2 = pickle.load(eeg)
                    eeg_data2 = eeg_data2.astype(numpy.int64)
                
                net_eeg_data = numpy.concatenate((eeg_data1[reject_samples:,:],eeg_data2[reject_samples:,:]),axis=0)

            except IndexError:
                sys.stderr.write('Have at least two freaking training samples :-/ . \n')
                sys.exit(0)
            
            for pickle_no in range(2,len(train_files)):
                with open(file_path + train_files[pickle_no]) as eeg:
                    eeg_data = pickle.load(eeg)
                    eeg_data = eeg_data.astype(numpy.int64)

                net_eeg_data = numpy.concatenate((net_eeg_data,eeg_data[reject_samples:,:]), axis=0)

                
            eeg_class_data[klass] = net_eeg_data

        return eeg_class_data
        
    def filter_the_damn_data(self,reject,lowcut,highcut,order,channel_nos):
        net_eeg = self.combine_data(reject)
        no_channels = len(channel_nos)

        eeg_filter_data = {}
        for klass in net_eeg:
            if no_channels > 1:
                channels = channel_nos.keys()
                eeg1 = butter_bandpass_filter(net_eeg[klass][:,channel_nos[channels[0]]],lowcut,highcut,self.sample_freq,order)
                eeg2 = butter_bandpass_filter(net_eeg[klass][:,channel_nos[channels[1]]],lowcut,highcut,self.sample_freq,order)

                eeg_filtered = numpy.vstack((eeg1,eeg2))
                for i in range(2,len(channels)):
                    eeg_filtered = numpy.vstack((eeg_filtered,net_eeg[:,channel_nos[channels[i]]]))

                eeg_filter_data[klass] = eeg_filtered

            elif no_channels == 1 :
                eeg_filter_data = {klass:butter_bandpass_filter(net_eeg[klass][:,0],lowcut,highcut,self.sample_freq,order) for klass in net_eeg}

            else:
                sys.stderr.write(' Dei. Give at least one channel :-/ ')
                sys.exit(0)

        return eeg_filter_data
        
    def build_feature_vector(self):
        lowcut = 3
        highcut = 40
        reject = 2
        order = 4

        channel_nos = {'F3':1, 'AF3':3}
        
        eeg_filter_data = self.filter_the_damn_data(reject,lowcut,highcut,order,channel_nos)

        eeg_feature = {}
        for klass in eeg_filter_data:
            eeg = eeg_filter_data[klass]
            diff_eeg = eeg[0] - eeg[1]
            split_len = len(diff_eeg)/(self.sample_freq*5)
            input_mat = numpy.array([ [max(sample),kurtosis(sample),min(sample)] for sample in numpy.split(diff_eeg,split_len) ])
            norm_mat,ps = mapminmax(numpy.transpose(input_mat))
            norm_mat = numpy.transpose(norm_mat)
            eeg_feature[klass] = [norm_mat[i] for i in range(split_len)]

        return eeg_feature
