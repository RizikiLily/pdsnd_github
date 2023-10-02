import pandas as pd
import numpy as np
import time
#Function to prompt user to enter the name of the city
def get_city():
    city_list = ['chicago', 'new york city', 'washington']
    while True:
        city = input("Enter the name of a city. Options are Chicago, New York City and Washington: ")
        if not city.replace(" ", "").isalpha():
            print('Please enter only letters')
            continue
        else:
            city = city.lower()
            if city not in city_list:
                print('{}  not an option! Choose one of the options'.format(city))
                continue
            else:
                print('You chose {}'.format(city.title()))   
                break
    return city

#Function to prompt user to enter the day
def get_day():
    day_list = ['sunday','monday', 'tuesday','wednesday', 'thursday', 'friday','saturday']
    day = []
    while True:
        day_choice = input('Enter a day(1-7) or all: ')
        
        
        if day_choice == 'all':
            for d in day_list:
                day.append(d.title())
            break
        else:        
            try:
                day_choice = int(day_choice)
                if day_choice < 1 or day_choice > 7:
                    print('Enter numbers between 1 and 7')
                    continue

                day_chosen = day_list[day_choice - 1]
            
                if day_chosen.title() not in day:
                    day.append(day_chosen.title())
                    more_picks = input("Do you want to filter for another day? (y/n): " )
                    if more_picks.lower() != 'y':
                        break
                    else:
                        continue
                else:
                    print('Day already chosen. Pick another')
            except ValueError:
                print('Wrong input! Enter a number (1-7)')
          
                
    print(day)
    return day

#Function to display raw data
def display_data():
    city = get_city()
    month =get_month()
    day = get_day()
    df = load_data(city, month, day)
    print('\n***Displaying 5 rows of data***\n')
    print(df.head(5))
    start_index = 5
    while True:
        ans = input('\nDo you want to display the next 5 rows? y/n: ')
        
        if ans.lower() == 'y':
            if start_index < len(df):
                end_index = start_index + 5
                print(df.iloc[start_index:end_index])
                start_index += end_index
            else:
                print('\nNo more rows to print')
                break
        else:
            break

#function to load the .csv file
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def load_data(city, month, day):
   
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month 
    df['week_day'] = df['Start Time'] .dt.day_name()
    df['route'] = df['Start Station'] + ' - ' + df['End Station']
    df = df[df['month'].isin(month)]
    df = df[df['week_day'].isin(day)]

    #print(df.head(20))
    #print(df.columns)
    #print('%%%%Trip duration%%%%')
    #print(df['Trip Duration'].dtype)
    #print(f"month count is {df['month'].value_counts}")
    return df

#Function to prompt user to enter the month
def get_month():
    month_list = [1, 2, 3, 4, 5, 6]
    month = []
    while True:
        month_choice = input('Enter the month(1-6) or all: ')
        
        
        if month_choice == 'all':
            for mon in month_list:
                month.append(mon)
            break
        else:        
            try:
                month_choice = int(month_choice)
            except:
                print('Wrong input! Enter 1-6')
                continue
            if month_choice < 1 or month_choice > 6:
                print('Enter numbers between 1 and 6')
                continue
            #month_chosen = month_list[month_choice - 1]
            if month_choice not in month:
                month.append(month_choice)
            else:
                print('Month already chosen. Pick another')
                continue
            
            more_picks = input('Do you to filter for another month? y/n:' )
            if more_picks.lower() == 'y':
                continue
            else:
                break
                
    #print(month)
    return month

#function to compute statistical information
def station_stats(df):
    """Displays statistics on the most popular stations and trips"""
    print('\n***Calculating the most popular stations and trips***\n')
    start_time = time.time()

    #Display the most commonly used start station
    start_mode = df['Start Station'].mode()
    if start_mode is not None and not start_mode.empty:
        most_common_start = start_mode.iloc[0]
        print(f"The most common start station is: {most_common_start}")
    else:
        print("There is no unique mode in the 'Start Station' column.")

    #Display the most commonly used end station
    end_mode = df['End Station'].mode()
    if end_mode is not None and not end_mode.empty:
        most_common_end = end_mode.iloc[0]
        print(f"The most common end station is: {most_common_end}")
    else:
        print("There is no unique mode in the 'End Station' column.")

     #Display the most commonly used start station
    route_mode = df['route'].mode()
    if route_mode is not None and not route_mode.empty:
        most_common_route = route_mode.iloc[0]
        print(f"The most common route  is: {most_common_route}")
    else:
        print("There is no unique mode in the 'route' column.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n***Calculating The Most Frequent Times of Travel***\n')
    start_time = time.time()

    # display the most common month
   
    
    mode_month= df['month'].mode()
 

    # Check if there is a mode

    if mode_month is not None and not mode_month.empty:
        most_common_month = mode_month.iloc[0]
        print(f"The most common month is: {most_common_month}")
    else:
        print("There is no unique mode in the 'month' column.")

    #display the most common day of the week
    mode_day = df['week_day'].mode()
    if mode_day is not None and not mode_day.empty:
        most_common_day = mode_day.iloc[0]
        print(f"The most common day of the week is: {most_common_day}")
    else:
        print("There is no unique mode in the 'week_day' column.")

    #display the mpst common start hour
    mode_hour = df['Start Time'].dt.hour.mode()
    if mode_hour is not None and not mode_hour.empty:
        most_common_hour = mode_hour.iloc[0]
        print(f"The most common time of the day is: {most_common_hour}")
    else:
        print("There is no unique mode in the 'Start Time' column.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n***Calculating Trip Duration***\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    hours = total // 3600
    rem_secs = total % 3600
    mins = rem_secs // 60
    secs = mins % 60
    print(f'The total travel time is {hours} hrs, {mins} mins and {secs}s')

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    mean_hours = mean_time // 3600
    mean_rem_secs = mean_time % 3600
    mean_mins = rem_secs // 60
    mean_secs = mins % 60
    print(f'The mean travel time is {mean_hours} hrs, {mean_mins} mins and {mean_secs}s')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\n***Calculating User Stats***\n')
    start_time = time.time()

    #Display counts of user types
    try:
        print('\n**The types of users are indicated below**\n')
        print(df['User Type'].value_counts())
    except:
        print(f"{city.title()} has no 'User Type' data\n")


    #Display counts of gender
    try:
        print(f"\n**The counts of gender is as below**\n {df['Gender'].value_counts()}")
     
    except:
        print(f"\n{city.title()} has no 'Gender' data\n")

    #Display earliest, most recent, and most common year of birth
    try:
        print(f"\nThe earliest birth year is {df['Birth Year'].min()}\n")
        print(f"The most recent birth year is {df['Birth Year'].max()}\n")
        print(f"The most common birth year is {df['Birth Year'].mode()[0]}\n")
    except:
        print(f"{city.title()} has no 'Birth Year' data!\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)



def main():
    while True:
        action = input('Enter 1 to view raw data or 2 to view decriptive statistics: ')
        if action == '2':
           
            city = get_city()
            month = get_month()
            day = get_day()
            df = load_data(city, month, day)
            time_stats(df)
            station_stats(df)
            user_stats(df,city)
            #print(city, month, day)

        elif action == '1':
               #print('You are about to view raw data')
              display_data()
        else:
                print('Invalid input')

        answer = input('Would you like to restart? Enter y/n: ')
        if answer.lower() != 'y':
            break
        else:
            continue


main()