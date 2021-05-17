"""

 ~ Neurorack project ~
 Graphics : Set of classes for graphical objects
 
 This file defines the main operations for the graphical objects.
 The functions here will be used for the LCD display.
 
 Author               :  Ninon Devis, Philippe Esling, Martin Vert
                        <{devis, esling}@ircam.fr>
 
 All authors contributed equally to the project and are listed aphabetically.

"""

class Graphic():
    
    def __init__(self):
        pass

    def render(self, ctx=None):
        raise NotImplementedError

class GraphicScene(Graphic):
    
    def __init__(self):
        super().__init__()
        self.elements = []

    def render(self, ctx=None):
        for e in self.elements:
            e.render(ctx)
        
class TextGraphic(Graphic):
    
    def __init__(self):
        super().__init__()

    def render(self, ctx=None):
        raise NotImplementedError
        
class ImageGraphic(Graphic):
    
    def __init__(self):
        super().__init__()

    def render(self, ctx=None):
        raise NotImplementedError
        
        
        