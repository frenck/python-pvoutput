# Python: Asynchronous client for the PVOutput API

[![GitHub Release][releases-shield]][releases]
[![Python Versions][python-versions-shield]][pypi]
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE.md)

[![Build Status][build-shield]][build]
[![Code Coverage][codecov-shield]][codecov]
[![Quality Gate Status][sonarcloud-shield]][sonarcloud]
[![Open in Dev Containers][devcontainer-shield]][devcontainer]

[![Sponsor Frenck via GitHub Sponsors][github-sponsors-shield]][github-sponsors]

[![Support Frenck on Patreon][patreon-shield]][patreon]

Asynchronous client for the PVOutput API.

## About

This package allows you to monitor PV systems connected to [PVOutput][pvoutput]
programmatically. It is mainly created to allow third-party programs to
integrate with PVOutput.

## Installation

```bash
pip install pvo
```

## Usage

```python
import asyncio

from pvo import PVOutput


async def main():
    """Show example on using the PVOutput API client."""
    async with PVOutput(
        api_key="API_KEY_FROM_PVOUTPUT_ORG",
        system_id=60017,
    ) as pvoutput:
        status = await pvoutput.status()
        print(status)


if __name__ == "__main__":
    asyncio.run(main())
```

## Changelog & Releases

This repository keeps a change log using [GitHub's releases][releases]
functionality. The format of the log is based on
[Keep a Changelog][keepchangelog].

Releases are based on [Semantic Versioning][semver], and use the format
of `MAJOR.MINOR.PATCH`. In a nutshell, the version will be incremented
based on the following:

- `MAJOR`: Incompatible or major changes.
- `MINOR`: Backwards-compatible new features and enhancements.
- `PATCH`: Backwards-compatible bugfixes and package updates.

## Contributing

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We've set up a separate document for our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Setting up development environment

The easiest way to start, is by opening a CodeSpace here on GitHub, or by using
the [Dev Container][devcontainer] feature of Visual Studio Code.

[![Open in Dev Containers][devcontainer-shield]][devcontainer]

This Python project is fully managed using the [Poetry][poetry] dependency
manager. But also relies on the use of NodeJS for certain checks during
development.

You need at least:

- Python 3.11+
- [Poetry][poetry-install]
- NodeJS 18+ (including NPM)

To install all packages, including all development requirements:

```bash
npm install
poetry install
```

As this repository uses the [pre-commit][pre-commit] framework, all changes
are linted and tested with each commit. You can run all checks and tests
manually, using the following command:

```bash
poetry run pre-commit run --all-files
```

To run just the Python tests:

```bash
poetry run pytest
```

## Authors & contributors

The original setup of this repository is by [Franck Nijhof][frenck].

For a full list of all authors and contributors,
check [the contributor's page][contributors].

## License

MIT License

Copyright (c) 2023-2025 Franck Nijhof

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[build-shield]: https://github.com/frenck/python-pvoutput/actions/workflows/tests.yaml/badge.svg
[build]: https://github.com/frenck/python-pvoutput/actions/workflows/tests.yaml
[codecov-shield]: https://codecov.io/gh/frenck/python-pvoutput/branch/main/graph/badge.svg
[codecov]: https://codecov.io/gh/frenck/python-pvoutput
[contributors]: https://github.com/frenck/python-pvoutput/graphs/contributors
[devcontainer-shield]: https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode
[devcontainer]: https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/frenck/python-pvoutput
[frenck]: https://github.com/frenck
[github-sponsors-shield]: https://frenck.dev/wp-content/uploads/2019/12/github_sponsor.png
[github-sponsors]: https://github.com/sponsors/frenck
[keepchangelog]: http://keepachangelog.com/en/1.0.0/
[license-shield]: https://img.shields.io/github/license/frenck/python-pvoutput.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2025.svg
[patreon-shield]: https://frenck.dev/wp-content/uploads/2019/12/patreon.png
[patreon]: https://www.patreon.com/frenck
[poetry-install]: https://python-poetry.org/docs/#installation
[poetry]: https://python-poetry.org
[pre-commit]: https://pre-commit.com/
[project-stage-shield]: https://img.shields.io/badge/project%20stage-production%20ready-brightgreen.svg
[pypi]: https://pypi.org/project/pvo/
[python-versions-shield]: https://img.shields.io/pypi/pyversions/pvo
[releases-shield]: https://img.shields.io/github/release/frenck/python-pvoutput.svg
[releases]: https://github.com/frenck/python-pvoutput/releases
[semver]: http://semver.org/spec/v2.0.0.html
[pvoutput]: https://pvoutput.org/
[sonarcloud-shield]: https://sonarcloud.io/api/project_badges/measure?project=frenck_python-pvoutput&metric=alert_status
[sonarcloud]: https://sonarcloud.io/summary/new_code?id=frenck_python-pvoutput
