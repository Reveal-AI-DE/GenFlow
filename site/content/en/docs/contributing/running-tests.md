+++
title = 'Running tests'
linkTitle= 'Running tests'
description= 'Instructions on how to run all existence tests.'
weight= 8
+++
# Server unit tests

**Initial steps**
1. Install necessary Python dependencies:
   ```
   pip install -r GeniFlow/requirements/testing.txt
   ```

**Running tests**
1. Python tests
   ```
   python manage.py test --settings geniflow.settings.testing geniflow/apps
   ```

If you want to get a code coverage report, run the next command:
   ```
   coverage run manage.py test --settings geniflow.settings.testing geniflow/apps
   ```

**Debugging**
1. Run `server: tests` debug task in VSCode
1. If you want to debug particular tests then change the configuration
of the corresponding task in `./vscode/launch.json`, for example:
   ```json
   {
       "name": "server: tests",
       "type": "python",
       "request": "launch",
       "justMyCode": false,
       "stopOnEntry": false,
       "python": "${command:python.interpreterPath}",
       "program": "${workspaceRoot}/manage.py",
       "args": [
           "test",
           "--settings",
           "geniflow.settings.testing",
           "geniflow/apps/core",
       ],
       "django": true,
       "cwd": "${workspaceFolder}",
       "env": {},
       "console": "internalConsole"
   }
   ```
