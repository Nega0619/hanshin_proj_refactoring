        select top(100) percent_01, count(*) from AutocareHCB.dbo.Patient group by percent_01 order by percent_01 desc
        select top(100) percent_02, count(*) from AutocareHCB.dbo.Patient group by percent_02 order by percent_02 desc
        select top(100) percent_03, count(*) from AutocareHCB.dbo.Patient group by percent_03 order by percent_03 desc
        select top(100) percent_04, count(*) from AutocareHCB.dbo.Patient group by percent_04 order by percent_04 desc
        select top(100) percent_05, count(*) from AutocareHCB.dbo.Patient group by percent_05 order by percent_05 desc
        select top(100) percent_06, count(*) from AutocareHCB.dbo.Patient group by percent_06 order by percent_06 desc
        select top(100) percent_07, count(*) from AutocareHCB.dbo.Patient group by percent_07 order by percent_07 desc
        select top(100) percent_08, count(*) from AutocareHCB.dbo.Patient group by percent_08 order by percent_08 desc
        select top(100) percent_09, count(*) from AutocareHCB.dbo.Patient group by percent_09 order by percent_09 desc
        select top(100) percent_10, count(*) from AutocareHCB.dbo.Patient group by percent_10 order by percent_10 desc
        select top(100) percent_11, count(*) from AutocareHCB.dbo.Patient group by percent_11 order by percent_11 desc
        select top(100) percent_12, count(*) from AutocareHCB.dbo.Patient group by percent_12 order by percent_12 desc
        select top(100) percent_13, count(*) from AutocareHCB.dbo.Patient group by percent_13 order by percent_13 desc
        select top(100) percent_14, count(*) from AutocareHCB.dbo.Patient group by percent_14 order by percent_14 desc

bash && conda activate hanshin
pyinstaller -F -n Initiator main_Initiator.py && pyinstaller -F -n APIServer main_APIServer.py && pyinstaller -F -n AutoUpdater main_AutoUpdater.py && pyinstaller -F -n PDFMaker main_PDFMaker.py