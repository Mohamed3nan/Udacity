import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city_list = ["chicago", "new york city", "washington"]
    month_list = ["all", "jan", "feb", "mar", "apr", "may", "jun"]
    day_list = ["all", "saturday", "sunday", "monday",
                "tuesday", "wednesday", "thursday", "friday"]

    city = ""
    month = ""
    day = ""

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in city_list:
        city = input("Please specify name of the city to analyze from these choices \n"
                     "(chicago - new york city - washington)\n"
                     "Input: ").lower()
        if city in city_list:
            print("Thank you for choosing a city! {} \n".format(city))

    # get user input for month (all, january, february, ... , june)
    while month[0:3] not in month_list:
        month = input("Please specify name of the month to filter by, or 'all' to apply no month filter \n"
                      "(all - jan - feb - mar - apr - may - jun)\n"
                      "Input: ").lower()
        month = month[0:3]
        if month in month_list:
            print("Thank you for choosing a month! {} \n".format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in day_list:
        day = input("Please specify name of the day of week to filter by, or 'all' to apply no day filter \n"
                    "(all - saturday - sunday - monday - tuesday - wednesday - thursday - friday)\n"
                    "Input: ").lower()
        day_list_small = [day[0:3] for day in day_list]
        if day in day_list:
            print("Thank you for choosing a day! {} \n".format(day))
            break
        elif day[0:3] in day_list_small:
            day = day_list[day_list_small.index(day[0:3])]
            print("Thank you for choosing a day! {} \n".format(day))
        else:
            print("{} Not a valid input, try again \n".format(day))

    print("+" * 40)
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
    if city == "chicago":
        df = pd.read_csv("chicago.csv")
    elif city == "new york city":
        df = pd.read_csv("new_york_city.csv")
    else:
        df = pd.read_csv("washington.csv")

    # convert the Time columns to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month and day of week to create new columns
    df["Month Number"] = df["Start Time"].dt.month
    df["Day of Week"] = df["Start Time"].dt.day_name()

    # filter by month if applicable
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ["all", "jan", "feb", "mar", "apr", "may", "jun"]
        month = months.index(month)

        # filter by month to create the new dataframe
        df = df[df["Month Number"] == month]

    # filter by day of week if applicable
    if day != "all":
        # filter by day of week to create the new dataframe
        df = df[df["Day of Week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df["Month Number"] = df["Start Time"].dt.month
    most_common_month = df[["Month Number"]].mode()["Month Number"][0]
    print("The most common month :  " + str(most_common_month))

    # display the most common day of week
    df["Day of Week"] = df["Start Time"].dt.day_name()
    most_common_day = df[["Day of Week"]].mode()["Day of Week"][0]
    print("The most common day :  " + str(most_common_day))

    # display the most common start hour
    df["Hour"] = df['Start Time'].dt.hour
    most_common_hour = df[["Hour"]].mode()["Hour"][0]
    print("The most common hour :  " + str(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("+" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df[["Start Station"]].mode()[
        "Start Station"][0]
    print("The most commonly used start station :  " +
          str(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df[["End Station"]].mode()["End Station"][0]
    print("The most commonly used end station :  " + str(most_common_end_station))

    # display most frequent combination of start station and end station trip
    df["Start To End Station"] = df["Start Station"] + " " + df["End Station"]
    most_freq_com = df[["Start To End Station"]
                       ].mode()["Start To End Station"][0]
    print("The most frequent combination :  " + str(most_freq_com))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("+" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df[["Trip Duration"]].sum()[0]
    print("Total travel time :  " + str(total_travel_time))

    # display mean travel time
    mean_travel_time = df[["Trip Duration"]].mean()[0]
    print("Mean travel time :  " + str(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("+" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df[["User Type"]].value_counts()
    print("Counts of user types :  \n" + str(count_user_types))

    # Display counts of gender
    gender_count = df[["Gender"]].value_counts()
    print("Counts of gender :  \n" + str(gender_count))

    # Display earliest, most recent, and most common year of birth
    earliest_birth = df[["Birth Year"]].min()[0]
    recent_birth = df[["Birth Year"]].max()[0]
    common_birth = df[["Birth Year"]].mode()["Birth Year"][0]

    print("Earliest year of birth :  \n" + str(earliest_birth))
    print("Most recent year of birth :  \n" + str(recent_birth))
    print("Most common year of birth :  \n" + str(common_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("+" * 40)


def display_data(df):
    view_data = str(input(
        "Would you like to view 5 rows of individual trip data? Enter yes or no?")).lower()
    start_loc = 0
    while view_data not in ["yes", "no"]:
        print("{} Not a valid input, try again".format(view_data))
        view_data = str(input(
            "Would you like to view 5 rows of individual trip data? Enter yes or no?")).lower()

    while view_data == "yes":
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_display = str(
            input("Do you wish to continue? Enter yes or no?")).lower()
        while view_display not in ["yes", "no"]:
            print("{} Not a valid input, try again".format(view_display))
        if view_display == "no":
            view_data = view_display


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
