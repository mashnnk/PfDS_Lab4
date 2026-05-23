CREATE DATABASE IF NOT EXISTS my_database;
USE my_database;

CREATE TABLE IF NOT EXISTS titanic (
    PassengerId INT,
    Survived    INT,
    Pclass      INT,
    Name        VARCHAR(255),
    Sex         VARCHAR(10),
    Age         FLOAT,
    SibSp       INT,
    Parch       INT,
    Ticket      VARCHAR(50),
    Fare        FLOAT,
    Cabin       VARCHAR(50),
    Embarked    VARCHAR(5)
);

-- Завантаження з CSV через змінні, щоб коректно обробити порожні значення як NULL
LOAD DATA INFILE '/var/lib/mysql-files/titanic.csv'
INTO TABLE titanic
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(PassengerId, Survived, Pclass, Name, Sex, @age, SibSp, Parch, Ticket, Fare, @cabin, @embarked)
SET
    Age      = NULLIF(@age, ''),
    Cabin    = NULLIF(@cabin, ''),
    Embarked = NULLIF(@embarked, '');
