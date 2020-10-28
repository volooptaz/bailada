#!/usr/bin/env python
"""
Masked wordcloud
================
Using a mask you can generate wordclouds in arbitrary shapes.
"""

from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import random

from wordcloud import WordCloud, STOPWORDS

RGB = [
    "rgba(255, 0, 0, 255)",
    "rgba(0, 255, 0, 255)",
    "rgba(0, 0, 255, 255)",
]

CMY = [
    "rgba(0, 255, 255, 255)",
    "rgba(255, 0, 255, 255)",
    "rgba(255, 255, 0, 255)",
]

def color_func(word, font_size, position, orientation, random_state=None,
                            **kwargs):
    #return random.choice(CMY)
    return random.choice(RGB)

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# Read the whole text.
text = open(path.join(d, 'entrada.txt')).read()

#manifao_mask = np.array(Image.open(path.join(d, "manifao_mask.png")))
manifao_mask = np.array(Image.open(path.join(d, "manifao_invertido_mask.png")))

stopwords = set(STOPWORDS)
stopwords.add("said")

wc = WordCloud(background_color="rgba(255, 255, 255, 0)", mode="RGBA", max_words=2000, mask=manifao_mask,
                       stopwords=stopwords)

# generate word cloud
wc.generate(text)

# store to file
wc.recolor(color_func=color_func, random_state=3).to_file(path.join(d, "manifao.png"))
