
class Id:
    __slots__ = ("__id",)
    __ids__ = {}
    
    def __new__(cls, id:'int|Id'):
        if isinstance(id, int):
            if id in cls.__ids__:
                return cls.__ids__[id]
            else:
                instance = super().__new__(cls)
                instance.__id = id
                cls.__ids__[id] = instance
                return instance
        elif isinstance(id, Id): # convert Id into my id type
            return cls(id.ID)
        else:
            return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, Id):
            return self.__id == other.__id
        elif isinstance(other, int):
            return self.__id == other
        else:
            return NotImplemented
    def __ne__(self, other):
        if isinstance(other, Id):
            return self.__id != other.__id
        elif isinstance(other, int):
            return self.__id != other
        else:
            return NotImplemented
    def __gt__(self, other):
        if isinstance(other, Id):
            return self.__id > other.__id
        elif isinstance(other, int):
            return self.__id > other
        else:
            return NotImplemented
    def __lt__(self, other):
        if isinstance(other, Id):
            return self.__id < other.__id
        elif isinstance(other, int):
            return self.__id < other
        else:
            return NotImplemented
    
    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)
    
    def __matmul__(self, other):
        return (self, other)
    def __rmatmul__(self, other):
        return (other, self)
    
    @classmethod
    def New(cls, name):
        return type(name, (cls,), {"__ids__": {}})
    
    @property
    def ID(self) -> int:
        return self.__id
    
    def __repr__(self):
        return f"|{self.__class__.__name__}:{self.__id}|"
    
    def __int__(self):
        return self.__id
    
    def __hash__(self):
        return hash((self.__id, self.__class__))

class Registry:
    __slots__ = ("values", "id_class", "step", "next_id", "__named__", "sealed")
    
    def seal(self):
        self.sealed = True
    def unseal(self):
        self.sealed = False
    def is_sealed(self):
        return self.sealed
    
    def __init__(self, step = 1, id_class=Id):
        if isinstance(id_class, str):
            id_class = Id.New(id_class)
        self.id_class = id_class
        self.sealed = False
        
        self.__named__ = {}
        
        self.next_id = 0
        self.step = step
        self.values = {}
    
    def __getitem__(self, id:Id):
        if isinstance(id, str):
            if id in self.__named__:
                id = self.__named__[id]
        return self.values[id]

    def __getattr__(self, name):
        if name in self.__named__:
            return self.__named__[name]
        raise AttributeError(f"{self} does not contain an attribute '{name}'")
    
    def __setitem__(self, id:Id, value):
        if self.is_sealed():
            raise SyntaxError(f"Cannot modify the entry of a sealed registry, {self}")
        self.values[id] = value
    
    def __auto__(self, id=None):
        if isinstance(id, Id):
            return id
        if id is None:
            id = self.next_id
        self.next_id = id + self.step
        return id
        
    
    def auto(self, value=None, id=None):
        if self.is_sealed():
            raise SyntaxError(f"Cannot add an entry to a sealed registry, {self}")
        id = self.id_class(self.__auto__(id))
        if isinstance(value, Id):
            raise TypeError(f"Cannot store an Id in the registry: '{value}' at '{id}'")
        self.values[id] = value
        return id
    def __lshift__(self, other):
        match other:
            case id1, id2 if (isinstance(id1, Id) and isinstance(id2, Id)):
                return self.auto(id1, id2)
            case value, id if isinstance(id, Id):

                return self.auto(value, id)
            case id, value if isinstance(id, Id):

                return self.auto(value, id)
            case id if isinstance(id, Id):

                return self.auto(id=id)
            case value:

                return self.auto(value)
    def __rshift__(self, id):
        return self.values[id]
    
    def name(self, id:Id, name):
        self.__named__[name] = id
    
    def __enter__(self):
        return self
        
    def __exit__(self, *exc_args):
        self.seal()

def __is_entry(name:str) -> bool:
    return name.isupper() and not (name.startswith('__') or name.endswith('__'))
def registry(cls) -> Registry:
    if hasattr(cls, '__is_entry__'):
        is_entry = cls.__is_entry__
    else:
        is_entry = __is_entry
    with Registry(id_class=cls.__name__) as reg:
        for attr_name in vars(cls):
            if is_entry(attr_name):
                id = reg << getattr(cls, attr_name)
                reg.name(id, attr_name)
                
    return reg