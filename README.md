# AWS_Transcribe

Simple scripts for Amazon Transcribe 

Amazon Transcribe Streaming: using their [python SDK](https://github.com/awslabs/amazon-transcribe-streaming-sdk).

## src
scripts dir

### Dependencies
See Pipfile

### test_streaming.py
Input: a wav file

Output: print out transcription, word, tart_time and end_time

### test_transcribe.py
Input: a wav file from s3

Results will be in s3
