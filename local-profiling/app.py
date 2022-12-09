import moviepy.editor as mp
import moviepy.video as mp_vid
from memory_profiler import profile
import random

FILE_NAME = "ElephantsDream"
BUCKET_NAME = 'ffmpeg-profile'
LOGO = 'logo'
RESIZE = 128*2
CROP = 128*4

@profile
def scaleDown(filename):
    clip = mp.VideoFileClip(filename + ".mp4")
    clip_resized = clip.resize(height=RESIZE) #(width/height ratio is conserved)
    outputFilename = filename + "_resized"
    clip_resized.write_videofile(outputFilename+".mp4")
    return outputFilename

@profile
def crop(filename):
    stream = mp.VideoFileClip(filename+".mp4")
    outputFilename = filename + "_cropped"
    stream=mp_vid.fx.all.crop(stream, width=CROP, height=CROP, x_center=CROP//2, y_center=CROP//2)
    stream.write_videofile(outputFilename+".mp4")
    return outputFilename

@profile
def mirror(filename):
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
    return outputFilename

@profile
def watermark(filename, logoname):
    video = mp.VideoFileClip(filename+".mp4")

    logo = (mp.ImageClip(logoname+".png")
            .set_duration(video.duration)
            .resize(height=50)
            .margin(right=8, top=8, opacity=0)
            .set_pos(("right","bottom")))

    final = mp.CompositeVideoClip([video, logo])
    outputFileName= filename+"_watermarked"
    final.write_videofile(outputFileName+".mp4")
    return outputFileName

@profile
def blackWhite(filename):
    stream = mp.VideoFileClip(filename+".mp4")
    outputFilename = filename + "_bw"
    stream=mp_vid.fx.all.blackwhite(stream)
    stream.write_videofile(outputFilename+".mp4")
    return outputFilename    

@profile
def rotate(filename):
    stream = mp.VideoFileClip(filename+".mp4")
    outputFilename = filename + "_rot"

    angles=[0, 90, 180, 270]
    ind=random.randint(0,3)
    angle=angles[ind]

    stream=mp_vid.fx.all.rotate(stream, angle)
    stream.write_videofile(outputFilename+".mp4")
    return outputFilename  

@profile
def pipeline(filename):

    # Stage I: Cropping the Video
    croppedFilename = crop(filename)

    # Stage II: Scaling Down the video
    scaledDownFilename = scaleDown(croppedFilename)

    # Stage III: Mirror on X/Y
    mirrFilename = mirror(scaledDownFilename)

    # Stage IV: Black and White
    bwFilename = blackWhite(mirrFilename)

    # Stage V: Rotate
    rotateFilename = rotate(bwFilename)

    # Stage VI: Adding the watermark
    waterFilename = watermark(rotateFilename, LOGO) 


if __name__ == "__main__":
    event = {"filename":FILE_NAME}
    pipeline(event["filename"])