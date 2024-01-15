SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [Процедура 1] 
	@Param1 int = 0,
	@Param2 int = 0
	
AS
BEGIN
	SET NOCOUNT ON;

	SELECT 'Сумма' = @Param1+@Param2
END
GO
