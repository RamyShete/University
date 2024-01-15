SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [Триггер1] 
   ON  dbo.Игрушки 
   AFTER INSERT
AS 
BEGIN
	SET NOCOUNT ON;
	PRINT 'Запись добавлена';

END
GO
