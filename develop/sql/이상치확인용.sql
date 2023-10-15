-- select N121115_2, count(*) from AutocareHCB.dbo.checkuppatients group by N121115_2 order by N121115_2
-- select N121116_1 from AutocareHCB.dbo.checkuppatients group by N121116_1 order by N121116_1


-- select sum(cnt) from (select N121115_2, count(*) as cnt from AutocareHCB.dbo.TEST WHERE N121115_2 LIKE '%신체활동%' group by N121115_2) a
-- select sum(cnt) from (select N121115_2, count(*) as cnt from AutocareHCB.dbo.TEST WHERE N121115_2 LIKE '%신체활동%' group by N121115_2) a
-- UPDATE AutocareHCB.dbo.TEST SET per1_life_code1=0 WHERE N121115_2 LIKE '해당사항'
-- UPDATE AutocareHCB.dbo.TEST SET per1_life_code1=1 WHERE N121115_2 LIKE '%음주%'

-- select per1_life_code1, count(*) from AutocareHCB.dbo.TEST group by per1_life_code1
-- select per1_life_code2, count(*) from AutocareHCB.dbo.TEST group by per1_life_code2
-- select per1_life_code3, count(*) from AutocareHCB.dbo.TEST group by per1_life_code3
-- select per1_life_code4, count(*) from AutocareHCB.dbo.TEST group by per1_life_code4

-- select N121116_1, count(*) as cnt from AutocareHCB.dbo.TEST WHERE N121116_1 LIKE '%고혈압%' group by N121116_1
-- select N121116_1, count(*) as cnt from AutocareHCB.dbo.TEST WHERE N121116_1 LIKE '%뇌졸증%' group by N121116_1
-- select N121116_1, count(*) as cnt from AutocareHCB.dbo.TEST WHERE N121116_1 LIKE '%심장병%' group by N121116_1
-- select N121116_1, count(*) as cnt from AutocareHCB.dbo.TEST WHERE N121116_1 LIKE '%당뇨%' group by N121116_1
-- select N121116_1, count(*) as cnt from AutocareHCB.dbo.TEST WHERE N121116_1 LIKE '%암%' group by N121116_1


-- select sum(cnt) from (select N121116_1, count(*) as cnt from AutocareHCB.dbo.TEST WHERE N121116_1 LIKE '%고혈압%' group by N121116_1) a
-- select sum(cnt) from (select N121116_1, count(*) as cnt from AutocareHCB.dbo.TEST WHERE N121116_1 LIKE '%뇌졸증%' group by N121116_1) a
-- select sum(cnt) from (select N121116_1, count(*) as cnt from AutocareHCB.dbo.TEST WHERE N121116_1 LIKE '%심장병%' group by N121116_1) a
-- select sum(cnt) from (select N121116_1, count(*) as cnt from AutocareHCB.dbo.TEST WHERE N121116_1 LIKE '%당뇨병%' group by N121116_1) a
-- select sum(cnt) from (select N121116_1, count(*) as cnt from AutocareHCB.dbo.TEST WHERE N121116_1 LIKE '%암%' group by N121116_1) a


-- select per1_kwa2, count(*) from AutocareHCB.dbo.TEST group by per1_kwa2
-- select per1_kwa3, count(*) from AutocareHCB.dbo.TEST group by per1_kwa3
-- select per1_kwa4, count(*) from AutocareHCB.dbo.TEST group by per1_kwa4
-- select per1_kwa5, count(*) from AutocareHCB.dbo.TEST group by per1_kwa5
-- select per1_kwa6, count(*) from AutocareHCB.dbo.TEST group by per1_kwa6

-- select N1101011, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101011 order by N1101011
-- select N1101013, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101013 order by N1101013
-- select N1101014, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101014 order by N1101014
-- select N1101017, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101017 order by N1101017



