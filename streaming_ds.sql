create database Streaming_DS;
use Streaming_DS; 

create table userplay(
	id_user int primary key auto_increment,
    username varchar(100) not null,
    password_user varchar(50) not null,
    email varchar(100) not null); 

create table genre(
	id_genre int primary key auto_increment,
    name_genre varchar(100) not null); 
    
create table media(
	id_media int primary key auto_increment,
    genre_id int,
    name_media varchar(100) not null,
    foreign key (genre_id) references genre (id_genre),
    description_media varchar (1000) not null);

create table playlist(
	id_playlist int primary key auto_increment,
    user_id int,
    media_id int,
    foreign key (user_id) references userplay(id_user),
    foreign key (media_id) references media(id_media),
    title varchar(100) not null);

create table playlist_history(
	id_history int primary key auto_increment,
    user_idplay int,
    media_idplay int,
    foreign key (user_idplay) references playlist(user_id),
    foreign key (media_idplay) references playlist(media_id),
    date_playisth varchar (100) not null); 

select *from playlist_history;
show tables;
