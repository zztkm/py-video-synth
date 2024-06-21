import argparse
import sys

import numpy as np
import pyaudio
import pygame

parser = argparse.ArgumentParser()
parser.add_argument("-input", required=False, type=int, help="Audio Input Device")
parser.add_argument("-f", action="store_true", help="Run in Fullscreen Mode")
args = parser.parse_args()

if not args.input:
    print("No input device specified. Printing list of input devices now: ")
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print("Device number (%i): %s" % (i, p.get_device_info_by_index(i).get("name")))
    print("Run this program with -input 1, or the number of the input you'd like to use.")
    sys.exit(1)

# Pygameの初期設定
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Real-Time Audio Waveform")

# PyAudioの設定
CHUNK = 1024  # 一度に読み取るフレーム数
FORMAT = pyaudio.paInt16  # 16ビットの音声
CHANNELS = 1  # モノラル
RATE = 44100  # サンプルレート（Hz）

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=args.input, frames_per_buffer=CHUNK)


def draw_waveform(data: bytes):
    screen.fill((0, 0, 0))  # 画面を黒で塗りつぶす
    amplitude = np.frombuffer(data, dtype=np.int16)
    wave_points = []
    for x in range(WIDTH):
        if x % 10 == 0:
            idx = int(x * CHUNK / WIDTH)
            y = int(amplitude[idx] + (HEIGHT / 2))
            wave_points.append((x, y))
    pygame.draw.lines(screen, (0, 255, 0), False, wave_points, 2)
    pygame.display.flip()


# メインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    data = stream.read(CHUNK, exception_on_overflow=False)
    draw_waveform(data)

# 終了処理
stream.stop_stream()
stream.close()
p.terminate()
pygame.quit()
