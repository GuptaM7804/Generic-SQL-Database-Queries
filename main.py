#
# header comment! Overview, name, etc.
#

import sqlite3
import matplotlib.pyplot as plt


##################################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    
    print("General stats:")

    # quite simple code to retrieve the number of stations in the table, we're basically counting every row (*)
    dbCursor.execute("Select count(*) From Stations;")
    row = dbCursor.fetchone()
    print("  # of stations:", row[0])

    # same as above but counting the number of stops
    dbCursor.execute("Select count(*) From Stops;")
    row = dbCursor.fetchone()
    print("  # of stops:", row[0])

    # same as above but counting the number of ride entries
    dbCursor.execute("Select count(*) From Ridership;")
    row = dbCursor.fetchone()
    print("  # of ride entries:", '{:,}'.format(row[0]))

    # Fetching the first and last date in the date entries in ridership table using sql functions min, max and strftime
    dbCursor.execute("Select min(strftime('%Y-%m-%d', Ride_Date)) from Ridership")
    row = dbCursor.fetchone()
    dbCursor.execute("Select max(strftime('%Y-%m-%d', Ride_Date)) from Ridership")
    row2 = dbCursor.fetchone()
    print("  date range:", row[0], "-", row2[0])

    # gets the total ridership by summing every ride entry
    dbCursor.execute("Select sum(Num_Riders) from Ridership;")
    row = dbCursor.fetchone()
    print("  Total ridership:", '{:,}'.format(row[0]))
    tot = row[0]

    # same as above but for weekdays using the identifier in the table
    dbCursor.execute("Select sum(Num_Riders) from Ridership where Type_of_Day = 'W';")
    row = dbCursor.fetchone()
    print("  Weekday ridership:", '{:,}'.format(row[0]), '({:0.2f}%)'.format(row[0]/tot * 100))

    # same as above but for Saturdays using the identifier in the table
    dbCursor.execute("Select sum(Num_Riders) from Ridership where Type_of_Day = 'A';")
    row = dbCursor.fetchone()
    print("  Saturday ridership:", '{:,}'.format(row[0]), '({:0.2f}%)'.format(row[0]/tot * 100))

    # same as above but for Sundays and holidays using the identifier in the table
    dbCursor.execute("Select sum(Num_Riders) from Ridership where Type_of_Day = 'U';")
    row = dbCursor.fetchone()
    print("  Sunday/holiday ridership:", '{:,}'.format(row[0]), '({:0.2f}%)'.format(row[0]/tot * 100))
    print("\n")
    # close the cursor after each function
    dbCursor.close()

#
##
# function one is the helper function for the command 1
# it outputs the station ID and station name for 1 or all stations that are 'like' the user input
def one(dbCursor, name):
  # the question mark is used as a parameter sort of, any information put in the second part of the cursor will fill this question mark and execute as a normal sql query
  sql = "Select Station_ID, Station_Name from Stations where Station_Name like ? group by Station_Name order by Station_Name asc"
  dbCursor.execute(sql, [name])
  row = dbCursor.fetchall()
  if len(row) == 0:
    print("**No stations found...")
    return
  
  for r in row:
    print(r[0], ":", r[1])

#
##
# function two is the helper function for command 2
# it outputs the station name and the amount of riders that have travelled to it
def two(dbCursor):
  # using join on the station id, ridership and station tables re connected and the station names and the total number of riders that have gone through the station is retrieved and ordered in ascending order by station name
  sql = "select Station_Name, sum(Num_Riders) from Ridership join Stations on (Stations.Station_ID=Ridership.Station_ID) group by Station_Name order by Station_Name asc"

  # helper sql query is used to determine the total number of riders in every station
  sql_Helper = "select sum(Num_Riders) from Ridership"

  dbCursor.execute(sql_Helper)
  grand_total = dbCursor.fetchone() # the total is stored in this variable

  dbCursor.execute(sql)
  row = dbCursor.fetchall()

  for r in row:
    print(r[0], ":", '{:,}'.format(r[1]), '({:0.2f}%)'.format(r[1]/grand_total[0] * 100))

#
##
# function three/four serves as a helper for both commands 3 and 4 as the two commands are the same but in the opposite direction
# order is the variable that determines descending or ascending order
def three_four(dbCursor, order):
  # the string is concatenated with order
  sql = "select Station_Name, sum(Num_Riders) from Ridership join Stations on (Stations.Station_ID=Ridership.Station_ID) group by Station_Name order by sum(Num_Riders) "+order+" limit 10"
  
  sql_Helper = "select sum(Num_Riders) from Ridership"

  dbCursor.execute(sql_Helper)
  grand_total = dbCursor.fetchone()

  dbCursor.execute(sql)
  row = dbCursor.fetchall()

  for r in row:
    print(r[0], ":", '{:,}'.format(r[1]), '({:0.2f}%)'.format(r[1]/grand_total[0] * 100))

