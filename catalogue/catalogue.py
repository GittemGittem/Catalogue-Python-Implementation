from typing import Any

class __catalogue(type):
    __root_class = None
    
    class Item:
        type ItemID = int
        type ItemName = str
        type ItemValue = Any
        
        def __init__(self, id, name, value, parent):
            self.__id = id
            self.__name = name
            self.__value = value
            self.__parent = parent
            
        @property
        def ID(self) -> ItemID:
            return self.__id
        @property
        def PARENT(self) -> "Catalogue":
            return self.__parent
        @property
        def NAME(self) -> ItemName:
            return self.__name
        @property
        def VALUE(self) -> ItemValue:
            return self.__value
        
        def __repr__(self) -> str:
            match self.VALUE:
                case None:
                    value = ""
                case anything_else:
                    value = f" -> {anything_else}"                    
            return f"|{self.__parent.__name__}.{self.NAME}/{self.__id}{value}|"
        
        def __eq__(self, other) -> bool:
            return (self.__id == other.ID)
        def __ne__(self, other) -> bool:
            return not self.__eq__(other)
        
        def __gt__(self, other) -> bool:
            return self.__id > other.ID
        def __lt__(self, other) -> bool:
            return self.__id < other.ID
        
        def __le__(self, other) -> bool:
            return self.__lt__(other) or self.__eq__(other)
        def __ge__(self, other) -> bool:
            return self.__gt__(other) or self.__eq__(other)
        
    def __new__(meta, name, bases, namespace, **keywords) -> "Catalogue":
        if meta.__root_class is None:
            meta.__root_class = super().__new__(meta, name, bases, namespace, **keywords)
            return meta.__root_class
        else:
            base = {
                        "next_id" : 0,
                        "instances":{},
                        "ids":{},
                        "step":1
                    }
            for key, val in namespace.items():
                if not (key.isupper() and not (key.startswith("__") and key.endswith("__"))):
                    base[key] = val
                    
                    
            cls = super().__new__(meta, name, bases, base, **keywords)
            for name, value in namespace.items():
                if (not name.startswith('__') and not name.endswith('__')) and name.isupper():
                    if isinstance(value, tuple):
                        item, id = value

                        if not isinstance(id, int):
                            id = None
                    elif isinstance(value, dict):
                        item = value.get("item", None) or value.get("ITEM")
                        id = value.get("id", None) or value.get("ID")
                    else:
                        item, id = value, None
                    meta.__call__(cls, name, item, id)
            return cls
    
    def __call__(cls, name, item, id=None) -> Item:
        
        if cls is cls.__class__.__root_class:
            raise SyntaxError("Cannot use Catalogue class as a catalogue")
        if id is None:
            id = cls.next_id
        cls.next_id = id + cls.step
        
        if id in cls.instances:
            instance = cls.instances[id]
            instance._Item__value = item
            instance._Item__name = name
        else:
            instance = cls.__class__.Item(id, name, item, cls)
            cls.instances[id] = instance
        cls.ids[name] = id
        return instance

    def __getattr__(cls, name):
        if name in cls.ids:
            return cls.instances[cls.ids[name]]
        else:
            raise KeyError(f"No item '{name}' in {cls.__name__}")


class Catalogue(metaclass = __catalogue):
    def __init_subclass__(cls, step=1):
        cls.step = step

        
if __name__ == "__main__":
    class Colors(Catalogue):
        RED = {"ITEM":(0, 0, 0), "ID":0}
        BLUE = (0, 0, 255), 0

    print(Colors.RED == Colors.BLUE)

    print(Colors.RED.PARENT)