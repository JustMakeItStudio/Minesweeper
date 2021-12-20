# Minesweeper Clone
Build in Python 3.
The aim is to recreate the legendary minesweeper game. This is a simpe clone.
The tile rendering is given as a separate repository here:
```sh
https://github.com/JustMakeItStudio/Tile-renderer
```

#### Libraries used:
- [math]
- [pygame]
- [pygame_gui]
- [numpy]
- [time]
- [random]
- [tkinter]

#### How it works:
- A tiled map is created using pygame.
- Each tile is an instance of a class called Tile.
- Every tile has 2 states, clicked, and not clicked, as well as, 2 further states, bomb, and not bomb.
- Any mouse event is used to change the state from not clicked to clicked.
- If it is a bomb then a pop up apears telling you, you died, using tkinter.
- Else all the connected tiles that are not near a bomb are changed to the clicked state and are now visible.


### Future updates:
  - Implement a menu system, starting screen, pause, failure and win screen.
  - Change the appearance, colors, fonts.
  - Add sounds.
  - Reduce the needed libraries.


### Installation

To run the code you need Python3, and the libraries above installed on your computer.
To install a libray for python open the command prompt and follow the example bellow.

```sh
$ pip install pygame
```

To clone the repository, open the command prompt at the directory of choice and type:
```sh
$  git clone --recursive https://github.com/JustMakeItStudio/Minesweeper
```
### Screen shots:
The red colored tiles represent the bombs, while the blue tiles have a number inside them that indicates how many bombs are one tile away, finaly the black tiles have not been not clicked yet.

![image](https://user-images.githubusercontent.com/71210416/111703526-75c70e80-8846-11eb-868f-955ded471241.png)

![image](https://user-images.githubusercontent.com/71210416/111703441-4e704180-8846-11eb-94a5-f96d1db288c3.png)

**Use this as you like**

   [math]: <https://docs.python.org/3/library/math.html>
   [pygame]: <https://www.pygame.org/docs/>
   [pygame_gui]: <https://pygame-gui.readthedocs.io/en/latest/>
   [numpy]: <https://numpy.org/doc/>
   [time]: <https://docs.python.org/3/library/time.html>
   [random]: <https://docs.python.org/3/library/random.html>
   [tkinter]: <https://docs.python.org/3/library/tk.html>
