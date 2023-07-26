# Happiness-Game
The Happiness Game is a CLI application developed to test your knowledge of countries and provide interesting statistics for you to learn. The game is developed using data from the World Happiness Report, which is an annual publication that publishes a variety of measures for every country in the world. The World Happiness Report tries to measure the success of countries in a more holistic approach than would be shown from using GDP alone as a measure.

## Instructions
1. The program will pick a random country and present the country name to the user.
2. The user will have to guess a country that has a higher overall world happiness rank than the randomly generated country.
3. The program then graphs a comparison between the two countries across all metrics reported by the World Happiness Report.
4. Then the user is prompted to enter any metric they are most interested in.
5. The program then shows the top 5 and bottom 5 countries for the user input metric.
  a. The program also displays statistical information regarding the mean, max, and minimum for the chosen metric.
6. Program ends.

## Features
1. Four data sets (year_2019, year_2020, year_2021, and year_2022) are imported and concatenated into one multi-index dataframe.
  a. Indexed on Country Name and Year.
  b. The full dataframe is changed to a pivottable & removes duplicate index values
2. Aggregate function is used on the total dataframe to add a new column ‘ Total’ for each country.
3. A second column labeled ‘Rank’ is added to the overall dataframe.
4. The modified full dataframe is sorted by Rank to generate the overall rankings in order.
5. The entire dataframe is grouped by country name and the mean is taken across all 4 years of data so that countries can be compared across an average of 4 years of data.
6. The code is formatted into three classes:
  a. The Data class accepts the excel data and organizes it into a useful format ready to play the happiness game.
  b. The HappinessGame class picks a random country in order to start playing the guessing game.
  c. The User class accepts the user input and compares it against the randomly generated country to determine a win / loss.
7. The program can throw a key value error and re-prompt the user for input if they enter an incorrect country name or metric name.
8. The user input is not case sensitive. The program can handle any case of user input.
9. A masking operation is used to extract only the randomly generated country data from the whole dataset.

## References
1. J. F. Helliwell, R. Layard, J. D. Sachs, J.E. De Neve, L. B. Aknin, and S. Wang, Eds., “World Happiness Report 2022”. New York: Sustainable Development Solutions Network, 2022.
2. J. F. Helliwell, R. Layard, J.D. Sachs, and J.E. De Neve, Eds., “World Happiness Report 2021”. New York: Sustainable Development Solutions Network, 2021.
3. J. F. Helliwell, R. Layard, J. Sachs, and J.E. De Neve, Eds., “World Happiness Report 2020”. New York: Sustainable Development Solutions Network, 2020.
4. J.F. Helliwell, R. Layard, and J. Sachs, "World Happiness Report 2019," New York: Sustainable Development Solutions Network, 2019.
