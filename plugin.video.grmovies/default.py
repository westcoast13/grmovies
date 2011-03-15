import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os, sys

# greek-movies.com xbmc plugin.
# created by westcoast13

#get path to me
osPath=os.getcwd()
pluginPath='special://profile/addon_data/plugin.video.grmovies'

def xbmcpath(path,filename):
    translatedpath = os.path.join(xbmc.translatePath( path )+'/resources/', ''+filename+'')
    return translatedpath

def getMyURL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
 
    return link

def CATEGORIES():
        addDir('Movies','http://www.greek-movies.com/movies.php',1,xbmcpath(osPath, 'movies.jpg') )
        addDir( 'Music','http://www.greek-movies.com/music.php',2,xbmcpath(osPath, 'music.jpg') )

def MOVIE_CATEGORIES(url):
        link=getMyURL(url)
        match=re.compile('<option selected value="(.+?)">(.+?)</option>').findall(link)
        for url,name in match:
                name=name.replace(" (all)","")
                addDir(name,'http://www.greek-movies.com/'+url,10,xbmcpath(osPath, 'movies.jpg'))

def MOVIE_INDEXES(url,name):
        link=getMyURL(url)
        link=link.replace(' (all)','')
        match=re.compile(name+'</option>(.+?)</select>').findall(link)
        for temp in match:
                print 'temp value is *************** ' + temp
                match2=re.compile('<option value="(.+?)"><p class="index">(.+?)</p></option>').findall(temp)
                for url,name in match2:
                        addDir(name,'http://www.greek-movies.com/'+url,100,xbmcpath(osPath, 'movies.jpg'))

def MOVIES_LIST(url):
        link=getMyURL(url)
        match=re.compile('<p class="movieheading1">(.+?)</p><center><a href="(.+?)"><IMG SRC="(.+?)" width=180 BORDER=0></a>').findall(link)
        for name,url,thumbnail in match:
                addDir(name,'http://www.greek-movies.com/'+url,1000,'http://www.greek-movies.com/'+thumbnail)

def ARTISTS(url):
        link=getMyURL(url)
        match=re.compile('<p class="artist(.+?)"><a name="(.+?)" href="(.+?)">(.+?)</a></p>').findall(link)
        for junk,junk,url,name in match:
                addDir(name,'http://www.greek-movies.com/'+url,20,xbmcpath(osPath, 'music.jpg'))

def ALBUMS(url):
        link=getMyURL(url)
        match=re.compile('<p class="album(.+?)"><a href="(.+?)">(.+?)</a></p>').findall(link)
        for junk,url,name in match:
                link=getMyURL('http://www.greek-movies.com/'+url)
                match=re.compile('<center><img src="(.+?)"').findall(link)
                for thumbnail in match:
                        addDir(name,'http://www.greek-movies.com/'+url,200,'http://www.greek-movies.com/'+thumbnail)

def SONGS(url):
        link=getMyURL(url)
        match=re.compile('<p class="song(.+?)"><a href="(.+?)">(.+?)</a></p>').findall(link)
        for junk,url,name in match:
                link=getMyURL('http://www.greek-movies.com/'+url)
                match=re.compile('<param name="movie" value="http://www.youtube.com/v/(.+?)&rel=1&autoplay=1"></param>').findall(link)
                for url2 in match:
                        addLink(name,'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url2,'')

def VIDEOLINKS(url,name):
        link=getMyURL(url)
        link=link.replace('watch%3Fv%3D','')
        link=link.replace('videoplay%3Fdocid%3D','')
        link=link.replace('videos%3Fv%3D','')
        link=urllib.quote(link,'"<> =/')
        match=re.compile('<a class="episodetitle" href="view.php%3Furl=http%253A%252F%252F(.+?)%252F(.+?)" target="_blank">(.+?)</a>').findall(link)
        print 'after compile'
        for host,url,name2 in match:
                #print 'name2 is *****' + name2 + '*****'
                realname=""
                if host.startswith('www.youtube.com'):
                    realname=name + " | YouTube"
                    if name2.startswith('<b>youtube</b>')==False:
                        realname=realname + " | " + name2
                    addLink(realname,'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url,xbmcpath(osPath, 'youtube-logo.png'))
                elif host.startswith('vimeo.com'):
                    realname=name + " | Vimeo"
                    if name2.startswith('<b>vimeo</b>')==False:
                        realname=realname + " | " + name2
                    addLink(realname,'plugin://plugin.video.vimeo/?action=play_video&videoid=%s' % url,xbmcpath(osPath, 'vimeo-logo.jpg'))
                elif host.startswith('www.datemule.com'):
                    realname=name + " | DateMule"
                    if name2.startswith('<b>datemule</b>')==False:
                        realname=realname + " | " + name2
                    link=getMyURL('http://www.datemule.com/videos?v='+url)
                    match2=re.compile('  <iframe src="(.+?)"').findall(link)
                    for url2 in match2:
                        link=getMyURL(url2)
                        match3=re.compile('<source src="(.+?)" type="video/mp4"').findall(link)
                        for url3 in match3:
                            print ' URL2 DATEMULE *************** ' +str(url3)
                            addLink(realname,url3,xbmcpath(osPath, 'datemule-logo.png'))
                elif host.startswith('video.google.com'):
                    realname=name + " | Google Video"
                    if name2.startswith('<b>google</b>')==False:
                        realname=realname + " | " + name2
                    link=getMyURL('http://video.google.com/videoplay?docid='+url+'#')
                    match2=re.compile('videoUrl(.+?)thumbnailUrl').findall(link)
                    #'videoUrl\x3d(.+?)\x26thumbnailUrl'
                    for url2 in match2:
                        url2=url2.replace('\\x3d','')
                        url2=url2.replace('\\x26','')
                        print "Google URL is ************* " + urllib.unquote(url2)
                        addLink(realname,urllib.unquote(url2),xbmcpath(osPath, 'google-logo.jpg'))
                #print 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
                #print name+' '+name2
                #addLink(name+' '+name2,'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url,xbmcpath(osPath, 'youtube-logo.png'))
                #addLink(name+' '+name2,'http://n64.stagevu.com/v/120d60f7bdc424ec6d7a95569e761b94/eylaoiegyssa.avi','http://www.technologos.eu/wp-content/uploads/2010/04/youtube-logo.png')
        

                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable', 'true')
        contextMenuItems = []
        contextMenuItems.append(('test', 'XBMC.RunPlugin(%s?mode=999&name=%s&url=%s)' % ('plugin://plugin.video.grmovies', name, urllib.quote_plus(url))))
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        MOVIE_CATEGORIES(url)
        
elif mode==10:
        print ""+url
        MOVIE_INDEXES(url,name)

elif mode==100:
        print ""+url
        MOVIES_LIST(url)

elif mode==1000:
        print ""+url
        VIDEOLINKS(url,name)

elif mode==2:
        print ""+url
        ARTISTS(url)

elif mode==20:
        print ""+url
        ALBUMS(url)


elif mode==200:
        print ""+url
        SONGS(url)

elif mode==999:
        print "Test menu activated "+name
        addDir(name,url,mode,xbmcpath(osPath, 'datemule-logo.png'))


xbmcplugin.endOfDirectory(int(sys.argv[1]))
