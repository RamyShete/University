USE [KinderGartenGames]
GO
/****** Object:  UserDefinedFunction [dbo].[Деление]    Script Date: 28.11.2021 18:32:40 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER FUNCTION [Деление]
(
	@Value1 Int, @Value Int
)
RETURNS Int
AS
BEGIN

	DECLARE @Result Int

	SELECT @Result = @Value1/@Value

	RETURN @Result

END
