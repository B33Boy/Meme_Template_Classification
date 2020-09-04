#!/usr/bin/python

'''
Note:

Run this script in the same directory where the memes.json file is located in.
This should be run only once and the rest of the application will use the preprocessed
data.

sample input -> python ./data_preprocessing.py "../data/memes.json" "../"

Original Data can be found here: https://www.kaggle.com/abhishtagatya/imgflipscraped-memes-caption-dataset

'''

import os
import pandas as pd
import random
import urllib.request
import sys


SEED = 448
random.seed(SEED)

# Helper Functions
def makeDirectory(path):
    try:
        os.makedirs(path)
    except:
        raise FileExistsError

def readJSONData(path):
    return pd.read_json(path)


def downloadImages(image_data):
    for file_path,img_url in image_data:
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        try:
            urllib.request.urlretrieve(img_url, file_path)
        except KeyboardInterrupt:
            print ('Caught KeyboardInterrupt')
            exit(1)
        except:
            print(f'Meme could not be downloaded: {file_path} Url : {img_url}')

def preprocess(data_path, output_path, train_test_split_ratio):
    df = readJSONData(data_path)
    meme_templates = df['id'].count()
    
    makeDirectory(f'{output_path}/processedData/training')
    makeDirectory(f'{output_path}/processedData/testing')

    # fill in the data
    for template in range(meme_templates): 
        template_name = df.iloc[template]['name']  
        memes = df.iloc[template]['generated_memes'] 

        makeDirectory(f'{output_path}/processedData/training/{template}')
        makeDirectory(f'{output_path}/processedData/testing/{template}')
    
        random.shuffle(memes)

        # Limiting the number of images to download per class
        cutoff = min(100,len(memes))
        memes = memes[:cutoff]

        train_test_split_index = int(len(memes)*train_test_split_ratio)
        train_sample = memes[:train_test_split_index]
        test_sample = memes[train_test_split_index:]
        
        # Setup images to be downloaded         
        queue_samples_for_download = []

        for meme in train_sample:
            file_path = f'{output_path}/processedData/training/{template}/{meme["id"]}.jpg'
            img_url = f'http:{meme["image_url"]}'
            queue_samples_for_download.append((file_path,img_url))

        for meme in test_sample:
            file_path = f'{output_path}/processedData/testing/{template}/{meme["id"]}.jpg'
            img_url = f'http:{meme["image_url"]}'
            queue_samples_for_download.append((file_path,img_url))

        print(f'Class {template}: {template_name} started')
        
        downloadImages(queue_samples_for_download)


# Main Function
def main():    
    if len(sys.argv) != 3:
        print('Invalid number of arguments')

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if os.path.exists(input_path) and os.path.exists(output_path):
        print('Started Pre-Processing...')
        preprocess(input_path, output_path, 0.7)
        print('Done')
    else:
        print('Either the input or output path is invalid')


if __name__ == "__main__": 
    main()
    



