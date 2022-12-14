import urllib.parse
import moviepy.editor as mp
import moviepy.video as mp_vid
import boto3
import os
import json

BUCKET_NAME = "ffmpeg-profile"
LOGO = "logo"

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

def watermark(filename, logoname):
    logoname = read_from_s3(logoname, ".png")
    filename = read_from_s3(filename, ".mp4")
    video = mp.VideoFileClip(filename + ".mp4")

    logo = (
        mp.ImageClip(logoname + ".png")
        .set_duration(video.duration)
        .resize(height=50)  # if you need to resize...
        .margin(right=8, top=8, opacity=0)  # (optional) logo-border padding
        .set_pos(("right", "bottom"))
    )

    final = mp.CompositeVideoClip([video, logo])
    outputFileName = filename + "_watermarked"
    final.write_videofile(outputFileName + ".mp4")
    write_to_s3(outputFileName, ".mp4")
    return outputFileName

def pipeline(filename):
    waterFilename = watermark(filename, LOGO)

def handler(event, context):

    os.chdir("/tmp/")
    pipeline(event["filename"])
    return {
        "statusCode": 200,
        "body": json.dumps("Lambda Completed: Watermark"),
    }
