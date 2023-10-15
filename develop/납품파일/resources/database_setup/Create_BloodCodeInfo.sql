SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [AutocareHCB].[dbo].[BloodCodeInfo](
	[index] [tinyint] NOT NULL,
	[analysis_index] [nvarchar](20) NULL,
	[analysis_index_kor] [nvarchar](20) NULL,
	[male_min_value] [numeric](13, 1) NULL,
	[male_max_value] [numeric](13, 1) NULL,
	[female_min_value] [numeric](13, 1) NULL,
	[female_max_value] [numeric](13, 1) NULL,
	[unit] [nvarchar](10) NULL,
	[gum_code] [nvarchar](20) NULL
) ON [PRIMARY]
GO
ALTER TABLE [AutocareHCB].[dbo].[BloodCodeInfo] ADD  CONSTRAINT [PK_HCB_FACTOR_INFO] PRIMARY KEY CLUSTERED 
(
	[index] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
