SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE Процедура3
	
AS
BEGIN

	SET NOCOUNT ON;

	SELECT [Номер игрушки],[Наименование],[Макс.возраст детей],[Номер группы]
	FROM dbo.запрос3
	WHERE [Макс.возраст детей] = 6;
END
GO