#
##
# function five is the helper for command five
# it outputs all the stops associated with the color input by the user
def five(dbCursor, color):
  # the color table is joined with stop details table using line ID, which is joined with stops table using stop ID, which is joined with stations table using station ID || The returned data is ordered by the stop name in ascending order
  sql = "select Stop_Name, Direction, ADA, Color from Lines join StopDetails on (StopDetails.Line_ID = Lines.Line_ID) join Stops on (Stops.Stop_ID = StopDetails.Stop_ID) join Stations on (Stations.Station_ID = Stops.Station_ID) where Color like ? order by Stop_Name asc"
  dbCursor.execute(sql, [color])
  row = dbCursor.fetchall()
  
  if len(row) == 0:
    print("**No such line...")
    return
  
  for r in row:
    str = r[0] + " : Direction = " + r[1] + " (accessible? "
    if r[2] == 1:
      str+="yes)"
    else:
      str+="no)"
    print(str)
    
#
##
# function six is the helper functino for command 6
# it outputs the Ridership by month-> total number of riders per month in all the years combined, it can also output a graph as per the users request
def six(dbCursor):
  # the query uses strftime for the date and sums the riders for the months, it is grouped by the months and ordered in ascending order
  sql = "select strftime('%m',Ride_Date), SUM(Num_Riders) from Ridership group by strftime('%m',Ride_Date) order by strftime('%m',Ride_Date) asc"
  dbCursor.execute(sql)
  row = dbCursor.fetchall()

  for r in row:
    print(r[0], ":", '{:,}'.format(r[1]))
  print("\n")
  inp = input("Plot? (y/n)")
  if inp != 'y':
    return

  # x and y are lists that will contain all the values of months and total riders for that month
  x = []
  y = []
  for r in row:
    x.append(r[0])
    y.append(int(r[1]))

  plt.xlabel("month")
  plt.ylabel("number of riders(x*10^8)")
  plt.title("monthly ridership")

  # using plot() and show(), the ouput graph is created
  plt.plot(x, y)
  plt.show()
  
#
##
# function seven is the helper function for command 7
# the output of this function is very similar to function six/command 6, however, this function returns the total ridership per year instead of month
def seven(dbCursor):
  sql = "select strftime('%Y',Ride_Date), SUM(Num_Riders) from Ridership group by strftime('%Y',Ride_Date) order by strftime('%Y',Ride_Date) asc"
  dbCursor.execute(sql)
  row = dbCursor.fetchall()

  for r in row:
    print(r[0], ":", '{:,}'.format(r[1]))
  print("\n")
  inp = input("Plot? (y/n)")
  if inp != 'y':
    return

  x = []
  y = []
  for r in row:
    x.append(r[0][2:])
    y.append(int(r[1]))

  plt.xlabel("year")
  plt.ylabel("number of riders(x*10^8)")
  plt.title("yearly ridership")

  plt.plot(x, y)
  plt.show()

#
##
# function eight is the helper function for command 8
# it outputs the first 5 and last 5 days and the ridership for that day for 2 user input stations during the user input year
# as per the request of the user, this information can also be graphed
def eight(dbCursor, year):
  station1 = input("Enter station 1 (wildcards _ and %): ")

  # query to check whether station name given is actually in the table or not
  errorcheck = "select count(distinct Station_Name) from Stations where Station_Name like ?"
  
  # query tht joins ridership to stations on station ID to retrieve the date and station name for user inputted station in the user inputted year, the two ? queries are for the year and the station anme respectively
  sql = "select Station_Name, strftime('%Y-%m-%d',Ride_Date), Num_Riders from Ridership join Stations on Stations.Station_ID = Ridership.Station_ID where strftime('%Y', Ride_date) like ? and Station_Name like ? group by strftime('%Y-%m-%d',Ride_Date) order by strftime('%Y-%m-%d',Ride_Date) asc"

  # error check for station 1, and...
  dbCursor.execute(errorcheck, [station1])
  error1 = dbCursor.fetchall()
  if error1[0][0] == 0:
    print("**No station found...") # if station not found
    return
  elif error1[0][0] >= 2:
    print("**Multiple stations found... ") # if multiple stations found
    return
  
  print("\n")

  # execute the sql statement for function for station 1 data
  dbCursor.execute(sql, [year, station1])
  row = dbCursor.fetchall()

  station2 = input("Enter station 2 (wildcards _ and %): ")

  # errorcheck for station 2 same as above
  dbCursor.execute(errorcheck, [station2])
  error2 = dbCursor.fetchall()
  if error2[0][0] == 0:
    print("**No station found...")
    return
  elif error2[0][0] >= 2:
    print("**Multiple stations found... ")
    return

  # sql statement for function for the station 2 data
  dbCursor.execute(sql, [year, station2])
  row2 = dbCursor.fetchall()

  # get the station ID of the stations, cannot get in previous query since it is an ambigous request as it is used for a join on tables
  sql = "select Station_ID from Stations where Station_Name like ?"
  dbCursor.execute(sql, [station1])
  name = dbCursor.fetchall()
  sql = "select Station_ID from Stations where Station_Name like ?"
  dbCursor.execute(sql, [station2])
  name2 = dbCursor.fetchall()

  print("Station 1:", name[0][0], row[0][0])
  for x in range(0,5):
    print(row[x][1], row[x][2])
  for x in range(-5,0):
    print(row[x][1], row[x][2])
  print("Station 2:", name2[0][0], row2[0][0])
  for x in range(0,5):
    print(row2[x][1], row2[x][2])
  for x in range(-5,0):
    print(row2[x][1], row2[x][2])
  print("\n")
  inp = input("Plot? (y/n)")
  if inp != 'y':
    return

  # similar to the plots above but x and y lists for station 1 and x2 and y2 lists for station 2
  x = []
  x2 = []
  y = []
  y2 = []

  # adding numbers instead of the date to keep things clean and concise on the graph
  j = 1
  for r in row:
    x.append(j)
    y.append(int(r[2]))
    j += 1

  j = 1
  for r in row2:
    x2.append(j)
    y2.append(int(r[2]))
    j += 1
    
  plt.xlabel("day")
  plt.ylabel("number of riders")
  str = "riders each day of "+year
  plt.title(str)

  # label the lines with their respective station names and place the legend at the top right
  plt.plot(x, y, label=row[0][0])
  plt.plot(x2,y2, label=row2[0][0])
  plt.legend(loc='upper right')
  plt.show()
    
