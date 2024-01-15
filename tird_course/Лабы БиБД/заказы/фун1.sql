SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE FUNCTION Табличная_функция1 
(	

)
RETURNS TABLE 
AS
RETURN 
(
	select Наименование from Игрушки
	where [Год покупки] = 2021
)
GO


