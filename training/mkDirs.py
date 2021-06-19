import os
import re

# numbers = re.compile(r'(\d+)')
# def numericalSort(value):
#     parts = numbers.split(value)
#     parts[1::2] = map(int, parts[1::2])
#     return parts

os.makedirs('./checkpoints')
os.makedirs('./checkpoints/stage1')
os.makedirs('./checkpoints/stage2')
os.makedirs('./checkpoints/stage3')
os.makedirs('./log')
