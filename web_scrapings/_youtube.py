import os
from math import ceil
import json
import time
import random
import dill
from datetime import datetime
import requests as r
import google.oauth2.credentials
from googleapiclient.discovery import build
import google_auth_oauthlib
from pytube import YouTube
from concurrent.futures import ThreadPoolExecutor as thread

# -*- coding: utf-8 -*-
import os

import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "web_scrapings/files/client_secret_web.json"
api_key = os.environ.get('YOUTUBE_API_KEY')

refresh_token = os.environ.get('REFRESH_TOKEN')
with open('web_scrapings/files/credentials.json', 'r') as json_token:
    refresh_token = json.load(json_token)['refresh_token']
with open(client_secrets_file) as cs_file:
    client_secrets = json.load(cs_file)
    client_id=client_secrets['web']['client_id']
    client_secret=client_secrets['web']['client_secret']
    token_uri=client_secrets['web']['redirect_uris'][0]

base_token_url = 'https://accounts.google.com/o/oauth2/token'

def authorize():
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file, scopes)
    flow.redirect_uri = 'http://127.0.0.1:5000/'

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        login_hint='nyassabu@gmail.com',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    code=input(f'follow link below to authorize\n{authorization_url}\npaste the code here: ')
    
    # code = "4/0QEdnIuhSJHWKWxHKJdKVuaaC3XNW1Ylo2UxwBNddcL8y0ydsbOAqwiKkgIj7BNWxT2wMCyXOUXe54ENDVdm55I"
    # state='sC2WZCetJP4b1iufi1gn015K6F7m3r'
    '''
    Now after getting the authorization code from the user. 
    We need to ensure that our program is siged in permanently(ie. if the user doesn't revoke the authorization)
    To do that we need to exchange the authorization code for a token(ie. Access Token) and refresh token
        as the access token expires within an hour.
        therefore the Refresh token is the most important
    The below code will do the exchange and with save the response in 'web_scrapings/files/resp.json'
    '''
    resp=f'code={code}&client_id={client_id}&client_secret={client_secret}&redirect_uri={flow.redirect_uri}&grant_type=authorization_code'
    p=f'''
    curl \\
    --request POST \\
    --data "{resp}" \\
    {base_token_url} > web_scrapings/files/resp.json
    '''
    os.system(p)

def generate_token():
    '''
    #*this will generate a new access token everytime it is run from the refresh token
    the access token expires within an hour
    so a simple logic is implemented which will run this function everytime the program is executed
        this is done by saving the time it was run in a pickle file
        #*so everytime the program is run the time in the pickle file is checked against the current time
        if it is more than an hour this function is run again
        #*the checker is below the funtion
    '''
    resp=f'client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}&grant_type=refresh_token'
    p=f'''
    curl \\
    --request POST \\
    --data "{resp}" \\
    {base_token_url} > web_scrapings/files/token.json
    '''
    os.system(p)
    with open('web_scrapings/files/token.json') as json_token:
        try:
            token = json.load(json_token)['access_token']
        except:
            print("invalid_grant")
            return
    with open('web_scrapings/files/credentials.json', 'r') as json_token:
        _credentials_ = json.load(json_token)
        _credentials_['token'] = token
        _credentials_['refresh_token'] = refresh_token
        _credentials_['token_uri'] = token_uri
        _credentials_['client_id'] = client_id
        _credentials_['client_secret'] = client_secret
        _credentials_['scopes'] = scopes
    with open('web_scrapings/files/credentials.json', 'w') as json_token:
        json.dump(_credentials_, json_token)
    with open('web_scrapings/files/time.pkl', 'wb') as t:
        dill.dump(datetime.utcnow(), t)

with open('web_scrapings/files/time.pkl', 'rb') as t:
    time_pkl = dill.load(t)
if time_pkl:
    if (datetime.utcnow()-time_pkl).seconds/3600 >= 1:
        generate_token()
with open('web_scrapings/files/credentials.json') as json_token:
    _credentials = json.load(json_token)

credentials = google.oauth2.credentials.Credentials(**_credentials)
#print(credentials)
youtube = build(api_service_name, api_version, credentials=credentials)

def get_vid_id(link='https://youtu.be/LoBJOkhtDQQ'):
    return link.split('/')[-1].split('=')[-1]

def rate(id="wLahz_owheU",r=1):
    id=get_vid_id(id)
    try:
        r -= 1
        ratings=['like', 'dislike', 'none']
        request = youtube.videos().rate(
            id=id,
            rating=ratings[r],
            prettyPrint=True
        )
        request.execute()
        print(id)
    except:
        print('connection error')

def channal(part='statistics',forUsername='schafer5'):
    request = youtube.channels().list(
            part=part,
            forUsername=forUsername
        )
    response = request.execute()
    return json.dumps(response, sort_keys=True, indent=4)

