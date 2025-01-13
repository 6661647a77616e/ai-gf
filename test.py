from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase

class TestApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Load the character model and its animation
        self.character = Actor(
            "models/character.egg",  # Path to the model
            {"talk": "models/character_walk.egg"}  # Path to animation
        )
        
        # Reparent to the render tree to make it visible
        self.character.reparentTo(self.render)
        
        # Set the position of the model
        self.character.setPos(0, 10, 0)
        
        # Play the animation
        self.character.loop("talk")

# Run the application
app = TestApp()
app.run()
