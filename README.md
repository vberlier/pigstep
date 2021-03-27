# pigstep

[![GitHub Actions](https://github.com/vberlier/pigstep/workflows/CI/badge.svg)](https://github.com/vberlier/pigstep/actions)
[![PyPI](https://img.shields.io/pypi/v/pigstep.svg)](https://pypi.org/project/pigstep/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pigstep.svg)](https://pypi.org/project/pigstep/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

> A beet plugin for importing songs into Minecraft.

## Installation

The package can be installed with `pip`.

```bash
$ pip install pigstep
```

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
