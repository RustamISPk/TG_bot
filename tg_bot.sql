create database if not exists tg_bot;
use tg_bot;

create table if not exists peoples
(
	id int not null auto_increment,
    Surname varchar(30) not null,
    Name varchar(30) not null,
    Patronymic varchar(30),
    Post varchar(30) not null,
    Project varchar(100) not null,
    Photo varchar(100),
    Date_Coming varchar(100),
    primary key(id)
);