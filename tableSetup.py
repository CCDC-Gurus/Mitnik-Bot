

tbl_member = """CREATE TABLE IF NOT EXISTS member(
    MemID int NOT NULL AUTOINCREMENT,
    FirstName varchar(255) NOT NULL,
    LastName varchar(255) NOT NULL,
    Box varchar(255),
    PRIMARY KEY (ID)
);"""

CREATE TABLE IF NOT EXISTS incident(
    IncID int NOT NULL AUTOINCREMENT,
    CreatorID int,
    Target varchar(255),
    Attacker varchar(255),
    Time DATETIME,
    Vulnerability varchar(255),
    Found varchar(255),
    PRIMARY KEY (ID),
    FOREIGN KEY(CreatorID) REFERENCES member(MemID)
);

CREATE TABLE IF NOT EXISTS incident_pic(
    PicID int NOT NULL AUTOINCREMENT,
    PicNum int NOT NULL,
    Data blob NOT NULL,
    PRIMARY KEY (ID, PicNum),
    FOREIGN KEY(PicID) REFERENCES inicdent(IncID)
);

CREATE TABLE IF NOT EXISTS inject(
    InjectNum int NOT NULL,
    Assigned varchar(255),
    PRIMARY KEY (InjectNum)
);

