import pyaudio
import wave

def record_audio(output_filename, duration=30):
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a stream to capture audio from the virtual audio device
    stream = p.open(format=pyaudio.paInt16,
                    channels=2,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

    print("Recording...")

    frames = []

    for _ in range(int(44100 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))

# Example usage
if __name__ == "__main__":
    # Play the Spotify song before running this script
    record_audio('spotify_song.wav', duration=30)  # Set duration according to your needs
