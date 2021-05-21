# Sentiment Analysis
### Dictionary-based sentiment analysis with Python
**This project was developed as part of the spring 2021 elective course Cultural Data Science - Language Analytics at Aarhus University.** <br>

__Task:__ Perform dictionary-based sentiment analysis on a dataset of over a million headlines taken from the Australian news source ABC 
and save plot of smoothed sentiments using a rolling average over one week and month as png file. <br>

The data for this project can be found in the data folder or be downloaded from Kaggle (https://www.kaggle.com/therohk/million-headlines). 
This is a dataset of over a million headlines taken from the Australian news source ABC (Start Date: 2003-02-19 ; End Date: 2020-12-31).

The script is located in the src folder and performs dictionary based sentiment analysis using the dictionary SpaCyTextBlob (for documentation see: https://spacy.io/universe/project/spacy-textblob).

The repository also contains the results from running the sentiment analysis across the million headlines. 
In the out folder, two plots can be found visualizing the rolling averages across a window of one week and one month, respectively. <br> 

__Dependencies:__ <br>
To ensure dependencies are in accordance with the ones used for the script, you can create the virtual environment ‘sentiment_environment"’ from the command line by executing the bash script ‘create_sentiment_venv.sh’. 
```
    $ bash ./create_sentiment_venv.sh
```
This will install an interactive command-line terminal for Python and Jupyter as well as all packages specified in the ‘requirements.txt’ in a virtual environment. 
After creating the environment, it will have to be activated before running the sentiment analysis script.
```    
    $ source sentiment_environment/bin/activate
```
After running these two lines of code, the user can commence running the script. <br>

### How to run sentiment.py <br>
The script sentiment.py can run from command line without additional input. 
However, the user can specify path to the csv file, output directory, number of headlines to use and batch size.
The outputs of the script are two png files of the rolling averages of sentiment across a week and a month.

__Parameters:__ <br>
```
    path: str <path-to-csv>, default = ../data/abcnews-date-text.csv
    output: str <path-to-output>, default = ../out
    n_headlines: int <number-of-headlines>
    batch_size: int <batch-size>, default = 5000

```
    
__Usage:__ <br>
```
    sentiment.py -p <path-to-csv> -o <path-to-output> -n <number-of-headlines> -b <batch-size>
```
    
__Example:__ <br>
```
    $ cd src
    $ python3 sentiment.py -p ../data/abcnews-date-text.csv -o ../out -n 10000 -b 100

```

The code has been developed in Jupyter Notebook and tested in the terminal on Jupyter Hub on worker02. I therefore recommend cloning the Github repository to worker02 and running the scripts from there. 

### Results:
The results of the sentiment analysis show that the one-week rolling average fluctuates much more than the one-month rolling average. This is because the span of the window for the rolling average influences the smoothing. Furthermore, in the one-week rolling average, there are a few values that are negative. However, in the one-month rolling average this is not the case. <br>

Generally, the trajectories of the sentiment are quite linear without much increase or decrease. However, it does seem that there is a slight increase from 2012 to 2015. 
The average sentiment then seems to decrease from 2015 to 2019, after which it increases slightly again. However, overall, the sentiments of the news headlines are positive. 
In the beginning of both plots, there are outliers. I am not exactly sure why they occur, but I believe it might have something to do with the window of the rolling average which take observations before and after the datapoint. 
If there are no observations prior to the datapoint this could potentially result in the spikes we see in the two plots.

