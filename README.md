An alternative to enum

Catalogue is an alternative to Python’s enum that lets you store items with optional values and auto‑generated IDs.  

I may port to c / cPython eventually to improve performance, but I don't know c right now.

USE:

after installing the package, you can import catalogue in your python project

a few examples of importing catalogue:

import catalogue # use would be catalogue.Catalogue
from catalogue import Catalogue
import catalogue.Catalogue as CatAlias # whatever alias you like :3

and then to actually use the catalogue:
from catalogue import Catalogue

class colors(Catalogue, step=1): # 1 is the default value of step
    RED = (255, 0, 0), 0
    YELLOW = {}
    BLUE = {"id":10}
    GREEN = (0, 255, 0), None

when you add RED like this, the first value is the item, and the second is the id
both can be excluded using a dict or filling in None instead, if you aren't interested in storing a value

if id is excluded
the catalogue generates one automatically by incrementing using step, but it continues from the last used id (id's can be overwritten) starting from 0

colors.RED returns an Item object which has an id which points to its value and its name

colors.RED.ID # returns RED's id -> 0
colors.RED.VALUE # returns the value of RED -> (0, 255, 0)
colors.BLUE.PARENT # returns the parent of BLUE -> colors (the catalogue itself)
colors.RED.Name # returns the name of RED -> "RED"

the representation of an id object will show up differently, depending on if it has a value:

no value:
    |colors.YELLOW/1|
    within two pipes
    the name of the item's catalogue
    .
    the item's current name
    /
    the item's id
value:
    |colors.GREEN/11 -> '(0, 255, 0)'|

