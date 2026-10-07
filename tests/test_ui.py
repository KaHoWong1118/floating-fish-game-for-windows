import os
import sys
import unittest


@unittest.skipUnless(sys.platform == 'win32' or os.environ.get('DISPLAY'), 'Needs a graphical display')
class PreviewTests(unittest.TestCase):
    def test_sprites_controls_and_animation(self):
        from aquarium import Animal
        from main import App, COLORS
        app = App(preview=True)
        try:
            app.world.animals = [Animal(kind, 100, 100, 30, 1, 0) for kind in COLORS]
            app.draw()
            self.assertGreater(len(app.canvas.find_withtag('animal')), 100)
            app.toggle_pause()
            self.assertTrue(app.paused)
            self.assertEqual(app.pause_button.cget('text'), 'Resume')
            app.pixel_size.set(8)
            app.draw()
            app.toggle_pause()
            before = app.world.animals[0].x
            app.root.after(200, app.root.quit)
            app.run()
            self.assertGreater(app.world.animals[0].x, before)
        finally:
            app.close()
