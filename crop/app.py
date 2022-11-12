import urllib.parse
import moviepy.editor as mp
import moviepy.video as mp_vid
import boto3
import os
import json

BUCKET_NAME = "ffmpeg-profile"  # replace with your bucket name
# KEY = 'ElephantsDream' # replace with your object key


def read_from_s3(filename):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(BUCKET_NAME)
    for object in bucket.objects.all():
        key = object.key
        print(key)
        if key == filename + ".mp4":
            body = object.get()["Body"].read()
            # print(type(body))
            with open(filename + ".mp4", "wb") as binary_file:
                binary_file.write(body)
            return filename
    return ""


def write_to_s3(filename):
    with open(filename + ".mp4", "rb") as f:
        string = f.read()
    encoded_string = string
    s3 = boto3.resource("s3")
    s3.Bucket(BUCKET_NAME).put_object(Key=filename + ".mp4", Body=encoded_string)


def scaleDown(filename):
    filename = read_from_s3(filename)
    clip = mp.VideoFileClip(filename + ".mp4")
    clip_resized = clip.resize(height=360)  # (width/height ratio is conserved)
    outputFilename = filename + "_resized"
    clip_resized.write_videofile(outputFilename + ".mp4")
    write_to_s3(outputFilename)
    return outputFilename


def crop(filename):
    filename = read_from_s3(filename)
    stream = mp.VideoFileClip(filename + ".mp4")
    outputFilename = filename + "_cropped"
    mp_vid.fx.all.crop(stream, 256, 256, 256 // 2, 256 // 2)
    # Stage IV: Saving
    stream.write_videofile(outputFilename + ".mp4")
    write_to_s3(outputFilename)


def handler(event, context):
    # s3 = boto3.client("s3")
    os.chdir("/tmp/")
    # os.environ["IMAGEIO_FFMPEG_EXE"] = "/tmp"

    print("EVENT:")
    print(event)

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    print("bucket", bucket, "key", key)

    crop(key.strip(".mp4"))

    return {
        "statusCode": 200,
        "body": json.dumps("Lambda completed Video cropping and saving!"),
    }
