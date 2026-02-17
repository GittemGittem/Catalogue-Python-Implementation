def not_implemented(*args, **kwargs):
    raise NotImplementedError("This method is not implemented.")

class Id:
    __slots__ = ("__id",)
    __ids__ = {}
    
    def __new__(cls, id):
        if id in cls.__ids__:
            return cls.__ids__[id]
        else:
            instance = super().__new__(cls)
            instance.__id = id
            cls.__ids__[id] = instance
            return instance
    
    @classmethod
    def Sub(cls, name):
        return type(name, (cls,), {"__ids__": {}})
    
    @property
    def ID(self):
        return self.__id
    
    def __repr__(self):
        return f"|ID:{self.__id}|"
    
    def __int__(self):
        return self.__id
    
    def __hash__(self):
        return hash((self.__id, self.__class__))

class Registry:
    __slots__ = ("values", "_in_full_context", "id_class", "step", "next_id")
    
    
    def full_context(self):
        self._in_full_context = True
        return self
    def exit_full_context(self):
        self._in_full_context = False
        return self
    
    def __init__(self, step = 1, id_class=Id):
        if isinstance(id_class, str):
            id_class = Id.Sub(id_class)
        self.id_class = id_class
        
        self.next_id = 0
        self.step = step
        self.values = {}
    
    def __getitem__(self, id:Id):
        return self.values[id]
    
    def __setitem__(self, id:Id, value):
        self.values[id] = value
    
    def __auto__(self, id=None):
        if id is None:
            id = self.next_id
        self.next_id = id + self.step
        return id
        
    
    def __create_id__(self, id=None, value=None):
        id = self.id_class(self.__auto__(id))
        self.values[id] = value
        return id
    
    def __enter__(self):
        if self._in_full_context:
            return self.__create_id__, self
        return self.__create_id__
        

    def __exit__(self, *exc_args):
        self.exit_full_context()