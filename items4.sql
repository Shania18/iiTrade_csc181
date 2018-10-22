CREATE TABLE `items` (
  `Item_id` int(5) NOT NULL AUTO_INCREMENT,
  `CategoryId` int(3) NOT NULL,
  `Item_name` varchar(50) NOT NULL,
  `Price` float NOT NULL,
  `Details` mediumtext NOT NULL,
  `Item_available` int(11) NOT NULL,
  `Cart_description` varchar(200) NOT NULL,
  `Image` longblob NOT NULL,
  `Updated_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Stock` float NOT NULL,
  PRIMARY KEY (`Item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1