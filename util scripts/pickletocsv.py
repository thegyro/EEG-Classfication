import csv
import pickle
import glob
import sys
import os

def convert_pickle_to_csv(pickle_path,ofile,reject):
	files = glob.glob(pickle_path + "EEG*")
	csvwriter = csv.writer(ofile,delimiter=',')
	for f in files:
		fullpath = f
		with open(fullpath) as e:
			eeg = pickle.load(e)

		for row in eeg:
			csvwriter.writerow(row)

	ofile.close()


def main():
	pickle_path = sys.argv[1]
	ofname = sys.argv[2]

	reject = 128*2
	if os.path.isfile(ofname):
		print("Hey! A file already exists in that name.You want to overwrite?")
		op = raw_input('Yes or No? (y or n): ')
		if op=='y' or op=='yes':
			ofile = open(ofname,'wb')
			convert_pickle_to_csv(pickle_path,ofile,reject)

		else:
			sys.exit(0)

	else:
		ofile = open(ofname,'wb')
		convert_pickle_to_csv(pickle_path,ofile,reject)

if __name__ == '__main__':
	main()