-- select per1_life_code1, count(*) from AutocareHCB.dbo.TEST where isnumeric(per1_life_code1) = 0 and per1_life_code1 is not null group by per1_life_code1 order by per1_life_code1
-- select per1_life_code2, count(*) from AutocareHCB.dbo.TEST where isnumeric(per1_life_code2) = 0 and per1_life_code2 is not null group by per1_life_code2 order by per1_life_code2
-- select per1_life_code3, count(*) from AutocareHCB.dbo.TEST where isnumeric(per1_life_code3) = 0 and per1_life_code3 is not null group by per1_life_code3 order by per1_life_code3
-- select per1_life_code4, count(*) from AutocareHCB.dbo.TEST where isnumeric(per1_life_code4) = 0 and per1_life_code4 is not null group by per1_life_code4 order by per1_life_code4
-- select per1_kwa2, count(*) from AutocareHCB.dbo.TEST where isnumeric(per1_kwa2) = 0 and per1_kwa2 is not null group by per1_kwa2 order by per1_kwa2
-- select per1_kwa3, count(*) from AutocareHCB.dbo.TEST where isnumeric(per1_kwa3) = 0 and per1_kwa3 is not null group by per1_kwa3 order by per1_kwa3
-- select per1_kwa4, count(*) from AutocareHCB.dbo.TEST where isnumeric(per1_kwa4) = 0 and per1_kwa4 is not null group by per1_kwa4 order by per1_kwa4
-- select per1_kwa5, count(*) from AutocareHCB.dbo.TEST where isnumeric(per1_kwa5) = 0 and per1_kwa5 is not null group by per1_kwa5 order by per1_kwa5
-- select per1_kwa6, count(*) from AutocareHCB.dbo.TEST where isnumeric(per1_kwa6) = 0 and per1_kwa6 is not null group by per1_kwa6 order by per1_kwa6
-- -- select N121115_2, count(*) from AutocareHCB.dbo.TEST where isnumeric(N121115_2) = 0 and N121115_2 is not null group by N121115_2 order by N121115_2
-- -- select N121116_1, count(*) from AutocareHCB.dbo.TEST where isnumeric(N121116_1) = 0 and N121116_1 is not null group by N121116_1 order by N121116_1
-- select N1101011, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1101011) = 0 and N1101011 is not null group by N1101011 order by N1101011
-- select N1101021, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1101021) = 0 and N1101021 is not null group by N1101021 order by N1101021
-- select N1101012, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1101012) = 0 and N1101012 is not null group by N1101012 order by N1101012
-- select N1101022, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1101022) = 0 and N1101022 is not null group by N1101022 order by N1101022
-- select N1101013, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1101013) = 0 and N1101013 is not null group by N1101013 order by N1101013
-- select N1101023, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1101023) = 0 and N1101023 is not null group by N1101023 order by N1101023
-- select N1101014, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1101014) = 0 and N1101014 is not null group by N1101014 order by N1101014
-- select N1101024, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1101024) = 0 and N1101024 is not null group by N1101024 order by N1101024
-- select N1101015, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1101015) = 0 and N1101015 is not null group by N1101015 order by N1101015
-- select N1101025, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1101025) = 0 and N1101025 is not null group by N1101025 order by N1101025
-- select N1101016, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1101016) = 0 and N1101016 is not null group by N1101016 order by N1101016
-- select N1101026, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1101026) = 0 and N1101026 is not null group by N1101026 order by N1101026
-- select N1101017, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1101017) = 0 and N1101017 is not null group by N1101017 order by N1101017
-- select N1101027, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1101027) = 0 and N1101027 is not null group by N1101027 order by N1101027
-- select N1102011, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1102011) = 0 and N1102011 is not null group by N1102011 order by N1102011
-- select N1102012, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1102012) = 0 and N1102012 is not null group by N1102012 order by N1102012
-- select N1102013, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1102013) = 0 and N1102013 is not null group by N1102013 order by N1102013
-- select N1102014, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1102014) = 0 and N1102014 is not null group by N1102014 order by N1102014
-- select N1102015, count(*) from AutocareHCB.dbo.TEST where isnumeric(N1102015) = 0 and N1102015 is not null group by N1102015 order by N1102015
-- select N110301, count(*) from AutocareHCB.dbo.TEST where isnumeric(N110301) = 0 and N110301 is not null group by N110301 order by N110301
-- select N110401, count(*) from AutocareHCB.dbo.TEST where isnumeric(N110401) = 0 and N110401 is not null group by N110401 order by N110401
-- select N110406, count(*) from AutocareHCB.dbo.TEST where isnumeric(N110406) = 0 and N110406 is not null group by N110406 order by N110406
-- select N110501, count(*) from AutocareHCB.dbo.TEST where isnumeric(N110501) = 0 and N110501 is not null group by N110501 order by N110501
-- select N110601, count(*) from AutocareHCB.dbo.TEST where isnumeric(N110601) = 0 and N110601 is not null group by N110601 order by N110601
-- select N110602, count(*) from AutocareHCB.dbo.TEST where isnumeric(N110602) = 0 and N110602 is not null group by N110602 order by N110602
-- select N110603, count(*) from AutocareHCB.dbo.TEST where isnumeric(N110603) = 0 and N110603 is not null group by N110603 order by N110603
-- select N110604, count(*) from AutocareHCB.dbo.TEST where isnumeric(N110604) = 0 and N110604 is not null group by N110604 order by N110604
-- select N110701, count(*) from AutocareHCB.dbo.TEST where isnumeric(N110701) = 0 and N110701 is not null group by N110701 order by N110701
-- select N110702, count(*) from AutocareHCB.dbo.TEST where isnumeric(N110702) = 0 and N110702 is not null group by N110702 order by N110702
-- select N110703, count(*) from AutocareHCB.dbo.TEST where isnumeric(N110703) = 0 and N110703 is not null group by N110703 order by N110703
-- select N110801, count(*) from AutocareHCB.dbo.TEST where isnumeric(N110801) = 0 and N110801 is not null group by N110801 order by N110801
-- select N110802, count(*) from AutocareHCB.dbo.TEST where isnumeric(N110802) = 0 and N110802 is not null group by N110802 order by N110802
-- select N110803, count(*) from AutocareHCB.dbo.TEST where isnumeric(N110803) = 0 and N110803 is not null group by N110803 order by N110803
-- select N110804, count(*) from AutocareHCB.dbo.TEST where isnumeric(N110804) = 0 and N110804 is not null group by N110804 order by N110804



