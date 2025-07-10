# Quebra_cabeca

A puzzle write in python, The goal was to create a puzzle where you can use any image you want.

> ⚠️ **Note**: The game is fully written in **Portuguese (Brazilian)**.

> ⚠️ **Note**: That a old project I did while learning basic python. It doesn’t reflect my current skills, but I’m keeping it here as a record of my progress.

## How its works

When you run the game, a configuration window is displayed where the user can choose the difficulty and image.

There is also a gallery feature that allows you to save images and reuse them later.

- The gallery is simply a folder where the selected image is copied and saved.
  
You can adjust some settings before starting the puzzle:

- *Convert the image to 1000x700?*: Resizes the image to fit this resolution.
- *Help image?*: Adds a faded background version of the image to assist while playing.
- *Save image in gallery?*: Saves the image to the gallery folder before starting the game.

After the configuration, the image is split into pieces based on the selected difficulty.

The gameplay is straightforward: just drag and place the pieces in the correct positions to complete the puzzle.

To start a new game, press `Enter` to reopen the configuration screen.

## Librays used

- `tkinter`
- `pygame`
- `PIL(PILLOW)`
- `random`
- `os`
- `stat`

## Known Issues
- There's no proper "end game" condition — to start over, you must manually reopen the config screen.

- The project may contain bugs throughout, as it was developed during an early learning phase.