class Playlist():
    def __init__(self, part='snippet',playlistId='PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH', videoId=None, prev=0 ,next_=0):
        self.part=part
        self.playlistId=playlistId
        self.videoId=videoId
        self.prev=prev
        self.next=next_
        self.request,self.response,self.json_data=self.items()
        self.total=self.response['pageInfo']['totalResults']
        self.per_page=self.response['pageInfo']['resultsPerPage']
        self.no_of_pages=ceil(self.total/self.per_page)
        to_print = f'| totalResults: {self.total} | resultsPerPage: {self.per_page} | No Of Pages: {self.no_of_pages} |'
        print('*'*len(to_print))
        print(to_print)
        print('*'*len(to_print))

    def items(self):
        request = youtube.playlistItems().list(
                part=self.part,
                playlistId=self.playlistId,
                videoId=self.videoId
            )
        response = request.execute()
        return request,response,json.dumps(response, sort_keys=True, indent=4)
    
    @property
    def get_responeses(self):
        request=self.request
        response = self.response
        responses=[response]
        for i in range(self.no_of_pages):
            request=youtube.playlistItems().list_next(request,response)
            
            try:
                response=request.execute()
                responses.append(response)
            except:
                break
        return responses
    
    def go_to_page(self,n=0, jsn=False):
        request=self.request
        response = self.response
        for i in range(self.no_of_pages):
            request=youtube.playlistItems().list_next(request,response)
            response=request.execute()
            try:
                print(response['nextPageToken'])
            except:
                print(response['prevPageToken'])
                break
            if n == i:
                break
        if n > self.no_of_pages:
            print(f'Remember the number of pages is not more {self.no_of_pages}.\nSo the last page will be returned')
            time.sleep(3)
        if jsn:
            return json.dumps(response, sort_keys=True, indent=4)
        else:
            return response
        # return response,json.dumps(response, sort_keys=True, indent=4)
    
    def snippets(self, dict_key=None, all=False,jsn=False):
        if dict_key:
            if all:
                all_resp = self.get_responeses
                return [response['items'][i]['snippet'][dict_key] for i in range(self.per_page) for response in all_resp]
            else:
                return [self.response['items'][i]['snippet'][dict_key] for i in range(self.per_page)]
        else:
            print('A key parameter is required to view a specific snippet\n')
            time.sleep(1)
            print('printing a full random snippet dictionary without a specific key\n\n')
            time.sleep(1)
            all_resp = self.get_responeses
            if jsn:
                response = random.choice(all_resp)
                snippets = random.choice(response['items'])['snippet']
                return json.dumps(snippets, sort_keys=True, indent=4)
            else:
                response = random.choice(all_resp)
                return random.choice(response['items'])['snippet']

    def video_links(self,all=False):
        videoIds = [item['videoId'] for item in self.snippets('resourceId', all)]
        return [f'https://www.youtube.com/watch?v={id}' for id in videoIds]

    def thumbnails(self,all=False,size=1):
        negetive=''
        if '-' in str(size):
            #so that it will raise an exception because negetive values are not allowed
            size = 10
            negetive='. Only positive numbers are allowed\n'
        size -= 1
        sizes=['default','medium','high','standard','maxres']
        try:
            thumbnails = [item[sizes[size]]['url'] for item in self.snippets('thumbnails', all)]
        except:
            print(f'An error occured \n{negetive} NOTE: The indexes ranges from 1 to 5')
            time.sleep(1)
            print('\nIf you specified the correct indexes, then that index value is not among that playlist Thumbnails\n')
            time.sleep(1)
            print("\nThe index values are 'default','medium','high','standard','maxres'")
            time.sleep(1)
            try:
                thumbnails = [item[sizes[-1]]['url'] for item in self.snippets('thumbnails', all)]
                print('Returning the maxres\n')
                time.sleep(3)
            except:
                thumbnails = [item[sizes[-2]]['url'] for item in self.snippets('thumbnails', all)]
                print('Printing the standard\n')
                time.sleep(3)
        return [id for id in thumbnails]

    def download(self, save_path='web_scrapings/files/downloads', ext='mp4', res='720p',typ='video'):
        videos = self.video_links(all=1)
        with thread() as executor:
            save_path = [save_path] * len(videos)
            ext = [ext] * len(videos)
            res = [res] * len(videos)
            typ = [typ] * len(videos)
            executor.map(download_vid, videos, save_path, ext, res, typ)

def download_vid(url, save_path='web_scrapings/files/downloads', ext='mp4', res='480p', typ='video'):
    t1=time.perf_counter()
    downloaded = False#this is just to help me check if a media is downloaded or not
    video_id = get_vid_id(url)
    url = f'https://www.youtube.com/watch?v={video_id}'
    print(url)
    _media_ = YouTube(url)
    _media = _media_.streams.filter(type=typ)
    print(f'video of: {_media_.author}\nviews: {_media_.views}\nvideo title: {_media_.title}\nratings: {_media_.rating}')
    if typ == 'video':
        media = _media.filter(file_extension=ext).filter(progressive=True)
        if not media.first():
            media = _media.filter(file_extension='mp4')
        try:
            vid = media.filter(res=res)[0].download(save_path)
            downloaded=True
        except:
            print(f'\nThe resolution {res} which you provided could not be downloaded')
            print('\nI am going to try other resolutions starting from the best posible quality')
            time.sleep(1)
            resolutions = ['1080p', '720p', '480p', '360p', '144p']
            if res in resolutions:
                resolutions.remove(res)
            print(f'\nresolutions: {resolutions}')
            for rs in resolutions:
                try: 
                    vid = media.filter(res=rs)[0].download(save_path)
                    print(f'\nDownloaded: {media.filter(res=rs)[0]}')
                    downloaded=True
                    break
                except:
                    continue
    elif typ == 'audio':
        try:
            _media.first().download(save_path)
            downloaded=True
        except:
            for a in _media:
                try:
                    a.download(save_path)
                    print(f'Downloaded {a}')
                    downloaded = True
                    break
                except:
                    continue
    if not downloaded:
        print(f'\nSorry could not download {_media_.title}'.upper())
    t2=time.perf_counter()
    print(f'\nIt took {t2 - t1 } secs to complete')

# CAUQAA
# CAoQAA
# "prevPageToken": "CAoQAQ"
# pageInfo
