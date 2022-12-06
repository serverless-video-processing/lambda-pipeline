import moviepy.editor as mp
import moviepy.video as mp_vid
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import boto3
import os
import json
import random
import urllib.parse

BUCKET_NAME = 'moviepy-video-batch'

def read_from_s3(filename, ext):
    session = boto3.Session()
    s3 = session.client('s3')
    s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=filename + ext)
    body = s3_object['Body'].read()
    with open(filename + ext, "wb") as binary_file:
        binary_file.write(body)
    return filename

def write_to_s3(filename, ext):
    with open(filename+ext, "rb") as f:
        string = f.read()
    encoded_string = string
    s3 = boto3.resource("s3")
    s3.Bucket(BUCKET_NAME).put_object(Key=filename+ext, Body=encoded_string)

def allBatchesExist():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    # Iterates through all the objects, doing the pagination for you. Each obj
    # is an ObjectSummary, so it doesn't contain the body. You'll need to call
    # get to get the whole body.
    cnt=0
    tot=-1
    for obj in bucket.objects.all():
        key = obj.key
        if key.endswith('_watermarked.mp4'):
            cnt+=1
            if tot==-1:
                tot=int(key.split('_')[2])

    return cnt==tot

def collector():

    if not allBatchesExist():
        return 

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    inps=[]
    first=''
    for obj in bucket.objects.all():
        key = obj.key
        if key.endswith('_watermarked.mp4'):
           inps.append((int(key.split('_')[1]), key))
           first = key.split('_')[0] 

    inps.sort()
    clips=[]
    for (_,inp) in inps:
        filename = read_from_s3(inp[:-4], ".mp4")
        clips.append(mp.VideoFileClip(inp))

    final = mp.concatenate_videoclips(clips, method='compose')
    final.write_videofile(first+"_ProcessedAggregated.mp4")
    write_to_s3(first+"_ProcessedAggregated", ".mp4")

def pipeline():
    collector()

def handler(event, context):
    os.chdir('/tmp/')
    pipeline()
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda Completed: Collector')
    }
