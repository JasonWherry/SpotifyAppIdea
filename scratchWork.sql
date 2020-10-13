SELECT sqlite_version();

select * from StreamingHistory limit 10;

select (msPLayed/(1000*60) % 60) as minutes from StreamingHistory;
select (msPLayed/(1000) % 60) as seconds from StreamingHistory;
select (msPLayed % 1000) as milliseconds from StreamingHistory;

select trackName , (msPLayed/(1000*60) % 60) || '_' || (msPLayed/(1000) % 60) || '_' || (msPLayed % 1000) as time_m_s_ms from StreamingHistory limit 10;


select COUNT(id) as total1 from StreamingHistory where user=1;
select COUNT(id) as total2 from StreamingHistory where user=2;

-- find the tracks that the Users have in common. 
-- going to need two separate tables for the users, then join them and see where user1.trackName = user2.trackName
select distinct * from Users as user1 JOIN Users as user2 where user1.userid != user2.userid and user1.tracks = user2.tracks;