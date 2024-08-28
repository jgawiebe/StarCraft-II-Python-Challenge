# StarCraft-II-Python-Challenge
A challenge environment for controlling SC2 units.

## Installation Instructions
1. Install dependencies in virtual environment `pip install -r requirements.txt`
2. Move challenge maps to `\<StarCraft II Installation Directory\>\Maps\EEE466\\*.SC2Map`
3. Add line `import challenge_maps  # use locally created maps` to `venv\Lib\site-packages\pysc2\maps\__init__.py`
4. Add `Version("5.0.13", 92174,"D44E66924A56B2D4BC94786D8A7EB5B8", None),` to `venv\Lib\site-packages\pysc2\run_configs\lib.py VERSIONS`
