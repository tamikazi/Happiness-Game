# happiness.py

# Tahmid Kazi

"""The World Happiness Game combines data from the World Happiness report and creates a guessing game to 
test your knowledge of the world.

Instructions:
1. One country will be chosen at random, and all the countries statistics will be presented.
2. The goal of the game is to pick a country with a higher world ranking at the trait chosen.
3. If you picked a country that is ranked higher than the randomly generated country, you win!

Example:
1. The program picks 'Albania' as the country name, which has a mean rank associated with it across the years 2019 - 2021.
2. Your goal is to pick a country with a higher life expectancy than Albania.
3. If you choose Finland, you win.

General statistics will be printed at the end for all countries.
"""
import numpy as np
import pandas as pd
import random as rd
import matplotlib.pyplot as plt

class Data: 

    """ The Data class is used to organize and combine all datasets for use later in the program.

    """
    #read all years of data into their own dataframes
    year_2019= pd.read_excel(r"./year_2019.xlsx")
    year_2020= pd.read_excel(r"./year_2020.xlsx")
    year_2021= pd.read_excel(r"./year_2021.xlsx")
    year_2022= pd.read_excel(r"./year_2022.xlsx")

    #concatenates all year data
    #uses pivot table functionality to combine across country name and year, while keeping all values
    #then converts back into a multi-index data frame indexed on country name and year
    all_countries_all_years = pd.concat([year_2019, year_2020, year_2021, year_2022]).pivot_table(index=['COUNTRY NAME', 'YEAR']).reset_index().set_index(['COUNTRY NAME', 'YEAR'])

    """This function will create two new columns in the all_countries_all_years dataframe
    Satisfies two parts of the project rubric:
    1. use aggregate function, 
    2. create two new columns in the dataframe.
    1. it will use an aggregate function to sum all columns across all years for a given country, add this into a column 'total'
    2. sort by highest total at the top
    2. then add a 'rank' column, highest rank = highest overall country score
    """
    #creates a column 'Total', that will sum the countries scores over all indicators, and provide and overall score
    #then sorts the array from top score to bottom score
    all_countries_all_years['TOTAL'] = all_countries_all_years.agg('sum', axis=1)
    all_countries_all_years.sort_values(by='TOTAL', ascending=False, inplace=True) #added 'Total' column, and sort so highest ranking country is top
    all_countries_all_years.insert(0, 'RANK', range(1, len(all_countries_all_years) + 1)) # add a ranking column for all countries across all years

    #create a sub array, collapsing all years into a mean of the countries value
    avg_total_scores = all_countries_all_years.groupby('COUNTRY NAME').mean().sort_values(by='TOTAL', ascending=False)

    #reset ranking index based on averages of all years
    avg_total_scores.drop(['RANK'], axis=1, inplace=True) #need to replace the ranking since now it's been corrupted
    avg_total_scores.insert(0, 'RANK', range(1, len(avg_total_scores) + 1)) #replace ranking based on maximum 'total' score
    sorted_countries = avg_total_scores

    sorted_countries.to_excel('all_data.xlsx') #export full data set to excel sheet


class HappinessGame:
    """ The happinessGame class is used to initialize and start the guessing game. picks the randomly generated country to begin guessing

    """

    #give an initial value to user input country, randomly selected country, and stat comparison.
    def __init__(self): 
        self.random_country_data = ""
        self.random_country_number = 0
 
    """ This function will pick a random country from the full list of countries
    1. must not pick the number 1 country, since then the user cannot win the game
    2. stores the row of data for the random country
    
    return: void
    """
    def pick_random_country(self):
        self.random_country_number = rd.randint(2,147) # pick a random number from 2 to highest rank
        self.random_country_data = Data.sorted_countries.loc[Data.sorted_countries['RANK'] == self.random_country_number] # extract only the row applicable to the random country chosen (uses masking operation)
        return self.random_country_number

class User:

    """User is a class that handles all the user inputs, 
    print statistics relevant to the user input country including a plot of all comparison statistics

    """
    #Only used as initialize conditions
    def __init__(self): 
        self.country_number = 0
        self.country_data = ""

    def calculate_game_stats(self, country, random_country_number):
        """ this function calculates all relevant statistics for the randomly generated country, and the user input country
        inputs: 
            - index rank for the random country generated
            - index rank for the user input country

        return: void
        """

        self.country_number = Data.sorted_countries.loc[country, 'RANK']
        if self.country_number < random_country_number: #check if the user input country ranks higher than the randomly generated country  ****for some reason, the logic only works if the sign is flipped??****
            print("\nCongratulations! You win!\n")
        else:
            print("\nNice try, but you lose :(\n")
        # Generates user input country data
        print("Please see the table below and figure for comparison of all categories for these 2 countries.\nYou can close the plot afterwards to continue the Program.\n")
        self.country_data = Data.sorted_countries.loc[Data.sorted_countries['RANK'] == self.country_number]
        

