import os
import httpx
import asyncio

async def adownload(url):
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
    return r.content

async def aprepare(ayats=range(1,7),path='./test.mp3'):
    audio_bytes = b''
    length=0
    for ayat in ayats:
        url = f'http://cdn.alquran.cloud/media/audio/ayah/ar.alafasy/{ayat}'
        audio_bytes += await adownload(url)
        length += len(audio_bytes)
        print(f'downloaded: {length}, bytes')
    save(audio_bytes,path)
    # return audio_bytes
def download(url):
    with httpx.Client() as client:
        r =  client.get(url)
    return r.content

def prepare(ayats=range(1,7),path='./test.mp3'):
    audio_bytes = b''
    length=0
    for ayat in ayats:
        url = f'http://cdn.alquran.cloud/media/audio/ayah/ar.alafasy/{ayat}'
        audio_bytes +=  download(url)
        length += len(audio_bytes)
        print(f'downloaded: {length}, bytes')
    save(audio_bytes,path)
    # return audio_bytes

def save(content, path):
    with open(path, 'wb') as f:
        f.write(content)
    return 'written'