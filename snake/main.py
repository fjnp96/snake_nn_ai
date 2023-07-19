import menu
import config
fps = 10

def main(menu):
    print("Hello world")
    if(not config.skip_menu):
        mainMenu = menu.Menu(800,600)
        mainMenu.display()
    menu.train()

if __name__ == "__main__":
    main(menu)
