USE dymar;
DROP TABLE IF EXISTS `Наряд задание`;
CREATE TABLE `Наряд задание` 
(
    `Номер НЗ` 			INT(2)		NOT NULL,
    `Номер договора` 				INT(3) 		NOT NULL,
    `Код игрушки` 		CHAR(13) 		NOT NULL,
    `Количество изделий` 		CHAR(10) 	NOT NULL,
    `Стоимость единицы` 	CHAR(10) 	NOT NULL,
    `Время производства единицы` 	CHAR(5) 	NOT NULL,
    `Номер бригады` 		INT(2)		NOT NULL
);