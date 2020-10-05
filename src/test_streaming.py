'''
Xinru Yan
Oct 2020

testing script for amazon transcribe streaming

Amazon Transcribe Streaming SDK for python: https://github.com/awslabs/amazon-transcribe-streaming-sdk
'''
import asyncio
import aiofile

from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent


class MyEventHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        for result in results:
            for alt in result.alternatives:
                print(alt.transcript)
                for item in alt.items:
                    print(item.content, item.start_time, item.end_time)


async def basic_trascribe():
    client = TranscribeStreamingClient(region="us-east-1")

    stream = await client.start_stream_transcription(language_code='en-US', media_sample_rate_hz=16000, media_encoding='pcm')

    async def write_chunks():
        async with aiofile.AIOFile('../../elizabethhau_emilyahn-finalproject/data/comparison/xinru_script1.wav', 'rb') as afp:
            reader = aiofile.Reader(afp, chunk_size=1024 * 16)
            async for chunk in reader:
                await stream.input_stream.send_audio_event(audio_chunk=chunk)
            await stream.input_stream.end_stream()

    handler = MyEventHandler(stream.output_stream)
    await asyncio.gather(write_chunks(), handler.handle_events())


loop = asyncio.get_event_loop()
loop.run_until_complete(basic_trascribe())
loop.close()