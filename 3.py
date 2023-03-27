import moviepy.editor
from pathlib import Path

video_file = Path('motivation2.mp4')

# Разделение видео и аудио дорожки с помощью библиотеку moviepy

video = moviepy.editor.VideoFileClip(f'{video_file}')
audio = video.audio
audio.write_audiofile(f'{video_file.stem}.mp3')


