# Snake game
#### Video Demo:  <https://www.youtube.com/watch?v=9slyV9zLMmg>
#### Description:
**Snake game** - is a classic snake game which is web-based application using **JavaScript**, **Python (FLask)** and **SQL (Sqlite)**. It is a fun game to play while waiting for things. Game area is 650x650 px square where player can move the snake around with the arrow keys, catch the food to grow bigger, and avoid hitting own tail (or window border).

The game itself is written using **JavaScript**. **Python (FLask)** is used to check player authentification, store settings and game scores to **Sqlite** database.

Player can change game settings at "Settings" section such as food color, snake color, background color, game speed or using area border as an obstacle.

Higher game speed and using area border as an obstacle **give player more score points**.

Player can view top 15 best scores at "Top scores" section.

**Game folder contains next folders and files**:
- **static** - a folder to store static files (styles, icon).
- **templates** - a folder to store .html templates.
- **app.py** - a file to store main backend logic (check player authentification, store settings and game scores to **Sqlite** database).
- **snake.db** - a **Sqlite** database, to store game values (users, settings, scores).

##### Game window description:
In the top left side of window there is an information about game score.
Game area is **650x650 px** square where player can move the snake around with the arrow keys, catch the food to grow bigger, and avoid hitting own tail (or window border).
When player hits own tail (or window border) the game is over and a big red "Game over" hint appears.
##### Settings section description:
Settings window is opened when Settings button is pressed. It contains next elements:
- **Speed** - to set game speed (from 1 to 10) with the help of dropdown.
- **Food color** - to choose food color with the help of color chooser.
- **Snake color** - to choose snake color with the help of color chooser.
- **Background color** - to choose background color with the help of color chooser.
- **Border obstacle** - to use window as game border or not with the help of check button.

##### Key assignment:
- **→** - move right
- **←** - move left
- **↑** - move up
- **↓** - move down

##### app.py file description:
**Functions**:
- **index()** - inits game settings and renders main game window using index.html template. Starts the game.
- **catch_food()** - update game score.
- **game_over()** - process game over.
- **scores()** - show top 15 best game scores.
- **about()** - show project description.
- **login()** - process user login.
- **logout()** - process user logout.
- **register()** - process user registration.
- **settings()** - load and render user setiings. Save settings.

##### index.html file description:
- **save_settings()** - saves user settings.
- **process_keypress()** - process pressing →, ←, ↑, ↓  buttons.
- **next_move()** - calculates the event that will occure after snake next move (checks if direction was changed and calculates new snake head position. If snake catches the food - it groves, if snake collides with own tail (or window border) - game over, otherwise - makes one step ahead).
- **get_new_head_coordinates()** - calculates and returns new snake head coordinates depends on its current position and direction.
- **change_direction(new_direction)** - sets new snake direction.
- **is_new_direction_allowed(new_direction)** - checks if the snake move direction can be changed.
- **check_collisions()** - check snake collision with own tail (or window border).
- **game_over()** - ends the game and shows "Game over" hint.
- **init_snake()** - inits snake.
- **draw_snake()** - draws snake.
- **init_food()** - inits food.
- **draw_food()** - draws food.
- **update_score()** - updates game score.