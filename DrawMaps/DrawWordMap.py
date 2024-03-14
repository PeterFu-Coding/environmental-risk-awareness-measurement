# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/9 14:29
@Auth ： Fu Yi
@ID ：2022202050049
"""
import pandas as pd
import wordcloud as wc
import matplotlib.pyplot as plt

def color_func(word, font_size, position, orientation, random_state, font_path):
    label = word_color_dict[word]
    if label == 20:
        return 'red'
    elif label == 30:
        return 'green'
    elif label == 40:
        return 'blue'
    elif label == 23:
        return 'orange'
    elif label == 24:
        return 'purple'

if __name__ == "__main__":
    data = pd.read_csv('WordCloudData.csv',header=None)
    words = data.iloc[:,0]
    amount = data.iloc[:,1]
    color = data.iloc[:,2]
    word_dict = {}
    word_color_dict = {}

    for i in range(len(words)):
        word_dict[words[i]] = amount[i]
        word_color_dict[words[i]] = color[i]

    w = wc.WordCloud(background_color='white',color_func=color_func,scale=32)
    w.fit_words(word_dict)
    plt.imshow(w)
    plt.axis('off')
    plt.subplots_adjust(bottom=0,left=0)
    plt.savefig('新闻媒体.png',dpi=300)
    # w.to_file(r'学术期刊词云.png')