import asyncio
import queue
import pyaudio
import openwakeword
import subprocess
from openwakeword.model import Model
from assistant import run_gemini_session

STATE_IDLE = "IDLE"
STATE_ACTIVE = "ACTIVE"

class AssistantEngine:
    def __init__(self):
        self.state = STATE_IDLE
        self.audio_queue = asyncio.Queue()
        self.wake_word_model = Model() # Local OWW
        
    def audio_callback(self, in_data, frame_count, time_info, status):
        # We use a thread-safe way to put data into the async queue
        loop.call_soon_threadsafe(self.audio_queue.put_nowait, in_data)
        return (None, pyaudio.paContinue)

    async def run(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                        input=True, stream_callback=self.audio_callback)
        
        print("--- Assistant Active: Monitoring Wake Word ---")
        
        while True:
            chunk = await self.audio_queue.get()
            
            if self.state == STATE_IDLE:
                # Local CPU-only check
                prediction = self.wake_word_model.predict(chunk)
                if any(v > 0.6 for v in prediction.values()):
                    self.state = STATE_ACTIVE
                    subprocess.run(["notify-send", "Gemini", "I'm listening..."])
                    
                    # HANDOVER: Pass the existing queue to Gemini
                    await run_gemini_session(self.audio_queue)
                    
                    self.state = STATE_IDLE
                    print("--- Back to Passive Monitoring ---")

def main():
    global loop
    loop = asyncio.get_event_loop()
    engine = AssistantEngine()
    loop.run_until_complete(engine.run())

if __name__ == "__main__":
    main()