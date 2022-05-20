import pygame as pg
import sys


class Input(object):

    def __init__(self):

        # has the user quit the application?
        self.quit = False

    def update(self):

        # iterate over all user input events
        # that have occured
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True

class Base(object):
    def __init__(self, screenSize=[512, 512]):

        # initialize all pg modules
        pg.init()

        #width and height
        screenSize = (512, 512)

        # indicate rendering details
        displayFlags = pg.DOUBLEBUF | pg.OPENGL

        # create and display the window
        self.screen = pg.display.set_mode(screenSize, displayFlags)

        # set the title bar of the window
        pg.display.set_caption("Graphics Window")

        # determine if main loop is active
        self.running = True

        # manage time-related data and operations
        self.clock = pg.time.Clock()

        # manage user input
        self.input = Input()


    # implemented by extending class
    def initialize(self):
        pass

    #implemented by the extending class
    def update(self):
        pass

    def run(self):
        ## startup ##
        self.initialize()

        ## main loop ##
        while self.running:
            ## process input ##
            self.input.update()
            if self.input.quit:
                self.running = False

            ## update ##
            self.update()

            ## render ##

            ## display image on screen
            pg.display.flip()

            # pause if necessary to achieve 60 FPS
            self.clock.tick(60)
        ## shutdown ##
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    Base().run()
