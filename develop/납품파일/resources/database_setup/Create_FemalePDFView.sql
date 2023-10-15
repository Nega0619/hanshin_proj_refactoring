SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- DECLARE @patientInfo TABLE(
-- 	[RegistKey] [uniqueidentifier] NOT NULL,
-- 	[CheckupDate] [date] NULL,
-- 	[PatientName] [varchar](50) NULL,
-- 	[PatientBirthday] [varchar](50) NULL,
-- 	[PatientAge] [decimal](9, 3) NOT NULL,
-- 	[AgeGroup] [smallint] NULL,
-- 	[PatientSex] [varchar](50) NULL
-- );

-- INSERT INTO @patientInfo 
-- 	SELECT top(100) RegistKey, CheckupDate, PatientName, PatientBirthday, PatientAge, 
-- 			(CASE 
-- 				WHEN cast(PatientAge as int) < 20 THEN 1  
-- 				WHEN cast(PatientAge as int) >= 20 AND cast(PatientAge as int) < 30 THEN 2 
-- 				WHEN cast(PatientAge as int) >= 30 AND cast(PatientAge as int) < 35 THEN 3 
-- 				WHEN cast(PatientAge as int) >= 35 AND cast(PatientAge as int) < 40 THEN 4 
-- 				WHEN cast(PatientAge as int) >= 40 AND cast(PatientAge as int) < 45 THEN 5 
-- 				WHEN cast(PatientAge as int) >= 45 AND cast(PatientAge as int) < 50 THEN 6 
-- 				WHEN cast(PatientAge as int) >= 50 AND cast(PatientAge as int) < 55 THEN 7 
-- 				WHEN cast(PatientAge as int) >= 55 AND cast(PatientAge as int) < 60 THEN 8 
-- 				WHEN cast(PatientAge as int) >= 60 AND cast(PatientAge as int) < 65 THEN 9 
-- 				WHEN cast(PatientAge as int) >= 65 AND cast(PatientAge as int) < 70 THEN 10 
-- 				WHEN cast(PatientAge as int) >= 70 AND cast(PatientAge as int) < 75 THEN 11 
-- 				WHEN cast(PatientAge as int) >= 75 AND cast(PatientAge as int) < 80 THEN 12 
-- 				WHEN cast(PatientAge as int) >= 80 AND cast(PatientAge as int) < 85 THEN 13 
-- 				WHEN cast(PatientAge as int) >= 85 THEN 14 
-- 			ELSE NULL END) as AgeGroup,
-- 			PatientSex
-- 	FROM AutocareHCB.dbo.HmisRegistPatient
-- 	where RegistStatusType = 2;

-- delete from AutocareHCB.dbo.CheckupPatients

