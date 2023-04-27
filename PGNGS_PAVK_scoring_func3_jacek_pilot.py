#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#######################################################################################
#######################################################################################
# PGNGS Scoring Script/Function for Pavlovia Keyboard Data       
# Written by Summer Frandsen                            
# Last edited 210810
#######################################################################################
#######################################################################################

def PGNGS_PAVK_scoring_func3(sub_id, out_dir, data_dir):

#######################################################################################
#Please Make edits to the specifications listed below as indicated by the instructions
#If unsure how to proceed, please contact the MEND2 Lab
#######################################################################################
    ## These parameters are based on how you set up your PGNGS experience. If unsure, most of these
    ## can be found by looking at some of your output data.
    
    # Which blocks you have -- Put 'yes' or 'no'. *Note that responses are all lowercase
    go_2T = 'yes'
    gng_2T = 'yes'
    gs_2T = 'no'
    go_3T = 'yes'
    gng_3T = 'yes'
    gs_3T = 'no'

    # The label of your stimuli target names (eg. "L_diamond.bmp", "L_r.bmp", "L_x.bmp", 'x', 'y')
    t1 = "L_s.bmp"
    t2 = "L_r.bmp"
    t3 = "L_t.bmp"

    # The label of your stop stimuli
    st = "Stop.bmp"

    # What your correct response is labeled (ex. 'n', 'space')
    cr = 'n'
    no_resp = "None"

    # The set timing of Stimuli (ex. .600, .700, .750)
    iti = .750

############################################################################################
############################################################################################
                    #DO NOT MAKE ANY CHANGES BEYOND THIS POINT
############################################################################################
############################################################################################


#############################
#          SETUP            #
#############################

    #importing necessary packages
    import numpy as np
    import pandas as pd
    import csv
    import re
    import sys

    #Read in data
    PGNGS_data = pd.read_csv((str(data_dir) + '/' + str(sub_id) + '_PGNGS.csv'), header=0, sep=',') 

    part_id = sub_id

    #Create Scoring Dataframes
    PGNGS_scores = pd.DataFrame(np.zeros((1,1)), columns=['user_id'])

    PGNGS_scores['user_id'] = part_id

    PGNGS_clean = pd.DataFrame()
    
    PGNGS_ind_scores = pd.DataFrame(np.zeros((1,1)), columns=['user_id'])
    PGNGS_ind_scores['user_id'] = part_id

################################
#   Go Condition - 2 Target    # 
################################

    if go_2T == 'yes':
        #Pull letters into separate dataframe
        mask = np.invert(PGNGS_data.loc[:,'block1_resp.corr'].isna())
        block1_s = PGNGS_data.loc[mask,['stimuli_1', 'block1_resp.keys', 'correct_resp1', 'block1_resp.corr', 'block1_resp.rt']]
        block1_s = block1_s.reset_index(drop=True)

        block1_c = block1_s
        PGNGS_clean = pd.concat([PGNGS_clean, block1_c], axis = 1)

        #Set the different scores = to 0
        b1_cor = 0
        b1_omm = 0
        b1_cor_rt = 0
        b1_cor_sd = 0

        #Set a column 
        conditions = [
            (block1_s['stimuli_1'] == t1),
            (block1_s['stimuli_1'] == t2),
            (block1_s['stimuli_1'] != t1) & (block1_s['stimuli_1'] != t2)
            ]

        # create a list of the values we want to assign for each condition
        values = ['G', 'G', 'N']

        # create a new column and use np.select to assign values to it using our lists as arguments
        block1_s['target'] = np.select(conditions, values)


        ### Computing Scores
        #Set empty response time dataframe
        block1_rt = pd.DataFrame()

        for i, row in block1_s.iterrows():

            #If it is a go target
            if row['target'] == 'G':
                #Correct response Score
                #If right on target
                if block1_s.loc[i, 'block1_resp.keys'] == cr: 
                    b1_cor = b1_cor + 1
                    #Save response times
                    block1_rt.loc[i, 'block1c_rt'] = (block1_s.loc[i, 'block1_resp.rt'])
                #If right one after target
                elif block1_s.loc[i + 1, 'block1_resp.keys'] == cr:
                    b1_cor = b1_cor + 1
                    #Save response times
                    block1_rt.loc[i, 'block1c_rt'] = iti + block1_s.loc[i+ 1, 'block1_resp.rt']
                #Ommission score (do not respond at target or one after target)
                elif row['block1_resp.keys'] == no_resp and block1_s.loc[i + 1, 'block1_resp.keys'] == no_resp:
                    b1_omm = b1_omm + 1
            else:
                continue

        #Create total Random Response
        b = (block1_s['block1_resp.keys'] == 'n').sum()
        b1_rand_resp = b - b1_cor

        #Create Response time scores
        try:
            b1_cor_rt = block1_rt["block1c_rt"].mean()
        except:
            b1_cor_rt = 0
            print("Error with 2G Go Block mean")

        try:
            b1_cor_sd = block1_rt["block1c_rt"].std()
            if len(block1_rt["block1c_rt"]) <= 1:
                b1_cor_sd = 0 
        except:
            b1_cor_sd = 0
            print("Error with 2G Go Block SD")

        #Create Percent correct
        pc = (block1_s.target == 'G').sum()
        b1_per_cor = b1_cor/pc


        #Check to see if participant responded too many times and num of responsess
        b1_sum = (block1_s['block1_resp.keys'] == 'n').sum()
        b1_tot = (block1_s.correct_resp1 == 'n').sum() 
        if b1_sum > (b1_tot + 5):
            print("Participant", "has too many responses in 2T Go Block")
            
        ###Saving responses to scoring dataframe
        PGNGS_scores['2T_go_hit'] = b1_cor
        PGNGS_scores['2T_go_omm'] = b1_omm

        PGNGS_scores['2T_go_rand_com'] = b1_rand_resp

        PGNGS_scores['2T_go_rt'] = b1_cor_rt
        PGNGS_scores['2T_go_sd'] = b1_cor_sd

        PGNGS_scores['2T_per_cor'] = b1_per_cor

