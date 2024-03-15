CREATE TABLE accounts2 (
  user_id SERIAL PRIMARY KEY,
  username VARCHAR (50) UNIQUE NOT NULL,
  password VARCHAR (50) NOT NULL,
  email VARCHAR (255) UNIQUE NOT NULL,

);

INSERT INTO accounts2(user_id,username,password)
 VALUES (1,'username','password');


 CREATE PUBLICATION dbz_publication
 FOR TABLE accounts;
