try:
    a = 2/0
    raise Exception('hohoho asdf')
except Exception as e:
    print str(e)
print('hohoh llalalal')