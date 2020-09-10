import random
import PySimpleGUI as sg

bag = ["Blue.png", "Red.png", "Black.png", "Yellow.png", "Cyan.png"] * 20

shuffled_bag = random.sample(bag, 100)

sg.theme("Dark Blue 3")  # please make your windows colorful

keys = iter(range(80, 100))


def tile():
    return sg.Image(shuffled_bag.pop(), key=next(keys))


def tiles():
    return sg.Column([[tile(), tile()], [tile(), tile()]])


def spacer(x, y):
    return sg.Column([[sg.Image("Spacer.png") for i in range(x)] for j in range(y)])


def get_window():
    layout = [
        [spacer(3, 2), tiles()],
        [spacer(8, 1)],
        [tiles(), spacer(4, 2), tiles()],
        [spacer(8, 1)],
        [spacer(1, 2), tiles(), spacer(2, 2), tiles(), spacer(1, 2)],
        [sg.Button("Next")],
    ]

    return sg.Window("Window", layout, finalize=True)


window = get_window()

while True:  # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "Next":
        # change the "output" element to be the value of "input" element
        for i in range(80, 100):
            try:
                window[i].update(filename=shuffled_bag.pop())
            except IndexError:
                for j in range(i, 100):
                    window[j].update(filename="Spacer.png")
                window2 = sg.Window(
                    "Input remaining colors",
                    [
                        [sg.Text(color), sg.InputText(default_text="0", key=color)]
                        for color in "Blue Red Black Yellow Cyan".split()
                    ]
                    + [
                        [
                            sg.Button("Fill Bag"),
                            sg.Button("Exit"),
                            sg.Button("Play Again"),
                        ]
                    ],
                    finalize=True,
                )
                while True:
                    event, values = window2.read()
                    if event == sg.WIN_CLOSED or event == "Exit":
                        window.close()
                        exit()
                    if event == "Fill Bag":
                        bag = sum(
                            [
                                [f"{color}.png"] * int(values[color])
                                for color in "Blue Red Black Yellow Cyan".split()
                            ],
                            [],
                        )
                        shuffled_bag = random.sample(bag, len(bag))
                        break
                    if event == "Play Again":
                        shuffled_bag = random.sample(bag, 100)
                        for i in range(80, 100):
                            window[i].update(filename=shuffled_bag.pop())
                        i = 100
                        break

                window2.close()
                for j in range(i, 100):
                    try:
                        window[j].update(filename=shuffled_bag.pop())
                    except IndexError:
                        break
                break


window.close()
