#!/usr/bin/env python3

import aws_cdk as cdk

from cloud_movies.cloud_movies_stack import CloudMoviesStack


app = cdk.App()
CloudMoviesStack(app, "CloudMoviesStack")

app.synth()
