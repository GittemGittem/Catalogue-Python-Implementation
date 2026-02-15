
class Group():
    
    class __Type:
                
        def __init__(self, step):
            self.next_id = 0
            self.step = step
        
        def __auto__(self, id=None):
            if id is None:
                id = self.next_id
            self.next_id = id + self.step
            return id
        
        def __enter__(self):
            return self.__auto__, self
        def __exit__(self, exc_type, exc_message, exc_traceback): pass
    class Enum(__Type): pass
    
    class Catalogue(__Type):
        def __init__(self, step):
            super().__init__(step)
            self.items = {}
        
        def __auto__(self, item, id=None):
            id = super().__auto__(id)
            self.items[id] = item
            return id
        
        def __getitem__(self, id=None):
            if id is None:
                try:
                    id = next(reversed(self.items))
                except StopIteration:
                    raise KeyError("No items available!")
            return self.items[id]
        
        def __iter__(self):
            for id in self.items:
                yield id
        def __contains__(self, id:int):
            return self.items[id]
            

with Group.Enum(step=1) as (auto, enum):
    X = auto()

print(X)

with Group.Catalogue(step = 1) as (auto, tileset):
    GRASS = auto("grass", 10)
    BRICK = auto("bricks")
print(GRASS)
print(tileset[BRICK])