SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [�������2] 
   ON  dbo.��������� 
   AFTER UPDATE
   AS 
BEGIN
	SET NOCOUNT ON;
	PRINT '������ ���������'
END
GO
