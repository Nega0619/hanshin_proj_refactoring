SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [AutocareHCB].[dbo].[InfinityTrainData](
	[RegistKey] [uniqueidentifier] NOT NULL,
	[CheckupDate] [date] NULL,
	[PatientName] [varchar](50) NULL,
	[PatientBirthday] [varchar](50) NULL,
	[PatientAge] [decimal](9, 3) NOT NULL,
	[AgeGroup] [smallint] NULL,
	[PatientSex] [varchar](50) NULL,
	[per1_spc_year] [smallint] NULL,
	[TP01] [nvarchar](100) NULL,
	[TP02] [nvarchar](100) NULL,
	[GP01] [nvarchar](100) NULL,
	[GP02] [nvarchar](100) NULL,
	[TP00] [nvarchar](100) NULL,
	[TP07] [nvarchar](100) NULL,
	[TP08] [nvarchar](100) NULL,
	[C037] [nvarchar](100) NULL,
	[C039] [nvarchar](100) NULL,
	[C904] [nvarchar](100) NULL,
	[C038] [nvarchar](100) NULL,
	[C026] [nvarchar](100) NULL,
	[C027] [nvarchar](100) NULL,
	[C029] [nvarchar](100) NULL,
	[C030] [nvarchar](100) NULL,
	[C054] [nvarchar](100) NULL,
	[C022] [nvarchar](100) NULL,
	[C023] [nvarchar](100) NULL,
	[C024] [nvarchar](100) NULL,
	[C018] [nvarchar](100) NULL,
	[U008] [nvarchar](100) NULL,
	[C032] [nvarchar](100) NULL,
	[E001] [nvarchar](100) NULL,
	[I521] [nvarchar](100) NULL,
	[I105] [nvarchar](100) NULL,
	[I022] [nvarchar](100) NULL,
	[I348] [nvarchar](100) NULL,
	[I502] [nvarchar](100) NULL,
	[I503] [nvarchar](100) NULL,
	[I349] [nvarchar](100) NULL
) ON [PRIMARY]
GO
ALTER TABLE [AutocareHCB].[dbo].[InfinityTrainData] ADD  CONSTRAINT [PK_InfinityTrainData] PRIMARY KEY CLUSTERED 
(
	[RegistKey] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = ON, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