def graphs(data):
    """ Plots the comparison data for the random country vs. user input country across all traits

    return: void

    """
    # excluding 'Rank' column
    compare_data = data.iloc[:2, 1:]

    # determine the number of columns and rows for subplots
    num_columns = len(compare_data.columns)
    num_rows = 1

    # subplot setup
    fig, axes = plt.subplots(nrows=num_rows, ncols=num_columns, figsize=(18, 6), sharey=False)

    # handle single column case - making sure the axes are treated as a list
    if num_columns == 1:
        axes = [axes]

    # plotting the bar graph for each column
    colors = ['#4E9EAD', '#AD5D4E']
    for i, column in enumerate(compare_data.columns):
        ax = axes[i]
        for j, country in enumerate(compare_data.index):
            ax.bar(j, compare_data.loc[country, column], color=colors[j])
            ax.text(j, compare_data.loc[country, column], f'{compare_data.loc[country, column]:.2f}',
                    ha='center', va='bottom', fontsize=10)
        ax.set_title(column, fontsize=9)
        ax.set_xticks([])
        ax.tick_params(axis='y', which='both', length=0)

    # legend creation
    legend_labels = compare_data.index
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors]
    fig.legend(legend_handles, legend_labels, loc='lower center', ncol=len(legend_labels))

    # adjust the spacing between subplots
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.1)

    # display the plot
    plt.show()


def calculate_all_stats(stat, data):

    """ calculate_all_stats calculates and prints the top 5 and bottom 5 ranked countries for the user input statistic
    - also prints the maximum, minimum, and mean for all countries along the given statistic

    return: void
    """
    #finds the top 5 countries in the given stat
    top_5 = data.sorted_countries.nlargest(5, stat)[[stat]] 
    print(f"\nThe highest ranked countries for {stat} are: \n")
    print(top_5)

    #finds the bottom 5 countries in the given stat
    bottom_5 = data.sorted_countries.nsmallest(5, stat)[[stat]]
    print(f"\nThe lowest ranked countries for {stat} are: \n")
    print(bottom_5)

    #use describe method to print the mean, min, and max values for all columns on the entire dataframe
    describe_df = data.sorted_countries.describe()
    print(f"\nThe mean, min, and max for the category {stat} are: \n")
    print(describe_df.loc[['mean', 'min', 'max'], stat].to_string(index=True))


def main():
    print("\n********** WORLD HAPPINESS GAME **********\n")
    print("The World Happiness Game combines data from the World Happiness report and creates a guessing game to test your knowledge of the world. Good luck!\n")
    print("Instructions: \n1. One country will be chosen at random. \n2. The goal of the game is to pick a \
country with a higher World Happiness Score than the chosen country. \n3. If you picked a country that is ranked higher than the randomly generated country, you win!\n")
    print("Example: \n1. The program picks 'Albania' as the country, which has a mean Rank associated from the years 2019 - 2022. \n\
2. Your goal is to pick a country that you think would rank higher than Albania. \n3. If you choose Finland, you win.")
    
    #Initialize all data sorting
    data = Data()

    #initialize and start the game
    game = HappinessGame()

    #Starts the game by letting the program pick a random country to compare to
    number = game.pick_random_country()

    #initialize user object 
    user = User() 

    #Guessing round begins, user inputs guess country to compare against the randomly generated country
    while(True):
        try:
            country = input(f"\nPlease guess a country that has a higher overall World Happiness Ranking than {game.random_country_data.index[0]}: ").upper() #accept user input for country guess
            if country in data.all_countries_all_years.index: #only pass if user spells country correctly and picks a valid country
                user.calculate_game_stats(country, number) 
                break
            else:
                raise KeyError()
        except KeyError:
            print("\nPlease enter a valid country name.")

    # Combines the randomly generated data and user input data
    combined_data = pd.concat([user.country_data, game.random_country_data])
    print(combined_data)

    # Graphs the combined data
    graphs(combined_data)
    
    #Prints categories to choose from for the 2nd user input
    print("\nPlease select a category from the below to see who ranks the highest and lowest in the category: \n")
    columns = data.sorted_countries.columns[1:9]
    for column in columns:
        print(column)

    # Second user input, to print general statistics for the entire dataframe.
    while(True):
        try:
            stat = input("\nEnter category: ").upper()
            if stat in columns.values: #only pass if user picks a valid category
                calculate_all_stats(stat, data)
                break
            else:
                raise KeyError()
        except KeyError:
            print("\nPlease enter a valid category name.\n")

    print("\nThanks for playing!\n") #game ends

if __name__ == '__main__':
    main()