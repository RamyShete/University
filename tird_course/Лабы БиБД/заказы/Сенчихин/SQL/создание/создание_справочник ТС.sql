USE sema;
DROP TABLE IF EXISTS `справочник «ТС»`;
CREATE TABLE `справочник «ТС»` 
(
    `Идентификационный номер` 		CHAR(11)	NOT NULL,
    `Название ТС` 				CHAR(50)			NOT NULL,
    `Тип средства` 						CHAR(50)		NOT NULL,
    `Основные характеристики` 						CHAR(100)		NOT NULL,
    `Дата покупки` 				DATE		NOT NULL,
    `Дата ввода в эксплуатацию` 				DATE		NOT NULL
);