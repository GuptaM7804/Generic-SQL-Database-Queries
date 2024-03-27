# Generic-SQL-Database-Queries

The goal is to write a console-based Python program that inputs commands from the user and outputs data from the CTA2 L daily ridership database. The program starts by outputting some basic stats retrieved from the database:
** Welcome to CTA L analysis app **
  General stats:
    # of stations: 147
    # of stops: 302
    # of ride entries: 1,070,894
    date range: 2001-01-01 - 2021-07-31
    Total ridership: 3,377,404,512
    Weekday ridership: 2,778,644,946 (82.27%)
    Saturday ridership: 330,165,977 (9.78%)
    Sunday/holiday ridership: 268,593,589 (7.95%)
  Please enter a command (1-9, x to exit):

The percentages shown in the last 3 outputs are computed using Python; all other data shown is retrieved / computed using SQL. After the stats, the program starts a command-loop, inputting string-based commands "1" - "9" or "x" to exit. All other inputs yield an error message.
