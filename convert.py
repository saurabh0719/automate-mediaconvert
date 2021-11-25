import json
import boto3

"""

This script serves as an example to demonstrate video file
conversion from S3 with AWS Elemental MediaConvert. 

It assumes that AWS Access keys are globally configured using AWS CLI

The transcode.json file attached with this repository converts the input .mp4 
file into 2 different types and generates thumbnails for them

1. HLS -> HTTP Live Streaming, an HTTP-based adaptive bitrate streaming protocol
2. MP4 -> Standard compressed MP4

"""

def convert(client, job_template):

    # List of files to convert and their destination S3 keys 
    # This can be modified programmatically to suit your requirements
    jobs = [
        # Store output of video 1 under key V1/ in output bucket
        {
            "Destination-HLS": "s3://output-bucket-1/V1/HLS/",
            "Destination-MP4": "s3://output-bucket-1/V1/MP4/",
            "Destination-Thumbnails": "s3://output-bucket-1/V1/Thumbnails/",
            "FileInput": "s3://input-bucket-1/Videos/test_video_1.mp4",
        },
        # Store output of video 2 under key V2/ in output bucket
        {
            "Destination-HLS": "s3://output-bucket-1/V2/HLS/",
            "Destination-MP4": "s3://output-bucket-1/V2/MP4/",
            "Destination-Thumbnails": "s3://output-bucket-1/V2/Thumbnails/",
            "FileInput": "s3://input-bucket-1/Videos/test_video_2.mp4",
        },
    ]

    # Modify the settings in the Job file for each video file 
    for job in jobs:
        # Set the input file S3 URL
        job_template["Settings"]["Inputs"][0]["FileInput"] = job["FileInput"]
        # S3 Destination file for HLS (.m3u8 and .ts files)
        job_template["Settings"]["OutputGroups"][0]["OutputGroupSettings"]["HlsGroupSettings"]["Destination"] = job["Destination-HLS"]
        # S3 Destination for converted .mp4 file
        job_template["Settings"]["OutputGroups"][1]["OutputGroupSettings"]["FileGroupSettings"]["Destination"] = job["Destination-MP4"]
        # S3 Destination for Thumbnails
        job_template["Settings"]["OutputGroups"][2]["OutputGroupSettings"]["FileGroupSettings"]["Destination"] = job["Destination-Thumbnails"]

        # unpack arguments from job_template and create a job for each file
        client.create_job(**job_template)


if __name__ == "__main__":

    # Get the endpoint for MediaConvert
    mediaconvert_endpoint = boto3.client("mediaconvert").describe_endpoints(
        MaxResults=100, Mode="GET_ONLY"
    )

    # Create a new MediaConvert client
    mediaconvert_client = boto3.client(
        "mediaconvert", endpoint_url=mediaconvert_endpoint["Endpoints"][0]["Url"]
    )

    # Load job template with transcoding details (OutputGroups, Inputs etc.)
    with open("transcode.json", "r") as job_template_file:
        job_template = json.load(job_template_file)

    convert(mediaconvert_client, job_template)
