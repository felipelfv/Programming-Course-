#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 19:09:09 2023

@author: Group 5 (Felipe Fontana Vieira and Marcelo Zilberberg)
"""
#important remark
##please set your working directory to a folder containing the csv files; 
#this might imply the need for certain modules or not. 
#Example below after importing some modules:
    
import glob
import csv
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#directory where the csv files are stored
path = '/Users/felipevieira/Desktop/_material/*.csv' #remember to insert your own path to the directory where the csv files from each run are stored

#list of all the csv files in the specified directory
csv_files = glob.glob(path) #you need to define your path. see line 20

#empty list that will hold the contents of all the csv files
all_results = []

#loop through the list of csv files
for file in csv_files:
    with open(file, 'r') as csvfile: #opens the current csv file in read mode
        reader = csv.reader(csvfile) #creates a csv reader object
        next(reader) #skips the header row of the current csv file
        all_results.extend([[float(row[0]), float(row[1]), int(row[2]), row[3]] for row in reader]) #adds the content of the current csv file to the all_results list

#opens a new csv file in write mode
with open('merged_results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',') #creates a csv writer object
    writer.writerow(['Score', 'Reaction Time', 'Trial Number','Same/Different'])
    writer.writerows(all_results) #writes the content of the all_results list to the new csv file

#getting a dictionary to hold the score and reaction time values for each trial number
trial_averages = {}

#loop through the all_results list
for row in all_results:
    #getting the trial number and score and reaction time values
    trial_number = row[2]
    score = row[0]
    reaction_time = row[1]
    same_different = row[3]
    
    #this step is done if the trial number is not already a key in the dictionary, then it will add it as a key and initialize the value as an empty list
    if trial_number not in trial_averages:
        trial_averages[trial_number] = []
    
    #adding score and reaction time values to the list based on the specific trial number
    trial_averages[trial_number].append(score)
    trial_averages[trial_number].append(reaction_time)

#preparing the data for multidimensional scaling
scores = []
reaction_times = []
colors =[]
for trial_number, values in trial_averages.items():
    average_score = sum(values[::2]) / len(values[::2])
    average_reaction_time = sum(values[1::2]) / len(values[1::2])
    scores.append(average_score)
    reaction_times.append(average_reaction_time)
    print(f"Trial {trial_number}: Average Score = {average_score}, Average Reaction Time = {average_reaction_time}, Similarity = {same_different}")

#getting the "same/different" value for the current trial
    same_different = all_results[trial_number][3]
    #giving a color to the colors list based on the "same/different" value
    if same_different == 's':
        colors.append('green')
    else:
        colors.append('salmon')

data = list(zip(scores, reaction_times))

#multidimensional scaling
mds = MDS(n_components=2, dissimilarity='euclidean', random_state=56)
mds_results = mds.fit_transform(data)

#getting the coordinates of the MDS results
scores_mds = mds_results[:, 0]
reaction_times_mds = mds_results[:, 1]

#plot
plt.scatter(scores_mds, reaction_times_mds, c=colors)
plt.title('Multidimensional Scaling Results')
#setting up the legend
green_patch = mpatches.Patch(color='green', label='Similar')
salmon_patch = mpatches.Patch(color='salmon', label='Different')
plt.legend(handles=[green_patch, salmon_patch])
plt.show()
