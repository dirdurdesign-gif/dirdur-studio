#!/usr/bin/env python3
"""Generate a static entry page per route (e.g. /mi-ze-shem/index.html) from index.html,
each with its own title, description and canonical URL for search engines, plus 404.html
and sitemap.xml. Run from the repo root after editing index.html:  python3 tools/build_pages.py"""
import json,re,os,html,shutil
BASE='https://dirdurstudio.com'
s=open('index.html',encoding='utf-8').read()
def obj(key,start=0):
    i=s.index(key,start)+len(key)-1
    return json.JSONDecoder().raw_decode(s,i)[0]
SLUG=obj('var SLUG={')
order=[str(x) for x in obj('"order": [')]
pv_start=s.index('var PV=')
HE=obj('"he": {',pv_start); TXT=obj('"txt": {',pv_start)
def esc(x):return html.escape(x,quote=True)
def page(path,title,desc):
    t=s
    url=BASE+path
    t=re.sub(r'<title>.*?</title>','<title>%s</title>'%esc(title),t,count=1)
    t=re.sub(r'(<meta name="description" content=")[^"]*(")',lambda m:m.group(1)+esc(desc)+m.group(2),t,count=1)
    t=re.sub(r'(<meta property="og:title" content=")[^"]*(")',lambda m:m.group(1)+esc(title)+m.group(2),t,count=1)
    t=re.sub(r'(<meta property="og:description" content=")[^"]*(")',lambda m:m.group(1)+esc(desc)+m.group(2),t,count=1)
    t=re.sub(r'(<meta property="og:url" content=")[^"]*(")',lambda m:m.group(1)+url+m.group(2),t,count=1)
    t=re.sub(r'(<link rel="canonical" href=")[^"]*(")',lambda m:m.group(1)+url+m.group(2),t,count=1)
    t=re.sub(r'(<link rel="alternate" hreflang="he" href=")[^"]*(")',lambda m:m.group(1)+url+m.group(2),t,count=1)
    t=re.sub(r'(<link rel="alternate" hreflang="en" href=")[^"]*(")',lambda m:m.group(1)+url+'?lang=en'+m.group(2),t,count=1)
    t=re.sub(r'(<link rel="alternate" hreflang="x-default" href=")[^"]*(")',lambda m:m.group(1)+url+m.group(2),t,count=1)
    d=path.strip('/')
    os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(t)
    return url
# clear old generated folders
for d in list(SLUG.values())+['about','contact','accessibility']:
    if os.path.isdir(d):shutil.rmtree(d)
urls=[BASE+'/']
for k in order:
    if k not in SLUG:continue
    name=HE.get(k,[SLUG[k]])[0]
    desc=re.sub(r'\s+',' ',(TXT.get(k) or '').replace('\n',' ')).strip()
    if len(desc)>155:desc=desc[:152].rsplit(' ',1)[0]+'…'
    urls.append(page('/'+SLUG[k]+'/',name+' | DIRDUR STUDIO דירדור סטודיו',desc or name))
urls.append(page('/about/','אודות | DIRDUR STUDIO דירדור סטודיו','DIRDUR STUDIO הוא סטודיו למיתוג ולעיצוב גרפי של המעצב הגרפי אדיר סיגרון, המחבר בין אסטרטגיה, תרבות ושפה חזותית.'))
urls.append(page('/contact/','צור קשר | DIRDUR STUDIO דירדור סטודיו','ספרו לנו על הפרויקט שלכם: מיתוג, עיצוב לוגו, אריזות, פוסטרים וטאמבניילים. DIRDUR STUDIO – אדיר סיגרון.'))
urls.append(page('/accessibility/','הצהרת נגישות | DIRDUR STUDIO','הצהרת הנגישות של אתר DIRDUR STUDIO.'))
shutil.copyfile('index.html','404.html')
sm=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for u in urls:
    sm.append('  <url><loc>%s</loc><xhtml:link rel="alternate" hreflang="he" href="%s"/><xhtml:link rel="alternate" hreflang="en" href="%s?lang=en"/></url>'%(u,u,u))
sm.append('</urlset>')
open('sitemap.xml','w',encoding='utf-8').write('\n'.join(sm)+'\n')
print(len(urls),'urls')
