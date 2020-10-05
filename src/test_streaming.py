'''
Xinru Yan
Oct 2020

Testing script for amazon transcribe streaming

Usage:
    python test_streaming.py -i INPUT_WAV_FILE

Amazon Transcribe Streaming SDK for python: https://github.com/awslabs/amazon-transcribe-streaming-sdk
'''
import asyncio
import aiofile
import click

from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent


class MyEventHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        # result: https://docs.aws.amazon.com/transcribe/latest/dg/API_streaming_Result.html
        for result in results:
            if not result.is_partial:
                alt = result.alternatives[0]
                print(f'transcript {alt.transcript}')
                # word item: https://docs.aws.amazon.com/transcribe/latest/dg/API_streaming_Item.html
                for item in alt.items:
                    print(f' word {item.content}, start_time {item.start_time}, end_time {item.end_time}')


async def basic_trascribe(wavfile: str):
    client = TranscribeStreamingClient(region="us-east-1")

    stream = await client.start_stream_transcription(language_code='en-US', media_sample_rate_hz=16000, media_encoding='pcm')

    async def write_chunks():
        async with aiofile.AIOFile(wavfile, 'rb') as afp:
            reader = aiofile.Reader(afp, chunk_size=1024 * 16)
            async for chunk in reader:
                await stream.input_stream.send_audio_event(audio_chunk=chunk)
            await stream.input_stream.end_stream()

    handler = MyEventHandler(stream.output_stream)
    await asyncio.gather(write_chunks(), handler.handle_events())


@click.command()
@click.option('-i', '--input_file', default='/Users/xinruyan/Developer/elizabethhau_emilyahn-finalproject/data/comparison/xinru_script1.wav', type=str)
def main(input_file):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(basic_trascribe(input_file))
    loop.close()


if __name__ == "__main__":
    main()