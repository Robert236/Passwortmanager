import sqlite3
import string
import random
con = sqlite3.connect("passwort_manager.db")
cur = con.cursor()

main_functions = [{'number': 1, 'name': 'Eintrag erstellen'},
                  {'number': 2, 'name': 'Einträge anzeigen'},
                  {'number': 3, 'name': 'Beenden'}]

sub_functions = [{'number': 1, 'name': 'Eintrag suchen'},
                 {'number': 2, 'name': 'Eintrag bearbeiten'},
                 {'number': 3, 'name': 'Eintrag löschen'},
                 {'number': 4, 'name': 'Zurück'}]


def start_main(programs):
    print(30 * '#')
    for func in programs:
        print(str(func['number']) + ': ' + func['name'])
    print(30 * '#')
    try:
        rv_main = int(input('Eingabe: '))
        for func2 in programs:
            if func2['number'] == rv_main:
                return func2
    except ValueError:
        print('- Nur numerische Eingabe!')


def generate_a_password():  # TODO Password auf 15 Stellen erweitern.
    password = ''
    specials = '$.:?/,;!/?$'
    for i in range(1, 4):  # Vier Iterationen für Passwort mit 15 Stellen.
        lower = string.ascii_lowercase[random.randint(0, 25)]
        integer = str(random.randint(1, 9))
        upper = string.ascii_uppercase[random.randint(0, 25)]
        special = specials[random.randint(0, 10)]
        integer2 = str(random.randint(1, 9))
        password += lower
        password += integer
        password += upper
        password += special
        password += integer2
    return password


def collect_data(attributes2):
    dic = {}
    for atri in attributes2:
        if atri == 'Passwort':
            print('Passwort auto. generieren?')
            decisions = [{'number': 1, 'name': 'Ja'}, {'number': 2, 'name': 'Nein'}]
            answer = None
            while True:
                rv3 = start_main(decisions)
                if rv3 is None:
                    continue
                else:
                    answer = rv3
                    break
            if answer['name'] == 'Ja':
                rv_4 = generate_a_password()
                print('- Neues Passwort: {}'.format(rv_4))
                dic[atri] = rv_4
            else:
                entry = str(input('Eingabe für {}: '.format(atri)))
                dic[atri] = entry
        else:
            entry = str(input('Eingabe für {}: '.format(atri)))
            dic[atri] = entry
    return dic


def write_data_to_database(data):
    sql_statement = ("INSERT INTO password_entry (title, user_name, password, url, note) "
                     "VALUES ('{}', '{}', '{}', '{}', '{}');").format(data['Titel'], data['Benutzername'],
                                                                      data['Passwort'], data['URL'], data['Notiz'])
    # print(sql_statement)
    cur.execute(sql_statement)
    con.commit()
    print('- Erfolgreich gespeichert!')


def write_data_to_database_with_id(data):
    sql_statement = ("INSERT INTO password_entry (id, title, user_name, password, url, note) "
                     "VALUES ({},'{}', '{}', '{}', '{}', '{}');").format(data['ID'], data['Titel'],
                                                                         data['Benutzername'], data['Passwort'],
                                                                         data['URL'], data['Notiz'])
    # print(sql_statement)
    cur.execute(sql_statement)
    con.commit()
    print('- Erfolgreich gespeichert!')


def search_from_data(data):                  # TODO Mach die Funktion so, dass in mehreren Datensätzen
    entry = str(input('Ihr Suchbegriff: '))  # der Suchbegriff gefunden werden kann.
    for row2 in data:
        for word in row2:
            if entry == str(word):
                return row2


def show_all_entries(data2):
    print('Id, Titel, Benutzername, Passwort, URL, Notiz'.upper())
    to_print = []
    for row in data2:
        line = ''
        for word in row:
            line += str(word) + ', '
        line = line[:-2]
        to_print.append(line)
    for nice_print in to_print:
        print(nice_print)
    print()


