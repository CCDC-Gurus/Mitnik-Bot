
del_members = """DROP TABLE members;"""
del_incident = """DROP TABLE incident;"""
del_incident_pic = """DROP TABLE incident_pic;"""
del_injects = """DROP TABLE injects;"""

# General tables

# name: name of event
# eventPath: path to db file
# active: bool whether it is active or not
# categoryID: Discord id of the category associated with event
tbl_events = """CREATE TABLE IF NOT EXISTS events(
    name varchar(255) NOT NULL,
    active int,
    categoryID int,
    PRIMARY KEY(name)
);
"""

# Event tables

# discordUID: the users unique id on discord
# fName: first name of the user (used for channel name)
# eventName: name of event they are active in, blank if not active
tbl_members = """CREATE TABLE IF NOT EXISTS members(
    discordUID int NOT NULL,
    fName varchar(255) NOT NULL,
    eventName varchar(255),
    PRIMARY KEY (discordUID)
);"""

tbl_incidents = """CREATE TABLE IF NOT EXISTS incidents(
    incNum int NOT NULL,
    eventName varchar(255) NOT NULL,
    creatorID varchar(255),
    target varchar(255),
    attacker varchar(255),
    time DATETIME,
    vulnerability varchar(255),
    found varchar(255),
    texPath varchar(255),
    PRIMARY KEY (incNum, eventName)
);"""

tbl_incident_pic = """CREATE TABLE IF NOT EXISTS incident_pic(
    PicID int NOT NULL,
    PicNum int NOT NULL,
    Data blob NOT NULL,
    PRIMARY KEY (PicID, PicNum),
    FOREIGN KEY(PicID) REFERENCES incident(IncID)
);"""

tbl_injects = """CREATE TABLE IF NOT EXISTS injects(
    injectNum int NOT NULL,
    eventName varchar(255) NOT NULL,
    title varchar(255),
    startTime DATETIME,
    endTime DATETIME,
    assigned varchar(255),
    PRIMARY KEY (injectNum, eventName)
);"""


# General insertions
ins_event = """INSERT INTO events VALUES(?, ?, ?);"""

# Sets all events in events table in general.db as inactive
upd_set_all_inactive = """UPDATE events SET active=0;"""
upd_activate_event = """UPDATE events SET active=1 WHERE name=?;"""

# For users joining events/being created
upd_member_join = """UPDATE members SET fName=?, eventName=? WHERE discordUID=?;"""
sel_member = """SELECT fName FROM members WHERE discordUID=?;"""
ins_new_member = """INSERT INTO members VALUES(?, ?, ?);"""
upd_remove_members_from_event = """UPDATE members SET eventName='' WHERE eventName=?;"""

sel_current_event = """SELECT name FROM events WHERE active=1;"""
sel_all_events = """SELECT name FROM events;"""
sel_event_categ_id = """SELECT categoryID FROM events WHERE name=?;"""
sel_curr_event_categ_id = """SELECT categoryID FROM events WHERE active=1;"""

del_event = """DELETE FROM events WHERE name=?"""