## DBManager
## Database and file manager for Mitnik. Controls the creation, access, and updating
## of database files.
## Gavin Lewis - 2021

import os
import sqlite3

import tableSetup as ts

def create_general():
    """Creates the general info db. Has a table with all events, 
       and keeps track of the active one.

       Runs on startup of bot, creates table IF NOT EXIST

       No default event, none could be active.
    """

    conn = sqlite3.connect("general.db")
    curs = conn.cursor()
    # Create the table
    curs.execute(ts.tbl_events)
    conn.commit()
    conn.close()


def create_event(event_name):
    """Creates a new database file with all relevant tables.
    
    Returns whether or not the event was created

    Also adds new event to the events table in general.db
    """
    
    db_path = os.path.join("data", str(event_name) + ".db")

    # Check to see if this event exist
    # TODO Check general.db instead
    if os.path.exists(db_path):
        # TODO Load the event
        pass
    else:
        # Create the db
        conn = sqlite3.connect(db_path)
        curs = conn.cursor()
        # Create the tables
        curs.execute(ts.tbl_members)
        curs.execute(ts.tbl_injects)
        curs.execute(ts.tbl_incidents)
        conn.commit()
        conn.close()

        conn = sqlite3.connect("general.db")
        curs = conn.cursor()
        # If we are creating an event, we need to make it active and
        # all others inactive
        curs.execute(ts.set_all_inactive)
        curs.execute(ts.ins_event, [event_name, db_path, 1])
        conn.commit()
        conn.close()

    return True



# def open_database():
#     """Open a connection to the database.

#     Returns a cursor for the defined database."""
#     co = sqlite3.connect('tutorial.db')
#     cu = co.cursor()

#     return co, cu


# def close_database(cur, conn):
#     """Close the connection to the database."""

#     cur.close()
#     conn.close()


# def create_tables(c):
#     c.execute(tableSetup.tbl_member)
#     c.execute(tableSetup.tbl_incident)
#     c.execute(tableSetup.tbl_incident_pic)
#     c.execute(tableSetup.tbl_inject)


# def delete_tables(c):
#     c.execute(tableSetup.del_member)
#     c.execute(tableSetup.del_incident)
#     c.execute(tableSetup.del_incident_pic)
#     c.execute(tableSetup.del_inject)


# def insert_member(c,name, box):
#     c.execute('INSERT INTO member VALUES()')
#     pass


# def data_entry(conn):
#     c.execute("INSERT INTO stuffToPlot VALUES(145123542, '2016-01-01', 'Python', 5)")
#     conn.commit()


# def enter_incident():
#     pass


# conn, cursor = open_database()
# delete_tables(cursor)
# create_tables(cursor)
# close_database(conn, cursor)

#create_tables()
#c.execute(tableSetup.tbl_delete)
#data_entry()
