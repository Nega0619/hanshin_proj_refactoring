-- bcp AutocareHCB.dbo.BloodCodeInfo in ./BloodCodeInfo.dat -S 192.168.0.35 -U sa -P shin#0313 -n
-- bcp AutocareHCB.dbo.Candidate in ./Candidate.dat -S 192.168.0.35 -U sa -P shin#0313 -n
-- bcp AutocareHCB.dbo.DiseasePerBloodCodes in ./DiseasePerBloodCodes.dat -S 192.168.0.35 -U sa -P shin#0313 -n
-- bcp AutocareHCB.dbo.HanshinTrainData in ./HanshinTrainData.dat -S 192.168.0.35 -U sa -P shin#0313 -n
-- bcp AutocareHCB.dbo.InfinityTrainData in ./InfinityTrainData.dat -S 192.168.0.35 -U sa -P shin#0313 -n
-- bcp AutocareHCB.dbo.Patient in ./Patient.dat -S 192.168.0.35 -U sa -P shin#0313 -n

-- bcp AutocareHCB.dbo.BloodCodeInfo in ./BloodCodeInfo.dat -S localhost -U sa -P \!hanshin22 -n
-- bcp AutocareHCB.dbo.Candidate in ./Candidate.dat -S localhost -U sa -P \!hanshin22 -n
-- bcp AutocareHCB.dbo.DiseasePerBloodCodes in ./DiseasePerBloodCodes.dat -S localhost -U sa -P \!hanshin22 -n
-- bcp AutocareHCB.dbo.HanshinTrainData in ./HanshinTrainData.dat -S localhost -U sa -P \!hanshin22 -n
-- bcp AutocareHCB.dbo.InfinityTrainData in ./InfinityTrainData.dat -S localhost -U sa -P \!hanshin22 -n
-- bcp AutocareHCB.dbo.Patient in ./Patient.dat -S localhost -U sa -P \!hanshin22 -n



SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[BloodCodeInfo](
	[index] [tinyint] NOT NULL,
	[analysis_index] [nvarchar](20) NULL,
	[analysis_index_kor] [nvarchar](20) NULL,
	[male_min_value] [numeric](13, 1) NULL,
	[male_max_value] [numeric](13, 1) NULL,
	[female_min_value] [numeric](13, 1) NULL,
	[female_max_value] [numeric](13, 1) NULL,
	[unit] [nvarchar](10) NULL,
	[gum_code] [nvarchar](20) NULL,
 CONSTRAINT [PK_HCB_FACTOR_INFO] PRIMARY KEY CLUSTERED 
(
	[index] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Candidate](
	[AgeGroup] [smallint] NOT NULL,
	[PatientSex] [nvarchar](1) NOT NULL,
	[analysis_index] [nvarchar](50) NOT NULL,
	[candidate_value] [nvarchar](100) NULL,
 CONSTRAINT [PK_Candidate] PRIMARY KEY CLUSTERED 
(
	[analysis_index] ASC,
	[AgeGroup] ASC,
	[PatientSex] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DiseasePerBloodCodes](
	[index] [tinyint] NOT NULL,
	[disease] [nvarchar](50) NULL,
	[analysis_index] [nvarchar](50) NULL,
 CONSTRAINT [PK_BloodCodePerDisease] PRIMARY KEY CLUSTERED 
(
	[index] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[HanshinTrainData](
	[RegistKey] [uniqueidentifier] NOT NULL,
	[CheckupDate] [date] NULL,
	[PatientName] [varchar](50) NULL,
	[PatientBirthday] [varchar](50) NULL,
	[PatientAge] [decimal](9, 3) NOT NULL,
	[AgeGroup] [smallint] NULL,
	[PatientSex] [varchar](50) NULL,
	[per1_life_code1] [smallint] NULL,
	[per1_life_code2] [smallint] NULL,
	[per1_life_code3] [smallint] NULL,
	[per1_life_code4] [smallint] NULL,
	[per1_kwa2] [smallint] NULL,
	[per1_kwa3] [smallint] NULL,
	[per1_kwa4] [smallint] NULL,
	[per1_kwa5] [smallint] NULL,
	[per1_kwa6] [smallint] NULL,
	[per1_spc_year] [smallint] NULL,
	[N1101011] [varchar](max) NULL,
	[N1101021] [varchar](max) NULL,
	[N1101012] [varchar](max) NULL,
	[N1101022] [varchar](max) NULL,
	[N1101013] [varchar](max) NULL,
	[N1101023] [varchar](max) NULL,
	[N1101014] [varchar](max) NULL,
	[N1101024] [varchar](max) NULL,
	[N1101015] [varchar](max) NULL,
	[N1101025] [varchar](max) NULL,
	[N1101016] [varchar](max) NULL,
	[N1101026] [varchar](max) NULL,
	[N1101017] [varchar](max) NULL,
	[N1101027] [varchar](max) NULL,
	[N1102011] [varchar](max) NULL,
	[N1102012] [varchar](max) NULL,
	[N1102013] [varchar](max) NULL,
	[N1102014] [varchar](max) NULL,
	[N1102015] [varchar](max) NULL,
	[N110301] [varchar](max) NULL,
	[N110401] [varchar](max) NULL,
	[N110406] [varchar](max) NULL,
	[N110501] [varchar](max) NULL,
	[N110601] [varchar](max) NULL,
	[N110602] [varchar](max) NULL,
	[N110603] [varchar](max) NULL,
	[N110604] [varchar](max) NULL,
	[N110701] [varchar](max) NULL,
	[N110702] [varchar](max) NULL,
	[N110703] [varchar](max) NULL,
	[N110801] [varchar](max) NULL,
	[N110802] [varchar](max) NULL,
	[N110803] [varchar](max) NULL,
	[N110804] [varchar](max) NULL,
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
	[I349] [nvarchar](100) NULL,
 CONSTRAINT [PK_HanshinTrainData] PRIMARY KEY CLUSTERED 
(
	[RegistKey] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = ON, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[InfinityTrainData](
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
	[I349] [nvarchar](100) NULL,
 CONSTRAINT [PK_InfinityTrainData] PRIMARY KEY CLUSTERED 
(
	[RegistKey] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = ON, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
) ON [PRIMARY]
GO


SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Patient](
	[RegistKey] [uniqueidentifier] NOT NULL,
	[CheckupNo] [int] NOT NULL,
	[PatientChartNo] [varchar](50) NULL,
	[CheckupDate] [date] NULL,
	[PatientName] [varchar](50) NULL,
	[PatientBirthday] [varchar](50) NULL,
	[PatientAge] [decimal](9, 3) NOT NULL,
	[AgeGroup] [smallint] NULL,
	[PatientSex] [varchar](50) NULL,
	[per1_life_code1] [smallint] NULL,
	[per1_life_code2] [smallint] NULL,
	[per1_life_code3] [smallint] NULL,
	[per1_life_code4] [smallint] NULL,
	[per1_kwa2] [smallint] NULL,
	[per1_kwa3] [smallint] NULL,
	[per1_kwa4] [smallint] NULL,
	[per1_kwa5] [smallint] NULL,
	[per1_kwa6] [smallint] NULL,
	[per1_spc_year] [smallint] NULL,
	[N121115_2] [varchar](max) NULL,
	[N121116_1] [varchar](max) NULL,
	[N1101011] [varchar](max) NULL,
	[N1101021] [varchar](max) NULL,
	[N1101012] [varchar](max) NULL,
	[N1101022] [varchar](max) NULL,
	[N1101013] [varchar](max) NULL,
	[N1101023] [varchar](max) NULL,
	[N1101014] [varchar](max) NULL,
	[N1101024] [varchar](max) NULL,
	[N1101015] [varchar](max) NULL,
	[N1101025] [varchar](max) NULL,
	[N1101016] [varchar](max) NULL,
	[N1101026] [varchar](max) NULL,
	[N1101017] [varchar](max) NULL,
	[N1101027] [varchar](max) NULL,
	[N1102011] [varchar](max) NULL,
	[N1102012] [varchar](max) NULL,
	[N1102013] [varchar](max) NULL,
	[N1102014] [varchar](max) NULL,
	[N1102015] [varchar](max) NULL,
	[N110301] [varchar](max) NULL,
	[N110401] [varchar](max) NULL,
	[N110406] [varchar](max) NULL,
	[N110501] [varchar](max) NULL,
	[N110601] [varchar](max) NULL,
	[N110602] [varchar](max) NULL,
	[N110603] [varchar](max) NULL,
	[N110604] [varchar](max) NULL,
	[N110701] [varchar](max) NULL,
	[N110702] [varchar](max) NULL,
	[N110703] [varchar](max) NULL,
	[N110801] [varchar](max) NULL,
	[N110802] [varchar](max) NULL,
	[N110803] [varchar](max) NULL,
	[N110804] [varchar](max) NULL,
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
	[I349] [nvarchar](100) NULL,
	[percent_01] [float] NULL,
	[percent_02] [float] NULL,
	[percent_03] [float] NULL,
	[percent_04] [float] NULL,
	[percent_05] [float] NULL,
	[percent_06] [float] NULL,
	[percent_07] [float] NULL,
	[percent_08] [float] NULL,
	[percent_09] [float] NULL,
	[percent_10] [float] NULL,
	[percent_11] [float] NULL,
	[percent_12] [float] NULL,
	[percent_13] [float] NULL,
	[percent_14] [float] NULL,
 CONSTRAINT [PK_Patient] PRIMARY KEY CLUSTERED 
(
	[RegistKey] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = ON, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