-- select TP01 from AutocareHCB.dbo.TEST where ISNUMERIC(TP01) = 0 and TP01 is not null group by TP01 order by TP01
-- select TP02 from AutocareHCB.dbo.TEST where ISNUMERIC(TP02) = 0 and TP02 is not null group by TP02 order by TP02
-- select GP01 from AutocareHCB.dbo.TEST where ISNUMERIC(GP01) = 0 and GP01 is not null group by GP01 order by GP01
-- select GP02 from AutocareHCB.dbo.TEST where ISNUMERIC(GP02) = 0 and GP02 is not null group by GP02 order by GP02
-- select TP00 from AutocareHCB.dbo.TEST where ISNUMERIC(TP00) = 0 and TP00 is not null group by TP00 order by TP00
-- select TP07 from AutocareHCB.dbo.TEST where ISNUMERIC(TP07) = 0 and TP07 is not null group by TP07 order by TP07
-- select TP08 from AutocareHCB.dbo.TEST where ISNUMERIC(TP08) = 0 and TP08 is not null group by TP08 order by TP08
-- select C037 from AutocareHCB.dbo.TEST where ISNUMERIC(C037) = 0 and C037 is not null group by C037 order by C037
-- select C039 from AutocareHCB.dbo.TEST where ISNUMERIC(C039) = 0 and C039 is not null group by C039 order by C039
-- select C904 from AutocareHCB.dbo.TEST where ISNUMERIC(C904) = 0 and C904 is not null group by C904 order by C904
-- select C038 from AutocareHCB.dbo.TEST where ISNUMERIC(C038) = 0 and C038 is not null group by C038 order by C038
-- select C026 from AutocareHCB.dbo.TEST where ISNUMERIC(C026) = 0 and C026 is not null group by C026 order by C026
-- select C027 from AutocareHCB.dbo.TEST where ISNUMERIC(C027) = 0 and C027 is not null group by C027 order by C027
-- select C029 from AutocareHCB.dbo.TEST where ISNUMERIC(C029) = 0 and C029 is not null group by C029 order by C029
-- select C030 from AutocareHCB.dbo.TEST where ISNUMERIC(C030) = 0 and C030 is not null group by C030 order by C030
-- select C054 from AutocareHCB.dbo.TEST where ISNUMERIC(C054) = 0 and C054 is not null group by C054 order by C054
-- select C022 from AutocareHCB.dbo.TEST where ISNUMERIC(C022) = 0 and C022 is not null group by C022 order by C022
-- select C023 from AutocareHCB.dbo.TEST where ISNUMERIC(C023) = 0 and C023 is not null group by C023 order by C023
-- select C024 from AutocareHCB.dbo.TEST where ISNUMERIC(C024) = 0 and C024 is not null group by C024 order by C024
-- select C018 from AutocareHCB.dbo.TEST where ISNUMERIC(C018) = 0 and C018 is not null group by C018 order by C018
-- select U008 from AutocareHCB.dbo.TEST where ISNUMERIC(U008) = 0 and U008 is not null group by U008 order by U008
-- select C032 from AutocareHCB.dbo.TEST where ISNUMERIC(C032) = 0 and C032 is not null group by C032 order by C032
-- select E001 from AutocareHCB.dbo.TEST where ISNUMERIC(E001) = 0 and E001 is not null group by E001 order by E001
-- select I521 from AutocareHCB.dbo.TEST where ISNUMERIC(I521) = 0 and I521 is not null group by I521 order by I521
-- select I105 from AutocareHCB.dbo.TEST where ISNUMERIC(I105) = 0 and I105 is not null group by I105 order by I105
-- select I022 from AutocareHCB.dbo.TEST where ISNUMERIC(I022) = 0 and I022 is not null group by I022 order by I022
-- select I348 from AutocareHCB.dbo.TEST where ISNUMERIC(I348) = 0 and I348 is not null group by I348 order by I348
-- select I502 from AutocareHCB.dbo.TEST where ISNUMERIC(I502) = 0 and I502 is not null group by I502 order by I502
-- select I503 from AutocareHCB.dbo.TEST where ISNUMERIC(I503) = 0 and I503 is not null group by I503 order by I503
-- select I349 from AutocareHCB.dbo.TEST where ISNUMERIC(I349) = 0 and I349 is not null group by I349 order by I349



