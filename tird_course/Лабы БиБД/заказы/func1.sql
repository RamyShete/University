SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE FUNCTION [Умножение] 
(
	@Value1 Int, @Value2 Int
)
RETURNS Int
AS
BEGIN

	DECLARE @Result Int

	SELECT @Result = @Value1 * @Value2

	RETURN @Result

END
GO

