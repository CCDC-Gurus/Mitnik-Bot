
del_member = """DROP TABLE member;"""
del_incident = """DROP TABLE incident;"""
del_incident_pic = """DROP TABLE incident_pic;"""
del_inject = """DROP TABLE inject;"""

tbl_member = """CREATE TABLE IF NOT EXISTS member(
    MemID int NOT NULL,
    FirstName varchar(255) NOT NULL,
    LastName varchar(255) NOT NULL,
    Box varchar(255),
    PRIMARY KEY (MemID)
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

tbl_inject = """CREATE TABLE IF NOT EXISTS inject(
    InjectNum int NOT NULL,
    Assigned varchar(255),
    PRIMARY KEY (InjectNum)
);"""

