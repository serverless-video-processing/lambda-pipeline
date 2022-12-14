import urllib.parse
import moviepy.editor as mp
import moviepy.video as mp_vid
import boto3
import os
import json

BUCKET_NAME = "ffmpeg-profile"

def read_from_s3(filename, ext):
    session = boto3.Session()
    s3 = session.client("s3")
    s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=filename + ext)
    body = s3_object["Body"].read()
    with open(filename + ext, "wb") as binary_file:
        binary_file.write(body)
    return filename

def write_to_s3(filename, ext):
    with open(filename + ext, "rb") as f:
        string = f.read()
    encoded_string = string
    s3 = boto3.resource("s3")
    s3.Bucket(BUCKET_NAME).put_object(Key=filename + ext, Body=encoded_string)

def blackWhite(filename):
    filename = read_from_s3(filename, ".mp4")
    stream = mp.VideoFileClip(filename + ".mp4")
    outputFilename = filename + "_bw"
    stream = mp_vid.fx.all.blackwhite(stream)
    stream.write_videofile(outputFilename + ".mp4")
    write_to_s3(outputFilename, ".mp4")
    return outputFilename

def pipeline(filename):
    bwFilename = blackWhite(filename)

def handler(event, context):

    os.chdir("/tmp/")
    pipeline(event["filename"])
    return {
        "statusCode": 200,
        "body": json.dumps("Lambda Completed: Scale Down"),
    }
