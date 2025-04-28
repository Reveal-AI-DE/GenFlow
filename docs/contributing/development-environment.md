# Development environment

## Ubuntu 24.04

### Setup the dependencies:

- Install necessary dependencies:

  ```bash
  sudo apt-get update && sudo apt-get --no-install-recommends install -y build-essential curl git python3-dev python3-pip python3-venv
  ```

  ```bash
  # Install Node.js 20 and yarn
  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash -
  sudo apt-get install -y nodejs
  sudo npm install --global yarn
  ```

- Install your favorite browser.

- Install [VS Code](https://code.visualstudio.com/docs/setup/linux#_debian-and-ubuntu-based-distributions).

- Install the following VScode extensions:

  - [JavaScript Debugger](https://marketplace.visualstudio.com/items?itemName=ms-vscode.js-debug)
  - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  - [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
  - [Stylelint](https://marketplace.visualstudio.com/items?itemName=stylelint.vscode-stylelint)
  - [Trailing Spaces](https://marketplace.visualstudio.com/items?itemName=shardulm94.trailing-spaces)
  - [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)

- Make sure to use Python 3.12.0 or higher

  ```
  python3 --version
  ```

- Install GenFlow on your local host:

  ```bash
  git clone https://github.com/Reveal-AI-DE/GenFlow
  cd GenFlow && mkdir logs keys
  python3 -m venv .env
  . .env/bin/activate
  pip install -r GenFlow/requirements/development.txt -r dev/requirements.txt
  ```

  Note that the `.txt` files in the `GenFlow/requirements` directory
  have pinned dependencies intended for the main target OS/Python version
  (the one used in the main Dockerfile).
  If you're unable to install those dependency versions,
  you can substitute the corresponding `.in` files instead.
  That way, you're more likely to be able to install the dependencies,
  but their versions might not correspond to those used in production.

- Install [Docker Engine](https://docs.docker.com/engine/install/ubuntu/) and [Docker Compose](https://docs.docker.com/compose/install/)

- Apply migrations and create a super user for GenFlow:

  ```bash
  python manage.py migrate
  python manage.py migrateredis
  python manage.py collectstatic
  python manage.py syncperiodicjobs
  python manage.py createsuperuser
  ```

- Install npm packages for UI (run the following command from GenFlow root directory):

  ```bash
  yarn --frozen-lockfile
  ```

### Run GenFlow

- Start npm UI debug server (run the following command from GenFlow root directory):
  - If you want to run GenFlow in localhost:
    ```sh
    yarn run start:genflow-ui
    ```
  - If you want to access GenFlow from outside of your host:
    ```sh
    GF_UI_HOST='<YOUR_HOST_IP>' GF_UI_PORT='<YOUR_PORT>' yarn run start:genflow-ui
    ```
- Open a new terminal window.
- Run VScode from the virtual environment (run the following command from GenFlow root directory):

  ```sh
  source .env/bin/activate && code
  ```

- Inside VScode, Open GenFlow root dir

- Select `server: debug` configuration and run it (F5) to run REST server and its workers
- Make sure that `Uncaught Exceptions` option under breakpoints section is unchecked
- Alternative: If you changed GF_UI_HOST just enter `<YOUR_HOST_IP>:3000` in your browser.

You have done! Now it is possible to insert breakpoints and debug server and client of the tool.
