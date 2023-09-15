drop table sensible_table;

CREATE table sensible_table(
 id BIGINT GENERATED ALWAYS AS IDENTITY,
 PRIMARY KEY(id),
 first_name TEXT NOT NULL,
 email TEXT NOT null,
 address text not null,
 updated_at timestamp
);

select * from sensible_table limit 100;

insert into sensible_table(first_name, email, address, updated_at)
select 
	'name' || "generate_series"
	, 'email' || "generate_series" || '@gmail.com'
	, 'stree' || "generate_series"
	, current_timestamp
from generate_series(1,10)

select * from sensible_table limit 100;

-- after the first load, you could insert the following values to se the incremental load in action
insert into sensible_table(first_name, email, address, updated_at)
select 
	'name' || "generate_series"
	, 'email' || "generate_series" || '@gmail.com'
	, 'stree' || "generate_series"
	, current_timestamp
from generate_series(11,12)

