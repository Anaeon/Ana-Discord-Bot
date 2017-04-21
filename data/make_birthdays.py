import shelve
import datetime

with shelve.open('birthdays', writeback = True) as db:
    db = {
        '154358313096577025' : datetime.datetime(1998, 1, 9),  # Jessie
        '206270882757214209' : datetime.datetime(1994, 1, 9),  # Cierra
        '108481713591582720' : datetime.datetime(1995, 1, 22),  # Brandon Pack
        '108485934147702784' : datetime.datetime(1994, 4, 23),  # Alex
        '84193605484314624' : datetime.datetime(1994, 6, 15),  # Brandon Clarke
        '108485649681657856' : datetime.datetime(1994, 7, 1),  # Michael
        '108478957115957248' : datetime.datetime(1993, 8, 16),  # EJ
        '108102797857148928' : datetime.datetime(1993, 8, 28),  # Travis
        '108479772081815552' : datetime.datetime(1992, 9, 23),  # Liz
        '259815606939811840' : datetime.datetime(1993, 10, 5),  # Krystal
        '108467075613216768': datetime.datetime(1991, 10, 26),  # Dustin
    }