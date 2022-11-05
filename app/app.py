import os
import wget
import moviepy.editor as mp
import moviepy.video as mp_vid

def download(url_link):
    filename = wget.download(url_link)
    filename = filename[:-4]
    return filename

def scaleDown(filename):
    clip = mp.VideoFileClip(filename+".mp4")
    clip_resized = clip.resize(height=360) #(width/height ratio is conserved)
    outputFilename = filename + "_resized"
    clip_resized.write_videofile(outputFilename+".mp4")
    return outputFilename

def crop(filename):
    outputFilename = filename +"_cropped"
    stream = mp.VideoFileClip(filename+".mp4")
    stream = mp_vid.fx.all.crop(stream, 256, 256, 256//2, 256//2)
    # Stage IV: Saving
    stream.write_videofile(outputFilename+".mp4")


def handler(event, context):
    # Stage I: Downloading the Video
    os.chdir('/tmp/')
    url_link= 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4'
    filename = download(url_link)

    # Stage II: Scaling Down the video
    scaledDownFilename = scaleDown(filename)

    # Stage III+IV: Cropping the Video and saving it using ffmpeg
    crop(scaledDownFilename)

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda completed Video cropping and saving!')
    }