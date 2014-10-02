from pybrain.datasets import SupervisedDataSet,ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer

from feature_extraction import FeatureExtractor

from pylab import ion,ioff,figure,draw,contourf,clf,show,hold,plot
from scipy import diag,arange,meshgrid,where
import numpy

class EegNeuralNetworkFeedForward:
    def __init__(self,classes,fs,channels,train_dir,duration):
        self.classes = classes
        f = FeatureExtractor(fs,duration,channels,train_dir,classes)
        self.feature_matrix = f.build_feature_vector()
        self.len_train = len(self.feature_matrix[self.classes[0]])
        self.testdata = None
        self.traindata = None
        self.alldata = None
        self.trainer = None
        self.fnet = None

    def populate_training_data(self,len_test):
        self.alldata = ClassificationDataSet(3,1,nb_classes=2)

        for klass in range(len(self.classes)):
            for fvector in self.feature_matrix[self.classes[klass]]:
                if(klass == 0):
                    self.alldata.addSample(fvector,[klass])
                else:
                    self.alldata.addSample(fvector,[klass])

        self.testdata,self.traindata = self.alldata.splitWithProportion(0.25)
        
        self.testdata._convertToOneOfMany()
        self.traindata._convertToOneOfMany()

    def train_the_network(self,no_hidden1,no_hidden2):
        input_neurons = len(self.feature_matrix[self.classes[0]][0])
        self.fnet = buildNetwork(input_neurons,no_hidden1,no_hidden2,2)
        self.trainer = BackpropTrainer(self.fnet,self.traindata)
        for i in range(125):
            error = self.trainer.train()
            #print('%d iteratrions of training completed' % i)
            #error = trainer.train()
            trnresult = percentError(self.trainer.testOnClassData(), self.traindata['class'])
            tstresult = percentError(self.trainer.testOnClassData(dataset=self.testdata),self.testdata['class'])
            print "epoch: %4d" % self.trainer.totalepochs," train error: %5.2f%%" % trnresult, " test error: %5.2f%%" % tstresult

    def test_network(self,len_test):
        err = self.trainer.train()
        test_score = 0
        train_score = 0
        for klass in range(len(self.classes)):
            for fvector in self.feature_matrix[self.classes[klass]][self.len_train-len_test : self.len_train]:
                output = self.fnet.activate(fvector)
                output = numpy.round(output)
                
                if klass == 0:
                    if numpy.array_equal(output,[1,0]):
                        test_score += 1
                else:
                    if numpy.array_equal(output,[0,1]):
                        test_score += 1

            for fvector in self.feature_matrix[self.classes[klass]][:self.len_train-len_test]:
                output = self.fnet.activate(fvector)
                output = numpy.round(output)

                if klass == 0:
                    if numpy.array_equal(output,[1,0]):
                        train_score += 1
                else:
                    if numpy.array_equal(output,[0,1]):
                        train_score += 1

        train_acc = float(train_score)/(2*self.len_train-2*len_test)
        test_acc = float(test_score)/(2*len_test)

        return train_acc,test_acc,err

def main():
    channels = ["F3", "FC5", "AF3", "F7", "T7", "P7", "O1", "O2", "P8",  "T8",  "F8", "AF4", "FC6", "F4"]
    #f = FeatureExtractor(128,7,channels,'/home/srinath/Code/PS-1/Code/Eye',['Blink','Open','Close'])
    eeg_neural = EegNeuralNetworkFeedForward(['Blink','Open'],128,channels,'/home/srinath/Code/PS-1/Code/Eye',7)
   
    eeg_neural.populate_training_data(20)
    eeg_neural.train_the_network(30,15)
    #[train_acc,test_acc,err] = eeg_neural.test_network(20)

    #print "Training error is %f" % err
    #print "Train Classification Accuracy %f" % train_acc
    #print "Test Classification Accuracy %f" % test_acc

if __name__ == '__main__':
    main() 