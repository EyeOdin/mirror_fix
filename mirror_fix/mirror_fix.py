# Import Krita
from krita import *
from PyQt5 import uic
import os.path

# Set Window Title Name
DOCKER_NAME = "Mirror Fix"

# Create Docker
class Mirror_Fix_Docker(DockWidget):
    """
    Complementary function to correct symmetry errors
    """
    # Initialize the Dicker Window
    def __init__(self):
        super(Mirror_Fix_Docker, self).__init__()

        # Window Title
        self.setWindowTitle(DOCKER_NAME)
        # Widget
        self.window = QWidget()
        self.layout = uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + '/mirror_fix.ui', self.window)
        self.setWidget(self.window)
        # Connect Buttons
        self.Connect()

    # Connect Funtions to Buttons
    def Connect(self):
        # Verify Condition
        cond = self.window.direction.currentText()
        # Connect Funtions
        self.window.mirror.clicked.connect(self.Mirror)

    # Function Operations
    def Mirror(self):
        # Verify Context
        cond = str(self.window.direction.currentText())
        # Krita Instance Objects
        ki = Krita.instance()
        ad = ki.activeDocument()
        # Read document size
        width = ad.width()
        height = ad.height()
        # Read mirror Tool position
        w2 = width / 2  # Center Width
        h2 = height / 2  # Center Height

        # Force the Mirror Axis to Center
        if (cond == "Left" or cond == "Right" or cond == "&Left" or cond == "&Right"):
            ki.action('mirrorX-moveToCenter').trigger()
        elif (cond == "Up" or cond == "Down" or cond == "&Up" or cond == "&Down"):
            ki.action('mirrorY-moveToCenter').trigger()

        # Is there a Selection from the User?
        sel = ad.selection()
        # Selection Sensitive
        if sel == None:
            # Create a Selection
            if (cond == "Left" or cond == "&Left"):
                xx = 0
                yy = 0
                ww = w2
                hh = height
                value = 255
            elif (cond == "Right" or cond == "&Right"):
                xx = w2
                yy = 0
                ww = w2
                hh = height
                value = 255
            elif (cond == "Up" or cond == "&Up"):
                xx = 0
                yy = 0
                ww = width
                hh = h2
                value = 255
            elif (cond == "Down" or cond == "&Down"):
                xx = 0
                yy = h2
                ww = width
                hh = h2
                value = 255
            # Place Selection
            ss = Selection()
            ss.select(xx, yy, ww, hh, value)
            ad.setSelection(ss)

        # Actions
        ki.action('duplicatelayer').trigger()
        self.Wait()

        ki.action('activateNextLayer').trigger()
        self.Wait()

        ki.action('invert_selection').trigger()
        self.Wait()

        ki.action('clear').trigger()
        self.Wait()

        ki.action('deselect').trigger()
        self.Wait()

        # Mirror Image considering direction
        if (cond == "Left" or cond == "Right" or cond == "&Left" or cond == "&Right"):
            Krita.instance().action('mirrorNodeX').trigger()
        elif (cond == "Up" or cond == "Down" or cond == "&Up" or cond == "&Down"):
            Krita.instance().action('mirrorNodeY').trigger()
        self.Wait()

        ki.action('merge_layer').trigger()
        self.Wait()

    def Wait(self):
        Krita.instance().activeDocument().waitForDone()
        Krita.instance().activeDocument().refreshProjection()

    # Change the Canvas
    def canvasChanged(self, canvas):
        pass
