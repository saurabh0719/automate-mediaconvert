# automate-mediaconvert

Automate video transcoding ( `.m3u8` , `.ts` , `.mp4`) and generate thumbnails with AWS Elemental Mediaconvert. 

This example takes an input `.mp4` file and converts it into HLS format and compressed MP4 while also generating Thumbnails (specified in `OutputGroups` in `transcode.json`)

* HLS - HTTP Live Streaming is an _HTTP-based adaptive bitrate streaming_ communications protocol
  - MediaConvert generates the `.m3u8` file and the `.ts` files (10s segments)
  
<hr>

### Process 

* Create an IAM role for Mediaconvert - 
  
  - `AmazonS3FullAccess` 
  - `AmazonAPIGatewayInvokeFullAccess`
  - Copy Role `arn` and put it in `transcode.json` (line 6)
  
* Create a Queue on MediaConvert or use `Default` queue (`transcode.json` line 2) (
  - Replace `121212121212` with your Account ID
  
* Set up 2 S3 buckets - one for the input file and one to store the output 
  - Ensure the input bucket contains some video files to convert
  
* Configure `awscli` with IAM Access key (or else modify `convert.py` to create a session)

* Run `python3 convert.py` after installing `requirements.txt` and configuring the jobs.

<hr>

### Resources 

* [AWS MediaConvert](https://aws.amazon.com/mediaconvert/) - You can export a json file from the dashboard
* [MediaConvert for python](https://docs.aws.amazon.com/mediaconvert/latest/apireference/python.html)
