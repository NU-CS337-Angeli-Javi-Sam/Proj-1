class SortedDict:
    def __init__(self):
        self.__internalDict = {}
        self.__sortedKeys = []

    def get(self, key):
        return self.__internalDict.get(key)

    def getKeys(self):
        return self.__internalDict.keys()

    def getValues(self):
        return self.__internalDict.values()

    def getSortedKeys(self):
        return self.__sortedKeys

    def add(self, key, value):
        self.__internalDict[key] = value
        self.sort()

    def remove(self, key):
        del self.__internalDict[key]
        self.__sortedKeys.remove(key)
        self.sort()

    def updateKV_Pair(self, key, value):
        if key in self.__internalDict:
            self.__internalDict[key] = value
            self.sort()
        else:
            self.add(key, value)

    def sort(self):
        self.__sortedKeys = sorted(self.__internalDict, key=self.__internalDict.get, reverse=True)

    def getTop(self, k = 1):
        if k <= len(self.__sortedKeys):
            top_values = []

            for key in self.__sortedKeys[0:k]:
                top_values.append([key, self.get(key)])

            return top_values

    def __str__(self):
        return str(self.getTop(len(self.__sortedKeys)))

    def __contains__(self, item):
        return item in self.__internalDict