import re
import os
import time
import sys
import glob
from tqdm import tqdm
import pandas as pd
from google.cloud import translate_v2
from bs4 import BeautifulSoup

def doTranslate(cloudKey):
    path = input('Enter the full path to the chat csv: ').strip('\"')
    # load the CSV into a dataframe
    df = pd.read_csv(path,delimiter=',')
    # Put message column into a list
    mList = df['Message'].tolist()
    # Translated text list
    tList = []
    # Load the access key for google cloud api
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"{cloudKey}"

    # initialize the translation client
    translate_client = translate_v2.Client()

    # specify a target language
    target = 'en'

    # iterate through mList and translate the text
    for text in tqdm(mList):
        output = translate_client.translate(text,target_language=target)
        # append the translated text to tList
        tList.append(output['translatedText'])
        # print the output to the screen
        # print(output['translatedText'],end='')

    # Create a new column in the dataframe and set the contents of tList into it
    df['Translation'] = tList
    # print the new column
    print(df['Translation'])
    # export the new dataframe 
    df.to_csv('translated.csv')

def editChatPreview(path):
    with open(path,encoding='utf-8') as fp:
        soup = BeautifulSoup(fp,'html.parser')

    df = pd.read_csv('translated.csv',delimiter=',')
    messageNumber = df['Chat thread preview'].tolist()
    numbers = []
        
    for i in messageNumber:
        numbers.append(re.sub(r'^.*#','',i))

    for i in tqdm(numbers):
        div = soup.find(id=f'{i}')
        h = ''
        if div != None: # and len(str(div)) <= 1000:
            s = BeautifulSoup(str(div),'html.parser')
            old_tag = s.find(class_='message-text')
            # strip out the text from the div
            t = re.sub(r'<div class="message-text">','',str(old_tag))
            p = re.sub(r'</div>','',str(t))
            h = str(p.strip())
            # strip out the translated message from the CSV using the message ID
            x = df[df['Chat thread preview'].str.contains(i)]
            word = x['Translation'].item()
            v = ' ----Translation:   ' + word
            old_tag.append(v)
            soup.append(s)
            div.decompose()

    new = open('out.html','w',encoding='utf-8')
    for line in soup:
        new.write(str(line))
    new.close()

def option1():
    os.system('cls')
    print('Translate and Chat Preview')
    print('[!] This action requires a valid Google Cloud API key with the Translate API activated and permission to access it.')
    cloud = input('Do you have this?  [yes or no]: ')
    cloud = cloud.lower()
    if cloud == 'yes':
        cPath = input('Enter the full path to the cloud key.json file: ').strip('\"')
        doTranslate(cPath)
        # This part needs fixed
        filenames = glob.glob('D:\Cases\HTCU-2023-035\CASE\Export\Chat preview report\*.html')
        if len(filenames) > 1:
            num = 1
            for i in filenames:
                print(f'[{num}]{1}')
            answer = int(input('Which chat preview should I use: '))
            chatPreview = filenames[answer-1]
            editChatPreview(chatPreview)
        else:
            editChatPreview(filenames[0])
        
    elif cloud == 'no':
        print('This program requires that you have the API key.')
        print('Closing')
    
def option2():
    os.system('cls')
    print('Translate Only')
    print('[!] This action requires a valid Google Cloud API key with the Translate API activated and permission to access it.')
    cloud = input('Do you have this?  [yes or no]: ')
    cloud = cloud.lower()
    if cloud == 'yes':
        cPath = input('Enter the full path to the cloud key.json file: ').strip('\"')
        doTranslate(cPath)
    elif cloud == 'no':
        print('This program requires that you have the API key.')
        print('Closing')

def option3():
    os.system('cls')
    print('Chat Preview Only')
    filenames = glob.glob('./Chat preview report/*.html')
    tra = glob.glob('*.csv')
    if 'translate.csv' not in tra:
        print('It looks like you dont have the translate.csv file')
    else:    
        print(filenames[0])
        if len(filenames) > 1:
            num = 1
            for i in filenames:
                print(f'[{num}]{1}')
            answer = int(input('Which chat preview should I use: '))
            chatPreview = filenames[answer-1]
            editChatPreview(chatPreview)
        else:
            editChatPreview(filenames[0])

os.system('cls')
print('Select an option:')
selection = int(input('''
[1] Translate and Chat Preview
[2] Translate Only
[3] Chat Preview Only
'''))

if selection == 1:
    option1()
elif selection == 2:
    option2()
elif selection == 3:
    option3()
