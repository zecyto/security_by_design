SQLite format 3   @    �              �                                                � .WJ    �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        �7�QtablelogslogsCREATE TABLE logs ( 
log_id INTEGER PRIMARY KEY,
editor_account VARCHAR(30),
role VARCHAR(10),
target_account VARCHAR(30),
timestamp VARCHAR(64),
mac VARCHAR(64))�;�UtableusersusersCREATE TABLE users ( 
customer_number INTEGER PRIMARY KEY,
email VARCHAR(45),
role VARCHAR(10) DEFAULT "user",
fname VARCHAR(35), 
lname VARCHAR(35), 
joining DATE,
password VARCHAR(64),
salt VARCHAR(64),
mfa VARCHAR(64) NULL,
failed_login INTEGER DEFAULT 0,
contract_model INTEGER DEFAULT 1)   � +j�                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              �; 7!�� 	s.claus@christmas.orguserSantaClaus2023-12-10e5ae738da325ca7ff90d5c25495f2fbb291d1d6a0e78d0a3d7a56d3bee712d8764fcd583d8ca3037b3d2db083e23bc60e1a32941a282de806c500fe40c472e66�> =!�� 	k.stroetmann@example.orguserKarlStroet2023-12-10a61e0d64ecc329be4ea534360c31d21fa483965fd2c13d916d0818081163abe92858162e24d8a7cedd49a2a46e0e224a89bfedd3550592cf099bbbfef898027f�R #!��M	admin@adminadminadminadmin2023-12-03468d59c4ee389f925c2f9e7d4da9521f1365357f497bfe4fb2989ffd4b66e13c03203557143c25249fac141445996a88eee43e0046cae0b3f9d1922478191775FJMXJNVZSYV5A4PFOIWC5MXQO5KSMUOT                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              