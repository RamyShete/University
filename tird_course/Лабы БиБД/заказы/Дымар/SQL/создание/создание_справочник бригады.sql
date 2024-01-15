USE dymar;
DROP TABLE IF EXISTS `справочник «Бригады»`;
CREATE TABLE `справочник «Бригады»` 
(
    `Номер бригады` 		INT(2)		NOT NULL,
    `ФИО бригадира` 		CHAR(50)	NOT NULL,
    `Количество работников` INT(2) 		NOT NULL
);