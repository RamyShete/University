SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [�������1] 
   ON  dbo.������� 
   AFTER INSERT
AS 
BEGIN
	SET NOCOUNT ON;
	PRINT '������ ���������';

END
GO
