import time
import datetime
import pandas as pd

pd.set_option('display.max_columns',200)

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

    city_choice = CITY_DATA.keys()
    city = input("Please enter the name of the city you would like to analyze. You can choose Chicago, New York City or Washington: ").lower()
    while city.lower() not in city_choice :
        city = input("Please enter a valid city name: ").lower()

    # get user input for month (all, january, february, ... , june)

    month_choice= ['All','January', 'February', 'March', 'April', 'May', 'June']
    month = input('Please enter the name of the month to filter by, or "all" to apply no month filter:').lower().capitalize()
    while month not in month_choice :
        month = input("Please enter a valid month name, or all: ").lower().capitalize()

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day_choice = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = input('Please enter the day of week to filter by, or "all" to apply no day filter:').lower()
    while day not in day_choice :
        day = input("Please enter a valid day of a week, or all: ").lower()


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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df=pd.read_csv(CITY_DATA[city])
        
    # Concert the Start Time column to datetime
    df['Start Time']=pd.to_datetime(df['Start Time'])
        
    
    # extract month and day of week from Start Time to create new columns
    df['month']=df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.dayofweek
            
    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['blank','January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month)
            
            
        # filter by month to create the new dataframe
        df= df.loc[df['month']==month]
                
                
    # filter by day of the week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'friday', 'staruday', 'sunday']
        day = days.index(day)
        df= df.loc[df['day_of_week']==day]
            

    


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    try:

        months = ['blank','January', 'February', 'March', 'April', 'May', 'June']
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'friday']

        # convert the Start Time column to datetime

        df["Start Time"]=pd.to_datetime(df["Start Time"])
        
        # display the most common month

        popular_month = df['month'].value_counts().idxmax()
        popular_month = months[popular_month]


        # display the most common day of week
        df['day_of_week'] = df['Start Time'].dt.dayofweek
        popular_day = df['day_of_week'].value_counts().idxmax()
        popular_day = days[popular_day]


        # display the most common start hour
        df['hour']=df["Start Time"].dt.hour
        popular_hour=df['hour'].value_counts().idxmax()



        print("\nThe most popular month is ", popular_month)
        print("\nThe most popular day of week  is ", popular_day)
        print("\nThe most popular hour is ", popular_hour)
        print('-'*40)
    except ValueError:
        print("Sorry, no data for chosen month")


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')

    try:

        # display most commonly used start station

        start_station=df['Start Station'].value_counts().idxmax()


        # display most commonly used end station

        end_station=df['End Station'].value_counts().idxmax()


        # display most frequent combination of start station and end station trip

        df['Start + End']= df['Start Station'] + ' and ' + df['End Station']
        combination_stations = df['Start + End'].value_counts().idxmax()


        print("\nThe most commonly used start station is ", start_station)
        print("\nThe most commonly used end station is ", end_station)
        print("\nThe most commonly used combination  is ", combination_stations)
        print('-'*40)
    except ValueError:
        print("Sorry, no data available for the chosen month")


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    try:

        # display total travel time
        sec_total=df['Trip Duration'].sum()
        total_duration = str(datetime.timedelta(seconds=int(sec_total)))
        
        # display mean travel time
        sec=df['Trip Duration'].mean()
        mean_duration = str(datetime.timedelta(seconds=int(sec)))

        print("\nTotal travel duration is ", total_duration)
        print("\nMean travel duration is  ", mean_duration)
    except ValueError:
        print("Sorry, no data available for the chosen month")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:

        # Display counts of user types
        user_types=df['User Type'].value_counts()


        # Display counts of gender
        gender_counts=df['Gender'].value_counts()


        # Display earliest, most recent, and most common year of birth

        youngest = int(df['Birth Year'].max())
        oldest = int(df['Birth Year'].min())
        common = int(df['Birth Year'].mode())

        print("\nThe youngest user is born in ", youngest)
        print("\nThe oldest user is born in ", oldest)
        print("\nThe common user is born in ", common)
    except:
        print("No available user data for Washington")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
    

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data = input('\nWould you like to see the raw data? Enter yes or no.\n')
        while raw_data.lower() not in ['yes','no'] :
            raw_data = input("Please enter 'yes' or 'no': ")

        i=0
        j=5
        while raw_data.lower() != 'no':
            print(df.iloc[i:j])
            i=j
            j = j+ 5
            raw_data = input('\nWould you like to see more raw data? Enter yes or no.\n')

        
        
        
    

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
