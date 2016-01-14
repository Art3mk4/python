class ListInstance:
    def __str__(self):
        return '<Instance of %s, address %s:\n%s>' % (
                           self.__class__.__name__,         # My class's name
                           id(self),                        # My address
                           self.__attrnames())              # name=value list
    def __attrnames(self):
        result = ''
        for attr in sorted(self.__dict__):                  # Instance attr dict
            result += '\tname %s=%s\n' % (attr, self.__dict__ [attr])
        return result
    def supers(self):
        names = []
        for super in self__class__.__bases__:
            names.append(super.__name__)
        return ', '.join(names)