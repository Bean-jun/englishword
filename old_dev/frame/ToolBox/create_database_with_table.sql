create table user_table
(
    userid     INTEGER not null
        primary key autoincrement,
    username   varchar(30),
    password varchar(30) default (123456) not null;
    user_group varchar(30),
    gender     varchar(4),
    tag        varchar(20)
);

create table word_table
(
    word_id        INTEGER not null
        primary key autoincrement,
    word           varchar(30) unique,
    word_translate varchar(30),
    word_sound     varchar(30)
);

create table user_word_table
(
    userid      int not null
        references user_table,
    word_id     int not null
        references word_table,
    study_count int
);