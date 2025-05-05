+++
title = 'API'
linkTitle= 'API'
description= 'How to interact with GenFlow.'
weight= 2
+++
## Overview

GenFlow server provides HTTP REST API for interaction. Each client application - be it a command line tool, browser or a script - all interact with GenFlow via HTTP requests and responses.

## API documentation

To access API documentation:

1. You first need to login through the admin interface

2. Access API root from the browser using the URL `http://localhost:7000/api/`

3. Access API documentation from the browser using the URL `http://localhost:7000/api/docs/`.

   ![API documentation](/images/api-docs.jpg)

4. Access Swagger UI, which is a user interface for exploring and testing RESTful APIs
that is generated automatically from an OpenAPI specification, from the browser using the URL `http://localhost:7000/api/swagger/`.

   ![Swagger UI](/images/api-swagger.jpg)

5. To download the OpenAPI 3 schema use the URL `http://localhost:7000/api/schema/`.
