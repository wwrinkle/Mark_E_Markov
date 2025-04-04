from random import random
from time import sleep, time, time_ns
import sys
import pygame
from tone import generate_tone
from decimal import *


if len(sys.argv) <= 1:
    raise "Tempo required!"
tempo = int(sys.argv[1])
getcontext().prec = 56
beat_duration = (Decimal(60) / Decimal(tempo)) * Decimal(1**9)


time_pointer = time_ns()
while True:
    now = time_ns()
    ns_since_last_beat = Decimal(now) % beat_duration
    ns_until_next_beat = beat_duration - ns_since_last_beat
    print("nsunb", ns_until_next_beat)
    delay = int(ns_until_next_beat * (1**6))
    print("delay", delay)
    pygame.time.delay(delay)
    generate_tone(440, duration=beat_duration)
    pointer_now = time_ns()
    print(f"***took {str(pointer_now - time_pointer)}ns")
    time_pointer = pointer_now
