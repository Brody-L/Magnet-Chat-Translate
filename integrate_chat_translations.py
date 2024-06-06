import re
import pandas as pd
from bs4 import BeautifulSoup

with open('./Chat preview report/iOS iMessage_SMS_MMS-5_23_2023 1_25_59 PM.html',encoding='utf-8') as fp:
    soup = BeautifulSoup(fp,'html.parser')

df = pd.read_csv('translated.csv',delimiter=',')
messageNumber = df['Chat thread preview'].tolist()
numbers = []
    
for i in messageNumber:
    numbers.append(re.sub(r'^.*#','',i))


for i in numbers:
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