-- select info.RegistKey, CheckupDate, PatientName, PatientBirthday, PatientAge, AgeGroup, PatientSex,
--   SUBSTRING(cast(CheckupDate as nvarchar), 1, 4),
--   N121115_2, N121116_1, N1101011, N1101021, N1101012, N1101022, N1101013, N1101023, N1101014,
--   N1101024, N1101015, N1101025, N1101016, N1101026, N1101017, N1101027, N1102011, N1102012, N1102013,
--   N1102014, N1102015, N110301, N110401, N110406, N110501, N110601, N110602, N110603, N110604, N110701,
--   N110702, N110703, N110801, N110802, N110803, N110804,
--   TP01, TP02, GP01, GP02, TP00, TP07, TP08, C037, C039, C904, C038, C026, C027,
--   C029, C030, C054, C022, C023, C024, C018, U008, C032, E001, I521, I105, I022,
--   I348, I502, I503, I349
-- from @patientInfo info
--   left outer join
--   (SELECT
--     *
--   FROM (select info.RegistKey, DataCode, MunjinValue
--     from @patientInfo info, (SELECT info.RegistKey, CheckupDataCode as DataCode, ResultValue1 as MunjinValue
-- FROM @patientInfo info inner JOIN AutocareHCB.dbo.HmisRegistNational ON HmisRegistNational.RegistKey = info.RegistKey
-- where CheckupDataCode in ('N121115_2', 'N121116_1', 'N1101011', 'N1101021', 'N1101012', 'N1101022', 'N1101013', 'N1101023', 'N1101014', 'N1101024', 'N1101015', 'N1101025', 'N1101016', 'N1101026', 'N1101017', 'N1101027', 'N1102011', 'N1102012', 'N1102013', 'N1102014', 'N1102015', 'N110301', 'N110401', 'N110406', 'N110501', 'N110601', 'N110602', 'N110603', 'N110604', 'N110701', 'N110702', 'N110703', 'N110801', 'N110802', 'N110803', 'N110804')-- where HealthMIS.dbo.HmisRegistNational.RegistKey is null
-- group by info.RegistKey, CheckupDataCode, ResultValue1) as temp_munjin
--     where info.registkey = temp_munjin.registkey) AS result
-- PIVOT (min(MunjinValue) FOR datacode IN ([N121115_2], [N121116_1], [N1101011], [N1101021], [N1101012], [N1101022], [N1101013], [N1101023], [N1101014],
--   [N1101024], [N1101015], [N1101025], [N1101016], [N1101026], [N1101017], [N1101027], [N1102011], [N1102012], [N1102013],
--   [N1102014], [N1102015], [N110301], [N110401], [N110406], [N110501], [N110601], [N110602], [N110603], [N110604], [N110701],
--   [N110702], [N110703], [N110801], [N110802], [N110803], [N110804])) as pivoted_munjin) as munjin on info.RegistKey = munjin.RegistKey
--   left outer join (SELECT
--     *
--   FROM (select info.RegistKey, DataCode, BloodValue
--     from @patientInfo info, (SELECT info.RegistKey, RegistDataCode as DataCode, ResultValue1 as BloodValue
-- FROM @patientInfo info inner JOIN AutocareHCB.dbo.HmisRegistResult ON HmisRegistResult.RegistKey = info.RegistKey
-- where RegistDataCode in ('TP01', 'TP02', 'GP01', 'GP02', 'TP00', 'TP07', 'TP08', 'C037', 'C039', 'C904', 'C038', 'C026', 'C027', 'C029', 'C030', 'C054', 'C022', 'C023', 'C024', 'C018', 'U008', 'C032', 'E001', 'I521', 'I105', 'I022', 'I348', 'I502', 'I503', 'I349')
-- group by info.RegistKey, RegistDataCode, ResultValue1) as temp_Blood
--     where info.registkey = temp_Blood.registkey) AS result
-- PIVOT (min(BloodValue) FOR datacode IN 
-- ([TP01], [TP02], [GP01], [GP02], [TP00], [TP07], [TP08], [C037], [C039], [C904], [C038], [C026], [C027], 
-- [C029], [C030], [C054], [C022], [C023], [C024], [C018], [U008], [C032], [E001], [I521], [I105], [I022], 
-- [I348], [I502], [I503], [I349])) as pivoted_blood) as blood on info.RegistKey = blood.RegistKey


-- drop table dbo.test

-- select top(10000) * into autocarehcb.dbo.test
--  from AutocareHCB.dbo.CheckupPatients

-- SELECT RegistKey, N110703 FROM AutocareHCB.dbo.test WHERE N110703 LIKE '% %'
-- select RegistKey, N121115_2+'.', trim(N121115_2)+'.' FROM AutocareHCB.dbo.test WHERE N121115_2 LIKE '% %'
-- update AutocareHCB.dbo.test set N110703 = trim(N110703) WHERE N110703 LIKE '% %'
-- SELECT RegistKey, N110703 FROM AutocareHCB.dbo.test WHERE N110703 LIKE '% %'

-- SELECT RegistKey, N110703 FROM AutocareHCB.dbo.test WHERE N110703 LIKE '% %'

-- select count(*) from autocarehcb.dbo.HmisRegistPatient
-- select PatientSSN, count(*) as cnt from autocarehcb.dbo.HmisRegistPatient group by PatientSSN order by cnt desc
-- select top(1) * from AutocareHCB.dbo.HmisRegistPatient
-- select CustomerCode, count(*) as cnt from autocarehcb.dbo.HmisRegistPatient group by CustomerCode order by cnt desc
 

