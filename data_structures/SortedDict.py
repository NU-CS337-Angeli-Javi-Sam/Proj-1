class SortedDict:
    def __init__(self):
        self.__internalDict = {}
        self.__sortedKeys = []

        self.__isSorted = False

    def get(self, key):
        return self.__internalDict.get(key)

    def getKeys(self):
        return self.__internalDict.keys()

    def getValues(self):
        return self.__internalDict.values()

    def getSortedKeys(self):
        if not self.__isSorted:
            self.sort()

        return self.__sortedKeys

    def add(self, key, value):
        self.__internalDict[key] = value

        self.__isSorted = False
        #self.sort()

    def remove(self, key):
        del self.__internalDict[key]
        self.__sortedKeys.remove(key)

        self.__isSorted = False
        #self.sort()

    def updateKV_Pair(self, key, value):
        if key in self.__internalDict:
            self.__internalDict[key] = value

            self.__isSorted = False
            #self.sort()

    def sort(self):
        self.__sortedKeys = sorted(self.__internalDict, key=self.__internalDict.get, reverse=True)

    def getTop(self, k = 1):
        sorted_keys = self.getSortedKeys()

        if k <= len(sorted_keys):
            top_values = []

            for key in sorted_keys[0:k]:
                top_values.append([key, self.get(key)])

            return top_values

    def __str__(self):
        return str(self.getTop(len(self.getSortedKeys())))

    def __contains__(self, item):
        return item in self.__internalDict