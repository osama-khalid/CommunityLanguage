import re
file=open('beaut.html','r').read()

blocks=file.split('<span class="nameBlock ">')

for b in blocks:
	if b.find('postMessage')>-1:
		c=b.split('postMessage')
		if b.find('postContainer')>-1:
			time=c[0].split('dateTime"')[1].split('<')[0].strip(" ").strip(">")
			q=c
			d=c[1].split('postContainer')[0].split('</blockquote>')[0].replace('<br>','<>\n').replace('undefined<','<').replace('&quot;','"')
			x=d.find('>')
			d=re.sub('<.*?>', '<>', d[x:])
			X=d.replace('>undefined<','><').replace('><','').replace('&gt;','>').replace('<>','').replace('&#039;',"'").replace('>>>','>>').replace('undefined>','>')
			r=X.rfind('undefined')
			print(time)
			comment=X[:r]
			print(X[:r])
			print('\n')
		else:
			time=c[0].split('dateTime"')[1].split('<')[0].strip(" ").strip(">")
			d=c[1].split('thread-stats')
			p=d
			d=p[0].split('postContainer')[0].split('</blockquote>')[0].replace('<br>','<>\n').replace('undefined<','<').replace('&quot;','"')
			
			x=d.find('>')
			
			d=re.sub('<.*?>', '<>', d[x:])
			
			X=d.replace('>undefined<','><').replace('><','').replace('&gt;','>').replace('<>','').replace('&#039;',"'").replace('>>>','>>').replace('undefined>','>')
			r=X.rfind('undefined')
			print(time)
			comment=X[:r]
			print(X[:r])
			print('\n')
			
			