import moviepy.editor as mp
import moviepy.video as mp_vid
import boto3
import os
import json
import random

BUCKET_NAME = 'ffmpeg-profile' # replace with your bucket name
KEY = 'ElephantsDream' # replace with your object key
LOGO = 'logo'
RESIZE = 180
CROP = 128

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

def mirror(filename):
    #filename=read_from_s3(filename, ".mp4")
    stream = mp.VideoFileClip(filename+".mp4")
    
    dirs=['X', 'Y']
    ind=random.randint(0,1)
    dir=dirs[ind]

    if dir=='X':
        stream=mp_vid.fx.all.mirror_x(stream)
    else:
        stream=mp_vid.fx.all.mirror_y(stream)

    outputFilename = filename + "_mirror"
    stream.write_videofile(outputFilename+".mp4")
    #write_to_s3(outputFilename, ".mp4")
    return outputFilename

def blackWhite(filename):
    #filename=read_from_s3(filename, ".mp4")
    stream = mp.VideoFileClip(filename+".mp4")
    outputFilename = filename + "_bw"
    stream=mp_vid.fx.all.blackwhite(stream)
    stream.write_videofile(outputFilename+".mp4")
    #write_to_s3(outputFilename, ".mp4")
    return outputFilename

def rotate(filename):
    #filename=read_from_s3(filename, ".mp4")
    stream = mp.VideoFileClip(filename+".mp4")
    outputFilename = filename + "_rot"

    angles=[0, 90, 180, 270]
    ind=random.randint(0,3)
    angle=angles[ind]

    stream=mp_vid.fx.all.rotate(stream, angle)
    stream.write_videofile(outputFilename+".mp4")
    #write_to_s3(outputFilename, ".mp4")
    return outputFilename  

def watermark(filename, logoname):
    logoname = read_from_s3(logoname, ".png")
    #filename = read_from_s3(filename, ".mp4")
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

def scaleDown(filename):
    filename=read_from_s3(filename, ".mp4")
    clip = mp.VideoFileClip(filename + ".mp4")
    clip_resized = clip.resize(height=RESIZE) #(width/height ratio is conserved)
    outputFilename = filename + "_resized"
    clip_resized.write_videofile(outputFilename+".mp4")
    #write_to_s3(outputFilename, ".mp4")
    return outputFilename  

def pipeline(filename):

    scaleDownFilename = scaleDown(filename)
    mirrFilename = mirror(scaleDownFilename)
    bwFilename = blackWhite(mirrFilename)
    rotFilename = rotate(bwFilename)
    watermarkFilename = watermark(rotFilename, LOGO)

def handler(event, context):
    os.chdir('/tmp/')
    pipeline(event['filename'])

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda Completed: Whole Pipeline')
    }