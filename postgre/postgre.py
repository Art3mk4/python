import psycopg2
import psycopg2.extras
params = {}
params['host'] = '192.168.98.149'
params['user'] = 'postgres'
params['password'] = 'abba'
params['dbname'] = 'poll_ast_generic'
#params['charset'] = 'utf8'
connectionString = ''
for key, param in params.iteritems():
    connectionString += str(key) + '=' + str(param) + ' '
#print(connectionString)
conn = psycopg2.connect(connectionString)
#conn = psycopg2.connect(params)
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#cur.execute("insert into users (login, phone) values ('login2', '12345678911')")

#cur.execute("SELECT login FROM users where id=10")
#result = cur.fetchall()
#cur.execute("UPDATE users set modified=date_part('epoch',now()) where id=10")
cur.execute("select * from operators where id=11222")
result = cur.fetchone()
conn.close()
print conn.closed, result
#.itervalues().next(), result['login']