USE dymar;
DROP TABLE IF EXISTS `справочник «каталог игрушек»`;
CREATE TABLE `справочник «каталог игрушек»` 
(
    `Код игрушки` 				CHAR(13)			NOT NULL,
    `Название игрушки` 						CHAR(50)		NOT NULL,
    `Стоимость игрушки` 				CHAR(10)		NOT NULL
);