select per1_life_code1, count(*) from AutocareHCB.dbo.CheckupPatients group by per1_life_code1 order by per1_life_code1
select per1_life_code2, count(*) from AutocareHCB.dbo.CheckupPatients group by per1_life_code2 order by per1_life_code2
select per1_life_code3, count(*) from AutocareHCB.dbo.CheckupPatients group by per1_life_code3 order by per1_life_code3
select per1_life_code4, count(*) from AutocareHCB.dbo.CheckupPatients group by per1_life_code4 order by per1_life_code4
select per1_kwa2, count(*) from AutocareHCB.dbo.CheckupPatients group by per1_kwa2 order by per1_kwa2
select per1_kwa3, count(*) from AutocareHCB.dbo.CheckupPatients group by per1_kwa3 order by per1_kwa3
select per1_kwa4, count(*) from AutocareHCB.dbo.CheckupPatients group by per1_kwa4 order by per1_kwa4
select per1_kwa5, count(*) from AutocareHCB.dbo.CheckupPatients group by per1_kwa5 order by per1_kwa5
select per1_kwa6, count(*) from AutocareHCB.dbo.CheckupPatients group by per1_kwa6 order by per1_kwa6
select N1101011, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101011 order by N1101011
select N1101021, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101021 order by N1101021
select N1101012, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101012 order by N1101012
select N1101022, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101022 order by N1101022
select N1101013, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101013 order by N1101013
select N1101023, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101023 order by N1101023
select N1101014, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101014 order by N1101014
select N1101024, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101024 order by N1101024
select N1101015, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101015 order by N1101015
select N1101025, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101025 order by N1101025
select N1101016, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101016 order by N1101016
select N1101026, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101026 order by N1101026
select N1101017, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101017 order by N1101017
select N1101027, count(*) from AutocareHCB.dbo.CheckupPatients group by N1101027 order by N1101027
select N1102011, count(*) from AutocareHCB.dbo.CheckupPatients group by N1102011 order by N1102011
select N1102012, count(*) from AutocareHCB.dbo.CheckupPatients group by N1102012 order by N1102012
select N1102013, count(*) from AutocareHCB.dbo.CheckupPatients group by N1102013 order by N1102013
select N1102014, count(*) from AutocareHCB.dbo.CheckupPatients group by N1102014 order by N1102014
select N1102015, count(*) from AutocareHCB.dbo.CheckupPatients group by N1102015 order by N1102015
select N110301, count(*) from AutocareHCB.dbo.CheckupPatients group by N110301 order by N110301
select N110401, count(*) from AutocareHCB.dbo.CheckupPatients group by N110401 order by N110401
select N110406, count(*) from AutocareHCB.dbo.CheckupPatients group by N110406 order by N110406
select N110501, count(*) from AutocareHCB.dbo.CheckupPatients group by N110501 order by N110501
select N110601, count(*) from AutocareHCB.dbo.CheckupPatients group by N110601 order by N110601
select N110602, count(*) from AutocareHCB.dbo.CheckupPatients group by N110602 order by N110602
select N110603, count(*) from AutocareHCB.dbo.CheckupPatients group by N110603 order by N110603
select N110604, count(*) from AutocareHCB.dbo.CheckupPatients group by N110604 order by N110604
select N110701, count(*) from AutocareHCB.dbo.CheckupPatients group by N110701 order by N110701
select N110702, count(*) from AutocareHCB.dbo.CheckupPatients group by N110702 order by N110702
select N110703, count(*) from AutocareHCB.dbo.CheckupPatients group by N110703 order by N110703
select N110801, count(*) from AutocareHCB.dbo.CheckupPatients group by N110801 order by N110801
select N110802, count(*) from AutocareHCB.dbo.CheckupPatients group by N110802 order by N110802
select N110803, count(*) from AutocareHCB.dbo.CheckupPatients group by N110803 order by N110803
select N110804, count(*) from AutocareHCB.dbo.CheckupPatients group by N110804 order by N110804