################################
#   GNG Condition - 2 Target   # 
################################

    if gng_2T == 'yes':
        #Pull letters into separate dataframe
        mask = np.invert(PGNGS_data.loc[:,'block2_resp.corr'].isna())
        block2_s = PGNGS_data.loc[mask,['stimuli_2', 'block2_resp.keys', 'correct_resp2', 'block2_resp.corr', 'block2_resp.rt']]
        block2_s = block2_s.reset_index(drop=True)

        block2_c = block2_s
        PGNGS_clean = pd.concat([PGNGS_clean, block2_c], axis = 1)
        
        ind_scores_2T_ng = pd.DataFrame()

        #Set the different scores = to 0
        b2_cor = 0
        b2_omm = 0
        b2_comm = 0
        b2_rej = 0
        b2_miss_opp = 0 
        b2_miss_op_sub = 0 

        #Set a column 
        conditions = [
            (block2_s['stimuli_2'] == t1),
            (block2_s['stimuli_2'] == t2),
            (block2_s['stimuli_2'] != t1) & (block2_s['stimuli_2'] != t2)
            ]

        # create a list of the values we want to assign for each condition
        values = [1, 2, 0]

        # create a new column and use np.select to assign values to it using our lists as arguments
        block2_s['stim_type'] = np.select(conditions, values)

        #Clarify Go and Lure conditions
        t = ''
        l = ''

        for a, type in block2_s.iterrows():
            if type['stim_type'] == 1:
                if t == 'd1' and l == 'n':
                    block2_s.loc[a, 'target'] = 'L'
                    l = 'y'
                    t = 'd1'
                elif t == 'd1' and l == 'y':
                    block2_s.loc[a, 'target'] = 'O'
                    l = 'y'
                    t = 'd1'
                else:
                    block2_s.loc[a, 'target'] = 'G'
                    l = 'n'
                    t = 'd1'
            elif type ['stim_type'] == 2:
                if t == 'd2' and l == 'n':
                    block2_s.loc[a, 'target'] = 'L'
                    l = 'y'
                    t = 'd2'
                elif t == 'd2' and l == 'y':
                    block2_s.loc[a, 'target'] = 'O'
                    l = 'y'
                    t = 'd2'
                else:
                    block2_s.loc[a, 'target'] = 'G'
                    l = 'n'
                    t = 'd2'
            else: 
                block2_s.loc[a, 'target'] = 'N'

        ####Create Scores
        block2cor_rt = pd.DataFrame()
        block2com_rt = pd.DataFrame()
        for d, row in block2_s.iterrows():
            #If row is a Go target
            if row['target'] == 'G':
                #If they respond
                if block2_s.loc[d, 'block2_resp.keys'] == cr:
                    block2_s.loc[d, 'miss_opp'] = 0
                    hold = d
                    b2_cor = b2_cor + 1
                    block2cor_rt.loc[d, 'block2cr_rt'] = block2_s.loc[d, 'block2_resp.rt']
                #If they respond one stimuli after
                elif block2_s.loc[d + 1, 'block2_resp.keys'] == cr:
                    block2_s.loc[d, 'miss_opp'] = 0
                    hold = d
                    b2_cor = b2_cor + 1
                    block2cor_rt.loc[d, 'block2cr_rt'] = iti + block2_s.loc[d + 1, 'block2_resp.rt']

                #If they don't respond
                else:
                    block2_s.loc[d, 'miss_opp'] = 1
                    hold = d
                    b2_omm = b2_omm + 1

            #If row is a lure        
            elif row['target'] == 'L':
                #If they respond
                if block2_s.loc[d, 'block2_resp.keys'] == cr:
                    #If they did not miss the go target before
                    if block2_s.loc[hold, 'miss_opp'] == 0:
                        block2_s.loc[d, 'lure_corr'] = 0
                        block2_s.loc[d, 'miss_opp'] = 0
                        b2_comm = b2_comm + 1
                        block2com_rt.loc[d, 'block2cm_rt'] = block2_s.loc[d, 'block2_resp.rt']
                    #If they missed the go target before
                    else: 
                        block2_s.loc[d, 'miss_opp'] = 1
                        block2_s.loc[d, 'lure_corr'] = 0
                        b2_miss_opp = b2_miss_opp + 1
                        b2_miss_op_sub = b2_miss_op_sub + 1
                #If they respond one stimiuli late        
                elif block2_s.loc[d + 1, 'block2_resp.keys'] == cr:
                    if block2_s.loc[hold, 'miss_opp'] == 0:
                        block2_s.loc[d, 'lure_corr'] = 0
                        block2_s.loc[d, 'miss_opp'] = 0
                        b2_comm = b2_comm + 1
                        block2com_rt.loc[d, 'block2cm_rt'] = iti + block2_s.loc[d + 1, 'block2_resp.rt']
                    else: 
                        block2_s.loc[d, 'miss_opp'] = 1
                        block2_s.loc[d, 'lure_corr'] = 0
                        b2_miss_opp = b2_miss_opp + 1
                        b2_miss_op_sub = b2_miss_op_sub + 1

                elif block2_s.loc[d, 'block2_resp.keys'] == no_resp and block2_s.loc[d + 1, 'block2_resp.keys'] == no_resp:
                    if block2_s.loc[hold, 'miss_opp'] == 0:
                        block2_s.loc[d, 'lure_corr'] = 1
                        block2_s.loc[d, 'miss_opp'] = 0
                        b2_rej = b2_rej + 1
                    else:
                        block2_s.loc[d, 'miss_opp'] = 1
                        block2_s.loc[d, 'lure_corr'] = 1
                        b2_miss_opp = b2_miss_opp + 1
                else:
                    print('error in Go/No-Go line', d)

        #Total Random Score:
        b = (block2_s['block2_resp.keys'] == 'n').sum()
        b2_rand_resp = b - (b2_cor + b2_comm + b2_miss_op_sub) 

        #Create Response time scores
        try:
            b2_cor_rt = block2cor_rt["block2cr_rt"].mean()
        except:
            b2_cor_rt = 0
            print("Error with 2T GNG Block correct mean")

        try:
            b2_cor_sd = block2cor_rt["block2cr_rt"].std()
            if len(block2cor_rt["block2cr_rt"]) <= 1:
                b2_cor_sd = 0 
        except:
            b2_cor_sd = 0
            print("Error with 2T GNG Block correct sd")

        try:
            b2_com_rt = block2com_rt["block2cm_rt"].mean()
        except:
            b2_com_rt = 0
            print("Error with 2T GNG Block commision mean")

        try:
            b2_com_sd = block2com_rt["block2cm_rt"].std()
            if len(block2com_rt["block2cm_rt"]) <= 1:
                b2_com_sd = 0
        except:
            b2_com_sd = 0
            print("Error with 2T GNG Block commission sd")

        #Create Percent correct
        pc_g = (block2_s.target == 'G').sum()
        b2_per_cor_g = b2_cor/pc_g               

        pc_l = (block2_s.target == 'L').sum()
        b2_per_cor_l = b2_rej/pc_l


        #Check to see if participant responded too many times and num of responses
        b2_sum = (block2_s['block2_resp.keys'] == 'n').sum()
        b2_tot = (block2_s.correct_resp2 == 'n').sum() 
        if b2_sum > (b2_tot + b2_comm + 5):
            print("Participant", "has too many responses in 2T GNG Block")

        if b2_rej <= 1:
            print("Participant has 1 or less correct rejections in 2T GNG Block")
        
        #Creating Individual Scored Dataa
        mask = block2_s.loc[:,'target'] == 'L'
        ind_scores_2T_ng['2T_ng_cor']= block2_s.loc[mask,['lure_corr']]
        ind_scores_2T_ng['T_ng_mo']= block2_s.loc[mask,['miss_opp']]
        ind_scores_2T_ng = ind_scores_2T_ng.reset_index(drop=True)

        PGNGS_ind_scores = pd.concat([PGNGS_ind_scores,ind_scores_2T_ng], axis=1)

        ###Save Scores to scoring dataframe
        PGNGS_scores['2T_gng_hit'] = b2_cor
        PGNGS_scores['2T_gng_omm'] = b2_omm
        PGNGS_scores['2T_gng_comm'] = b2_comm
        PGNGS_scores['2T_gng_reject'] = b2_rej
        PGNGS_scores['2T_gng_missopp'] = b2_miss_opp

        PGNGS_scores['2T_gng_rand_com'] = b2_rand_resp

        PGNGS_scores['2T_gng_cor_rt'] = b2_cor_rt
        PGNGS_scores['2T_gng_cor_sd'] = b2_cor_sd

        PGNGS_scores['2T_gng_com_rt'] = b2_com_rt
        PGNGS_scores['2T_gng_com_sd'] = b2_com_sd

        PGNGS_scores['2T_gng_cor_per_g'] = b2_per_cor_g
        PGNGS_scores['2T_gng_cor_per_l'] = b2_per_cor_l

