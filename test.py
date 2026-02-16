from catalogue import Catalogue

with Catalogue() as Colors:
    Colors.RED = 1, 2, 3, Catalogue.ID(10)
    
print(Colors.RED)