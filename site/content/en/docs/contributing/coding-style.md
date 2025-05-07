+++
title = 'Coding Style'
linkTitle= 'Coding Style'
description= 'Information about coding style that is used in GenFlow development.'
weight= 1
+++
We follow the [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript) for TypeScript code,
with one exception: we use 4 spaces for indentation of nested blocks and statements.

For Python, we use [Black](https://github.com/psf/black) and [isort](https://pycqa.github.io/isort/) to
enforce coding standards and automatically format files. You can run `dev/format_python_code.sh` to apply
these formatters.