################################
# Go/Stop Condition - 2 Target # 
################################

    if gs_2T == 'yes':
        mask = np.invert(PGNGS_data.loc[:,'block3_resp.corr'].isna())
        block3_s = PGNGS_data.loc[mask,['stimuli_3', 'correct_resp3', 'block3_resp.keys', 'block3_resp.corr', 'block3_resp.rt', 'time_3']]
        block3_s = block3_s.reset_index(drop=True)

        block3_c = block3_s
        PGNGS_clean = pd.concat([PGNGS_clean, block3_c], axis = 1)
        
        ind_scores_2T_gs = pd.DataFrame() 

        #Set all scores = to 0
        b3_cor = 0
        b3_omm = 0
        b3_comm = 0
        b3_rej = 0
        b3_stoptime = 0
        b3_fstoptime = 0

        ###Clarify Go/Stop Conditions
        conditions = [
            (block3_s['stimuli_3'] == t1),
            (block3_s['stimuli_3'] == t2),
            (block3_s['stimuli_3'] != t1) & (block3_s['stimuli_3'] != t2)
            ]

        # create a list of the values we want to assign for each condition
        values = ['G', 'G', 'N']

        # create a new column and use np.select to assign values to it using our lists as arguments
        block3_s['target'] = np.select(conditions, values)

        for i, row in block3_s.iterrows():
            if row['stimuli_3'] == st:
                block3_s.loc[i-1, 'target'] = 'S'
            else:
                continue 

        ### Compute Scores
        block3cor_rt = pd.DataFrame()
        block3com_rt = pd.DataFrame()
        block3f_stp = pd.DataFrame()
        block3cor_stp = pd.DataFrame()

        for i, row in block3_s.iterrows():
            if row['target'] == 'G':
                #make sure not following a stop#
                #if block3_s.loc[i-1, 'target'] != 'S':
                    #correct in event and one event after
                if block3_s.loc[i, 'block3_resp.keys'] == cr:
                    b3_cor = b3_cor + 1
                    block3cor_rt.loc[i, 'block3cr_rt'] = block3_s.loc[i, 'block3_resp.rt']
                elif block3_s.loc[i + 1, 'block3_resp.keys'] == cr:
                    b3_cor = b3_cor + 1
                    block3cor_rt.loc[i, 'block3cr_rt'] = iti + block3_s.loc[i+1, 'block3_resp.rt']
                #Ommission 
                elif block3_s.loc[i, 'block3_resp.keys'] == no_resp and block3_s.loc[i+1, 'block3_resp.keys'] == no_resp:
                    b3_omm = b3_omm + 1
                else:
                    continue
                #commission (letter time + stop time + additional time -- anytime within 3 of next letter)
            elif row['target'] == 'S':
                #Correct Rejections
                if block3_s.loc[i, 'block3_resp.keys'] == no_resp and block3_s.loc[i + 1, 'block3_resp.keys'] == no_resp:
                    block3_s.loc[i, 'stop_corr'] = 1
                    b3_rej = b3_rej + 1
                    block3cor_stp.loc[i, 'block3stp_time_cr'] = block3_s.loc[i, 'time_3']
                #Commisions
                elif block3_s.loc[i, 'block3_resp.keys'] == cr: 
                    block3_s.loc[i, 'stop_corr'] = 0
                    b3_comm = b3_comm + 1
                    block3f_stp.loc[i, 'block3stp_time_fail'] = block3_s.loc[i, 'time_3']
                    block3com_rt.loc[i, 'block3cm_rt'] = block3_s.loc[i, 'block3_resp.rt']
                elif block3_s.loc[i + 1, 'block3_resp.keys'] == cr:
                    block3_s.loc[i, 'stop_corr'] = 0
                    b3_comm = b3_comm + 1
                    block3f_stp.loc[i, 'block3stp_time_fail'] = block3_s.loc[i, 'time_3']
                    block3com_rt.loc[i, 'block3cm_rt'] = block3_s.loc[i, 'time_3'] + block3_s.loc[i+1, 'block3_resp.rt']
                elif block3_s.loc[i + 2, 'block3_resp.keys'] == cr:
                    block3_s.loc[i, 'stop_corr'] = 0
                    b3_comm = b3_comm + 1
                    block3f_stp.loc[i, 'block3stp_time_fail'] = block3_s.loc[i, 'time_3']
                    block3com_rt.loc[i, 'block3cm_rt'] = block3_s.loc[i, 'time_3'] + block3_s.loc[i+1, 'time_3'] + block3_s.loc[i+2, 'block3_resp.rt']

                else:
                    continue

        #Total Random Responses
        b = (block3_s['block3_resp.keys'] == 'n').sum()
        b3_rand_resp = b - (b3_cor + b3_comm)

        #Create Response time scores
        try:
            b3_cor_rt = block3cor_rt['block3cr_rt'].mean()
        except:
            b3_cor_rt = 0
            print("Error with 2G GS Block correct mean")

        try:
            b3_cor_sd = block3cor_rt['block3cr_rt'].std()
            if len(block3cor_rt["block3cr_rt"]) <= 1:
                b3_cor_sd = 0 
        except:
            b3_cor_sd = 0
            print("Error with 2G GS Block correct sd")

        try:
            b3_com_rt = block3com_rt['block3cm_rt'].mean()
        except:
            b3_com_rt = 0
            print("Error with 2G GS Block commission mean")

        try:
            b3_com_sd = block3com_rt['block3cm_rt'].std()
            if len(block3com_rt["block3cm_rt"]) <= 1:
                b3_com_sd = 0 
        except:
            b3_com_sd = 0
            print("Error with 2G GS Block commission sd")

        try:
            b3_stp_tm = block3cor_stp['block3stp_time_cr'].mean()
        except:
            b3_stp_tm = 0
            print("Error with 2G GS Block correct stop mean")

        try:
            b3_stp_tm_f = block3f_stp['block3stp_time_fail'].mean()
        except:
            b3_stp_tm_f = 0
            print("Error with 2G GS Block failed stop mean")

        #Create Percent correct
        pc_g = (block3_s.target == 'G').sum()
        b3_per_cor_g = b3_cor/pc_g               

        pc_l = (block3_s.target == 'S').sum()
        b3_per_cor_l = b3_rej/pc_l

        #Check to see if participant responded too many times and num of responsses
        b3_sum = (block3_s['block3_resp.keys'] == 'n').sum()
        b3_tot = (block3_s.correct_resp3 == 'n').sum() 
        if b3_sum > (b3_tot + b3_comm + 5):
            print("Participant", "has too many responses in 2T GS Block")

        if b3_rej <= 1:
            print("Participant has 1 or less correct rejections in 2T GS Block")
            
        #Create Individual Scored Data
        mask = block3_s.loc[:,'target'] == 'S'
        ind_scores_2T_gs['2T_gs_cor']= block3_s.loc[mask,['stop_corr']]
        ind_scores_2T_gs = ind_scores_2T_gs.reset_index(drop=True)

        PGNGS_ind_scores = pd.concat([PGNGS_ind_scores,ind_scores_2T_gs], axis=1)
        
        #Save Scores to scoring dataframe
        PGNGS_scores['2T_gs_hit'] = b3_cor
        PGNGS_scores['2T_gs_omm'] = b3_omm
        PGNGS_scores['2T_gs_comm'] = b3_comm
        PGNGS_scores['2T_gs_reject'] = b3_rej

        PGNGS_scores['2T_gs_rand_com'] = b3_rand_resp

        PGNGS_scores['2T_gs_cor_rt'] = b3_cor_rt
        PGNGS_scores['2T_gs_cor_sd'] = b3_cor_sd

        PGNGS_scores['2T_gs_com_rt'] = b3_com_rt
        PGNGS_scores['2T_gs_com_sd'] = b3_com_sd

        PGNGS_scores['2T_gs_stp_tm'] = b3_stp_tm
        PGNGS_scores['2T_gs_stp_tm_f'] = b3_stp_tm_f

        PGNGS_scores['2T_gs_cor_per_g'] = b3_per_cor_g
        PGNGS_scores['2T_gs_cor_per_l'] = b3_per_cor_l

