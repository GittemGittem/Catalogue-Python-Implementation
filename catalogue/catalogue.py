class ID:
        __slots__ = ("__id", "VALUE")
        def __init__(self, id, value=None):
            self.__id = id
            self.VALUE = value
        @property
        def ID(self):
            return self.__id
        
        def __repr__(self):
            value = getattr(self, "VALUE", None)
            if value is not None and value != "": value = " -> " + str(value)
            return f"|ID:{self.ID}{value or ''}|"
        
        def __eq__(self, other):
            match other:
                case other if isinstance(other, ID):
                    return self.ID == other.ID
                case other if isinstance(other, int):
                    return self.ID == other
                case _:
                    raise TypeError(f"Cannot compare '{self.__class__.__name__}' with '{other.__class__.__name__}'")
        def __ne__(self, other):
            return not self.__eq__(other)
        def __gt__(self, other):
            match other:
                case other if isinstance(other, ID):
                    return self.ID > other.ID
                case other if isinstance(other, int):
                    return self.ID > other
                case _:
                    raise TypeError(f"Cannot compare '{self.__class__.__name__}' with '{other.__class__.__name__}'")
        def __lt__(self, other):
            match other:
                case other if isinstance(other, ID):
                    return self.ID < other.ID
                case other if isinstance(other, int):
                    return self.ID < other
                case _:
                    raise TypeError(f"Cannot compare '{self.__class__.__name__}' with '{other.__class__.__name__}'")
        def __ge__(self, other):
            return self.__gt__(other) or self.__eq__(other)
        def __le__(self, other):
            return self.__lt__(other) or self.__eq__(other)
        
        def __and__(self, other):
            if self.VALUE is not None:
                if isinstance(other, ID):
                    return self.VALUE == other.VALUE
                return self.VALUE == other
            return False
            
class Registry:
    
    def seal(self):
        self.__sealed = True
    def unseal(self):
        self.__sealed = False
        
    def toggle_seal(self):
        self.__sealed = not self.__sealed
    
    def is_sealed(self):
        return self.__sealed
    
    
    def __enter__(self):
        self.unseal()
        return self.register
    
    def __exit__(self, *exc_args):
        self.seal()
    
    def __init__(self, name=None, step=1):
        self.step = step
        self.next_id = 0
        self.name = name
        self.__sealed = False
    
        self.ids = {}
    
    def __auto__(self, id):
        if id is None:
            id = self.next_id
        self.next_id = id + self.step
        return id
    
    def register(self, value:object=None, id:int=None) -> ID:
        if isinstance(value, ID):
            raise TypeError("Cannot set ID's value to an ID")
        if self.is_sealed(): # but if it has been locked, it can no longer be used unless context managered again
            name = getattr(self, 'name', None)
            if name is not None and name != "": name = f" '{name}'"
            raise SyntaxError(f"Cannot use a Registry{name or ""} while it is sealed")

        id = self.__auto__(id)
        if id in self.ids:
            instance = self.ids[id]
        else:
            instance = ID(id)
            self.ids[id] = instance
        instance.VALUE = value
        return instance
    def __getitem__(self, id):
        return self.ids[id]
    

with Registry() as auto:
    X = auto("hello", 10)
    Z = auto("hello", 10)
Y = ID(Z.ID, "hello")