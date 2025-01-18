create table if not exists messages
(
    message_id Uuid,
    text Utf8 not null,
    
    primary key (message_id)
);