SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE FUNCTION Табличная_функция2 
(	

)
RETURNS TABLE 
AS
RETURN 
(
	select * from dbo.запрос3
)
GO


