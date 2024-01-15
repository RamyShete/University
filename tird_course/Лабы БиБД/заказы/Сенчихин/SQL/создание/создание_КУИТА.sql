USE sema;
DROP TABLE IF EXISTS `КУИТА`;
CREATE TABLE `КУИТА` 
(
    `Идентификационый номер` 				CHAR(11)		NOT NULL,
    `Наименование ИТ-актива` 		CHAR(50) 		NOT NULL,
    `Группа ИТ-актива` 	CHAR(20) 		NOT NULL,
    `Подгруппа ИТ-актива` 					CHAR(50)		NOT NULL,
    `Код подразделения`					CHAR(3)		NOT NULL,
    `Материально ответственное лицо` 					CHAR(20)		NOT NULL
);