##############s#########################
#          3 Target Blocks            #
#######################################

################################
#   Go Condition - 3 Target    # 
################################

    if go_3T == 'yes':
        #Pull letters into separate dataframe
        mask = np.invert(PGNGS_data.loc[:,'block4_resp.corr'].isna())
        block4_s = PGNGS_data.loc[mask,['stimuli_4', 'correct_resp4', 'block4_resp.keys', 'block4_resp.corr','block4_resp.rt']]
        block4_s = block4_s.reset_index(drop=True)

        block4_c = block4_s
        PGNGS_clean = pd.concat([PGNGS_clean, block4_c], axis = 1)

        #Set the different scores = to 0
        b4_cor = 0
        b4_omm = 0

        #Set a column 
        conditions = [
            (block4_s['stimuli_4'] == t1),
            (block4_s['stimuli_4'] == t2),
            (block4_s['stimuli_4'] == t3),
            (block4_s['stimuli_4'] != t1) & (block4_s['stimuli_4'] != t2) & (block4_s['stimuli_4'] != t3)
            ]

        # create a list of the values we want to assign for each condition
        values = ['G', 'G', 'G', 'N']

        # create a new column and use np.select to assign values to it using our lists as arguments
        block4_s['target'] = np.select(conditions, values)

        ### Computing Scores
        #Set empty response time dataframe
        block4_rt = pd.DataFrame()

        for i, row in block4_s.iterrows():

            #If it is a go target
            if row['target'] == 'G':
                #Correct response Score
                #If right on target
                if block4_s.loc[i, 'block4_resp.keys'] == cr: 
                    b4_cor = b4_cor + 1
                    #Save response times
                    block4_rt.loc[i, 'block4c_rt'] = (block4_s.loc[i, 'block4_resp.rt'])
                #If right one after target
                elif block4_s.loc[i + 1, 'block4_resp.keys'] == cr:
                    b4_cor = b4_cor + 1
                    #Save response times
                    block4_rt.loc[i, 'block4c_rt'] = iti + block4_s.loc[i+ 1, 'block4_resp.rt']
                #Ommission score (do not respond at target or one after target)
                elif row['block4_resp.keys'] == no_resp and block4_s.loc[i + 1, 'block4_resp.keys'] == no_resp:
                    b4_omm = b4_omm + 1
            else:
                continue

        #Create total Random Response
        b = (block4_s['block4_resp.keys'] == 'n').sum()
        b4_rand_resp = b - b4_cor

        #Create Response time scores
        try:
            b4_cor_rt = block4_rt["block4c_rt"].mean()
        except:
            b4_cor_rt = 0
            print("Error with 3T Go Block mean")

        try:
            b4_cor_sd = block4_rt["block4c_rt"].std()
            if len(block4_rt["block4c_rt"]) <= 1:
                b4_cor_sd = 0 
        except:
            b4_cor_sd = 0
            print("Error with 3T Go Block sd")

        #Create Percent correct
        pc = (block4_s.target == 'G').sum()
        b4_per_cor = b4_cor/pc

        #Check to see if participant responded too many times and num of responses
        b4_sum = (block4_s['block4_resp.keys'] == 'n').sum()
        b4_tot = (block4_s.correct_resp4 == 'n').sum() 
        if b4_sum > (b4_tot + 5):
            print("Participant", "has too many responses in 3T Go Block")

        #Saving responses to scoring dataframe
        PGNGS_scores['3T_go_hit'] = b4_cor
        PGNGS_scores['3T_go_omm'] = b4_omm

        PGNGS_scores['3T_go_rand_com'] = b4_rand_resp

        PGNGS_scores['3T_go_rt'] = b4_cor_rt
        PGNGS_scores['3T_go_sd'] = b4_cor_sd

        PGNGS_scores['3T_per_cor'] = b4_per_cor

