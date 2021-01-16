## DBManager
## Database and file manager for Mitnik. Controls the creation, access, and updating
## of database files.
## Gavin Lewis - 2021

import os
import sqlite3

import tableSetup as ts


def open_database():
    """Open a connection to the database.

    Returns a cursor for the defined database."""
    co = sqlite3.connect('general.db')
    cu = co.cursor()

    return co, cu

def create_general():
    """Creates the general info db. Has a table with all events, 
       and keeps track of the active one.

       Runs on startup of bot, creates table IF NOT EXIST

       No default event, none could be active.
    """

    conn, curs = open_database()
    # Create the table
    curs.execute(ts.tbl_events)
    curs.execute(ts.tbl_members)
    curs.execute(ts.tbl_injects)
    curs.execute(ts.tbl_incidents)
    conn.commit()
    conn.close()


def create_event(event_name, categ_id):
    """Creates a new database file with all relevant tables.
    
    Returns whether or not the event was created

    Also adds new event to the events table in general.db
    """
    
    #db_path = os.path.join("data", str(event_name) + ".db")

    conn, curs = open_database()
    # If we are creating an event, we need to make it active and
    # all others inactive
    curs.execute(ts.upd_set_all_inactive)
    curs.execute(ts.ins_event, [event_name, 1, categ_id])
    conn.commit()
    conn.close()

    return True

def activate_event(event_name):
    """Activates a different event.
    
    Need to set the other events as inactive.
    """
    conn, curs = open_database()
    curs.execute(ts.upd_set_all_inactive)
    curs.execute(ts.upd_activate_event, [event_name])
    conn.commit()
    conn.close()

def event_deletion(event_name):
    """Needs delete the event, and remove all users from the event if they are in it."""
    conn, curs = open_database()
    curs.execute(ts.del_event, [event_name])
    curs.execute(ts.upd_remove_members_from_event, [event_name])
    conn.commit()
    conn.close()

def member_join_event(discordUID, fName, eventName):
    """Adds member to member table, otherwise updates their row in member table"""

    conn, curs = open_database()
    # Check if member in db
    curs.execute(ts.sel_member, [discordUID])
    if curs.fetchone():
        # Member in db, just update their current event
        curs.execute(ts.upd_member_join, [fName, eventName, discordUID])
    else:
        # Create new member with new event
        curs.execute(ts.ins_new_member, [discordUID, fName, eventName])

    conn.commit()
    conn.close()
    
def get_current_event():
    """Gets the current running event and returns a string. Empty if no current."""
    conn, curs = open_database()
    curs.execute(ts.sel_current_event)
    name = curs.fetchone()
    conn.close()
    # name is a tuple, gotta make it a string
    if name:
        return name[0]
    else:
        return ""

def get_all_events():
    """Returns a list of all events in the database. Can be empty."""
    conn, curs = open_database()
    curs.execute(ts.sel_all_events)
    events = curs.fetchall()
    conn.close()
    # events is a list of 1-tuples, gotta make it just a list
    return [x[0] for x in events]

def get_event_categid(event_name):
    """Gets the specifies events category id."""
    conn, curs = open_database()
    curs.execute(ts.sel_event_categ_id, [event_name])
    cid = curs.fetchone()
    conn.close()
    return cid[0]

def get_current_event_categid():
    """Gets the current events category id."""
    conn, curs = open_database()
    curs.execute(ts.sel_curr_event_categ_id)
    cid = curs.fetchone()
    conn.close()
    # cid is a tuple, return the string
    return cid[0]




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
