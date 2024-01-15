USE sema;
DROP TABLE IF EXISTS `справочник «ПС»`;
CREATE TABLE `справочник «ПС»` 
(
	`Идентификационный номер` 		CHAR(11)	NOT NULL,
    `Название ПС` 		CHAR(50)		NOT NULL,
    `Тип изделия` 		CHAR(20)	NOT NULL,
    `Версия ПС` 		CHAR(20)	NOT NULL,
    `Фирма-производитель ПС` 		CHAR(20)	NOT NULL,
    `Дата поставки` 		DATE	NOT NULL,
    `Список отделов пользователей` CHAR(100) 		NOT NULL
);