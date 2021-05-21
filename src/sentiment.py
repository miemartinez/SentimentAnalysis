#!/usr/bin/env python
"""
Specify path to a csv file containing headlines from news articles, calculate sentiment scores for each headline, smooth the sentiment scores using a rolling average over one week and one month, respectively. Save output plots as png.

Parameters:
    path: str <path-to-csv>, default = ../data/abcnews-date-text.csv
    output: str <path-to-output>, default = ../out
    n_headlines: int <number-of-headlines>
    batch_size: int <batch-size>, default = 5000
Usage:
    sentiment.py -p <path-to-csv> -o <path-to-output> -n <number-of-headlines> -b <batch-size>
Example:
    $ python3 sentiment.py -p ../data/abcnews-date-text.csv -o ../out -n 10000 -b 100
## Task
- Calculate sentiment scores and save plot of smoothed sentiments using a rolling average over one week and month as png file.
"""

# importing libraries
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import tqdm

# spacy
import spacy 
from spacytextblob.spacytextblob import SpacyTextBlob
# initialise spacy 
nlp = spacy.load("en_core_web_sm")


# argparse 
ap = argparse.ArgumentParser()
# adding arguments
# path to csv
ap.add_argument("-p", "--path2csv",
                default = "../data/abcnews-date-text.csv", 
                help= "Path to csv-file")

# path for output directory
ap.add_argument("-o", "--output", 
                default = "../out", 
                help= "Path to output directory")

# number of headlines to extract
ap.add_argument("-n", "--n_headlines", 
                required = False, 
                type = int,
                help= "Number of headlines")
# batch size
ap.add_argument("-b", "--batch_size", 
                default = 5000,
                type = int,
                help= "Batch_size")

# parsing arguments
args = vars(ap.parse_args())


def main(args):
    # get path to image directory
    path = args["path2csv"]
    
    # get output directory
    out = args["output"]
    
    # number of headlines to extract from the csv
    n_headlines = args["n_headlines"]
    
    # batch size
    batch_size = args["batch_size"]
    
    print(f"\n[INFO] Setting batch size to {batch_size}.")
    
    
    # create output directory if it doesn't exist
    create_out_dir(out)
    
    # read csv file as a pandas data frame
    news_data = pd.read_csv(path, nrows = n_headlines)   
    
    # calculate sentiment and save as new data frame with formatted date
    rolling_data = calc_sentiment(data = news_data, 
                                  batch_size = batch_size)
    
    # Plot and save the smoothed sentiment with a rolling average across a week
    smoothed_plot(rolling_data, 7, out)

    # Plot and save the smoothed sentiment with a rolling average across a month
    smoothed_plot(rolling_data, 30, out)


    
def calc_sentiment(data, batch_size):
    '''
    Calculating sentiment scores for the abcnews million headlines data using the spacy text blob pipeline component to add polarity scores.
    Creating a new data frame with sentiment scores and formatted date from publish date to use for the rolling average.
    '''
    # add spacy text blob to nlp pipeline
    spacy_text_blob = SpacyTextBlob()
    nlp.add_pipe(spacy_text_blob)
    
    # Making an empty list for the sentiment scores
    sentiment_scores = []
    
    print("\n[INFO] Calculating sentiment")
    
    # take the headline_text column from the news_data data frame
    headlines = data["headline_text"]
    
    # for each headline
    for headline in nlp.pipe(headlines, batch_size = batch_size):
        # extracting a polarity score
        sentiment = headline._.sentiment.polarity
        # appending the score to the empty list
        sentiment_scores.append(sentiment)
    
    # adding the scores to the dataframe as last column specified with the length of the number of columns
    data.insert(len(data.columns), "sentiment", sentiment_scores)

    # defining a new dataframe that holds the publish date as the index (formatted as a date) and sentiment scores
    rolling_data = pd.DataFrame({"sentiment": sentiment_scores}, 
                            index = pd.to_datetime(data["publish_date"], format='%Y%m%d')) #, errors='ignore'
    
    # return new data frame
    return rolling_data

    
    
# define a rolling mean plotting function
def smoothed_plot(rolling_df, days_for_window, out):
    
    """ 
    Function to make the plot of the smoothed sentiment scores using a rolling average over a specified number of days.
    The function takes a dataframe with calculated sentiment scores and dates.
    Similarly, the function takes a number of days to use as the window for averaging the scores.        
    """

    # if 7 days is specified
    if days_for_window == 7:
        # defining time as a week for plot title
        time = "one week"
        # and for saving the plot
        save_time = "week"
        
    # if 30 days is specified
    elif days_for_window == 30:
        # defining time as a month for plot title
        time = "one month"
        # and for saving the plot
        save_time = "month"
        
    # else 
    else:
        # keep number of days for plot
        time = days_for_window + " days"
        # and for saving the plot
        save_time = days_for_window + "_days"
    
    
    # defining the smoothed sentiment scores from the dataframe with date as index
    # and define the number of days for calculating the rolling average
    smoothed_df = rolling_df.rolling(window = f"{days_for_window}d").mean()
    
    # output path and filename
    plot_save = os.path.join(out, f'news_sentiment_{save_time}.png')
    
    # Plotting the smoothed sentiment scores
    plt.figure()
    # adding title
    plt.title(f"Sentiment over time with a {time} rolling average")
    # adding x-label
    plt.xlabel("Date")
    # rotating x-labels for visibility
    plt.xticks(rotation=45)
    # adding y-label
    plt.ylabel("Sentiment score")
    # plotting with label 
    plt.plot(smoothed_df, label = f"{time} rolling average")
    # using label as legend in the upper right corner
    plt.legend(loc="upper right")
    # saving plot as week_sentiment in current working directory
    plt.savefig(plot_save, bbox_inches='tight')
    print(f"\n[INFO] Plot is saved as {plot_save}")
    
    
def create_out_dir(output_directory):
    '''
    Create out directory if it doesn't exist
    '''
    dirName = os.path.join(output_directory)
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        # print that it has been created
        print("\n[INFO] Directory " , dirName ,  " created ")
    else:   
        # print that it exists
        print("\n[INFO] Directory " , dirName ,  " already exists")
         
    
    
# Define behaviour when called from command line
if __name__=="__main__":
    main(args)
