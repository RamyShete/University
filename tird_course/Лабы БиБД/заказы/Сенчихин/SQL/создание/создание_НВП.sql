USE sema;
DROP TABLE IF EXISTS `Накладная на внутреннее перемещение`;
CREATE TABLE `Накладная на внутреннее перемещение` 
(
	`Идентификационый номер` 				CHAR(11)		NOT NULL,
	`Наименование` 		CHAR(50)			NOT NULL,
	`Дата приобретения` 				DATE		NOT NULL,
    `Количество` 	CHAR(10)		NOT NULL
);