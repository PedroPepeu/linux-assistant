import asyncio
from google import genai
from tools import AVAILABLE_TOOLS
import pyaudio
import os

# Read API Key from your systemd environment
API_KEY = os.getenv("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1beta1'})

async def run_gemini_session(shared_queue):
    async with client.aio.live.connect(
        model="gemini-2.0-flash-exp", 
        config={"tools": AVAILABLE_TOOLS, "response_modalities": ["AUDIO"]}
    ) as session:
        
        p = pyaudio.PyAudio()
        # ONLY open the Output (Speaker) stream
        out_stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

        async def send_loop():
            # While in this session, keep taking chunks from the shared queue
            while True:
                chunk = await shared_queue.get()
                await session.send(chunk, end_of_turn=False)

        async def receive_loop():
            async for message in session.receive():
                # Play audio chunks as they arrive
                if message.server_content and message.server_content.model_turn:
                    for part in message.server_content.model_turn.parts:
                        if part.inline_data:
                            out_stream.write(part.inline_data.data)
                
                # Logic to exit session (e.g., if Gemini is done talking)
                if message.server_content and message.server_content.turn_complete:
                    return 

        # Run both until the conversation turn is finished
        try:
            await asyncio.wait_for(asyncio.gather(send_loop(), receive_loop()), timeout=30)
        except asyncio.TimeoutError:
            pass
        finally:
            out_stream.stop_stream()
            out_stream.close()