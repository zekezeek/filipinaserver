from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client
import random
from pyrogram import enums
import datetime
import time
import subprocess
import os
import asyncio
# Target channel/supergroup
import ffmpeg
from pyrogram.types import InputMediaPhoto, InputMediaVideo
import os.path
from os import path
import shutil
import subprocess
import json

TARGET = -1001749494447

app = Client("my_account")
app.start()



ffmpeg = "./ffmpeg.exe"

async def get_duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    tofloat = float(result.stdout)
    return(int(tofloat))

async def take_screen_shot(video_file, output_directory, ttl):
    # https://stackoverflow.com/a/13891070/4723940

    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        output_directory
    ]
 
    if subprocess.run(file_genertor_command).returncode == 0:
        print ("Thumbnail Generated Successfully \n")
    else:
        print ("There was an error running your Thumnail Generator FFmpeg script \n")


async def addwatermark(inputvideo,outputvideo,filename):

    commands_list = [
    ffmpeg,
    "-y",
    "-i",
    inputvideo,
    "-i",
    "./watermark.png",
    "-filter_complex",
    f"[1][0]scale2ref=w='iw*40/100':h='ow/mdar'[wm][vid];[vid][wm]overlay=main_w-overlay_w-5:main_h-overlay_h-5",
    outputvideo
    ]
    
    if subprocess.run(commands_list).returncode == 0:
        print ("FFmpeg Script Ran Successfully \n")
    else:
        print ("There was an error running your FFmpeg script \n")

    print("Successfully Added Watermark To " + str(filename) + "\n")


async def refolder():
    print("Starting Process... ID = ReFolder \n")
    downloadfolder = "./downloads"
    if(path.exists(downloadfolder)):
        shutil.rmtree(downloadfolder)
        os.mkdir(downloadfolder)
        print("Deleted and Created Downloads Folder... \n")
    else:
        print("Created Downloads Folder... \n")
        os.mkdir(downloadfolder)

    watermarkfolder = "./watermarkedvideos"
    if(path.exists(watermarkfolder)):
        shutil.rmtree(watermarkfolder)
        os.mkdir(watermarkfolder)
        print("Deleted and Created watermarked Folder... \n")
    else:
        print("Created atermarked Folder... \n")
        os.mkdir(downloadfolder)


async def startProcess():
    # GET RANDOM VIDEO
    x = await app.get_messages(TARGET, random.randint(1,30000))

    # GET DURATION
    #x.video.duration 

    # CHECK IF VIDEO DO EXIST
    if x.video != '':

        try:
            # CHECKER FOR DURATION 
            # VIDEO MUST NOT BE TOO LONG OR SHORT
            if x.video.duration <= 400 and x.video.duration > 100:

                # DOWNLOADER STARTING

                print("Start Downloading Process... \n")
                global totaldownloaded
                while totaldownloaded != 4:

                    totaldownloaded = totaldownloaded + 1
                    filename = "video" + str(totaldownloaded) + ".mp4"
                    await app.download_media(x.video.file_id,file_name=filename)
                    print("Successfully Downloaded " + filename + "\n" )

                    # ADDING WATERMARK TO VIDEOS /
                    print("Adding Watermark to " + filename + "\n")
                    await addwatermark("./downloads/" + filename,"./watermarkedvideos/" + filename, filename)

                    # TAKING A THUMBNAIL FROM THE VIDEO
                    print("Taking thumbnail from " + filename + "\n")
                    await take_screen_shot("./downloads/" + filename,"./watermarkedvideos/" + "thumb_video" + str(totaldownloaded) + ".png", 20)
                    await startProcess()

                if totaldownloaded == 4:

                    print("Successfully Watermarked 4 Videos \n")

                    # SENDING WATERMARKED VIDEOS AS MEDIAGROUP
                    try:

                        upload = await app.send_media_group(
                            -1001740185578,
                            [
                                
                                InputMediaVideo("./watermarkedvideos/video1.mp4",caption="https://t.me/+MHvud45FcKs5OGI1",thumb="./watermarkedvideos/thumb_video1.png",duration=await get_duration("./watermarkedvideos/video1.mp4"),supports_streaming=True),
                                InputMediaVideo("./watermarkedvideos/video2.mp4",caption="https://t.me/+MHvud45FcKs5OGI1",thumb="./watermarkedvideos/thumb_video2.png",duration=await get_duration("./watermarkedvideos/video2.mp4"),supports_streaming=True),
                                InputMediaVideo("./watermarkedvideos/video3.mp4",caption="https://t.me/+MHvud45FcKs5OGI1",thumb="./watermarkedvideos/thumb_video3.png",duration=await get_duration("./watermarkedvideos/video3.mp4"),supports_streaming=True),
                                InputMediaVideo("./watermarkedvideos/video4.mp4",caption="https://t.me/+MHvud45FcKs5OGI1",thumb="./watermarkedvideos/thumb_video4.png",duration=await get_duration("./watermarkedvideos/video4.mp4"),supports_streaming=True)
                            ]
                        )
                        #print(upload)
                        await app.stop()
                        time.sleep(60)
                        app.run(main())
                    except BaseException as e:
                        print("An Error Occured...  Error 2: Reason: " + str(e) + "\n")
                        await app.stop()



            else:
                # VIDEO IS EITHER TOO LONG OR TOO SHORT
                print("Restarting app...    Reason: Too short or Too long \n")
                time.sleep(3)
                await startProcess()

        except BaseException as e:
            #print(e)
            print("Restarting...  Error 1: Reason: " + str(e) + "\n")
            time.sleep(3)
            await startProcess()
            if(str(e)) == "Client has not been started yet":
                app.start()
                await startProcess()


    # NOT A VIDEO WILL BE RESTARTING FUNCTION        
    else:
        print("Restarting...  Reason: Unexpected Error Occured \n")
        time.sleep(3)
        await startProcess()









async def main():

    await refolder()
    global totaldownloaded
    totaldownloaded = 0
    await startProcess()




#app.run(get_duration("C:/Users/daveg/OneDrive/Desktop/ProjectsPython/watermarkedvideos/video1.mp4"))

app.run(main())
