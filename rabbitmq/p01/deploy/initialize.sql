/*

*/
ALTER  USER user1 PASSWORD 'Password!';
ALTER  USER flask PASSWORD 'Password!';


/* Rule key
nsxId:sectionId:ruleId
*/
DROP TABLE IF EXISTS deployments CASCADE;
CREATE TABLE deployments(
    id             serial PRIMARY KEY,
    type           VARCHAR (50) NOT NULL,
    request        VARCHAR (200) NOT NULL,
    state          VARCHAR (200) NOT NULL,
    state_summary  VARCHAR (50) NOT NULL,
    taskId         VARCHAR (50)
);



GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO user1;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO user1;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO flask;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO flask;


insert into deployments
(type, request, state, state_summary)
values
('vm', '{"az":"RAT-AZ1", "os":"RHEL8"}','','new'),
('vm', '{"az":"RAT-AZ1", "os":"RHEL8"}','','new')
;

/*
insert into machineprefix (name,template,counter) values ('es-yr','es%04dyr',0);
insert into machineprefix (name,template,counter) values ('de-yr','es%04dyr',0);
*/