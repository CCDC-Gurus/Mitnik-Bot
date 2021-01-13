
del_members = """DROP TABLE members;"""
del_incident = """DROP TABLE incident;"""
del_incident_pic = """DROP TABLE incident_pic;"""
del_injects = """DROP TABLE injects;"""

tbl_members = """CREATE TABLE IF NOT EXISTS members(
    discordUID int NOT NULL,
    fName varchar(255) NOT NULL,
    PRIMARY KEY (discordUID)
);"""

tbl_incident = """CREATE TABLE IF NOT EXISTS incident(
    IncID int NOT NULL,
    CreatorID int,
    Target varchar(255),
    Attacker varchar(255),
    Time DATETIME,
    Vulnerability varchar(255),
    Found varchar(255),
    PRIMARY KEY (IncID),
    FOREIGN KEY(CreatorID) REFERENCES member(MemID)
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

