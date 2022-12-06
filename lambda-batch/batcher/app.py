import moviepy.editor as mp
import moviepy.video as mp_vid
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import boto3
import os
import json
import random

BUCKET_NAME = 'moviepy-video-batch'
BATCH_LEN = 2*60

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

def batcher(filename):
    filename=read_from_s3(filename, ".mp4")
    stream = mp.VideoFileClip(filename+".mp4")
    lenVid = int(stream.duration)
    total = int(lenVid//BATCH_LEN)

    if lenVid%BATCH_LEN!=0:
        total+=1

    for i, start_time in enumerate(range(0, lenVid, BATCH_LEN)):
        ffmpeg_extract_subclip(filename+".mp4", start_time, min(start_time+BATCH_LEN, lenVid), targetname=filename+str(BATCH_LEN//60)+ "_"+str(i+1)+"_"+str(total)+"_batch.mp4")
        write_to_s3(filename + str(BATCH_LEN//60) + "_"+str(i+1)+"_"+str(total)+"_batch", ".mp4")

def pipeline(filename):
    batcher(filename)

def handler(event, context):
    os.chdir('/tmp/')
    pipeline(event['filename'])
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda Completed: Batcher')
    }