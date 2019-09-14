# Choice: A Nightmare

import curses, random

class Data(object):
    def __init__(self):
        self.letter_pairs = dict()
        self.losing_outcome = dict()

    def reverse_lookup(self, dictionary, value):
        for key in dictionary:
            if dictionary[key] == value:
                return key
        return None

class Arbiter(object):
    def decide_winner(self, candidates):
        self.winner = random.choice(candidates)

class String(object):
    # on creation, open a file and load it into a file object
    def __init__(self, filename):
        try:
            self.file_object = open(filename)
        finally:
            self.string = self.file_object.read()
            self.file_object.close()

    def send(self):
        return self.string

    def send_list(self):
        return self.string.split()

class Switch(object):
    # emulate switch/case
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        yield self.match, True
        raise StopIteration

    def match(self, *args):
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

class Screen(object):
    def __init__(self):
        self.running = True
        curses.initscr()
        curses.noecho()
        curses.cbreak()

    def __del__(self):
        try:
            curses.nocbreak()
            curses.echo()
            curses.endwin()
        except:
            pass

class Window(Screen):
    def __init__(self, windowtype):
        for case, default in Switch(windowtype):
            if case("top"):
                self.frame = curses.newwin(8, 80, 0, 0)
                self.frame.addstr(0, 0, title.send())
                self.frame.addstr(1, 0, intro.send())
                break
            if case("item"):
                self.frame = curses.newwin(17, 15, 7, 0)

                iterator = 0
                for each in item_list:
                    self.frame.addstr(iterator, 0, each)
                    iterator += 1
                break
            if case("output"):
                self.frame = curses.newwin(17, 62, 7, 18)
                break
            if default:
                pass
        self.frame.refresh()

    def draw(self, outcome):
        self.frame.erase()
        self.frame.addstr(0, 0, outcome)
        self.frame.refresh()

    #emboldens selected choice
    def highlight_choice(self, choice):
        self.frame.erase()
        iterator = 0
        for each in item_list:
            if each == choice:
                self.frame.addstr(iterator, 0, each, curses.A_BOLD)
            else:
                self.frame.addstr(iterator, 0, each)
            iterator += 1
        self.frame.refresh()

screen = Screen()
data = Data()

title = String("title")
intro = String("intro")

items = String("items")
item_list = items.send_list()
random.shuffle(item_list)

arbiter = Arbiter()
arbiter.decide_winner(item_list)
if_only = "\n\nYou really should have chosen the "+arbiter.winner+"."
congrats = "\n\nCongratualations! You chose well."

for item in item_list:
    data.letter_pairs[item] = item[0][0]
    if item != arbiter.winner:
        path = "losing/" + item
        associated_string = String(path)
        data.losing_outcome[item] = associated_string.send()
    if item == arbiter.winner:
        path = "winning/" + item
        associated_string = String(path)
        data.winning_outcome = associated_string.send()

top_window = Window("top")
item_window = Window("item")
output_window = Window("output")

while screen.running:
    key_press = item_window.frame.getkey()
    key_press = key_press.lower()

    for item in data.letter_pairs:
        if key_press in item:
            try:
                entered = data.reverse_lookup(data.letter_pairs, key_press)
                won = (entered==arbiter.winner)
                if not won:
                    output_window.draw(data.losing_outcome[entered]
                        + if_only)
                    item_window.highlight_choice(entered)
                    item_window.frame.getkey()
                    screen.running = False
                    break
                if won:
                    output_window.draw(data.winning_outcome
                        + congrats)
                    item_window.highlight_choice(entered)
                    item_window.frame.getkey()
                    screen.running = False
                    break
            except:
                error_message = \
                "Nothing on the table begins with the letter"\
                +" "+key_press+"!"
                output_window.draw(error_message)
        elif key_press in "q":
            screen.running = False

del screen
