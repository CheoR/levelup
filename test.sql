-- CONFIRM FIXTURE INSERTED 3 OBJECTS INTO gametype TABLE
SELECT *
FROM levelupapi_gametype;
-- CONFIRM FIXTURES INSERTED 1 USER OBJECT INTO THE FOLLOWING TABLES
SELECT *
FROM auth_user;
SELECT *
FROM authtoken_token;
SELECT *
FROM levelupapi_gamer;
SELECT *
FROM levelupapi_game;
SELECT *
FROM levelupapi_event;
SELECT *
FROM levelupapi_eventattendee;