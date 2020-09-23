###
import os
import time
from flask import Flask, render_template, url_for, flash, redirect,abort
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
import secrets
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from pytube import YouTube

app = Flask(__name__)

app.config['SECRET_KEY'] = '1429964e1d66d029a7568398662aafdd'

class downloadForm(FlaskForm):
    url = StringField('VideoID or Video URL', validators=[DataRequired('Common Ibrahim please enter a video link or ID')])
    ext = SelectField('Video Extention', choices=[(1,'mp4'), (2,'webm')], coerce=int, validators=[DataRequired()])
    res = SelectField('Video Resolution', choices=[(1,'1080p'), (2,'720p'), (3,'480p'), (4,'360p'), (5, '144p')], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Download')

@app.route('/', methods=['POST','GET'])
def home():
    form = downloadForm()
    if form.validate_on_submit():
        url=form.url.data
        ext= 'mp4' if form.ext.data==1 else 'webm'
        _res=form.res.data
        res = ['0','1080p', '720p', '480p', '360p', '144p'][_res]
        url=url.split('/')[-1]
        return redirect(url_for('download_vid', url=url, ext=ext, res=res))
    return render_template('d.html', form=form)

@app.route('/download/<string:url>/<string:ext>/<string:res>', methods=['POST','GET'])
def download_vid(url, ext='mp4', res='720p'):
    t1=time.perf_counter()
    typ='video'
    save_path='static/'
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
            media.filter(res=res).first().download(save_path, filename='_yt_v')
            _media_.streams.filter(type='audio').filter(file_extension=ext).filter(progressive=False).first().download(save_path, filename='_yt_a')
            command = f"ffmpeg -i {save_path}_yt_v.{ext} -i {save_path}_yt_a.{ext} -c copy {save_path}'{title}'.{ext}"
            os.system(command)
            os.remove(f'{save_path}_yt_v.{ext}')
            os.remove(f'{save_path}_yt_a.{ext}')
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
                    media.filter(res=res).first().download(save_path, filename='_yt_v')
                    _media_.streams.filter(type='audio').filter(file_extension=ext).filter(progressive=False).first().download(save_path, filename='_yt_a')
                    command = f"ffmpeg -i {save_path}_yt_v.{ext} -i {save_path}_yt_a.{ext} -c copy {save_path}'{title}'.{ext}"
                    os.system(command)
                    os.remove(f'{save_path}_yt_v.{ext}')
                    os.remove(f'{save_path}_yt_a.{ext}')
                print(f'\nDownloaded: {media.filter(res=rs)[0]}')
                downloaded=True
                break
            except:
                continue
    if not downloaded:
        print(f'\nSorry could not download {title}'.upper())
        return redirect(url_for('home'))
    t2=time.perf_counter()
    print(f'\nIt took {t2 - t1 } secs to complete')
    token = generate_token(title)
    return redirect(url_for('downloaded_video',token=token, video=title, ext=ext))

@app.route('/your_video_is_ready/<string:token>/<string:video>/<string:ext>')
def downloaded_video(token,video,ext):
    if not verify_token(video, token):
        abort()
    video=f"{video}.{ext}"
    return render_template('d.html', downloaded=True, filename=video)

def generate_token(video, expires_in=3600):
    s = Serializer(app.config['SECRET_KEY'], expires_in)
    token_data = s.dumps({'video': video}).decode('utf-8')
    return token_data

def verify_token(video, token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        token_data = s.loads(token.encode('utf-8'))
    except:
        return False
    if token_data.get('video') == video:
        return True
    return False

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run('localhost', 8000, debug=True)