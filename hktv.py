# -*- coding: utf-8 -*-
#!/usr/bin/env python
#hktv.py
# HKTV香港電視
 
import httplib, urllib, hashlib, time, urllib2, xbmcplugin, xbmcgui, xbmc, xbmcaddon

p1080 = ''
p720 = ''
p576 = ''
 
def generateSignature(file, time1, qsv):
 m =  hashlib.md5()
 m.update(''.join([file,qsv,'43e814b31f8764756672c1cd1217d775',time1]))
 return m.hexdigest()

def generatetoken(ts):
    ki = '12'
    muid = '0'
    s1 = generateSignature('account/token',ts,''.join([ki,'0']))
    params = urllib.urlencode({'ki': ki, 'ts': ts, 's': s1, 'muid': muid})
    headers = {"Content-type": "application/x-www-form-urlencoded"
                    , "Accept": "text/plain"}
    httpClient = httplib.HTTPConnection("webservices.hktv.com.hk", 80, timeout=30)
    httpClient.request("POST", "/account/token", params, headers)
 
    response = httpClient.getresponse()
    #print response.status
    #print response.reason
    data1 = response.read()
    #print response.getheaders() #?????
    t_s = data1.find('token')
    t_e = data1.find('"',t_s+8)
    if httpClient:
        httpClient.close()
    return data1[t_s+8:t_e-len(data1)]

def generatelink(ts):
    ki = '12'
    muid = '0'
    ts = str(int(time.time()))
    token1 = generatetoken(ts)
    print token1
    vid = '1'
    uid = '1'
    d = 'USB Android TV'
    mf = 'SONY'
    mdl = 'C1905'
    os = '4.1.2'
    udid = '00000000-0000-0000-0000-000000000000'
    mxres = '1920' #maximum screen dimension
    net = 'fixed' #3G/4G/fixed/wifi
    s2 = generateSignature('playlist/request',ts,''.join([d,ki,mdl,mf,mxres,net,os,token1,udid,uid,vid]));

def main():
 httpClient = None
 try:
    data1 = ''
    data2 = ''
    ki = '12'
    muid = '0'
    ts = str(int(time.time()))
    token1 = generatetoken(ts)
    #print token1
    vid = '1'
    uid = '1'
    d = 'USB Android TV'
    mf = 'SONY'
    mdl = 'C1905'
    os = '4.1.2'
    udid = '00000000-0000-0000-0000-000000000000'
    mxres = '1920' #maximum screen dimension
    net = 'fixed' #3G/4G/fixed/wifi
    s2 = generateSignature('playlist/request',ts,''.join([d,ki,mdl,mf,mxres,net,os,token1,udid,uid,vid]));
    params1 = urllib.urlencode({
             'd': d,
             'ki': ki,
             'mdl': mdl,
             'mf': mf,
             'mxres': mxres,
             'net': net,
             'os': os,
             't': token1,
             'udid': udid,
             'uid': uid,
             'vid': vid,
             'ts':ts,
             's': s2,
             })
    headers1 = {"Content-type": "application/x-www-form-urlencoded"
                    , "Accept": "text/plain"}
    httpClient1 = httplib.HTTPConnection("ott-www.hktvmall.com", 80, timeout=30)
    httpClient1.request("POST", "/api/playlist/request", params1, headers1)
    response1 = httpClient1.getresponse()
    #print response1.status
    #print response1.reason
    data2 = response1.read()
    #print response1.getheaders() #?????
    l_s = data2.find('http')
    l_e = data2.find('"',l_s)
    surl = data2[l_s:l_e-len(data2)]
    if httpClient1:
        httpClient1.close()
    httpClient2 = httplib.HTTPConnection("webservices.hktv.com.hk", 80, timeout=30)
    httpClient2.request("POST", "/playlist/request", params1, headers1)
    response2 = httpClient2.getresponse()
    data4 = response2.read()
    if httpClient2:
        httpClient2.close()
    l_s = data4.find('http')
    l_e = data4.find('"',l_s)
    surl2 = data4[l_s:l_e-len(data4)]
    data3 = urllib2.urlopen(surl).read()
    data4 = urllib2.urlopen(surl2).read()
    global p1080
    global p720
    global p576
    p576_pos = data3.find('576p')
    if p576_pos != -1:
        p576_pos_s = data3.rfind('http://',0,p576_pos)
        p576_pos_e = data3.find('\n',p576_pos)
        p576 = data3[p576_pos_s:p576_pos_e-len(data3)-1]
    else:
        p576 = ''
    p720_pos = data4.find('1280x720')
    if p720_pos != -1:
        p720_pos_s = data4.find('http://',p720_pos)
        p720_pos_e = data4.find('\n',p720_pos+p720_pos_s)
        p720 = data4[p720_pos_s:p720_pos_e-len(data4)-1]
    else:
        p720_pos = data3.find('720p')
        if p720_pos != -1:
            p720_pos_s = data3.rfind('http://',0,p720_pos)
            p720_pos_e = data3.find('\n',p720_pos)
            p720 = data3[p720_pos_s:p720_pos_e-len(data3)-1]
        else:
            p720 = ''
    p1080_pos = data4.find('1920x1080')
    if p1080_pos != -1:
        p1080_pos_s = data4.find('http://',p1080_pos)
        p1080_pos_e = data4.find('\n',p1080_pos+p1080_pos_s)
        p1080 = data4[p1080_pos_s:p1080_pos_e-len(data4)-1]
    else:
        p1080_pos = data3.find('1080p')
        if p1080_pos != -1:
            p1080_pos_s = data3.rfind('http://',0,p1080_pos)
            p1080_pos_e = data3.find('\n',p1080_pos)
            p1080 = data3[p1080_pos_s:p1080_pos_e-len(data3)-1]
        else:
            p1080 = ''
    #if returnres == '1080p':
       #return p1080
    #if returnres == '720p':
       #return p720
    #if returnres == '576p':
       #return p576
 except Exception, e:
    print e
 #finally:
    #print ts
    #print ki
settings = xbmcaddon.Addon(id='plugin.video.hktv')
selres_set = int(settings.getSetting("sel_res"))
url=''
handle=int(sys.argv[1])
#listitem=xbmcgui.ListItem(settings.getSetting("sel_res"))
#xbmcplugin.addDirectoryItem(handle, url, listitem)
directsurl = ''
lsres = ''
main()
if selres_set >= 2 and p1080 != '':
    directsurl = p1080
    lsres = '1080P'
elif selres_set >= 1 and p720 != '':
    directsurl = p720
    lsres = '720P'
elif selres_set >= 0 and p576 != '':
    directsurl = p576
    lsres = '576P'
listitem1=xbmcgui.ListItem (label='HKTV',path=directsurl)
listitem1.setInfo('video', {'Title': 'HKTV ' + lsres})
player1 = xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER)
__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
language = xbmc.getLanguage()
if language == "Chinese (Traditional)":
    line1 = "因為689，網絡塞死無得睇"
else:
    line1 = "Sorry! Network Traffic Jam"
time2 = 5000  #in miliseconds
if directsurl == '':
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time2, __icon__))
else:
    player1.play(directsurl,listitem1)
time.sleep(10)
listitem1.setInfo('video', {'Title': 'test'})
player1.play(directsurl,listitem1)
