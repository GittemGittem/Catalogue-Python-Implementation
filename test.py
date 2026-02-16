from catalogue import Catalogue

with Catalogue() as Colors:
    Colors.RED = Catalogue.ID(10)[1]
    
print(Colors.RED)