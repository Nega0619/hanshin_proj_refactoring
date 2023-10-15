SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[HmisRegistNational](
	[RegistNationalKey] [uniqueidentifier] NOT NULL,
	[RegistKey] [uniqueidentifier] NOT NULL,
	[CheckupNationalType] [int] NOT NULL,
	[CheckupDataCode] [varchar](50) NOT NULL,
	[ResultNational] [varchar](max) NULL,
	[ResultValue1] [varchar](max) NULL,
	[ResultValue2] [varchar](max) NULL,
	[ResultMarker] [varchar](50) NULL,
	[ResultRemarkCode] [varchar](50) NULL,
	[RegistedByName] [varchar](50) NOT NULL,
	[RegistedDate] [datetime2](7) NOT NULL,
	[ModifiedByName] [varchar](50) NOT NULL,
	[ModifiedDate] [datetime2](7) NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
ALTER TABLE [dbo].[HmisRegistNational] ADD  CONSTRAINT [PK_HmisRegistNational] PRIMARY KEY CLUSTERED 
(
	[RegistNationalKey] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[HmisRegistResult](
	[RegistResultKey] [uniqueidentifier] NOT NULL,
	[RegistKey] [uniqueidentifier] NOT NULL,
	[RegistProfileCode] [varchar](50) NULL,
	[RegistPackageCode] [varchar](50) NULL,
	[RegistDataCode] [varchar](50) NOT NULL,
	[RegistSeqNo] [int] NOT NULL,
	[ResultLocked] [bit] NOT NULL,
	[ResultInput] [varchar](max) NULL,
	[ResultValue1] [varchar](max) NULL,
	[ResultValue2] [varchar](max) NULL,
	[ResultMarker] [varchar](50) NULL,
	[ResultColor] [varchar](50) NULL,
	[ResultRemarkCode] [varchar](50) NULL,
	[TestStartByName] [varchar](50) NULL,
	[TestStartDate] [datetime2](7) NULL,
	[TestEndByName] [varchar](50) NULL,
	[TestEndDate] [datetime2](7) NULL,
	[RfidEndDate] [datetime2](7) NULL,
	[RfidEndByName] [varchar](50) NULL,
	[RegistedByName] [varchar](50) NOT NULL,
	[RegistedDate] [datetime2](7) NOT NULL,
	[ModifiedByName] [varchar](50) NOT NULL,
	[ModifiedDate] [datetime2](7) NOT NULL,
	[ResultNational] [varchar](max) NULL,
	[RfidStatus] [varchar](50) NULL,
	[ReTest] [varchar](2) NULL,
	[endRoom] [varchar](100) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
ALTER TABLE [dbo].[HmisRegistResult] ADD  CONSTRAINT [PK_HmisRegistResult] PRIMARY KEY CLUSTERED 
(
	[RegistResultKey] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[HmisRegistPatient](
	[RegistKey] [uniqueidentifier] NOT NULL,
	[RegistDate] [date] NOT NULL,
	[RegistNo] [int] NOT NULL,
	[RegistKindCode] [varchar](50) NULL,
	[RegistStatusType] [int] NOT NULL,
	[RegistStatusCode] [varchar](50) NULL,
	[CheckupDate] [date] NULL,
	[CheckupNo] [int] NOT NULL,
	[CheckupStartDate] [datetime2](7) NULL,
	[CheckupStartByName] [varchar](50) NULL,
	[CheckupEndDate] [datetime2](7) NULL,
	[CheckupEndByName] [varchar](50) NULL,
	[CheckupLocationCode] [varchar](50) NULL,
	[CheckupReportingCode] [varchar](50) NULL,
	[CustomerCode] [varchar](50) NOT NULL,
	[CustomerOffice] [varchar](50) NULL,
	[AgreeMessageReceivedDate] [varchar](50) NULL,
	[AgreeGuideReceivedDate] [varchar](50) NULL,
	[AgreeResultUsedDate] [varchar](50) NULL,
	[PatientName] [varchar](50) NULL,
	[PatientSSN] [varchar](50) NULL,
	[PatientInsuranceNo] [varchar](50) NULL,
	[PatientCardNo] [varchar](50) NULL,
	[PatientChartNo] [varchar](50) NULL,
	[PatientBirthday] [varchar](50) NULL,
	[PatientAge] [decimal](9, 3) NOT NULL,
	[PatientSex] [varchar](50) NULL,
	[PatientRelationCode] [varchar](50) NULL,
	[PatientPhoneNo] [varchar](50) NULL,
	[PatientMobileNo] [varchar](50) NULL,
	[PatientEmail] [varchar](500) NULL,
	[PatientZipCode] [varchar](50) NULL,
	[PatientAddress01] [varchar](500) NULL,
	[PatientAddress02] [varchar](500) NULL,
	[PatientCountryCode] [varchar](50) NULL,
	[PatientClassCode] [varchar](50) NULL,
	[PatientMemo] [varchar](max) NULL,
	[NationalCharged] [bit] NOT NULL,
	[NationalJoinKindCode] [varchar](50) NULL,
	[NationalOfficeCode] [varchar](50) NULL,
	[NationalJoinTypeCode] [varchar](50) NULL,
	[NationalClinicCode] [varchar](50) NULL,
	[NationalCheckup1] [int] NOT NULL,
	[NationalCheckup2] [int] NOT NULL,
	[NationalCheckupC] [int] NULL,
	[NationalOption1] [int] NOT NULL,
	[NationalOption2] [int] NOT NULL,
	[NationalOption3] [int] NOT NULL,
	[NationalOption4] [int] NOT NULL,
	[NationalOption5] [int] NOT NULL,
	[MilitaryHospitalCode] [varchar](50) NULL,
	[EmployeeHireDate] [varchar](50) NULL,
	[EmployeePosition] [varchar](50) NULL,
	[EmployeeDepartment] [varchar](500) NULL,
	[EmployeeNumber] [varchar](50) NULL,
	[EmployeeWorkingMode] [varchar](50) NULL,
	[VisitPathCode] [varchar](50) NULL,
	[VisitSubscriberName] [varchar](50) NULL,
	[VisitSubscriberPhone] [varchar](50) NULL,
	[VisitDueDate] [date] NULL,
	[VisitDueTime] [time](7) NULL,
	[VisitDueNo] [int] NOT NULL,
	[VisitConfirmByName] [varchar](50) NULL,
	[VisitConfirmDate] [datetime2](7) NULL,
	[VisitMemo] [varchar](max) NULL,
	[RfidTagNo] [varchar](50) NULL,
	[CheckupCont] [int] NULL,
	[CancelYN] [varchar](50) NULL,
	[RegistedByName] [varchar](50) NOT NULL,
	[RegistedDate] [datetime2](7) NOT NULL,
	[ModifiedByName] [varchar](50) NOT NULL,
	[ModifiedDate] [datetime2](7) NOT NULL,
	[NationalDate1] [varchar](50) NULL,
	[NationalDate2] [varchar](50) NULL,
	[NationalCheck1] [bit] NULL,
	[NationalCheck2] [bit] NULL,
	[NationalCheck3] [bit] NULL,
	[NationalCheck4] [bit] NULL,
	[NationalCheck5] [bit] NULL,
	[NationalCheck6] [bit] NULL,
	[NationalCheck7] [bit] NULL,
	[LifeCheckup] [int] NULL,
	[StudentGubun] [varchar](50) NULL,
	[StudentGrade] [varchar](50) NULL,
	[StudentClass] [varchar](50) NULL,
	[StudentNo] [varchar](50) NULL,
	[StudentNorYN] [varchar](50) NULL,
	[AgreeCancerResultUsedDate] [varchar](50) NULL,
	[AgeOption1] [varchar](50) NULL,
	[AgeOption2] [varchar](50) NULL,
	[AgeOption3] [varchar](50) NULL,
	[AgeOption4] [varchar](50) NULL,
	[AgeOption5] [varchar](50) NULL,
	[AgeOption6] [varchar](50) NULL,
	[AgeOption7] [varchar](50) NULL,
	[AgeOption8] [varchar](50) NULL,
	[PregnantCheck] [varchar](50) NULL,
	[NationalOption6] [int] NULL,
	[SSN1] [varchar](50) NULL,
	[etcColumn] [varchar](50) NULL,
	[RegistKeyOne] [uniqueidentifier] NULL,
	[totEnd] [varchar](1) NULL,
	[Flow] [varchar](50) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [PK_HmisRegistPatient] PRIMARY KEY CLUSTERED 
(
	[RegistKey] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [idx_HmisRegistPatient_ssn1] ON [dbo].[HmisRegistPatient]
(
	[SSN1] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistpaitent_RegistNo] ON [dbo].[HmisRegistPatient]
(
	[RegistNo] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [ix_HmisRegistPatient_CancelYN] ON [dbo].[HmisRegistPatient]
(
	[CancelYN] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_CheckupDate] ON [dbo].[HmisRegistPatient]
(
	[CheckupDate] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_CheckupNo] ON [dbo].[HmisRegistPatient]
(
	[CheckupNo] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_CustomerCode] ON [dbo].[HmisRegistPatient]
(
	[CustomerCode] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_CustomerOffice] ON [dbo].[HmisRegistPatient]
(
	[CustomerOffice] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [ix_HmisRegistPatient_ModifiedByName] ON [dbo].[HmisRegistPatient]
(
	[ModifiedByName] DESC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_NationalCheckup1] ON [dbo].[HmisRegistPatient]
(
	[NationalCheckup1] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_NationalCheckup2] ON [dbo].[HmisRegistPatient]
(
	[NationalCheckup2] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_NationalOption1] ON [dbo].[HmisRegistPatient]
(
	[NationalOption1] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_NationalOption2] ON [dbo].[HmisRegistPatient]
(
	[NationalOption2] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_NationalOption3] ON [dbo].[HmisRegistPatient]
(
	[NationalOption3] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_NationalOption4] ON [dbo].[HmisRegistPatient]
(
	[NationalOption4] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_NationalOption5] ON [dbo].[HmisRegistPatient]
(
	[NationalOption5] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_PatientCardNo] ON [dbo].[HmisRegistPatient]
(
	[PatientCardNo] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_PatientChartNo] ON [dbo].[HmisRegistPatient]
(
	[PatientChartNo] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_PatientClassCode] ON [dbo].[HmisRegistPatient]
(
	[PatientClassCode] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_PatientInsuranceNo] ON [dbo].[HmisRegistPatient]
(
	[PatientInsuranceNo] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_PatientMobileNo] ON [dbo].[HmisRegistPatient]
(
	[PatientMobileNo] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_PatientName] ON [dbo].[HmisRegistPatient]
(
	[PatientName] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_PatientRelation] ON [dbo].[HmisRegistPatient]
(
	[PatientRelationCode] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_PatientSSN] ON [dbo].[HmisRegistPatient]
(
	[PatientSSN] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_PatientStatusCode] ON [dbo].[HmisRegistPatient]
(
	[RegistStatusCode] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_RegistDate] ON [dbo].[HmisRegistPatient]
(
	[RegistedDate] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_RegistKindCode] ON [dbo].[HmisRegistPatient]
(
	[RegistKindCode] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_RegistNo] ON [dbo].[HmisRegistPatient]
(
	[RegistNo] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_RegistStatusType] ON [dbo].[HmisRegistPatient]
(
	[RegistStatusType] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_VisitConfirmDate] ON [dbo].[HmisRegistPatient]
(
	[VisitConfirmDate] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_VisitDueDate] ON [dbo].[HmisRegistPatient]
(
	[VisitDueDate] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_VisitDueTime] ON [dbo].[HmisRegistPatient]
(
	[VisitDueTime] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [IX_HmisRegistPatient_VisitSubscriberName] ON [dbo].[HmisRegistPatient]
(
	[VisitSubscriberName] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [NonClusteredIndex-20161101-103544] ON [dbo].[HmisRegistPatient]
(
	[CheckupLocationCode] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
CREATE NONCLUSTERED INDEX [NonClusteredIndex-20230118-221658] ON [dbo].[HmisRegistPatient]
(
	[PatientBirthday] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [NonClusteredIndex-20230216-203640] ON [dbo].[HmisRegistPatient]
(
	[RegistKeyOne] ASC
)WITH (PAD_INDEX = ON, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [DF_HmisRegistPatient_CancelYN]  DEFAULT ('N') FOR [CancelYN]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [DF_HmisRegistPatient_LifeCheckup]  DEFAULT ((0)) FOR [LifeCheckup]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [DF_HmisRegistPatient_StudentGubun]  DEFAULT ('') FOR [StudentGubun]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [DF_HmisRegistPatient_StudentGrade]  DEFAULT ('') FOR [StudentGrade]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [DF_HmisRegistPatient_StudentClass]  DEFAULT ('') FOR [StudentClass]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [DF_HmisRegistPatient_StudentNo]  DEFAULT ('') FOR [StudentNo]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [DF_HmisRegistPatient_StudentNorYN]  DEFAULT ('') FOR [StudentNorYN]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [DF_HmisRegistPatient_AgeOption1]  DEFAULT ('') FOR [AgeOption1]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [DF_HmisRegistPatient_AgeOption2]  DEFAULT ('') FOR [AgeOption2]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [DF_HmisRegistPatient_AgeOption3]  DEFAULT ('') FOR [AgeOption3]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [DF_HmisRegistPatient_AgeOption4]  DEFAULT ('') FOR [AgeOption4]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [DF_HmisRegistPatient_AgeOption5]  DEFAULT ('') FOR [AgeOption5]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [DF_HmisRegistPatient_AgeOption6]  DEFAULT ('') FOR [AgeOption6]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [DF_HmisRegistPatient_AgeOption7]  DEFAULT ('') FOR [AgeOption7]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [DF_HmisRegistPatient_AgeOption8]  DEFAULT ('') FOR [AgeOption8]
GO
ALTER TABLE [dbo].[HmisRegistPatient] ADD  CONSTRAINT [DF_HmisRegistPatient_Pregnant]  DEFAULT ('') FOR [PregnantCheck]
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'인지기능' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'HmisRegistPatient', @level2type=N'COLUMN',@level2name=N'AgeOption7'
GO