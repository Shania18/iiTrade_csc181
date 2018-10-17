CREATE TABLE IF NOT EXISTS Items(
ItemI int(5) PRIMARY KEY AUTO_INCREMENT,
CategoryId int(3),
Item_name varchar(50),
Price Float,
Details varchar(100000),
Item_available int,
Cart_description varchar(200),
Image LONGBLOB,
Updated_date Timestamp,
Stock float
)                                                                     