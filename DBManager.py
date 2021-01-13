import os
import re
import sqlite3

import tableSetup as ts

def is_safe_path(basedir, path, follow_symlinks=True):
    """Makes sure paths are gucci"""
    # Taken from
    # https://security.openstack.org/guidelines/dg_using-file-paths.html
    # resolves symbolic links
    if follow_symlinks:
        return os.path.realpath(path).startswith(basedir)

    return os.path.abspath(path).startswith(basedir)


def create_event(event_name):
    """Creates a new database file with all relevant tables.
    
    Returns whether or not the event was created
    """
    event_name.replace(" ", "_")
    db_path = os.path.join("data", str(event_name) + ".db")
    
    # Check if the path is fine, otherwise fail to create the event
    if not is_safe_path(os.getcwd(), db_path):
        return False

    # Check to see if this event exists
    if os.path.exists(db_path):
        # TODO Load the event
        
    else:
        # Create the db
        conn = sqlite3.connect(db_path)
        curs = conn.cursor()
        # Create the tables
        curs.execute(ts.tbl_members)
        curs.execute(ts.tbl_injects)

    conn.commit()
    conn.close()

    return True



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
