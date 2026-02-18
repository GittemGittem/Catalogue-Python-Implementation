
class Id:
    __slots__ = ("__id",)
    __ids__ = {}
    
    def __new__(cls, id:int):
        if id in cls.__ids__:
            return cls.__ids__[id]
        else:
            instance = super().__new__(cls)
            instance.__id = id
            cls.__ids__[id] = instance
            return instance
    
    def __eq__(self, other):
        if isinstance(other, Id):
            return self.__id == other.__id
        elif isinstance(other, int):
            return self.__id == other
        else:
            raise NotImplementedError(f"Cannot compare equivalence of type '{self.__class__.__name__}' {self} with type {other.__class__.__name__} {other}")
    def __ne__(self, other):
        return not self.__eq__(other)
    def __gt__(self, other):
        if isinstance(other, Id):
            return self.__id > other.__id
        elif isinstance(other, int):
            return self.__id > other
        else:
            raise NotImplementedError(f"Cannot compare instances of type '{self.__class__.__name__}' {self} and type {other.__class__.__name__} {other}")
    def __lt__(self, other):
        if isinstance(other, Id):
            return self.__id < other.__id
        elif isinstance(other, int):
            return self.__id < other
        else:
            raise NotImplementedError(f"Cannot compare instances of type '{self.__class__.__name__}' {self} and type {other.__class__.__name__} {other}")
    
    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)
    
    def __matmul__(self, other):
        return self is other
    
    @classmethod
    def New(cls, name):
        return type(name, (cls,), {"__ids__": {}})
    
    @property
    def ID(self):
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
        if id is None:
            id = self.next_id
        self.next_id = id + self.step
        return id
        
    
    def auto(self, value=None, id=None):
        if self.is_sealed():
            raise SyntaxError(f"Cannot add an entry to a sealed registry, {self}")
        id = self.id_class(self.__auto__(id))
        self.values[id] = value
        return id
    
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
        for attr_name in dir(cls):
            if is_entry(attr_name):
                match getattr(cls, attr_name):
                    case value, id if isinstance(id, Id):
                        reg.__named__[attr_name] = reg.auto(value, id.ID)
                    case value:
                        if isinstance(value, Id):
                            reg.__named__[attr_name] = reg.auto(id=id)
                        else:
                            reg.__named__[attr_name] = reg.auto(value)                 
    return reg
