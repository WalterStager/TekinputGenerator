import pyglet
import imgui
import sys
from imgui.integrations.pyglet import create_renderer


def main():
    window = pyglet.window.Window(width=1280, height=720, resizable=True)
    pyglet.gl.glClearColor(1,1,1,1)
    imgui.core.create_context()
    impl = create_renderer(window)

    def update(dt):
        impl.process_inputs()
        imgui.new_frame()
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", "Cmd+Q", False, True
                )

                if clicked_quit:
                    sys.exit(0)

                imgui.end_menu()
            imgui.end_main_menu_bar()
            
        imperative_window()
        imgui.end_frame()

    def imperative_window():
        imgui.begin("Hello window", True)
        imgui.text("Hello world!")
        imgui.end()


    def draw(dt):
        update(dt)
        window.clear()
        imgui.render()
        impl.render(imgui.get_draw_data())

    pyglet.clock.schedule_interval(draw, 1 / 120.0)
    pyglet.app.run()
    impl.shutdown()

if __name__ == "__main__":
    main()