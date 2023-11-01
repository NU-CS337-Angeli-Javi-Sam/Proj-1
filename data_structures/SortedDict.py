class SortedDict:
    """
    A dictionary-like data structure with sorted keys and additional utility methods for managing key-value pairs.

    Attributes:
    - internalDict (dict): The internal dictionary for storing key-value pairs.
    - sortedKeys (list): A list of sorted keys.
    - isSorted (bool): A flag indicating whether the keys are sorted.

    """

    def __init__(self):
        """
        Initializes a SortedDict with an empty internal dictionary, an empty list of sorted keys,
        and sets the 'isSorted' flag to False.
        """
        self.__internalDict = {}  # Internal dictionary for storing key-value pairs.
        self.__sortedKeys = []  # A list of sorted keys.
        self.__isSorted = False  # Flag indicating whether the keys are sorted.


    def get(self, key):
        """
        Get the value associated with a given key.

        Parameters:
        - key: The key to retrieve the associated value.

        Returns:
        - The value associated with the key, or None if the key is not present.
        """
        return self.__internalDict.get(key)

    def getKeys(self):
        """
        Get all keys in the dictionary.

        Returns:
        - A list of keys in the dictionary.
        """
        return self.__internalDict.keys()

    def getSortedKeys(self):
        """
        Get sorted keys, sorting the dictionary by values in descending order.

        Returns:
        - A list of keys sorted by their corresponding values in descending order.
        """
        if not self.__isSorted:
            self.sort()

        return self.__sortedKeys

    def getItems(self):
        """
        Get all key-value pairs as a list of (key, value) tuples.

        Returns:
        - A list of (key, value) tuples representing all key-value pairs in the dictionary.
        """
        return self.__internalDict.items()

    def getValues(self):
        """
        Get all values in the dictionary.

        Returns:
        - A list of all values stored in the dictionary.
        """
        return self.__internalDict.values()

    def add(self, key, value):
        """
        Add a new key-value pair to the dictionary.

        Parameters:
        - key: The key to add.
        - value: The value to associate with the key.
        """
        self.__internalDict[key] = value

        self.__isSorted = False

    def remove(self, key):
        """
        Remove a key-value pair from the dictionary.

        Parameters:
        - key: The key to remove from the dictionary.
        """
        del self.__internalDict[key]
        self.__sortedKeys.remove(key)

        self.__isSorted = False

    def updateKV_Pair(self, key, value):
        """
        Update the value associated with a given key.

        Parameters:
        - key: The key to update.
        - value: The new value to set for the key.
        """
        if key in self.__internalDict:
            self.__internalDict[key] = value
            self.__isSorted = False

    def getTop(self, k = 1):
        """
        Get the top k key-value pairs, ordered by values.

        Parameters:
        - k (int): The number of top key-value pairs to retrieve.

        Returns:
        - A list of the top k key-value pairs ordered by values.
        """
        sorted_keys = self.getSortedKeys()

        if k <= len(sorted_keys):
            top_values = []

            for key in sorted_keys[0:k]:
                top_values.append([key, self.get(key)])

            return top_values

    def sort(self):
        """
        Sort the keys based on their corresponding values in descending order.
        """
        self.__sortedKeys = sorted(self.__internalDict, key=self.__internalDict.get, reverse=True)


    def __str__(self):
        """
        Get a string representation of the top key-value pairs.

        Returns:
        - A formatted string representation of the top key-value pairs.
        """
        return str(self.getTop(len(self.getSortedKeys())))

    def __contains__(self, item):
        """
        Check if a given item is contained in the dictionary.

        Parameters:
        - item: The item to check for existence in the dictionary.

        Returns:
        - True if the item is in the dictionary, False otherwise.
        """
        return item in self.__internalDict

    def __len__(self):
        """
        Get the number of key-value pairs in the dictionary.

        Returns:
        - The number of key-value pairs in the dictionary.
        """

        return len(self.__internalDict)

    def __getitem__(self, key):
        """
        Get the value associated with a given key.

        Parameters:
        - key: The key to retrieve the associated value.

        Returns:
        - The value associated with the key, or None if the key is not present.
        """

        return self.__internalDict[key]

    def __setitem__(self, key, value):
        """
        Set or update the value associated with a given key.

        Parameters:
        - key: The key to set or update.
        - value: The new value to associate with the key.
        """

        self.__internalDict[key] = value
