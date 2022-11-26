import urllib.parse
import moviepy.editor as mp
import moviepy.video as mp_vid
import boto3
import os
import json
from codeguru_profiler_agent import with_lambda_profiler

BUCKET_NAME = "ffmpeg-profile"  # replace with your bucket name
KEY = "ElephantsDream"  # replace with your object key
LOGO = "logo"
RESIZE = 180
CROP = 128


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


def rotate(filename, angle):
    filename = read_from_s3(filename, ".mp4")
    stream = mp.VideoFileClip(filename + ".mp4")
    outputFilename = filename + "_rot"
    stream = mp_vid.fx.all.rotate(stream, angle)
    stream.write_videofile(outputFilename + ".mp4")
    write_to_s3(outputFilename, ".mp4")
    return outputFilename


def pipeline(filename):
    rotFilename = rotate(filename, 180)


@with_lambda_profiler()
def handler(event, context):

    os.chdir("/tmp/")
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )
    pipeline(key.strip(".mp4"))

    return {
        "statusCode": 200,
        "body": json.dumps("Lambda Completed: Rotated"),
    }