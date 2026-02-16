
class Item:
    __slots__ = ("__id", "NAME", "VALUE", "PARENTS", "PARENT")
    def __init__(self, id:int):

        self.__id = id
        self.PARENT = None
        self.PARENTS = ()
        self.VALUE = None
        self.NAME = None
    

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
        return self.PARENT == other.PARENT and self.PARENT is not None

    def __xor__(self, other): # ^
        return self.VALUE is other.VALUE
    
    @staticmethod
    def is_id_name(name:str):
        return (not name.startswith('__') and not name.endswith('__')) and name.isupper()
    
    def __repr__(self):
        parent_name = getattr(self.PARENT, "name", None)
        name = self.NAME
        id = self.__id
        value = self.VALUE
        
        if parent_name is not None: parent_name = str(parent_name) + (":" if name is None else ".")
        if name is not None: name = name + "/"
        if value is not None: value = f" -> '{value}'"
        
        
        return f"|{parent_name or ""}{name or ""}{id}{value or ""}|"
    
    def __getitem__(self, value):
        if isinstance(value, Item):
            self.VALUE = value.VALUE
            self.NAME = value.NAME
            self.PARENTS = (*self.PARENTS, *value.PARENTS)
        else:
            self.VALUE = value
        return self
                
    @property
    def ID(self):
        return self.__id

class Catalogue:
    def __init__(self, name=None, step=1):
        self.step = step
        self.next_id = 0
        self.name = name
        
        self.items = {}
        self.ids = {}
    
    def __auto__(self, id=None):
        if id is None:
            id = self.next_id
        self.next_id = id + self.step
        return id
    
    def __create_item(self, id=None):
        if id in self.items:
            item = self.items[id]
        else:
            item = Item(self.__auto__(id))
        item.PARENT = self
        if self not in item.PARENTS:
            item.PARENTS = (*item.PARENTS, self)
        elif item.PARENTS[-1] != self:
            item.PARENTS = (*(parent for parent in item.PARENTS if parent is not self), self)
        return item
    
    def __getattr__(self, name):
        if name == "Item":
            return self.__create_item
        elif Item.is_id_name(name):
            return self.items[self.ids[name]]
        else:
            raise AttributeError(f"No attribute {name} in {self}")

    def __setattr__(self, name, value):
        match name, value:
            case name, value if name == "Item":
                raise ValueError("Cannot set Item on catalogue")
            case name, value if Item.is_id_name(name):
                if isinstance(value, Item):
                    value.NAME = name
                    value.PARENT = self
                    if self not in value.PARENTS:
                        value.PARENTS = (*value.PARENTS, self)
                    elif value.PARENTS[-1] != self:
                        value.PARENTS = (*(parent for parent in value.PARENTS if parent is not self), self)
                    self.items[value.ID] = value
                    self.ids[name] = value.ID
                else:
                    raise ValueError(f"Can only set item to 'Item' type not '{value.__class__.__name__}'")
            case name, value:
                super().__setattr__(name, value)