-- select TP01 from AutocareHCB.dbo.CheckupPatients group by TP01 order by TP01
-- select TP02 from AutocareHCB.dbo.CheckupPatients group by TP02 order by TP02
-- select GP01 from AutocareHCB.dbo.CheckupPatients group by GP01 order by GP01
-- select GP02 from AutocareHCB.dbo.CheckupPatients group by GP02 order by GP02
-- select TP00 from AutocareHCB.dbo.CheckupPatients group by TP00 order by TP00
-- select TP07 from AutocareHCB.dbo.CheckupPatients group by TP07 order by TP07
-- select TP08 from AutocareHCB.dbo.CheckupPatients group by TP08 order by TP08
-- select C037 from AutocareHCB.dbo.CheckupPatients group by C037 order by C037
-- select C039 from AutocareHCB.dbo.CheckupPatients group by C039 order by C039
-- select C904 from AutocareHCB.dbo.CheckupPatients group by C904 order by C904
-- select C038 from AutocareHCB.dbo.CheckupPatients group by C038 order by C038
-- select C026 from AutocareHCB.dbo.CheckupPatients group by C026 order by C026
-- select C027 from AutocareHCB.dbo.CheckupPatients group by C027 order by C027
-- select C029 from AutocareHCB.dbo.CheckupPatients group by C029 order by C029
-- select C030 from AutocareHCB.dbo.CheckupPatients group by C030 order by C030
-- select C054 from AutocareHCB.dbo.CheckupPatients group by C054 order by C054
-- select C022 from AutocareHCB.dbo.CheckupPatients group by C022 order by C022
-- select C023 from AutocareHCB.dbo.CheckupPatients group by C023 order by C023
-- select C024 from AutocareHCB.dbo.CheckupPatients group by C024 order by C024
-- select C018 from AutocareHCB.dbo.CheckupPatients group by C018 order by C018
-- select U008 from AutocareHCB.dbo.CheckupPatients group by U008 order by U008
-- select C032 from AutocareHCB.dbo.CheckupPatients group by C032 order by C032
-- select E001 from AutocareHCB.dbo.CheckupPatients group by E001 order by E001
-- select I521 from AutocareHCB.dbo.CheckupPatients group by I521 order by I521
-- select I105 from AutocareHCB.dbo.CheckupPatients group by I105 order by I105
-- select I022 from AutocareHCB.dbo.CheckupPatients group by I022 order by I022
-- select I348 from AutocareHCB.dbo.CheckupPatients group by I348 order by I348
-- select I502 from AutocareHCB.dbo.CheckupPatients group by I502 order by I502
-- select I503 from AutocareHCB.dbo.CheckupPatients group by I503 order by I503
-- select I349 from AutocareHCB.dbo.CheckupPatients group by I349 order by I349