################################
#   GNG Condition - 3 Target   # 
################################

    if gng_3T == 'yes':
        #Pull letters into separate dataframe
        mask = np.invert(PGNGS_data.loc[:,'block5_resp.corr'].isna())
        block5_s = PGNGS_data.loc[mask,['stimuli_5_reversed', 'block5_resp.keys', 'correct_resp5', 'block5_resp.corr', 'block5_resp.rt']]
        block5_s['correct_resp5'] = pd.read_csv("3t_gng_reverse_fix.csv").actual_correct_resp5_reversed.values
        block5_s['block5_resp.corr'] = [1 if x[0] == x[1] else 0 for x in block5_s[['block5_resp.keys','correct_resp5']].values]
        block5_s = block5_s.reset_index(drop=True)

        block5_c = block5_s
        PGNGS_clean = pd.concat([PGNGS_clean, block5_c], axis = 1)
        
        ind_scores_3T_ng = pd.DataFrame()

        #Set the different scores = to 0
        b5_cor = 0
        b5_omm = 0
        b5_comm = 0
        b5_rej = 0
        b5_miss_opp = 0 
        b5_miss_op_sub = 0

        #Set a column 
        conditions = [
            (block5_s['stimuli_5_reversed'] == t1),
            (block5_s['stimuli_5_reversed'] == t2),
            (block5_s['stimuli_5_reversed'] == t3),
            (block5_s['stimuli_5_reversed'] != t1) & (block5_s['stimuli_5_reversed'] != t2) & (block5_s['stimuli_5_reversed'] != t3)
            ]

        # create a list of the values we want to assign for each condition
        values = [1, 2, 3, 0]

        # create a new column and use np.select to assign values to it using our lists as arguments
        block5_s['stim_type'] = np.select(conditions, values)

        ### Clarify Go and Lure conditions
        t = ''
        l = ''
        for a, type in block5_s.iterrows():
            if type['stim_type'] == 1:
                if t == 'd1' and l == 'n':
                    block5_s.loc[a, 'target'] = 'L'
                    t = 'd1'
                    l = 'y'
                elif t == 'd1' and l == 'y':
                    block5_s.loc[a, 'target'] = 'O'
                    t = 'd1'
                    l = 'y'
                else:
                    block5_s.loc[a, 'target'] = 'G'
                    t = 'd1'
                    l = 'n'
            elif type ['stim_type'] == 2:
                if t == 'd2' and l == 'n':
                    block5_s.loc[a, 'target'] = 'L'
                    t = 'd2'
                    l = 'y'
                elif t == 'd2' and l == 'y':
                    block5_s.loc[a, 'target'] = 'O'
                    t = 'd2'
                    l = 'y'
                else:
                    block5_s.loc[a, 'target'] = 'G'
                    t = 'd2'
                    l = 'n'
            elif type ['stim_type'] == 3:
                if t == 'd3' and l == 'n':
                    block5_s.loc[a, 'target'] = 'L'
                    t = 'd3'
                    l = 'y'
                elif t == 'd3' and l == 'y':
                    block5_s.loc[a, 'target'] = 'O'
                    t = 'd3'
                    l = 'y'
                else:
                    block5_s.loc[a, 'target'] = 'G'
                    t = 'd3'
                    l = 'n'
            else: 
                block5_s.loc[a, 'target'] = 'N'

        ### Compute Scores
        block5cor_rt = pd.DataFrame()
        block5com_rt = pd.DataFrame()
        for d, row in block5_s.iterrows():
            #If row is a Go target
            if row['target'] == 'G':
                #If they respond
                if block5_s.loc[d, 'block5_resp.keys'] == cr:
                    block5_s.loc[d, 'miss_opp'] = 0
                    hold = d
                    b5_cor = b5_cor + 1
                    block5cor_rt.loc[d, 'block5cr_rt'] = block5_s.loc[d, 'block5_resp.rt']
                #If they respond one stimuli after
                elif block5_s.loc[d + 1, 'block5_resp.keys'] == cr:
                    block5_s.loc[d, 'miss_opp'] = 0
                    hold = d
                    b5_cor = b5_cor + 1
                    block5cor_rt.loc[d, 'block5cr_rt'] = iti + block5_s.loc[d + 1, 'block5_resp.rt']

                #If they don't respond
                else:
                    block5_s.loc[d, 'miss_opp'] = 1
                    hold = d
                    b5_omm = b5_omm + 1

            #If row is a lure        
            elif row['target'] == 'L':
                #If they respond
                if block5_s.loc[d, 'block5_resp.keys'] == cr:
                    #If they did not miss the go target before
                    if block5_s.loc[hold, 'miss_opp'] == 0:
                        block5_s.loc[d, 'miss_opp'] = 0
                        block5_s.loc[d, 'lure_corr'] = 0
                        b5_comm = b5_comm + 1
                        block5com_rt.loc[d, 'block5cm_rt'] = block5_s.loc[d, 'block5_resp.rt']
                    #If they missed the go target before
                    else: 
                        block5_s.loc[d, 'miss_opp'] = 1
                        block5_s.loc[d, 'lure_corr'] = 0
                        b5_miss_opp = b5_miss_opp + 1
                        b5_miss_op_sub = b5_miss_op_sub + 1
                #If they respond one stimiuli late        
                elif block5_s.loc[d + 1, 'block5_resp.keys'] == cr:
                    if block5_s.loc[hold, 'miss_opp'] == 0:
                        block5_s.loc[d, 'miss_opp'] = 0
                        block5_s.loc[d, 'lure_corr'] = 0
                        b5_comm = b5_comm + 1
                        block5com_rt.loc[d, 'block5cm_rt'] = iti + block5_s.loc[d + 1, 'block5_resp.rt']
                    else: 
                        block5_s.loc[d, 'miss_opp'] = 1
                        block5_s.loc[d, 'lure_corr'] = 0
                        b5_miss_opp = b5_miss_opp + 1
                        b5_miss_op_sub = b5_miss_op_sub + 1

                elif  block5_s.loc[d, 'block5_resp.keys'] == no_resp and block5_s.loc[d + 1, 'block5_resp.keys'] == no_resp:
                    if block5_s.loc[hold, 'miss_opp'] == 0:
                        block5_s.loc[d, 'miss_opp'] = 0
                        block5_s.loc[d, 'lure_corr'] = 1
                        b5_rej = b5_rej + 1
                    else:
                        block5_s.loc[d, 'miss_opp'] = 1
                        block5_s.loc[d, 'lure_corr'] = 1
                        b5_miss_opp = b5_miss_opp + 1
                else:
                    print('error in Go/No-Go line', d)

        #Total Random Score:
        b = (block5_s['block5_resp.keys'] == 'n').sum()
        b5_rand_resp = b - (b5_cor + b5_comm + b5_miss_op_sub) 

        #Create Response time scores
        try:
            b5_cor_rt = block5cor_rt["block5cr_rt"].mean()
        except:
            b5_cor_rt = 0
            print("Error with 3T GNG Block correct mean")

        try:
            b5_cor_sd = block5cor_rt["block5cr_rt"].std()
            if len(block5cor_rt["block5cr_rt"]) <= 1:
                b5_cor_sd = 0 
        except:
            b5_cor_sd = 0
            print("Error with 3T GNG Block correct sd")

        try:
            b5_com_rt = block5com_rt["block5cm_rt"].mean()
        except:
            b5_com_rt = 0
            print("Error with 3T GNG Block commissions mean")

        try:
            b5_com_sd = block5com_rt["block5cm_rt"].std()
            if len(block5com_rt["block5cm_rt"]) <= 1:
                b5_com_sd = 0 
        except:
            b5_com_sd = 0
            print("Error with 3T GNG Block commissions sd")

        #Create Percent correct
        pc_g = (block5_s.target == 'G').sum()
        b5_per_cor_g = b5_cor/pc_g               

        pc_l = (block5_s.target == 'L').sum()
        b5_per_cor_l = b5_rej/pc_l

        #Check to see if participant responded too many times and num of rejections
        b5_sum = (block5_s['block5_resp.keys'] == 'n').sum()
        b5_tot = (block5_s.correct_resp5 == 'n').sum() 
        if b5_sum > (b5_tot + b5_comm + 5):
            print("Participant", "has too many responses in 3T GNG Block")

        if b5_rej <= 1:
            print("Participant has 1 or less correct rejections in 3T GNG Block")
        
        #Creating individual scored data
        mask = block5_s.loc[:,'target'] == 'L'
        ind_scores_3T_ng['3T_ng_cor']= block5_s.loc[mask,['lure_corr']]
        ind_scores_3T_ng['3T_ng_mo']= block5_s.loc[mask,['miss_opp']]
        ind_scores_3T_ng = ind_scores_3T_ng.reset_index(drop=True)

        PGNGS_ind_scores = pd.concat([PGNGS_ind_scores,ind_scores_3T_ng], axis=1)
        
        #Save Scores to scoring dataframe
        PGNGS_scores['3T_gng_hit'] = b5_cor
        PGNGS_scores['3T_gng_omm'] = b5_omm
        PGNGS_scores['3T_gng_comm'] = b5_comm
        PGNGS_scores['3T_gng_reject'] = b5_rej
        PGNGS_scores['3T_gng_missopp'] = b5_miss_opp

        PGNGS_scores['3T_gng_rand_com'] = b5_rand_resp

        PGNGS_scores['3T_gng_cor_rt'] = b5_cor_rt
        PGNGS_scores['3T_gng_cor_sd'] = b5_cor_sd

        PGNGS_scores['3T_gng_com_rt'] = b5_com_rt
        PGNGS_scores['3T_gng_com_sd'] = b5_com_sd

        PGNGS_scores['3T_gng_cor_per_g'] = b5_per_cor_g
        PGNGS_scores['3T_gng_cor_per_l'] = b5_per_cor_l

