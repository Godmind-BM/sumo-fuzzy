'''
Provides utility functions
'''
import os

from app import Config

def save_samples(files:list, datas:list) -> None:
    queue_file = os.path.join(Config.SAMPLES_URI, files[0])
    waiting_file = os.path.join(Config.SAMPLES_URI, files[1])

    with open(queue_file, 'w') as queue, open(waiting_file, 'w') as waiting:
        for q, w in zip(datas[0], datas[1]):
            queue.write(str(q) + '\n')
            waiting.write(str(w) + '\n')