#
##
# function nine is the helper function for command 9
# it outputs all the stations associated with a line color and if requested, graphs this data on a map as well using the longitude and latitude
def nine(dbCursor, color):

  # query to get the station name and latitude and longitude of the stations associated with the given color. The lines table is onnected to stop details on Line ID-> connected to stops on stop ID-> connected to stations on station ID
  sql = "select distinct Station_Name, Latitude, Longitude from Lines join StopDetails on (StopDetails.Line_ID = Lines.Line_ID) join Stops on (Stops.Stop_ID = StopDetails.Stop_ID) join Stations on (Stations.Station_ID = Stops.Station_ID) where Color like ? order by Station_Name asc"

  dbCursor.execute(sql, [color])
  row = dbCursor.fetchall()

  if len(row) == 0:
    print("**No such line...")
    return
    
  for r in row:
    print(r[0], ":", "({:,}, {:,})".format(r[1], r[2]))
  print("\n")
  inp = input("Plot? (y/n)")
  if inp != 'y':
    return

  # similar to above plots, longitude in x, latitude in y
  x = []
  y = []

  for r in row:
    x.append(r[2])
    y.append(r[1])
  # get the image
  image = plt.imread("chicago.png")
  xydims = [-87.9277, -87.5569, 41.7012, 42.0868] # area covered by the map
  plt.imshow(image, extent=xydims)
  plt.title(color + " line")
  # have to encode this separately since it is the only line with extra bits in the name
  if (color.lower() == "purple-express"):
    color="Purple"
  plt.plot(x, y, "o", c=color)
  # annotating each (x,y) coordinate with its station name
  for r in row: 
    plt.annotate(r[0], (r[2], r[1]))
  plt.xlim([-87.9277, -87.5569])
  plt.ylim([41.7012, 42.0868])
  # 4 ticks for x-axis
  plt.locator_params(axis='x', nbins=4)
  plt.show()
  
#
##
# function that puts all the commands together, essentially the main menu
# it contains a while loop that checks whether a command to execute or an exit command is given, loops indefinitely till the exit command is given, if neither functional command nor exit command is given then an error statement is outputted and the loop starts again
def commands(dbConn):
  dbCursor = dbConn.cursor()
  cmd = input("Please enter a command (1-9, x to exit): ")
  while cmd != "x":
    if cmd == "1":
      print("\n")
      name = input("Enter partial station name (wildcards _ and %): ")
      one(dbCursor, name)
      print("\n")
    
    elif cmd == "2":
      print("** ridership all stations **")
      two(dbCursor)
      print("\n")
      
    elif cmd == "3":
      print("** top-10 stations **")
      three_four(dbCursor, "desc")
      print("\n")
    
    elif cmd == "4":
      print("** least-10 stations ** ")
      three_four(dbCursor, "asc")
      print("\n")
    
    elif cmd == "5":
      print("\n")
      color = input("Enter a line color (e.g. Red or Yellow): ")
      five(dbCursor, color)
      print("\n")
      
    elif cmd == "6":
      print("** ridership by month **")
      six(dbCursor)
      print("\n")
      
    elif cmd == "7":
      print("** ridership by year **")
      seven(dbCursor)
      print("\n")
      
    elif cmd == "8":
      print("\n")
      year = input("Year to compare against? ")
      print("\n")
      eight(dbCursor, year)
      print("\n")
      
    elif cmd == "9":
      print("\n")
      color = input("Enter a line color (e.g. Red or Yellow): ")
      nine(dbCursor, color)
      print("\n")
    else:
      print("**Error, unknown command, try again...")
      print("\n")
    cmd = input("Please enter a command (1-9, x to exit): ")
  dbCursor.close()
##################################################################  
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

# general stats
print_stats(dbConn)

# main menu
commands(dbConn)

# close the connection once program is finished
dbConn.close()

#
# done
#