################################
# Go/Stop Condition - 3 Target # 
################################

    if gs_3T == 'yes':
        mask = np.invert(PGNGS_data.loc[:,'block6_resp.corr'].isna())
        block6_s = PGNGS_data.loc[mask,['stimuli_6', 'correct_resp6', 'block6_resp.keys', 'block6_resp.corr', 'block6_resp.rt', 'time_6']]
        block6_s = block6_s.reset_index(drop=True)

        block6_c = block6_s
        PGNGS_clean = pd.concat([PGNGS_clean, block6_c], axis = 1)
        
        ind_scores_3T_gs = pd.DataFrame() 
        
        #Set all scores = to 0
        b6_cor = 0
        b6_omm = 0
        b6_comm = 0
        b6_rej = 0
        b6_stoptime = 0
        b6_fstoptime = 0

        ### Clarify Go/Stop Conditions
        conditions = [
            (block6_s['stimuli_6'] == t1),
            (block6_s['stimuli_6'] == t2),
            (block6_s['stimuli_6'] == t3),
            (block6_s['stimuli_6'] != t1) & (block6_s['stimuli_6'] != t2) & (block6_s['stimuli_6'] != t3)
            ]

        # create a list of the values we want to assign for each condition
        values = ['G', 'G', 'G', 'N']

        # create a new column and use np.select to assign values to it using our lists as arguments
        block6_s['target'] = np.select(conditions, values)

        for i, row in block6_s.iterrows():
            if row['stimuli_6'] == st:
                block6_s.loc[i-1, 'target'] = 'S'
            else:
                continue 

        ### Compute Scores
        block6cor_rt = pd.DataFrame()
        block6com_rt = pd.DataFrame()
        block6f_stp = pd.DataFrame()
        block6cor_stp = pd.DataFrame()

        for i, row in block6_s.iterrows():
            if row['target'] == 'G':
                #correct in event and one event after
                if block6_s.loc[i, 'block6_resp.keys'] == cr:
                    b6_cor = b6_cor + 1
                    block6cor_rt.loc[i, 'block6cr_rt'] = block6_s.loc[i, 'block6_resp.rt']
                elif block6_s.loc[i + 1, 'block6_resp.keys'] == cr:
                    b6_cor = b6_cor + 1
                    block6cor_rt.loc[i, 'block6cr_rt'] = iti + block6_s.loc[i+1, 'block6_resp.rt']
                #Ommission 
                elif block6_s.loc[i, 'block6_resp.keys'] == no_resp and block6_s.loc[i+1, 'block6_resp.keys'] == no_resp:
                    b6_omm = b6_omm + 1
                else:
                    continue
                #commission (letter time + stop time + additional time -- anytime within 3 of next letter)
            elif row['target'] == 'S':
                #Correct Rejections
                if block6_s.loc[i, 'block6_resp.keys'] == no_resp and block6_s.loc[i + 1, 'block6_resp.keys'] == no_resp:
                    block6_s.loc[i, 'stop_corr'] = 1
                    b6_rej = b6_rej + 1
                    block6cor_stp.loc[i, 'block6stp_time_cr'] = block6_s.loc[i, 'time_6']
                #Commisions
                elif block6_s.loc[i, 'block6_resp.keys'] == cr: 
                    block6_s.loc[i, 'stop_corr'] = 0
                    b6_comm = b6_comm + 1
                    block6f_stp.loc[i, 'block6stp_time_fail'] = block6_s.loc[i, 'time_6']
                    block6com_rt.loc[i, 'block6cm_rt'] = block6_s.loc[i, 'block6_resp.rt']
                elif block6_s.loc[i + 1, 'block6_resp.keys'] == cr:
                    block6_s.loc[i, 'stop_corr'] = 0
                    b6_comm = b6_comm + 1
                    block6f_stp.loc[i, 'block6stp_time_fail'] = block6_s.loc[i, 'time_6']
                    block6com_rt.loc[i, 'block6cm_rt'] = block6_s.loc[i, 'time_6'] + block6_s.loc[i+1, 'block6_resp.rt']
                elif block6_s.loc[i + 2, 'block6_resp.keys'] == cr:
                    block6_s.loc[i, 'stop_corr'] = 0
                    b6_comm = b6_comm + 1
                    block6f_stp.loc[i, 'block6stp_time_fail'] = block6_s.loc[i, 'time_6']
                    block6com_rt.loc[i, 'block6cm_rt'] = block6_s.loc[i, 'time_6'] + block6_s.loc[i+1, 'time_6'] + block6_s.loc[i+2, 'block6_resp.rt']

                else:
                    continue

        #Total Random Responses
        b = (block6_s['block6_resp.keys'] == 'n').sum()
        b6_rand_resp = b - (b6_cor + b6_comm)

        #Create Response time scores
        try:
            b6_cor_rt = block6cor_rt['block6cr_rt'].mean()
        except:
            b6_cor_rt = 0
            print("Error with 3T GS Block correct mean")

        try:
            b6_cor_sd = block6cor_rt['block6cr_rt'].std()
            if len(block6cor_rt["block6cr_rt"]) <= 1:
                b6_cor_sd = 0 
        except:
            b6_cor_sd = 0
            print("Error with 3T GS Block correct sd")

        try:
            b6_com_rt = block6com_rt['block6cm_rt'].mean()
        except:
            b6_com_rt = 0
            print("Error with 3T GS Block commission mean")

        try:
            b6_com_sd = block6com_rt['block6cm_rt'].std()
            if len(block6com_rt["block6cm_rt"]) <= 1:
                b6_com_sd = 0 
        except:
            b6_com_sd = 0
            print("Error with 3T GS Block commission sd")

        try:
            b6_stp_tm = block6cor_stp['block6stp_time_cr'].mean()
        except:
            b6_stp_tm = 0
            print("Participant", 'has no correct stops in 3T GS Block')

        try:
            b6_stp_tm_f = block6f_stp['block6stp_time_fail'].mean()
        except:
            b6_stp_tm_f = 0
            print("Participant", 'has no failed stops in 3T GS Block')

        #Create Percent correct
        pc_g = (block6_s.target == 'G').sum()
        b6_per_cor_g = b6_cor/pc_g               

        pc_l = (block6_s.target == 'S').sum()
        b6_per_cor_l = b6_rej/pc_l

        #Check to see if participant responded too many times and num of rejections
        b6_sum = (block6_s['block6_resp.keys'] == 'n').sum()
        b6_tot = (block6_s.correct_resp6 == 'n').sum() 
        if b6_sum > (b6_tot + b6_comm + 5):
            print("Participant", "has too many responses in 3T GS Block")

        if b6_rej <= 1:
            print("Participant has 1 or less correct rejections in 3T GS Block")

        #Create_individual Scores    
        mask = block6_s.loc[:,'target'] == 'S'
        ind_scores_3T_gs['3T_gs_cor']= block6_s.loc[mask,['stop_corr']]
        ind_scores_3T_gs = ind_scores_3T_gs.reset_index(drop=True)

        PGNGS_ind_scores = pd.concat([PGNGS_ind_scores,ind_scores_3T_gs], axis=1)    
        
        
        #Save Scores to scoring dataframe
        PGNGS_scores['3T_gs_hit'] = b6_cor
        PGNGS_scores['3T_gs_omm'] = b6_omm
        PGNGS_scores['3T_gs_comm'] = b6_comm
        PGNGS_scores['3T_gs_reject'] = b6_rej

        PGNGS_scores['3T_gs_rand_com'] = b6_rand_resp

        PGNGS_scores['3T_gs_cor_rt'] = b6_cor_rt
        PGNGS_scores['3T_gs_cor_sd'] = b6_cor_sd

        PGNGS_scores['3T_gs_com_rt'] = b6_com_rt
        PGNGS_scores['3T_gs_com_sd'] = b6_com_sd

        PGNGS_scores['3T_gs_stp_tm'] = b6_stp_tm
        PGNGS_scores['3T_gs_stp_tm_f'] = b6_stp_tm_f

        PGNGS_scores['3T_gs_cor_per_g'] = b6_per_cor_g
        PGNGS_scores['3T_gs_cor_per_l'] = b6_per_cor_l

###########################
#        Save Data        #
###########################
    PGNGS_clean.to_csv((str(out_dir)+'/cleaned/'+str(sub_id) + '_PGNGS_PAVK_scored.csv'), index=False)

    PGNGS_ind_scores.to_csv((str(out_dir)+'/ind_scored/'+str(sub_id) + '_PGNGS_PAVK_ind_scored.csv'), index=False)

    PGNGS_scores.to_csv((str(out_dir)+'/scored/'+str(sub_id) + '_PGNGS_PAVK_scored.csv'), index=False)

    return PGNGS_scores

