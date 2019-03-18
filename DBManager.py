import sqlite3

import tableSetup


def open_database():
    """Open a connection to the database.

    Returns a cursor for the defined database."""
    co = sqlite3.connect('tutorial.db')
    cu = co.cursor()

    return co, cu


def close_database(cur, conn):
    """Close the connection to the database."""

    cur.close()
    conn.close()


def create_tables(c):
    c.execute(tableSetup.tbl_member)
    c.execute(tableSetup.tbl_incident)
    c.execute(tableSetup.tbl_incident_pic)
    c.execute(tableSetup.tbl_inject)


def delete_tables(c):
    c.execute(tableSetup.del_member)
    c.execute(tableSetup.del_incident)
    c.execute(tableSetup.del_incident_pic)
    c.execute(tableSetup.del_inject)


def insert_member(c,name, box):
    c.execute('INSERT INTO member VALUES()')
    pass


def data_entry(conn):
    c.execute("INSERT INTO stuffToPlot VALUES(145123542, '2016-01-01', 'Python', 5)")
    conn.commit()


def enter_incident():
    pass


conn, cursor = open_database()
delete_tables(cursor)
create_tables(cursor)
close_database(conn, cursor)

#create_tables()
#c.execute(tableSetup.tbl_delete)
#data_entry()
