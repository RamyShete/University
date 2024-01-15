SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [Триггер2] 
   ON  dbo.Категория 
   AFTER UPDATE
   AS 
BEGIN
	SET NOCOUNT ON;
	PRINT 'Запись обновлена'
END
GO
