import moviepy.editor as mp
import moviepy.video as mp_vid
import boto3
import os
import json

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

def scaleDown(filename):
    filename=read_from_s3(filename, ".mp4")
    clip = mp.VideoFileClip(filename + ".mp4")
    clip_resized = clip.resize(height=RESIZE) #(width/height ratio is conserved)
    outputFilename = filename + "_resized"
    clip_resized.write_videofile(outputFilename+".mp4")
    write_to_s3(outputFilename, ".mp4")
    return outputFilename

def crop(filename):
    filename=read_from_s3(filename, ".mp4")
    stream = mp.VideoFileClip(filename+".mp4")
    outputFilename = filename + "_cropped"
    mp_vid.fx.all.crop(stream, CROP, CROP, CROP//2, CROP//2)
    # Stage IV: Saving
    stream.write_videofile(outputFilename+".mp4")
    write_to_s3(outputFilename, ".mp4")
    return outputFilename

def mirror(filename, dir):
    filename=read_from_s3(filename, ".mp4")
    stream = mp.VideoFileClip(filename+".mp4")
    if dir=='X':
        stream=mp_vid.fx.all.mirror_x(stream)
        outputFilename = filename + "_mirrorx"
    else:
        stream=mp_vid.fx.all.mirror_y(stream)
        outputFilename = filename + "_mirrory"
    stream.write_videofile(outputFilename+".mp4")
    write_to_s3(outputFilename, ".mp4")
    return outputFilename

def watermark(filename, logoname):
    logoname=read_from_s3(logoname, ".png")
    filename = read_from_s3(filename, ".mp4")
    video = mp.VideoFileClip(filename+".mp4")

    logo = (mp.ImageClip(logoname+".png")
            .set_duration(video.duration)
            .resize(height=50) # if you need to resize...
            .margin(right=8, top=8, opacity=0) # (optional) logo-border padding
            .set_pos(("right","bottom")))

    final = mp.CompositeVideoClip([video, logo])
    outputFileName= filename+"_watermarked"
    final.write_videofile(outputFileName+".mp4")
    write_to_s3(outputFileName, ".mp4")
    return outputFileName

def blackWhite(filename):
    filename=read_from_s3(filename, ".mp4")
    stream = mp.VideoFileClip(filename+".mp4")
    outputFilename = filename + "_bw"
    stream=mp_vid.fx.all.blackwhite(stream)
    stream.write_videofile(outputFilename+".mp4")
    write_to_s3(outputFilename, ".mp4")
    return outputFilename    

def rotate(filename, angle):
    filename=read_from_s3(filename, ".mp4")
    stream = mp.VideoFileClip(filename+".mp4")
    outputFilename = filename + "_rot"
    stream=mp_vid.fx.all.rotate(stream, angle)
    stream.write_videofile(outputFilename+".mp4")
    write_to_s3(outputFilename, ".mp4")
    return outputFilename  

def pipeline():

    # Stage I: Scaling Down the video
    scaledDownFilename = scaleDown(KEY)

    # Stage II: Cropping the Video
    croppedFilename = crop(scaledDownFilename)

    # Stage III: Mirror on X
    mirrxFilename = mirror(croppedFilename, 'X')

    # Stage IV: Mirror on Y
    mirryFilename = mirror(mirrxFilename, 'Y')

    # Stage V: Black and White
    bwFilename = blackWhite(mirryFilename)

    # Stage VI: Rotate
    rotateFilename = rotate(bwFilename, 180)

    # Stage VII: Adding the watermark
    waterFilename = watermark(rotateFilename, LOGO) 

def handler(event, context):
    os.chdir('/tmp/')
    pipeline()
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda Completed: Whole Pipeline')
    }