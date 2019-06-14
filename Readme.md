# The official Twitter bot of the NFL theme song
### How to use it:  
Comment underneath a twitter video @NflTheme. The spelling is very
important! The server may or may not be up at any given time, so have some
patience.

### How it works
The bot uses a specific branch of the `tweepy` twitter api for python.  
https://github.com/conversocial/tweepy/tree/video_upload2/tweepy  
This is because the official `tweepy` api does not support video upload :(  

The bot uses `youtube-dl` to get the video file. `youtube-dl` is pretty
convenient tool, as it will accept URLS from almost every major video host
website.

The boot uses `ffmpeg` to edit the video. `ffmpeg` is a very complex
audio-video stream editing utility. If you look at the script
src/dl_and_alter.sh you will notice the `ffmpeg` calls have a long and
specific argument list.