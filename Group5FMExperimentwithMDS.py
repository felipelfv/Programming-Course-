#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 18:01:20 2023

Programming for Psychologists
Class Project

@author: Group 5 (Felipe Fontana Vieira and Marcelo Zilberberg)
"""
#important remark
#about the working directory, please, set your working directory to a folder containing the stimuli images;
#this might imply the need for certain modules, such as we did below:
    
import random
import datetime

#set working directory
#import os
#wd = '/Users/m/Library/Mobile Documents/com~apple~CloudDocs/Leuven/Programming/Project/'
#os.chdir(wd)
#another option:
#os.chdir('/Users/felipevieira/Desktop/_material')


#create stimulus names in line with list provided

#list to create all pairs
pairs_all = []

for i in range(1,9):
    stim_a_s = "stimuli/{}_a_s.jpeg".format(i)
    stim_b_s = "stimuli/{}_b_s.jpeg".format(i)
    stim_a_d = "stimuli/{}_a_d.jpeg".format(i+8)
    stim_b_d = "stimuli/{}_b_d.jpeg".format(i+8)
    pairs_all.append((stim_a_s,stim_b_s))
    pairs_all.append((stim_b_s,stim_a_s))
    pairs_all.append((stim_a_d,stim_b_d))
    pairs_all.append((stim_b_d,stim_a_d))

print (pairs_all)

#shuffle order
random.shuffle(pairs_all)

#create a list including data of each trial per participant
participant_trial = []

#%%

#import psychopy
from psychopy import visual, event, core

#start psychopy window for welcome and instructions
win = visual.Window(size = (800, 800), units = 'pix', color="DarkGray")

#welcome text
welcome = visual.TextStim(win, 'Welcome to the study. \n\n\n Two bird images are quickly shown in succession. \n\n You will be asked to rate the similarity between the two birds: \n\n From 1 (low similarity) to 7 (high similarity). \n\n Quickly type a number from 1 to 7 on the keyboard to submit your rating. \n\n\n\n\n Now, press any key to continue.',color="black")
welcome.pos = [0,0]
welcome.draw()
win.flip()
event.waitKeys()
win.close()   

#begin the trial
win = visual.Window(size = (800, 800), units = 'pix', color="DarkGray")
timer = core.Clock()

#define user ID based on unique date and time
current_time = datetime.datetime.now()
user_id = current_time.strftime("%Y%m%d%H%M%S")


#loop to present stimuli and run a full trial
for j in range (0,32): #later change to full length of stimulus
    

    #generate fixer cross and rating text
    fixer = visual.TextStim(win, '+',color="black")
    fixer.pos = [0,0]

    rating_q = visual.TextStim(win, 'Rate similarity 1 to 7',color="black")
    rating_q.pos = [0,0]
    
    #generate stimulus
    stim_1 = visual.ImageStim(win, pairs_all[j][0])
    stim_2 = visual.ImageStim(win, pairs_all[j][1])


    #present cross, stimulus and rating text
    fixer.draw()
    win.flip()
    core.wait(0.2)
    
    stim_1.draw()
    win.flip()
    core.wait(0.2)
  
    stim_2.draw()
    win.flip()

    core.wait(0.2)
    
    timer.reset()
    
    rating_q.draw()
    win.flip()
    
    #collect user input
    user_response = event.waitKeys(keyList=['1','2','3','4','5','6','7'], timeStamped= timer) 
    user_key = user_response[0][0]
    user_rt  = user_response[0][1]
    participant_trial.append ([user_key,
                               user_rt,
                               pairs_all[j][1][8:-9],
                               pairs_all[j][1][-6]])    

win.close()   

print (participant_trial)

#save data for each participant
import csv
with open(f"result-{user_id}.csv", 'w', newline='') as csvfile:
    name_writer = csv.writer(csvfile, delimiter=',')
    name_writer.writerow(['Score', 'Reaction Time', 'Trial Number','Same/Different'])
    name_writer.writerows(participant_trial)


#inform participant that the trial is over
win = visual.Window(size = (800, 800), units = 'pix', color="DarkGray")

#goodbye text
goodbye = visual.TextStim(win, 'THE END \n\n\n\n\n Thank you for your participation! \n\n\n\n\n Press any key to close the window.',color="black")
goodbye.pos = [0,0]
goodbye.draw()
win.flip()
event.waitKeys()
win.close()   


#####
#####multidimensional scaling
#####
import csv
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#loading the data from the csv files
data = [] #creates an empty list that will be used to store the data points
colors = [] #creates an empty list that will be used to store the colors for each data point
with open(f"result-{user_id}.csv", 'r') as csvfile: #opens the csv file in read mode
    csv_reader = csv.reader(csvfile, delimiter=',') #creates a csv reader object that will be used to read the data from the CSV file
    next(csv_reader) #skipping the header row
    for row in csv_reader:
        data.append([float(row[0]), float(row[1])]) #here the loop iterates over the rows of the csv file and stores the first and second values of each row as a list in the data list created before. Then we convert the values to floats
        if row[3] == "s": #if the "same/different" column has an "s", set the color to red
            colors.append("green")
        else: #if any other letter, set the color to blue
            colors.append("salmon")

#converting the data to a distance matrix
distance_matrix = [] #creates an empty list called distance_matrix that will be used to store the distance matrix
for l in range(len(data)):
    distance_matrix.append([])
    for k in range(len(data)):
        #calculates the euclidean distance between data points i and j
        distance = ((data[l][0] - data[k][0]) ** 2 +
                    (data[l][1] - data[k][1]) ** 2) ** 0.5
        distance_matrix[l].append(distance)

#doing the MDS on the distance matrix
mds = MDS(n_components=2, dissimilarity='precomputed')
result = mds.fit_transform(distance_matrix)

#plot with the results
plt.scatter(result[:,0], result[:,1], c=colors)
green_patch = mpatches.Patch(color='green', label='Similar')
salmon_patch = mpatches.Patch(color='salmon', label='Different')
plt.legend(handles=[green_patch, salmon_patch])
plt.title('Multidimensional Scaling Results')
plt.show()

