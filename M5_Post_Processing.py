import numpy as np
import scipy
import pickle

# Mean Travel Time Estimation
def Mean_Travel_Time_Stats(Travel_Time_Record):
    # mean travel time for each rep
    mean_travel_times_each_rep = [np.mean(x) for x in Travel_Time_Record]
    mean_travel_time = np.mean(mean_travel_times_each_rep)
    # std for the mean travel times
    std_travel_time = np.std(mean_travel_times_each_rep, ddof=1)
    return mean_travel_times_each_rep, mean_travel_time, std_travel_time


# Estimating Half-width
def Est_Precision_Half_Width(confidence, num_reps, sample_std):
    est_hw = scipy.stats.t.ppf(1-(1-confidence)/2,num_reps-1) * sample_std/np.sqrt(num_reps)
    return est_hw


# Save to a File
def Save_To_File(file_name, Record, exist=False):
    # Scratch the file new
    if exist == False:
        with open(file_name, 'wb') as f:
            pickle.dump(Record, f)     
    # Append to a existing file
    elif exist == True:
        # read old record
        with open(file_name, 'rb') as f:
            old_record = pickle.load(f)
        # append new record
        new_record = old_record + Record
        # save new record
        with open(file_name, 'wb') as f:
            pickle.dump(new_record, f)

def Write_Log(log_file_name, new_line):
    with open(log_file_name, 'a') as file:
        file.write(new_line + '\n')
    print(new_line)

