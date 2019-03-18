command={
    'GoHome': r"schtasks /Create /sc weekly /d MON,TUE,WED,THU,FRI /tn 'GoHome' /tr 'py c:\Users\swhang\Documents\Tasks\GoHome.py /st 16:55",
    'GoLunch':r"schtasks /Create /sc weekly /d MON,TUE,WED,THU,FRI /tn 'Lunch' /tr 'py c:\Users\swhang\Documents\Tasks\GoLunch.py /st 11:55",
    'TimeSheet': r"schtasks /Create /sc weekly /d FRI /tn 'TimeSheet' /tr 'py c:\Users\swhang\Documents\Tasks\TimeSheet.py /st 16:30",
    'Beep': "python -c \"print('\a')\"",
    'CMD': "start cmd.exe /c \"mode con: cols=30 lines=1 && set /p acknowledge= 'Time to go home, Sangwoo'",
    }