-- select per1_life_code1, count(*) from AutocareHCB.dbo.CheckupPatients where per1_life_code1 like '% %' group by per1_life_code1 order by per1_life_code1
-- select per1_life_code2, count(*) from AutocareHCB.dbo.CheckupPatients where per1_life_code2 like '% %' group by per1_life_code2 order by per1_life_code2
-- select per1_life_code3, count(*) from AutocareHCB.dbo.CheckupPatients where per1_life_code3 like '% %' group by per1_life_code3 order by per1_life_code3
-- select per1_life_code4, count(*) from AutocareHCB.dbo.HanshinTrainData where per1_life_code4 like '% %' group by per1_life_code4 order by per1_life_code4
-- select per1_kwa2, count(*) from AutocareHCB.dbo.HanshinTrainData where per1_kwa2 like '% %' group by per1_kwa2 order by per1_kwa2
-- select per1_kwa3, count(*) from AutocareHCB.dbo.HanshinTrainData where per1_kwa3 like '% %' group by per1_kwa3 order by per1_kwa3
-- select per1_kwa4, count(*) from AutocareHCB.dbo.HanshinTrainData where per1_kwa4 like '% %' group by per1_kwa4 order by per1_kwa4
-- select per1_kwa5, count(*) from AutocareHCB.dbo.HanshinTrainData where per1_kwa5 like '% %' group by per1_kwa5 order by per1_kwa5
-- select per1_kwa6, count(*) from AutocareHCB.dbo.HanshinTrainData where per1_kwa6 like '% %' group by per1_kwa6 order by per1_kwa6
-- select N1101011, count(*) from AutocareHCB.dbo.HanshinTrainData where N1101011 like '% %' group by N1101011 order by N1101011
-- select N1101021, count(*) from AutocareHCB.dbo.HanshinTrainData where N1101021 like '% %' group by N1101021 order by N1101021
-- select N1101012, count(*) from AutocareHCB.dbo.HanshinTrainData where N1101012 like '% %' group by N1101012 order by N1101012
-- select N1101022, count(*) from AutocareHCB.dbo.HanshinTrainData where N1101022 like '% %' group by N1101022 order by N1101022
-- select N1101013, count(*) from AutocareHCB.dbo.HanshinTrainData where N1101013 like '% %' group by N1101013 order by N1101013
-- select N1101023, count(*) from AutocareHCB.dbo.HanshinTrainData where N1101023 like '% %' group by N1101023 order by N1101023
-- select N1101014, count(*) from AutocareHCB.dbo.HanshinTrainData where N1101014 like '% %' group by N1101014 order by N1101014
-- select N1101024, count(*) from AutocareHCB.dbo.HanshinTrainData where N1101024 like '% %' group by N1101024 order by N1101024
-- select N1101015, count(*) from AutocareHCB.dbo.HanshinTrainData where N1101015 like '% %' group by N1101015 order by N1101015
-- select N1101025, count(*) from AutocareHCB.dbo.HanshinTrainData where N1101025 like '% %' group by N1101025 order by N1101025
-- select N1101016, count(*) from AutocareHCB.dbo.HanshinTrainData where N1101016 like '% %' group by N1101016 order by N1101016
-- select N1101026, count(*) from AutocareHCB.dbo.HanshinTrainData where N1101026 like '% %' group by N1101026 order by N1101026
-- select N1101017, count(*) from AutocareHCB.dbo.HanshinTrainData where N1101017 like '% %' group by N1101017 order by N1101017
-- select N1101027, count(*) from AutocareHCB.dbo.HanshinTrainData where N1101027 like '% %' group by N1101027 order by N1101027
-- select N1102011, count(*) from AutocareHCB.dbo.HanshinTrainData where N1102011 like '% %' group by N1102011 order by N1102011
-- select N1102012, count(*) from AutocareHCB.dbo.HanshinTrainData where N1102012 like '% %' group by N1102012 order by N1102012
-- select N1102013, count(*) from AutocareHCB.dbo.HanshinTrainData where N1102013 like '% %' group by N1102013 order by N1102013
-- select N1102014, count(*) from AutocareHCB.dbo.HanshinTrainData where N1102014 like '% %' group by N1102014 order by N1102014
-- select N1102015, count(*) from AutocareHCB.dbo.HanshinTrainData where N1102015 like '% %' group by N1102015 order by N1102015
-- select N110301, count(*) from AutocareHCB.dbo.HanshinTrainData where N110301 like '% %' group by N110301 order by N110301
-- select N110401, count(*) from AutocareHCB.dbo.HanshinTrainData where N110401 like '% %' group by N110401 order by N110401
-- select N110406, count(*) from AutocareHCB.dbo.HanshinTrainData where N110406 like '% %' group by N110406 order by N110406
-- select N110501, count(*) from AutocareHCB.dbo.HanshinTrainData where N110501 like '% %' group by N110501 order by N110501
-- select N110601, count(*) from AutocareHCB.dbo.HanshinTrainData where N110601 like '% %' group by N110601 order by N110601
-- select N110602, count(*) from AutocareHCB.dbo.HanshinTrainData where N110602 like '% %' group by N110602 order by N110602
-- select N110603, count(*) from AutocareHCB.dbo.HanshinTrainData where N110603 like '% %' group by N110603 order by N110603
-- select N110604, count(*) from AutocareHCB.dbo.HanshinTrainData where N110604 like '% %' group by N110604 order by N110604
-- select N110701, count(*) from AutocareHCB.dbo.HanshinTrainData where N110701 like '% %' group by N110701 order by N110701
-- select N110702, count(*) from AutocareHCB.dbo.HanshinTrainData where N110702 like '% %' group by N110702 order by N110702
-- select N110703, count(*) from AutocareHCB.dbo.HanshinTrainData where N110703 like '% %' group by N110703 order by N110703
-- select N110801, count(*) from AutocareHCB.dbo.HanshinTrainData where N110801 like '% %' group by N110801 order by N110801
-- select N110802, count(*) from AutocareHCB.dbo.HanshinTrainData where N110802 like '% %' group by N110802 order by N110802
-- select N110803, count(*) from AutocareHCB.dbo.HanshinTrainData where N110803 like '% %' group by N110803 order by N110803
-- select N110804, count(*) from AutocareHCB.dbo.HanshinTrainData where N110804 like '% %' group by N110804 order by N110804

