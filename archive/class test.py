class animal:
    def __init__(self, name):
        self.name = name
    
    def what_is_my_name(self):
        return(self.name)

    def speak(self, inputt):
        return str(inputt) 
    
class dog(animal):
    def speak(self):
        return 'woof'