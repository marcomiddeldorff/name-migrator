import pymysql
from config import config

db = pymysql.connect(host=config['host'], user=config['username'], password=config['password'], database=config['database'] )

cursor = db.cursor()

cursor.execute('SELECT `{}`, `name` FROM {}'.format(config['identifier_column'], config['users_table']))

data = cursor.fetchall()

newNames = []
for row in data:
    splittedName = row[1].split(' ')
    last_name = splittedName[len(splittedName) - 1]
    
    first_name = splittedName[0]
    if len(splittedName) > 2:
        first_name_ph = []
        for i in range (len(splittedName) - 1):
            first_name_ph.append(splittedName[i])
        realFirstName = " ".join(first_name_ph)
        splittedName.pop()
        first_name = realFirstName
    newNames.append([
        row[0],
        first_name,
        last_name
    ])
    
for names in newNames:
    cursor.execute('UPDATE {} SET `{}` = \'{}\', `{}` = \'{}\' WHERE `{}` = \'{}\''.format(config['users_table'], config['firstname'], names[1], config['lastname'], names[2], config['identifier_column'], names[0]))
    print('Updated user with id '+ names[0])
        
db.commit()


    