-- select TP01 from AutocareHCB.dbo.HanshinTrainData where TP01 like '% %' group by TP01 order by TP01
-- select TP02 from AutocareHCB.dbo.HanshinTrainData where TP02 like '% %' group by TP02 order by TP02
-- select GP01 from AutocareHCB.dbo.HanshinTrainData where GP01 like '% %' group by GP01 order by GP01
-- select GP02 from AutocareHCB.dbo.HanshinTrainData where GP02 like '% %' group by GP02 order by GP02
-- select TP00 from AutocareHCB.dbo.HanshinTrainData where TP00 like '% %' group by TP00 order by TP00
-- select TP07 from AutocareHCB.dbo.HanshinTrainData where TP07 like '% %' group by TP07 order by TP07
-- select TP08 from AutocareHCB.dbo.HanshinTrainData where TP08 like '% %' group by TP08 order by TP08
-- select C037 from AutocareHCB.dbo.HanshinTrainData where C037 like '% %' group by C037 order by C037
-- select C039 from AutocareHCB.dbo.HanshinTrainData where C039 like '% %' group by C039 order by C039
-- select C904 from AutocareHCB.dbo.HanshinTrainData where C904 like '% %' group by C904 order by C904
-- select C038 from AutocareHCB.dbo.HanshinTrainData where C038 like '% %' group by C038 order by C038
-- select C026 from AutocareHCB.dbo.HanshinTrainData where C026 like '% %' group by C026 order by C026
-- select C027 from AutocareHCB.dbo.HanshinTrainData where C027 like '% %' group by C027 order by C027
-- select C029 from AutocareHCB.dbo.HanshinTrainData where C029 like '% %' group by C029 order by C029
-- select C030 from AutocareHCB.dbo.HanshinTrainData where C030 like '% %' group by C030 order by C030
-- select C054 from AutocareHCB.dbo.HanshinTrainData where C054 like '% %' group by C054 order by C054
-- select C022 from AutocareHCB.dbo.HanshinTrainData where C022 like '% %' group by C022 order by C022
-- select C023 from AutocareHCB.dbo.HanshinTrainData where C023 like '% %' group by C023 order by C023
-- select C024 from AutocareHCB.dbo.HanshinTrainData where C024 like '% %' group by C024 order by C024
-- select C018 from AutocareHCB.dbo.HanshinTrainData where C018 like '% %' group by C018 order by C018
-- select U008 from AutocareHCB.dbo.HanshinTrainData where U008 like '% %' group by U008 order by U008
-- select C032 from AutocareHCB.dbo.HanshinTrainData where C032 like '% %' group by C032 order by C032
-- select E001 from AutocareHCB.dbo.HanshinTrainData where E001 like '% %' group by E001 order by E001
-- select I521 from AutocareHCB.dbo.HanshinTrainData where I521 like '% %' group by I521 order by I521
-- select I105 from AutocareHCB.dbo.HanshinTrainData where I105 like '% %' group by I105 order by I105
-- select I022 from AutocareHCB.dbo.HanshinTrainData where I022 like '% %' group by I022 order by I022
-- select I348 from AutocareHCB.dbo.HanshinTrainData where I348 like '% %' group by I348 order by I348
-- select I502 from AutocareHCB.dbo.HanshinTrainData where I502 like '% %' group by I502 order by I502
-- select I503 from AutocareHCB.dbo.HanshinTrainData where I503 like '% %' group by I503 order by I503
-- select I349 from AutocareHCB.dbo.HanshinTrainData where I349 like '% %' group by I349 order by I349