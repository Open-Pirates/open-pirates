from direct.distributed.DistributedObjectAI import DistributedObjectAI
from enum import Enum
class DTutorialObjectBase:

    class Sandwiches(Enum):
        Rye = 1
        Cheese = 2
        Ham = 3
        PeanutButter = 4

    class Fruit(Enum):
        Apple = 1
        Pear = 2
        Strawberries = 3
        Cherries = 4

    class Cake(Enum):
        Carrot = 1
        Chocolate = 2
        Pound = 3
        Bundt = 4
        Rum = 5

    Meals = {0: (Sandwiches.Rye, Fruit.Pear, Cake.Pound),
             1: (Sandwiches.Ham, Fruit.Apple, Cake.Rum),
             2: (Sandwiches.Cheese, Fruit.Pear, Cake.Carrot),
             3: (Sandwiches.Rye, Fruit.Cherries, Cake.Chocolate),
             }
