-- 두번째 Insert 구문에서, 
-- where RegistStatusType = 2 and CheckupDate>'{pre}' and CheckupDate<'{aft}';
-- {pre}, {aft} 날짜부분을 수정해주면 됩니다.

DECLARE @patientInfo TABLE(
                    [RegistKey] [uniqueidentifier] NOT NULL,
                    [CheckupNo] [int] NOT NULL,
                    [PatientChartNo] [varchar](50) NULL,
                    [CheckupDate] [date] NULL,
                    [PatientName] [varchar](50) NULL,
                    [PatientBirthday] [varchar](50) NULL,
                    [PatientAge] [decimal](9, 3) NOT NULL,
                    [AgeGroup] [smallint] NULL,
                    [PatientSex] [varchar](50) NULL
                );

                INSERT INTO @patientInfo 
                    SELECT RegistKey, CheckupNo, PatientChartNo, CheckupDate, PatientName, PatientBirthday, PatientAge, 
                            (CASE 
                                WHEN cast(PatientAge as int) < 20 THEN 1  
                                WHEN cast(PatientAge as int) >= 20 AND cast(PatientAge as int) < 30 THEN 2 
                                WHEN cast(PatientAge as int) >= 30 AND cast(PatientAge as int) < 35 THEN 3 
                                WHEN cast(PatientAge as int) >= 35 AND cast(PatientAge as int) < 40 THEN 4 
                                WHEN cast(PatientAge as int) >= 40 AND cast(PatientAge as int) < 45 THEN 5 
                                WHEN cast(PatientAge as int) >= 45 AND cast(PatientAge as int) < 50 THEN 6 
                                WHEN cast(PatientAge as int) >= 50 AND cast(PatientAge as int) < 55 THEN 7 
                                WHEN cast(PatientAge as int) >= 55 AND cast(PatientAge as int) < 60 THEN 8 
                                WHEN cast(PatientAge as int) >= 60 AND cast(PatientAge as int) < 65 THEN 9 
                                WHEN cast(PatientAge as int) >= 65 AND cast(PatientAge as int) < 70 THEN 10 
                                WHEN cast(PatientAge as int) >= 70 AND cast(PatientAge as int) < 75 THEN 11 
                                WHEN cast(PatientAge as int) >= 75 AND cast(PatientAge as int) < 80 THEN 12 
                                WHEN cast(PatientAge as int) >= 80 AND cast(PatientAge as int) < 85 THEN 13 
                                WHEN cast(PatientAge as int) >= 85 THEN 14 
                            ELSE NULL END) as AgeGroup,
                            PatientSex
                    FROM HealthMIS.dbo.HmisRegistPatient
                    where RegistStatusType = 2 and CheckupDate>'{pre}' and CheckupDate<'{aft}';

                insert into AutocareHCB.dbo.Patient(RegistKey, CheckupNo, PatientChartNo, CheckupDate, PatientName, PatientBirthday, PatientAge, AgeGroup, PatientSex, per1_spc_year, N121115_2, N121116_1, N1101011, N1101021, N1101012, N1101022, N1101013, N1101023, N1101014, N1101024, N1101015, N1101025, N1101016, N1101026, N1101017, N1101027, N1102011, N1102012, N1102013, N1102014, N1102015, N110301, N110401, N110406, N110501, N110601, N110602, N110603, N110604, N110701, N110702, N110703, N110801, N110802, N110803, N110804, TP01, TP02, GP01, GP02, TP00, TP07, TP08, C037, C039, C904, C038, C026, C027, C029, C030, C054, C022, C023, C024, C018, U008, C032, E001, I521, I105, I022, I348, I502, I503, I349)
                    select info.RegistKey, CheckupNo, PatientChartNo, CheckupDate, PatientName, PatientBirthday, PatientAge, AgeGroup, PatientSex,
                            SUBSTRING(cast(CheckupDate as nvarchar), 1, 4),
                            N121115_2, N121116_1, N1101011, N1101021, N1101012, N1101022, N1101013, N1101023, N1101014,
                            N1101024, N1101015, N1101025, N1101016, N1101026, N1101017, N1101027, N1102011, N1102012, N1102013,
                            N1102014, N1102015, N110301, N110401, N110406, N110501, N110601, N110602, N110603, N110604, N110701,
                            N110702, N110703, N110801, N110802, N110803, N110804,
                            TP01, TP02, GP01, GP02, TP00, TP07, TP08, C037, C039, C904, C038, C026, C027,
                            C029, C030, C054, C022, C023, C024, C018, U008, C032, E001, I521, I105, I022,
                            I348, I502, I503, I349
                    from @patientInfo info
                        left outer join
                            (SELECT *
                            FROM (select info.RegistKey, DataCode, MunjinValue 
                                    from @patientInfo info, 
                                            (SELECT info.RegistKey, CheckupDataCode as DataCode, ResultValue1 as MunjinValue
                                            FROM @patientInfo info inner JOIN HealthMIS.dbo.HmisRegistNational ON HmisRegistNational.RegistKey = info.RegistKey
                                            where CheckupDataCode in ('N121115_2', 'N121116_1', 'N1101011', 'N1101021', 'N1101012', 'N1101022', 'N1101013', 'N1101023', 'N1101014', 'N1101024', 'N1101015', 'N1101025', 'N1101016', 'N1101026', 'N1101017', 'N1101027', 'N1102011', 'N1102012', 'N1102013', 'N1102014', 'N1102015', 'N110301', 'N110401', 'N110406', 'N110501', 'N110601', 'N110602', 'N110603', 'N110604', 'N110701', 'N110702', 'N110703', 'N110801', 'N110802', 'N110803', 'N110804')
                                            group by info.RegistKey, CheckupDataCode, ResultValue1) as temp_munjin
                                    where info.registkey = temp_munjin.registkey) AS result
                            PIVOT (min(MunjinValue) FOR datacode IN ([N121115_2], [N121116_1], [N1101011], [N1101021], [N1101012], [N1101022], [N1101013], [N1101023], [N1101014],
                            [N1101024], [N1101015], [N1101025], [N1101016], [N1101026], [N1101017], [N1101027], [N1102011], [N1102012], [N1102013],
                            [N1102014], [N1102015], [N110301], [N110401], [N110406], [N110501], [N110601], [N110602], [N110603], [N110604], [N110701],
                            [N110702], [N110703], [N110801], [N110802], [N110803], [N110804])) as pivoted_munjin) as munjin on info.RegistKey = munjin.RegistKey
                        left outer join 
                            (SELECT *
                            FROM (select info.RegistKey, DataCode, BloodValue
                                    from @patientInfo info, 
                                            (SELECT info.RegistKey, RegistDataCode as DataCode, ResultValue1 as BloodValue
                                            FROM @patientInfo info inner JOIN HealthMIS.dbo.HmisRegistResult ON HmisRegistResult.RegistKey = info.RegistKey
                                            where RegistDataCode in ('TP01', 'TP02', 'GP01', 'GP02', 'TP00', 'TP07', 'TP08', 'C037', 'C039', 'C904', 'C038', 'C026', 'C027', 'C029', 'C030', 'C054', 'C022', 'C023', 'C024', 'C018', 'U008', 'C032', 'E001', 'I521', 'I105', 'I022', 'I348', 'I502', 'I503', 'I349')
                                            group by info.RegistKey, RegistDataCode, ResultValue1) as temp_Blood
                                    where info.registkey = temp_Blood.registkey) AS result
                            PIVOT (min(BloodValue) FOR datacode IN 
                            ([TP01], [TP02], [GP01], [GP02], [TP00], [TP07], [TP08], [C037], [C039], [C904], [C038], [C026], [C027], 
                            [C029], [C030], [C054], [C022], [C023], [C024], [C018], [U008], [C032], [E001], [I521], [I105], [I022], 
                            [I348], [I502], [I503], [I349])) as pivoted_blood) as blood on info.RegistKey = blood.RegistKey;