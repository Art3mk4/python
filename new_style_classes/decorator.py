class Spam:
    numInstances = 0
    def __init__(self):
        Spam.numInstances = Spam.numInstances + 1
    @staticmethod
    def printNumInstaces():
        print("Number of instances created: ", Spam.numInstances)

if __name__ == '__main__':
    a = Spam()
    b = Spam()
    c = Spam()
    Spam.printNumInstaces()

    a.printNumInstaces()