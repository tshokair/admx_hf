"""
    get_dates.py Author Sami Lewis 03/02/16
    This function allows the user to find all folders of data within a certain date range.
    Relies in shell script to generate updated list of available folders.
"""
import subprocess

def get_available_dates():
    # Instructions to the user
    print("Choose a range of dates to see available uploads within that range.")
    print("All dates must be entered in YYYYMMDD format. For January 01 2016, input 20160101")
    # Get date for beginnning of range
    while True:
        try:
            start = int(input("Enter range start date: "))
            if len(str(start)) !=8:
                print("This is not a complete date. Please use YYYYMMDD format.")
                continue
            else:
                break
        except ValueError:
            print("Invalid input. Date must be entered in YYYYMMDD format using only numbers.")

    # Get date for end of range
    while True:
        try:
            end = int(input("Enter range end date: "))
            if len(str(start)) !=8:
                print("This is not a complete date. Please use YYYYMMDD format.")
                continue
            else:
                break
        except ValueError:
            print("Invalid input. Date must be entered in YYYYMMDD format using only numbers.")
    
    # Run shell script to generate updated list of dates.
    subprocess.call(["./findFolders.sh"])

    # Read lines of text file generated by shell script
    F = open("./dates_avail.txt","r")
    dates = F.read().splitlines()
    dates = list(map(int,dates))
 
    # Go through list of available dates and confirm whether they're in our desired range
    available = []
    for folder in dates:
        if start <= folder <= end:
            available.append(folder)
        else:
            pass
    
    # Print list of available dates
    if len(available) == 0:
        print("There are no available runs in the specified range.")
    else:
        print("The available runs in the specified range are:")
        for r in available:
            print(r)
    
    # Return list of dates

get_available_dates()
