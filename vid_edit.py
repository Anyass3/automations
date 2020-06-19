##
## Simple video editor actually 
##

import os
import time
import string
from moviepy.editor import *
from concurrent.futures import ProcessPoolExecutor as thread

def vid_folder(path='files/trimmed_files',r=True):
    while os.path.isdir(path):
        if path.endswith(')'):
            digits=string.digits
            path_split=path.split('(')
            path_split[-1]=str(int(''.join([i for i in list(path_split[-1]) if i in digits]))+1)+')'
            path = '('.join(path_split)
        else:
            path += '(1)'
    os.mkdir(path)
    if r:
        return path

#this is a sub funtion of trim_video function
#so not advisable to run it
def equal_trim(vid_file, vid):
    try:
        num_of_trims=int(input('Please enter the number of trims to make: '))
    except ValueError:
        try:
            print('Invalid Entry')
            num_of_trims=int(input('Please re-enter the number of trims to make: '))
        except:
            print('Error!!! closing program')
            return
    lenght = vid_file.duration/num_of_trims
    start=0
    end=lenght
    path = vid_folder()
    for i in range(num_of_trims):
        #print(start, end)
        if start<60:
            if end == 60:
                name=f"{i+1}-({round(start)}, {round(end/60.0)} min).mp4"
            elif end > 60:
                name=f"{i+1}-({round(start)}, {round(end/60.0)} mins).mp4"
            else:
                name=f"{i+1}-({round(start)}, {round(end)} secs).mp4"
        else:
            name=f"{i+1}-({round(start/60.0)}, {round(end/60.0)} mins).mp4"
        name= os.path.join(path, name)
        #print(name)
        clip = VideoFileClip(vid)
        clip.subclip(start, end).write_videofile(name)
        clip.close()
        start+=lenght
        end+=lenght

#this is a sub funtion of specific_trim function
#so not advisable to run it
def _specific_trim_(trim_interval, vid, path, num):
    #print(start, end)
    path = path
    start, end = trim_interval.split(' ')
    start, end = int(start), int(end)
    i=num
    if start<60:
        if end == 60:
            name=f"{i+1}-({round(start)}, {round(end/60.0)} min).mp4"
        elif end > 60:
            name=f"{i+1}-({round(start)}, {round(end/60.0)} mins).mp4"
        else:
            name=f"{i+1}-({round(start)}, {round(end)} secs).mp4"
    else:
        name=f"{i+1}-({round(start/60.0)}, {round(end/60.0)} mins).mp4"
    name= os.path.join(path, name)
    #print(name)
    clip = VideoFileClip(vid)
    clip.subclip(start, end).write_videofile(name)
    clip.close()

#this is a sub funtion of trim_video function
#so not advisable to run it
def specific_trim(vid_file, vid):
    try:
        print('''
        Please note that the trim intervals should be entered in the form of=> a b; c d; etc 
        that is from a to b trim it and from c to d trim it and so on 
        Also the the units should be in seconds
        ''')
        trim_intervals=input('Please enter the trim intervals here: ').split(';')
        a,b=trim_intervals[0].split(' ')
    except ValueError:
        try:
            print('Invalid Entry')
            trim_intervals=input('Please re-enter the trim intervals here: ').split(';')
            a,b=trim_intervals[0].split(' ')
        except:
            print('Error!!! closing program')
            return
    path = vid_folder()
    with thread() as executor:
        vid=[vid]*len(trim_intervals)
        path=[path]*len(trim_intervals)
        num = range(len(trim_intervals))
        # [executor.submit(_specific_trim_(trim_interval, vid)) for trim_interval in trim_intervals]
        executor.map(_specific_trim_,trim_intervals, vid, path, num)

def trim_video(equal_len=False):
    t1 = time.perf_counter()
    print(
        '''
        this will be most useful for long video files
        
            Advanced Video Trimmer @me
    if equal_len equals to true
		This is a simple program thats trims a video file into equal lenghts
		based on the num of trims desired 
		and also it saves them in a new relative folder
		the longer the video the longer the waiting time
	else if one desires to input specific secs to trim the video then equal_len should be 	false
        Enjoy!!! let begin
        NOTE:   if the video is from a different folder then 
                when inputing the file name add also 
                the relative or absolute path 
        '''
    )
    vid = input('Please input the full video name including extention: ')
    try:
        vid_file=VideoFileClip(vid)
    except IOError:
        try:
            print('Error!!! Please check the the file name or path.')
            vid = input('Please re-input the full video name including extention: ')
            vid_file=VideoFileClip(vid)
        except:
            print('Error!!! closing program')
            return
    d=vid_file.duration
    if d<60:
        d=f"{round(d)} secs"
    elif d>60 and d<3600:
        d=f'{round(d/60.0)} mins'
    else:
        d=f"{round(d/3600.0)} hours"
    print(f"Your video's duration is: {d}")
    if equal_len:
        equal_trim(vid_file, vid)
    else:
        specific_trim(vid_file, vid)
    t2 = time.perf_counter()
    print(f'It took {t2-t1} secs to completed')

def convert_video(path, from_ext=None, to_ext='mp4', use_ffmpeg=False):
    if os.path.isdir(path):
        folder = input('input file name: ')
        for r, d, f in os.walk(path):
            files=[(os.path.join(r, file),(os.path.join(r, folder, file))) for file in f if file.split('.')[-1] == from_ext and not file.startswith('.')]
            print(files)
            vid_folder(os.path.join(r, folder))
            break
    elif os.path.isfile(path):
        files = [path]
    else:
        return 'path/file does not exist'
    for f in files:
        if f[0] == f[-1]:
            newpath = (f"{f[0].split('.')[0]}--converted.{to_ext}")
        else:
            newpath = (f"{f[-1].split('.')[0]}--converted.{to_ext}")
        print(newpath)
        if not use_ffmpeg:
            file = VideoFileClip(f[0])
            file.write_videofile(newpath)
            file.close()
	    else:
        	os.system(f'ffmpeg -i {f[0]} -vcodec copy -acodec copy {newpath}')

def count_audiolen(path):
    #not very usefull
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    suras=[]
    for s in files:
        f=AudioFileClip(s)
        suras.append(f.duration)
        f.close()
    a=0
    for s in suras:
        a+=s
    print(a)