-- delete from autocarehcb.dbo.CheckupPatients
-- delete from autocarehcb.dbo.hanshintraindata
-- CREATE VIEW pdfView AS SELECT TOP(100) disease, analysis_index_kor, male_min_value, male_max_value FROM AutocareHCB.dbo.DiseasePerBloodCodes, AutocareHCB.dbo.BloodCodeInfo
-- WHERE DiseasePerBloodCodes.analysis_index = BloodCodeInfo.analysis_index
-- order by DiseasePerBloodCodes.[index]

-- select * from pdfview
-- drop view dbo.FemalePDFView

-- CREATE VIEW dbo.MalePDFView AS SELECT TOP(100) DiseasePerBloodCodes.[index], disease, analysis_index_kor, male_min_value, male_max_value, gum_code FROM AutocareHCB.dbo.DiseasePerBloodCodes, AutocareHCB.dbo.BloodCodeInfo
-- WHERE DiseasePerBloodCodes.analysis_index = BloodCodeInfo.analysis_index
-- order by DiseasePerBloodCodes.[index];

CREATE VIEW [dbo].[FemalePDFView] AS SELECT TOP(100) DiseasePerBloodCodes.[index], disease, analysis_index_kor, female_min_value, female_max_value, gum_code FROM AutocareHCB.dbo.DiseasePerBloodCodes, AutocareHCB.dbo.BloodCodeInfo
WHERE DiseasePerBloodCodes.analysis_index = BloodCodeInfo.analysis_index
order by DiseasePerBloodCodes.[index];

-- SELECT factor.[index], factor.disease, factor.analysis_index_kor, factor.male_min_value, factor.male_max_value, real_data.VALUE\
--                         FROM (SELECT A.[index], disease, analysis_index_kor, male_min_value, male_max_value, gum_code \
--                                 FROM ANAL_2022.dbo.HCB_Disease_Factor A, ANAL_2022.dbo.HCB_Factor_Info B \
--                                 WHERE A.analysis_index=b.analysis_index) factor,\
--                             (SELECT per1_name, value, CONVERT(NVARCHAR(10), code) AS gum_code \
--                             FROM \
--                                 (SELECT * \
--                                 FROM ANAL_2022.dbo.AutoCare_HCB_afterinfer \
--                                 WHERE per1_date='{per1_date}' AND per1_chat_no='{per1_chat_no}' AND per1_bun_no = '{per1_bun_no}')  A\
--                             UNPIVOT(value FOR code IN (C024,C023,C022,GP02,I349,I348,I022,I105,I502,C039,C904,I503,C026,C018,TP07,C030,U008,TP08,C038,C029,C037,C032)) AS UNPVT) real_data\
--                         WHERE factor.gum_code=real_data.gum_code\
--                         ORDER BY factor.[index]

-- select pdf.disease, pdf.analysis_index_kor, pdf.male_min_value, pdf.male_max_value, real_value.VALUE
-- from MalePDFView,
--      (SELECT value, CONVERT(NVARCHAR(10), code) AS gum_code 
--             FROM 
--                 (SELECT * 
--                 FROM AutocareHCB.dbo.test
--                 WHERE registkey = '13482ed4-e63b-4e22-ae03-0002d8e7aab9')  A
--             UNPIVOT(value FOR code IN (C024,C023,C022,GP02,I349,I348,I022,I105,I502,C039,C904,I503,C026,C018,TP07,C030,U008,TP08,C038,C029,C037,C032)) AS UNPVT) real_data

-- SELECT pdf.disease, pdf.analysis_index_kor, pdf.male_min_value, pdf.male_max_value, real_data.VALUE                        FROM MalePDFView AS pdf,                             (SELECT value, CONVERT(NVARCHAR(10), code) AS gum_code                                FROM                                    (SELECT *                                        FROM AutocareHCB.dbo.test                                            WHERE registkey = 'cd3bdef7-a002-46c1-bfcb-011cacfc9c68') A                                            UNPIVOT(value FOR code IN (C024,C023,C022,GP02,I349,I348,I022,I105,I502,C039,C904,I503,C026,C018,TP07,C030,U008,TP08,C038,C029,C037,C032)) AS UNPVT)                                             as real_data                        WHERE pdf.gum_code = real_data.gum_code
            

-- select * from malepdfview
GO
