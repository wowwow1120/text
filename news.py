#/!/usr/bin/python

#-*-coding:utf-8-*-

import os, re
import sys
import html

if __name__ == '__main__':
    target_dir = sys.argv[1]
    out_dir = '/home/minds/maum/resources/MRC/' + sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)

    open_dir = os.listdir(target_dir)
    for f in open_dir :
        with open (target_dir + '/'+ f, 'r') as ff:
            news = ff.read()
        news = news.replace('\n','')
   
        r = re.compile(r'<DataContent>(.*?)\<\/DataContent\>')
        if re.search(r, news):
            con = re.search(r, news).group(1)
            con = con.replace('<![CDATA[','').replace(']]>','')
            con = html.unescape(con)
            con = re.sub(r'\ +', ' ', con)
            
        if len(con) >= 2000:
            l = '/long_'
        elif len(con) < 2000 and len(con) >= 800:
            l = '/mid_'
        elif len(con) < 800 and len(con) >= 300:
            l = '/short_'
        else:
            continue

        with open(out_dir + l + f.split('.')[1] + '.txt', 'w') as new:
            new.write(con)
