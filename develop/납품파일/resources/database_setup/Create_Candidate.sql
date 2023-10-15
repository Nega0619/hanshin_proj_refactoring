SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [AutocareHCB].[dbo].[Candidate](
	[AgeGroup] [smallint] NOT NULL,
	[PatientSex] [nvarchar](1) NOT NULL,
	[analysis_index] [nvarchar](50) NOT NULL,
	[candidate_value] [nvarchar](100) NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [AutocareHCB].[dbo].[Candidate] ADD  CONSTRAINT [PK_Candidate] PRIMARY KEY CLUSTERED 
(
	[analysis_index] ASC,
	[AgeGroup] ASC,
	[PatientSex] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
