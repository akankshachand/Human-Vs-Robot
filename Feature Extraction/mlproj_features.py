# -*- coding: utf-8 -*-
"""MLProj_features.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19pZcdJ4_49aFChQSJGNqmxpKiM3Yg14I
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',20)
pd.set_option('display.width',1000)

b_data = pd.read_csv('bids.csv', sep=',')

#noramlizing time in bids file
minimum_time = b_data['time'].min()
b_data['time_norm'] = round((b_data['time'] - minimum_time) * 19 / 1e9,2)

train = pd.read_csv('train.csv', sep=',')
#merging bids and train files
b_data['outcome'] = b_data.merge(train, how='left', on='bidder_id').outcome

del b_data['merchandise']
del b_data['device']
del b_data['url']
b_data.to_csv('bids_time_norm.csv', sep=',', header=True, index=False)
print('bids_time_norm created')

bids_norm = pd.read_csv('bids_time_norm.csv', sep=',')
test = pd.read_csv('test.csv', sep=',')

# deleting columns not needed
del train['address']
del train['payment_account']
del test['address']
del test['payment_account']

######################### Total no. of  Unique ips,auctions,bids  ##########
print('getting no. of unique ips, auctions and bids')
print('from train')
train['total_unique_ips'] = 0
train['total_no_auctions'] = 0
train['total_no_bids'] = 0

for bidder in train['bidder_id']:
      count_ips = bids_norm[bids_norm.bidder_id == bidder]['ip'].nunique()
      count_aucs = bids_norm[bids_norm.bidder_id == bidder]['auction'].nunique()
      count_bids = bids_norm[bids_norm.bidder_id == bidder].count()[0]
      train.loc[train[train.bidder_id == bidder].index, ['total_unique_ips','total_no_auctions','total_no_bids']] = count_ips, count_aucs, count_bids
    
    

print('from test')
test['total_unique_ips'] = 0
test['total_no_auctions'] = 0
test['total_no_bids'] = 0

for bidder in test['bidder_id']:
      count_ips = bids_norm[bids_norm.bidder_id == bidder]['ip'].nunique()
      count_aucs = bids_norm[bids_norm.bidder_id == bidder]['auction'].nunique()
      count_bids = bids_norm[bids_norm.bidder_id == bidder].count()[0]
      test.loc[test[test.bidder_id == bidder].index, ['total_unique_ips','total_no_auctions','total_no_bids']] = count_ips, count_aucs, count_bids
    
#train.to_csv('/content/drive/My Drive/MLProject/train.csv', sep=',', header=True, index=False)
#test.to_csv('/content/drive/My Drive/MLProject/test.csv', sep=',', header=True, index=False)
##########################################################################


##################################### Number of bids per auction#################
print('getting no. of bids per auction')
print('from train')
train['no_bids_per_auction'] = train.total_no_bids.divide(train.total_no_auctions)
train['no_bids_per_auction'] = round(train['no_bids_per_auction'], 3)

print('from test')
test['no_bids_per_auction'] = test.total_no_bids.divide(test.total_no_auctions)
test['no_bids_per_auction'] = round(test['no_bids_per_auction'], 3)

#train.to_csv('/content/drive/My Drive/MLProject/train.csv', sep=',', header=True, index=False)
#test.to_csv('/content/drive/My Drive/MLProject/test.csv', sep=',', header=True, index=False)
##########################################################################


#################### no. of unique ips/(#bids/auction) ratio #######
print('getting no. of unique ips/(#bids/auction) ratio')
print('from train')
train['ip_per_bids_auc'] = train.total_unique_ips.divide(train.no_bids_per_auction)
train['ip_per_bids_auc'] = round(train['ip_per_bids_auc'], 3)

print('from test')
test['ip_per_bids_auc'] = test.total_unique_ips.divide(test.no_bids_per_auction)
test['ip_per_bids_auc'] = round(test['ip_per_bids_auc'], 3)

#train.to_csv('/content/drive/My Drive/MLProject/train.csv', sep=',', header=True, index=False)
#test.to_csv('/content/drive/My Drive/MLProject/test.csv', sep=',', header=True, index=False)
#####################################################################


#############  mean_time_between_bids  ###############
print('getting mean_time_between_bids')
print('from train')
train['mean_time_between_bids'] = 0
for bidder in train['bidder_id']:

    mn = (bids_norm[bids_norm.bidder_id == bidder].sort_values('time_norm')[['time_norm']] -
         bids_norm[bids_norm.bidder_id == bidder].sort_values('time_norm')[['time_norm']].shift(1)).mean()[0]
    train.loc[train[train.bidder_id == bidder].index, 'mean_time_between_bids'] = mn

train.loc[:, 'mean_time_between_bids'] = round(train.mean_time_between_bids, 4)

print('from test')
test['mean_time_between_bids'] = 0
i = 0
for bidder in test['bidder_id']:
    if i % 200 == 0:
        print(i)
    i += 1

    mn = (bids_norm[bids_norm.bidder_id == bidder].sort_values('time_norm')[['time_norm']] -
         bids_norm[bids_norm.bidder_id == bidder].sort_values('time_norm')[['time_norm']].shift(1)).mean()[0]
    test.loc[test[test.bidder_id == bidder].index, 'mean_time_between_bids'] = mn

test.loc[:, 'mean_time_between_bids'] = round(test.mean_time_between_bids, 4)

train['mean_time_between_bids'] = round(train['mean_time_between_bids'], 3)
test['mean_time_between_bids'] = round(test['mean_time_between_bids'], 3)

#train.to_csv('/content/drive/My Drive/MLProject/train.csv', sep=',', header=True, index=False)
#test.to_csv('/content/drive/My Drive/MLProject/test.csv', sep=',', header=True, index=False)
#######################################################################3


print('writing to train and test')
train.to_csv('train.csv', sep=',', header=True, index=False)
test.to_csv('test.csv', sep=',', header=True, index=False)
print('done')

####################################################################