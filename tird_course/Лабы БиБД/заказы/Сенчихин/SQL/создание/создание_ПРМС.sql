USE sema;
DROP TABLE IF EXISTS `Подразделения`;
CREATE TABLE `Подразделения` 
(
    `Код подразделения` 		CHAR(3) 		NOT NULL,
    `Название подразделения` 		CHAR(15) 		NOT NULL,
    `Номер помещения` 		CHAR(5) 		NOT NULL,
    `Наименование помещения` 		CHAR(50) 	NOT NULL,
    `Номер рабочего места` 	CHAR(20) 	NOT NULL,
    `Ответственный за помещение` 	CHAR(20) 	NOT NULL
);