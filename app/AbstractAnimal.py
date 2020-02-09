from abc import ABC, abstractmethod


class AbstractAnimal(ABC):

    name = None

    def __init__(self, name):
        self.name = name
        super().__init__()

    def make_lots_of_noises(self):
        print(self.name, "is hungry");
        self.make_noise();
        self.make_noise();
        self.make_noise();

    @abstractmethod
    def make_noise(self):
        pass

class Cat(AbstractAnimal):
    def __init__(self, name):
        super().__init__(name)

    def make_noise(self):
        print("Meow!")

class Dog(AbstractAnimal):
    def __init__(self, name):
        super().__init__(name)

    def make_noise(self):
        print("Woof!")

newman = Cat("Newman")
blue = Cat("Blue")
woofred = Dog("Woofred")
newman.make_lots_of_noises()
woofred.make_lots_of_noises()

