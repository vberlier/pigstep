# pigstep

[![GitHub Actions](https://github.com/vberlier/pigstep/workflows/CI/badge.svg)](https://github.com/vberlier/pigstep/actions)
[![PyPI](https://img.shields.io/pypi/v/pigstep.svg)](https://pypi.org/project/pigstep/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pigstep.svg)](https://pypi.org/project/pigstep/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

> A beet plugin for importing songs into Minecraft.

## Introduction

This [`beet`](https://github.com/mcbeet/beet) plugin lets you include songs created with [Open Note Block Studio](https://opennbs.org/) in your project. It takes care of converting `.nbs` files to data packs.

**Features**

- Keep `.nbs` files alongside the rest of your project
- Embed note block studio songs into your output data pack
- Automatically bundle extra notes when needed to support 6 octaves
- Efficient function tree generation and chord deduplication
- Flexible, can be used for making custom visualizers

**Why not just export from Note Block Studio directly?**

- It's a bit more convenient to set up the plugin once and then have it automatically convert the latest version of the song
- Less clutter, you can forget about having to navigate around the generated files
- The plugin bundles the sound files required by your songs, no need to remember to activate the extra notes resource pack or to copy the sounds you need when you start using them

## Installation

The package can be installed with `pip`.

```bash
$ pip install pigstep
```

## Usage

The plugin generates scoreboard objectives that must be included in the output data pack. If you're not using it already, running the `beet.contrib.scoreboard` plugin at the end of the pipeline will create a function that adds all the generated objectives for you.

```json
{
  "pipeline": ["pigstep", "beet.contrib.scoreboard"],
  "meta": {
    "pigstep": {
      "load": ["*.nbs"],
      "source": "ambient",
      "templates": {
        "play": "custom_play.mcfunction"
      }
    }
  }
}
```

You can require the plugin programmatically by using the `pigstep` plugin factory.

```python
from beet import Context
from pigstep import pigstep

def my_plugin(ctx: Context):
    ctx.require(
        pigstep(
            load=["*.nbs"],
            source="ambient",
            templates={"play": "custom_play.mcfunction"},
        )
    )
```

All the configuration is optional. The plugin is a no-op if the `load` option is not specified or empty. The `source` option defaults to `record`. The `templates` option lets you override the templates used by the plugin.

Here are the functions generated for each song:

- `{namespace}:song/{song_name}/play` - Play the song
- `{namespace}:song/{song_name}/pause` - Pause the song, to resume run the play function again
- `{namespace}:song/{song_name}/stop` - Stop the song, playing the song again will start from the beginning

## Contributing

Contributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request. The project uses [`poetry`](https://python-poetry.org).

```bash
$ poetry install
```

You can run the tests with `poetry run pytest`.

```bash
$ poetry run pytest
```

The project must type-check with [`pyright`](https://github.com/microsoft/pyright). If you're using VSCode the [`pylance`](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension should report diagnostics automatically. You can also install the type-checker locally with `npm install` and run it from the command-line.

```bash
$ npm run watch
$ npm run check
```

The code follows the [`black`](https://github.com/psf/black) code style. Import statements are sorted with [`isort`](https://pycqa.github.io/isort/).

```bash
$ poetry run isort pigstep tests
$ poetry run black pigstep tests
$ poetry run black --check pigstep tests
```

---

License - [MIT](https://github.com/vberlier/pigstep/blob/main/LICENSE)
