from moviepy.editor import TextClip

speakers = {
    "man": "John",
    "boy": "Mike",
    "wom": "Mary",
    "grl": "Linda"
}

text = {
    # font size
    "size": 80,

    # text clip is at 50% of the width, 70% of the height:
    "pos": (0.5, 0.7),

    # Number of characters for each line
    # The bigger the font size, the more you should increase the number below
    "lineChars": 30,

    # color ... 
    "color": "white",
}

api = "13abe1d0ea004089a03ba6455189f773"

# uncomment any line below and run to see all available choices
if __name__ == '__main__':
    # print(TextClip.list('color'))
    print(TextClip.list('font'))
    pass