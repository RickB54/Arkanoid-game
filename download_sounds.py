import requests
import os

def download_sound(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        os.makedirs('sounds', exist_ok=True)
        with open(f'sounds/{filename}', 'wb') as f:
            f.write(response.content)
        print(f'Downloaded {filename}')
    else:
        print(f'Failed to download {filename}')

# Free sound effects from freesound.org
sounds = {
    'paddle-hit.mp3': 'https://cdn.freesound.org/sounds/415/415912-8d5f9f0f-ping-pong-hit.mp3',
    'block-break.mp3': 'https://cdn.freesound.org/sounds/442/442943-d9f0-break.mp3',
    'life-gain.mp3': 'https://cdn.freesound.org/sounds/339/339912-5c5e-powerup.mp3',
    'life-loss.mp3': 'https://cdn.freesound.org/sounds/442/442912-d9f0-negative.mp3'
}

for filename, url in sounds.items():
    download_sound(url, filename)
