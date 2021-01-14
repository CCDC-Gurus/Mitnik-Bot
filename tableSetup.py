
del_members = """DROP TABLE members;"""
del_incident = """DROP TABLE incident;"""
del_incident_pic = """DROP TABLE incident_pic;"""
del_injects = """DROP TABLE injects;"""

# General tables
tbl_events = """CREATE TABLE IF NOT EXISTS events(
    name varchar(255) NOT NULL,
    eventPath varchar(255),
    active int,
    PRIMARY KEY(name)
);
"""


# Event tables
tbl_members = """CREATE TABLE IF NOT EXISTS members(
    discordUID int NOT NULL,
    fName varchar(255) NOT NULL,
    PRIMARY KEY (discordUID)
);"""

tbl_incidents = """CREATE TABLE IF NOT EXISTS incidents(
    incNum int NOT NULL,
    creatorID varchar(255),
    target varchar(255),
    attacker varchar(255),
    time DATETIME,
    vulnerability varchar(255),
    found varchar(255),
    texPath varchar(255),
    PRIMARY KEY (incNum),
    FOREIGN KEY(creatorID) REFERENCES member(discordUID)
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
    title varchar(255),
    startTime DATETIME,
    endTime DATETIME,
    assigned varchar(255),
    PRIMARY KEY (injectNum)
);"""


# General insertions
ins_event = """INSERT INTO events VALUES(?, ?, ?);"""

# Sets all events in events table in general.db as inactive
set_all_inactive = """UPDATE events SET active=0;"""