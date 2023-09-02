# Polyrhythm audiovisual generator

<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

A configurable application to generate [polyrhythms](https://en.wikipedia.org/wiki/Polyrhythm). Balls will move across the screen, sounding a tone each time they hit one of the sides of the screen. Each ball is assigned a different interval at which it oscillates, causing different combinations of balls to hit at different times, producing varying chords.

## Dependencies
Requires Python 3.10 or later.

To install dependencies:

```
pip install -r requirements.txt
```

## To run
```
python main.py
```

## To configure
Modify `config.yaml` to adjust colors, notes, etc. The configuration file is divided into four sections:

### `window`
Contains size, background color, and borderless configuration for the application window.

### `ball`
Contains visual configuration options for the balls that move across the screen (color, size, spacing, etc.).

### `rhythm`
Contains audio configuration options for the notes assigned to the balls, as well as the timing of the balls' movement.

### `mixer`
Contains configuration options for the [pygame mixer](https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.init).