def read_data_from_database():
    def change_data_structure(rows2):
        input_for_delete = []
        for row in rows2:
            dic2 = dict()
            dic2['number'] = row[0]
            dic2['name'] = row[1]
            input_for_delete.append(dic2)
        return input_for_delete
    rows = cur.execute("SELECT * FROM password_entry;").fetchall()
    show_all_entries(rows)
    while True:
        rv6 = start_main(sub_functions)
        if rv6 is None:
            continue
        elif rv6['name'] == 'Eintrag suchen':
            print()
            print(30 * '#')
            print('Willkommen in {}'.format(rv6['name'].upper()))
            print(30 * '#')
            print()
            rv7 = search_from_data(rows)
            if rv7 is None:
                print('- Es gibt keinen Treffer!')
                print()
            else:
                print('- Es gibt ein Treffer!')
                print()
                print('Id, Titel, Benutzername, Passwort, URL, Notiz'.upper())
                line = ''  # TODO an der Stelle kann die verbesserte Funktion (oben) eingesetzt werden.
                for word in rv7:
                    line += str(word) + ', '
                line = line[:-2]
                print(line)
                print()
        elif rv6['name'] == 'Eintrag löschen':  # TODO Hier noch ein Abbruch mit reinprogrammieren!
            rv15 = change_data_structure(rows)
            while True:
                if len(rv15) == 0:
                    print('- Keine Daten gefunden!')
                    print()
                    break
                rv8 = start_main(rv15)
                if rv8 is None:
                    continue
                else:
                    sql_statement = 'DELETE FROM password_entry WHERE id={};'.format(rv8['number'])
                    cur.execute(sql_statement)
                    con.commit()
                    print('- Der Eintrag wurde gelöscht!')
                    print()
                    break
            break
        elif rv6['name'] == 'Eintrag bearbeiten':
            rv16 = change_data_structure(rows)
            while True:
                if len(rv16) == 0:
                    print('- Keine Daten gefunden!')
                    print()
                    break
                rv20 = start_main(rv16)
                if rv20 is None:
                    continue
                else:
                    attributes2 = ['ID', 'Titel', 'Benutzername', 'Passwort', 'URL', 'Notiz']
                    attributes3 = [{'number': 1, 'name': 'Titel'}, {'number': 2, 'name': 'Benutzername'},
                                   {'number': 3, 'name': 'Passwort'}, {'number': 4, 'name': 'URL'},
                                   {'number': 5, 'name': 'Notiz'}]
                    sql_statement = 'SELECT * FROM password_entry WHERE id={};'.format(rv20['number'])
                    searched_data = cur.execute(sql_statement).fetchall()[0]
                    searched_data = list(searched_data)
                    work_data = dict(zip(attributes2, searched_data))
                    while True:
                        rv21 = start_main(attributes3)
                        if rv21 is None:
                            continue
                        else:
                            entry = str(input('Eingabe für {}: '.format(rv21['name'])))
                            work_data[rv21['name']] = entry
                            sql_statement = 'DELETE FROM password_entry WHERE id={};'.format(searched_data[0])
                            cur.execute(sql_statement)
                            con.commit()
                            write_data_to_database_with_id(work_data)
                            break
                    break
            break
        elif rv6['name'] == 'Zurück':
            break


# main code


while True:
    print()
    print(30 * '#')
    print('Willkommen im Hauptmenü')
    print(30 * '#')
    print()
    rv = start_main(main_functions)
    if rv is None:
        continue
    elif rv['name'] == 'Eintrag erstellen':
        print()
        print(30 * '#')
        print('Willkommen in {}'.format(rv['name'].upper()))
        print(30 * '#')
        print()
        attributes = ['Titel', 'Benutzername', 'Passwort', 'URL', 'Notiz']
        rv2 = collect_data(attributes)
        write_data_to_database(rv2)
    elif rv['name'] == 'Einträge anzeigen':
        print()
        print(30 * '#')
        print('Willkommen in {}'.format(rv['name'].upper()))
        print(30 * '#')
        print()
        read_data_from_database()
    elif rv['name'] == 'Beenden':
        break
