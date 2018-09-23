# Package Templates
This is a template repo for any Travis CICD package which automatically builds and uploads to PyPI.

## Getting Started

#### Auto Version Management

First, run this script from the root directory of the project to set up the local git hooks.

```bash
bash .support/setup.sh
```

This will set up the automatic version bumping. It will update the micro version string in `version` file, which is used by `setup.py` to generate the package version, and also injected into the `__init__.py` file of the package so that when imported, the user can use `<package>.__version__` . This will be done as a git hook on every commit. Major and minor versions must be updated manually.

#### 3rd Party Services

To use this, you will need to hook up this repository with a [Travis account](travis-ci.org), a [CodeCov](https://codecov.io) account, and a [PyPI](https://pypi.org) account.

On Travis, you must set your environment variables for the project to the login credentials for your PyPI account.

```bash
export REPO_USER="krinj"
export REPO_PASS=[redacted]
```

#### Setup Config

Modify the fields at the top of `setup.py`:

```python
AUTHOR = "Jakrin Juangbhanich"
EMAIL = "juangbhanich.k@gmail.com"
PACKAGE_NAME = "my_package"
DESCRIPTION = "My awesome package."
REPO = "https://github.com/krinj/package"
```

The `PACKAGE_NAME` also specifies the directory which will be exported and bundled (and will be also the name of the package). Everything under that directory will be exported, and everything outside will not.

If you want to export some other packages, or have more custom control, modify this line in the setup script instead:

```python
packages=["foo", "bar"]
```

#### Unit Tests

Unit tests should be named in the format of `test_*.py` and should reside in the `tests` directory. These tests will be run automatically by the Travis service.

In `travis.yml` you must change this line so that the `--source` points to whatever package you are testing coverage for.

```yaml
script:
  - coverage run --source {YOUR_PACKAGE} -m unittest tests/test_*.py
```
