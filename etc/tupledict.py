class TupleDict(dict):

    def __contains__(self, key):
        e1, e2 = key
        return super().__contains__((e1, e2)) or super().__contains__((e2, e1))

    def __delitem__(self, key):
        e1, e2 = key
        if super().__contains__((e1, e2)):
            super().__delitem__((e1, e2))
        elif super().__contains__((e2, e1)):
            super().__delitem__((e2, e1))
    
    def __getitem__(self, key):
        e1, e2 = key
        if super().__contains__((e1, e2)):
            return super().__getitem__((e1, e2))
        elif super().__contains__((e2, e1)):
            return super().__getitem__((e2, e1))
        else:
            raise ValueError(f"Key {key} does not exist")

    def __setitem__(self, key, value):
        e1, e2 = key
        if super().__contains__((e2, e1)):
            super().__setitem__((e2, e1), value)
        else:
            super().__setitem__((e1, e2), value)