'''
Xinru Yan
Oct 2020

Testing script for amazon transcribe with speaker identification

Adapted from https://docs.aws.amazon.com/code-samples/latest/catalog/python-transcribe-getting_started.py.html
More complex one: https://docs.aws.amazon.com/code-samples/latest/catalog/python-transcribe-transcribe_basics.py.html

Usage:
    python test_transcribe.py -i INPUT_FILE_URI

boto3 documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe.html#TranscribeService.Client.start_transcription_job
'''
import boto3
import time
import click


def transcribe_file(job_name, file_uri, transcribe_client):
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        MediaFormat='wav',
        LanguageCode='en-US',
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 2,
        }
    )
    max_tries = 60
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            print(f"Job {job_name} is {job_status}.")
            if job_status == 'COMPLETED':
                print(
                    f"Download the transcript from\n"
                    f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}.")
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(5)


@click.command()
@click.option('-i', '--input_file_uri', default='s3://transcribetryoutsheenroo/SBC005NEW.wav', type=str)
@click.option('-j', '--transcribe_job_name', default='TranscribeTryoutSomething', type=str)
def main(input_file_uri, transcribe_job_name):
    transcribe_client = boto3.client('transcribe')
    # transcribe_job_name needs update
    transcribe_file(transcribe_job_name, input_file_uri, transcribe_client)


if __name__ == '__main__':
    main()
