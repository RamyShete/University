USE dymar;
DROP TABLE IF EXISTS `справочник «Работники бригад»`;
CREATE TABLE `справочник «Работники бригад»` 
(
	`Номер бригады` 		INT(2)		NOT NULL,
	`Учетный номер сотрудника` 				INT(7)		NOT NULL,
    `ФИО сотрудника` 	CHAR(50)		NOT NULL,
    `Код профессии` 				INT(7)	NOT NULL,
    `Разряд` 		INT(1)			NOT NULL,
    `Сетка оплаты` 		INT(1)			NOT NULL,
    `Фактически отработанное время` 		CHAR(10)			NOT NULL,
    `Коэффициент трудового учета` 		CHAR(3)			NOT NULL
);