import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs    
    while True :
        city = input("Which city's data would you like to see Chichago, New York City or Washington?: ").lower()
        if city not in ['chicago', 'new york city','washington']:
            print("Please enter a valid city in Chicago, New York City or Washington")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:        
        month = input("Which month's data would you like to see January, February, March, April, May, June or All  :").lower()
        if month not in ['january','february','march','april','may','june','all']:
            print("Please enter a valid mont in January, February, March, April, May, June or All")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True :        
        day = input("Which day's data would you like to see Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or All: ").lower()
        if day not in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']:
            print("Please enter a valid day in Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or All")
            continue
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    
    # extract month,day,hour from the Start Time column to create an hour column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    # display the most common month
    popular_month = df['month'].mode()[0]
    print("According to filters, the most popular month is : {}".format(popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("According to filters, the most popular day is : {}".format(popular_day))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("According to filters, the most popular hour is : {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("According to filters, most commonly used start station is : {}".format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("According to filters, most commonly used end station is : {}".format(common_end_station))

    # display most frequent combination of start station and end station trip
    combination_station_number = df.groupby(['Start Station', 'End Station'])['Start Station'].count().max()
    combination_station = df.groupby(['Start Station', 'End Station'])['Start Station'].count().idxmax()
    print("According to filters, most frequent combination of start station and end station trip is :{}".format(combination_station))
    print("According to filters, most frequent combination of start station and end station trip number is :{}".format(combination_station_number))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("According to filters, total travel time : {}".format(total_travel_time))

    # display mean travel time
    mean_travel_time =  df['Trip Duration'].mean()
    print("According to filters, mean travel time : {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print("According to filters, counts of user types {}".format(user_types_count))

    # Display counts of gender
    if city in ['chicago','new york city']:
        gender_count = df['Gender'].value_counts()
        print("According to filters, counts of gender {}".format(gender_count))
    else:
        print("There is no gender data in washington!")

    # Display earliest, most recent, and most common year of birth
    if city in ['chicago','new york city']:
        date_of_birth = df["Birth Year"]
        earliest_dob = date_of_birth.min()
        most_recent_dob = date_of_birth.max()
        most_common_dob = date_of_birth.mode()[0] 
        print("According to filters, earliest year of birth is : {}".format(earliest_dob))
        print("According to filters, most recent year of birth is : {}".format(most_recent_dob))
        print("According to filters, most common year of birth is : {}".format(most_common_dob))
    else:
        print("There is no year of birth data in washington!")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    counter = 10
    loop_value = True
    while loop_value == True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        
        show_data = input('\nWould you like to see first 5 row data Enter yes or no.\n')
        if show_data.lower() == 'yes' :
            print(df.head())                     
            while True:
                add_data = input('\nWould you like to see 5 more row data Enter yes or no.\n')                
                if add_data.lower() == 'yes' :                    
                    print(df.head(counter))
                    counter +=5
                    continue
                else:
                    restart = input('\nWould you like to restart? Enter yes or no.\n')
                    if restart.lower() != 'yes':
                        loop_value = False
                        break
                    else:
                        counter = 10                        
                        break
        else:            
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break


if __name__ == "__main__":
	main()
