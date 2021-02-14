import pickle

class pickleBot:
    def __init__(self):
        self.__picklingFile = ''
    
    def getPickleFile(self):
        if self.__picklingFile == '':
            print("Pickle Bot: Pickling File is currently not available")
            return
        return self.__picklingFile
    
    def setPickleFile(self, fileName):
        if fileName == '':
            print("Pickle Bot: File Name is able to be empty and was not set")
            return
        self.__picklingFile = fileName
    
    def pickle(self, data):
        if self.__picklingFile == '':
            print("Pickle Bot: Cannot pickle, Pickling File not set")
            return
        with open(self.__picklingFile, 'wb') as f:
            pickle.dump(data, f)
            print("Pickle Bot: Successfully pickled your data")
    
    def depickle(self):
        if self.__picklingFile == '':
            print("Pickle Bot: Cannot depickle, Pickling File not set")
            return
        with open(self.__picklingFile, "rb") as f:
            data = pickle.load(f)
            print("Pickle Bot: Successfully unpickled your data")
            return data