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
client_secrets_file = "files/client_secret_web.json"
api_key = os.environ.get('YOUTUBE_API_KEY')

refresh_token = os.environ.get('REFRESH_TOKEN')
with open('files/credentials.json', 'r') as json_token:
    refresh_token = json.load(json_token)['refresh_token']
with open(client_secrets_file) as cs_file:
    client_secrets = json.load(cs_file)
    client_id=client_secrets['web']['client_id']
    client_secret=client_secrets['web']['client_secret']
    token_uri=client_secrets['web']['redirect_uris'][0]

base_token_url = 'https://accounts.google.com/o/oauth2/token'

def authorize():
    '''
    this function should be called once
    You will need curl to be able to do this
    '''
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file, scopes)
    flow.redirect_uri = 'http://127.0.0.1:5000/'

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        #login_hint='nyassabu@gmail.com',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    code=input(f'\nfollow link below to authorize:\n\n{authorization_url}\n\npaste the code here: ')
    
    '''
    Now after getting the authorization code from the user. 
    We need to ensure that our program is signed in permanently(ie. if the user doesn't revoke the authorization)
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
    {base_token_url} > files/token.json
    '''
    os.system(p)
    with open('files/token.json') as json_token:
        try:
            token = json.load(json_token)['access_token']
        except:
            print("invalid_grant")
            return
    with open('files/credentials.json', 'r') as json_token:
        _credentials_ = json.load(json_token)
        _credentials_['token'] = token
        _credentials_['refresh_token'] = refresh_token
        _credentials_['token_uri'] = token_uri
        _credentials_['client_id'] = client_id
        _credentials_['client_secret'] = client_secret
        _credentials_['scopes'] = scopes
    with open('files/credentials.json', 'w') as json_token:
        json.dump(_credentials_, json_token)
    with open('files/time.pkl', 'wb') as t:
        dill.dump(datetime.utcnow(), t)
def _generate_token_():
    '''
    this is the checker for the generate_token function as described in it.
    '''
    with open('files/time.pkl', 'rb') as t:
        time_pkl = dill.load(t)
    if time_pkl:
        if (datetime.utcnow()-time_pkl).seconds/3600 >= 1:
            generate_token()

_generate_token_()
with open('files/credentials.json') as json_token:
    _credentials = json.load(json_token)

credentials = google.oauth2.credentials.Credentials(**_credentials)
#print(credentials)
youtube = build(api_service_name, api_version, credentials=credentials)

def get_vid_id(link='https://youtu.be/LoBJOkhtDQQ'):
    return link.split('/')[-1]

def upload():
    pass
def update():
    pass
def delete():
    pass

def rate(id="wLahz_owheU",r=1):
    '''
    id = the youtube videoId but you can also write the youtube video link
    this will rate any youtube video
        'like' r=1, 'dislike' r=2, 'none' r=3
    '''
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
    
    def go_to_page(self,n=1, jsn=False):
        n -= 1
        if n < 0:
            n = 0
        request=self.request
        response = self.response
        if n > self.no_of_pages:
            print(f'Remember the number of pages is not more {self.no_of_pages}.\nSo the last page will be returned')
            time.sleep(2)
            n=self.no_of_pages
        for i in range(n):
            r=youtube.playlistItems().list_next(request,response)
            request = r
            response=request.execute()
            try:
                print(response['nextPageToken'])
            except:
                print(response['prevPageToken'])
                break
            # if n == i:
            #     break
        if jsn:
            return json.dumps(response, sort_keys=True, indent=4)
        else:
            return response
        # return response,json.dumps(response, sort_keys=True, indent=4)
    
    def snippets(self, dict_key=None, all=False,jsn=False):
        if dict_key:
            if all:
                all_resp = self.get_responeses
                # to_be_returned = [response['items'][i]['snippet'][dict_key] for i in range(len(response['items'])) for response in all_resp]
                to_be_returned = []
                for response in all_resp:
                    try:
                        to_be_returned += [response['items'][i]['snippet'][dict_key] for i in range(len(response['items']))]
                    except:
                        break
                return to_be_returned
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

    def download(self, save_path='files/downloads', ext='mp4', res='720p',typ='video'):
        videos = self.video_links(all=1)
        with thread() as executor:
            save_path = [save_path] * len(videos)
            ext = [ext] * len(videos)
            res = [res] * len(videos)
            typ = [typ] * len(videos)
            executor.map(download_vid, videos, save_path, ext, res, typ)

def download_vid(url, save_path='files/downloads', ext='mp4', res='480p', typ='video'):
    t1=time.perf_counter()
    downloaded = False#this is just to help me check if a media is downloaded or not
    if not [1 for i in ('http', 'youtub', '.com') if i in url]:
        url = f'https://www.youtube.com/watch?v={url}'
    print(url)
    _media_ = YouTube(url)
    title=_media_.title.replace(' ', '_').replace('#', '')

    details = (f'video of: {_media_.author}\nviews: {_media_.views}\nvideo title: {title}\nratings: {_media_.rating}')
    _media = _media_.streams.filter(type=typ)
    media = _media.filter(file_extension=ext)
    if not media.first():
        ext = 'mp4'
        media = _media.filter(file_extension=ext)
    try:
        vid = media.filter(res=res).filter(progressive=True).first()
        print(f'This is vid: {vid}')
        if vid:
            print('there is vid')
            vid.download(save_path)
        else:
            join_v_a(save_path,res, ext, title)
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
                vid = media.filter(res=rs).filter(progressive=True)[0]
                if vid:
                    vid.download(save_path)
                else:
                    join_v_a(save_path,res, ext, title)
                print(f'\nDownloaded: {media.filter(res=rs)[0]}')
                downloaded=True
                break
            except:
                continue
    if not downloaded:
        print(f'\nSorry could not download {_media_.title}'.upper())
    t2=time.perf_counter()
    print(f'\nIt took {t2 - t1 } secs to complete')

def join_v_a(save_path,res, ext, title):
    '''
    this function will be called when progressive is False
    that is the video downloaded is without a sound so we are to 
    download the sound and the video indipendently and later merge them
    together
    '''
    media.filter(res=res).first().download(save_path, filename='_yt_v')
    _media_.streams.filter(type='audio').filter(file_extension=ext).filter(progressive=False).first().download(save_path, filename='_yt_a')
    command = f"ffmpeg -i {save_path}_yt_v.{ext} -i {save_path}_yt_a.{ext} -c copy {save_path}'{title}'.{ext}"
    os.system(command)
    os.remove(f'{save_path}_yt_v.{ext}')
    os.remove(f'{save_path}_yt_a.{ext}')