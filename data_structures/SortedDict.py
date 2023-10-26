class SortedDict:
    def __init__(self):
        self.__internalDict = {}
        self.__sortedKeys = []

<<<<<<< HEAD
        self.__isSorted = False

    #Getters------------------------------------------
=======
>>>>>>> main
    def get(self, key):
        return self.__internalDict.get(key)

    def getKeys(self):
        return self.__internalDict.keys()
<<<<<<< HEAD
    def getSortedKeys(self):
        if not self.__isSorted:
            self.sort()

        return self.__sortedKeys
    def getValues(self):
        return self.__internalDict.values()

    # Setters------------------------------------------
    def add(self, key, value):
        self.__internalDict[key] = value

        self.__isSorted = False
        #self.sort()
=======

    def getValues(self):
        return self.__internalDict.values()

    def getSortedKeys(self):
        return self.__sortedKeys

    def add(self, key, value):
        self.__internalDict[key] = value
        self.sort()
>>>>>>> main

    def remove(self, key):
        del self.__internalDict[key]
        self.__sortedKeys.remove(key)
<<<<<<< HEAD

        self.__isSorted = False
        #self.sort()
=======
        self.sort()
>>>>>>> main

    def updateKV_Pair(self, key, value):
        if key in self.__internalDict:
            self.__internalDict[key] = value
<<<<<<< HEAD

            self.__isSorted = False
            #self.sort()

    # Utils------------------------------------------
    def getTop(self, k = 1):
        sorted_keys = self.getSortedKeys()

        if k <= len(sorted_keys):
            top_values = []

            for key in sorted_keys[0:k]:
                top_values.append([key, self.get(key)])

            return top_values
    def sort(self):
        self.__sortedKeys = sorted(self.__internalDict, key=self.__internalDict.get, reverse=True)

    # Object Functionalities------------------------------------------

    # allows print() function usage on data struct
    def __str__(self):
        return str(self.getTop(len(self.getSortedKeys())))

    # allows 'in' key word usage
    def __contains__(self, item):
        return item in self.__internalDict

    # allows len() function usage on data struct
    def __len__(self):
        return len(self.__internalDict)

    # Allows indexing O(1)
    def __getitem__(self, key):
        return self.__internalDict[key]

    #Allows item assignment, e.g. list[key] += 1
    def __setitem__(self, key, value):
        self.__internalDict[key] = value

    #Allows del to work on dict
    # def __del__(self, key):
    #     del self.__internalDict[key]

=======
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
>>>>>>> main
