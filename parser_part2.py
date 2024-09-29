import sqlite3

connection = sqlite3.connect(r'C:\MyProject\contacts.db')
cursor = connection.cursor()

cursor.execute('''
    SELECT name, phone, debt FROM contacts
    WHERE debt != '0'
               ''')

rows = cursor.fetchall()

messages = []
for name, phone, debt in rows:
    msg_txt = f'Dzień dobry, prosimy o pilne uregulowanie zaległości. Uzceń: {
        name.upper()}. Do zapłaty: {debt} zł. Pozdrawiamy, firma MyProject.'
    messages.append(msg_txt)

connection.close()

with open(r'C:\MyProject\messages.txt', 'w', encoding='utf-8') as file:
    for msg in messages:
        file.write(msg + '\n')

print('Success')
