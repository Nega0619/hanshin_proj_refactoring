SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [AutocareHCB].[dbo].[Habit](
	[index] [tinyint] NOT NULL,
	[disease] [nvarchar](50) NOT NULL,
	[habit_guide] [nvarchar](250) NULL
) ON [PRIMARY]
GO
