import sqlobject
builder = sqlobject.mysql.builder()
connection = builder(user='ixtlan', password='noyouavsunochletal', host='localhost', db='poll_ast_generic')

class User(sqlobject.SQLObject):
        _connection = connection
        class sqlmeta:
             table = "users"
        login = sqlobject.StringCol()
        fullname = sqlobject.StringCol()

for user in User.select(User.q.login=='admin1@ixtlan.org'):
        print(user.login)