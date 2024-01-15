USE dymar;
DROP TABLE IF EXISTS `Карточка складсого учета`;
CREATE TABLE `Карточка складсого учета` 
(
    `Номер карточки` 						INT(5)		NOT NULL,
    `Код игрушки` 		CHAR(13) 		NOT NULL,
    `Стоимость игрушки` 	CHAR(10) 		NOT NULL,
    `Остаток на 1 число месяца` 					CHAR(10)		NOT NULL,
    `Номер договора` 					INT(3)		NOT NULL,
    `Приход` 					CHAR(10)		NOT NULL,
    `Дата` 					DATE		NOT NULL,
    `Расход` 					CHAR(10)		NOT NULL,
    `Остаток` 					CHAR(10)		NOT NULL
);