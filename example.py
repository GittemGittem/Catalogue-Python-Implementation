# IMPORTING
# if the user has correctly installed rising-registry from pypi as shown below
# (in terminal run "pip install rising-registry" or pip install --upgrade rising-registry)

from registry import Registry, registry, Id # import it's features like this

#CREATING ID OBJECTS

# an id can be used on it's own without a registry
# but an integer must be passed in manually this way
X = Id(0)
Y = Id(0)
print(X) # -> |Id:0|

# for id values of the same Id class, the same id will always return the same Id object
# I made Id's this way because I wanted stricter control over their behavior
# simply using an int, an id itself could be overwritten
print(X is Y) # -> True

# you can easily create a class inherited from Id using Id.New(name)
# Id.New() only takes name as a parameter and uses that to create a new Id class
ColorId = Id.New("ColorId")


#CREATING REGISTRY OBJECTS
# a registry is an object meant for managing id's and values

# a registry can be created with two optional parameters
# step -> determines the distance between id's this registry creates| default = 1
# id_class -> the Id class to use, if this isn't defined the registry uses the same set of Id's
# as any other Registry that also didn't define it,
# this is only important if you want it's keys to be unique
# also accepts a string and uses that as the name to automatically create a new Id class
# | default = Id

colors = Registry(step=1, id_class=ColorId)

#USING A REGISTRY OBJECT

# you can use registry.auto(value, id) to add a new id to it
# value and id are both optional parameters
# value -> a value to store in the registry
# | default = None (it is not required to store a value in the registry)
# id:int -> an integer used to initialize an Id instance
# | default = None (the registry will use it's internal state to determine which id to use next)

# assigning a value/Id to a registry

RED = colors.auto((255, 0, 0), 10)
print(RED) # -> |ColorId:10|

# retrieving a stored value from a registry

print(colors[RED]) # -> (255, 0, 0)


# SEALING A REGISTRY OBJECT
# you can seal and unseal a registry object, to lock its state
# a registry object is unsealed by default

colors.seal()

# colors.auto() would now throw an error because the registry is not meant to be edited

colors.unseal()

# you can also use a context manager on it (will automatically seal once the context is exited)

with colors:
    pass
colors.unseal()

#USING 'registry' DECORATOR

# the registry decorator works almost exactly like using a regular Registry object
# except now you define it using a class

@registry
class Mynums:
    Y = 1 # store 0 as a value at |Mynums:0|
    X = 0, Id(0) # change value at |Mynums:0| to 0
    
    # now both names X and Y point to the same value
    
    Z = Id(1) # set Z to |Mynums:1|
    
    # even though you pass an Id object
    # the registry uses it's own internal id class
    # this is just to let it know, the value you are passing should be used as the Id
    
# the decorator still returns a registry object, but the Id's are stored inside instead of globally
# The Id's can be accessed by their names

print(Mynums.X) # -> |Mynums:0|
print(Mynums[Mynums.Y]) # -> 0

# you can also access the value stored at an Id by passing it's name as a string

print(Mynums["X"]) # -> 0

# the naming behavior is possible with a regular registry, its just not automatic
# because I was trying to reduce overhead to the absolute minimum
# it probably would only be a tiny tiny amount of time
# but I wanted to design this to be AS FAST AS POSSIBLE, or at least as fast
# as I could make it with python