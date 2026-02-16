

class Catalogue():
    @staticmethod
    def isitemname(name:str) -> bool:
        return name.isupper() and not (name.startswith('__') and name.endswith('__'))
    class Item:
        def __init__(self):
            self.VALUE = None
            self.ID = None
            self.NAME = None
            self.PARENTS = ()
            self.PARENT = None
        def __repr__(self):
            return f"|{self.PARENT.__name__ + '.' if self.PARENT.__name__ is not None else ''}{self.NAME}/{self.ID} -> '{self.VALUE}'|"
            
        def __eq__(self, other):
            return self.ID == other.ID
        def __ne__(self, other):
            return not self.__eq__(other)
        def __gt__(self, other):
            return self.ID > other.ID
        def __lt__(self, other):
            return self.ID < other.ID
        def __ge__(self, other):
            return self.__gt__(other) or self.__eq__(other)
        def __le__(self, other):
            return self.__lt__(other) or self.__eq__(other)

        def __matmul__(self, other): # @
            return len(set(self.PARENTS) & set(other.PARENTS)) > 0
        
        def __and__(self, other): # &
            return self.PARENT == other.PARENT

        def __xor__(self, other): # ^
            return self.VALUE is other.VALUE
        
    def __init__(self, name=None, step=1):
        self.__name__ = name
        self.step = step
        self.__locked = True
        
        self.next_id = 0
        
        self.items = {}
        self.ids = {}
        
    def __iter__(self):
        yield from self.items.values()
            
    def __contains__(self, value):
        match value:
            case item if isinstance(item, self.Item):
                return item in self.items.values()
            case id if isinstance(id, int):
                return id in self.items
    def LOCK(self):
        if self.__locked:
            raise SyntaxError("Items must be assigned while in assignment mode (use with to enter assignment mode)")
        
                    
    def __getattr__(self, name):
        if name in self.ids:
            return self.items[self.ids[name]]
        else:
            raise AttributeError(f"There is no '{name}' item in {self}")
    def register(self, name, value, id=None):
        self.LOCK()
        parents = ()
        if isinstance(value, self.Item):
            name = value.NAME
            parents = value.PARENTS
            value = value.VALUE        
        if id is None:
            id = self.next_id
        self.next_id = id + self.step
        
        self.ids[name] = id
        if id in self.items:
            item = self.items[id]
        else:
            item = Catalogue.Item()
            self.items[id] = item
        item.VALUE = value
        item.ID = id
        item.NAME = name
        if self not in parents:
            parents = (*parents, self)
        item.PARENTS = parents
        item.PARENT = self
        return item
        
    def __setattr__(self, name, value):
        if self.isitemname(name):
            self.LOCK()
            if isinstance(value, tuple):
                value, id = value
            else:
                id = None
            self.register(name, value, id)
        else:
            super().__setattr__(name, value)
    
    def __enter__(self):
        self.__locked = False
        return self
    def __exit__(self, exc_type, exc_message, exc_traceback):
        self.__locked = True
                    

with Catalogue("TILESET", 1) as tileset:
    tileset.GRASS = "grass", 10
    DIRT = tileset.register("DIRT", "dirt")

print(DIRT)
print(tileset.GRASS.VALUE)
print(tileset.DIRT.ID)
print(tileset.GRASS.NAME)
