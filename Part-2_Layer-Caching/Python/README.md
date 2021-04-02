# Simple Flask app with Caching
## Repo Structure
<pre>
.
├── .dockerignore       Files to ignore in Docker build
├── .env                Contains Flask config for 'flask run'
├── app.py              Main Flask App
├── Dockerfile          Main Dockerfile
├── Dockerfile.builder  Builder Dockerfile (Only contains steps till pulling deps)
├── gunicorn.conf.py    Contains configuration for gunicorn
├── README.md           **This file**
├── requirements.txt    Python dependency list
├── templates           Contains web templates
│   └── upload.html     Page for uploading the jpeg image
└── wsgi.py             Points to the flask app
</pre>
## Introduction
This repo showcases speeding up a single stage docker build by building a separate builder image created by commenting all lines in the main Dockerfile post fetching the dependencies.
This flask application allows upload of a `jpeg` image at `/blurr` by POST (One can open `/blurr` to see the upload form) and returns the image post applying Gaussian Blur on the image.

## Building in local env
We are building container image in local env, so will be skipping the step where we pull builder image.
```bash
# Building the builder image and using it's own image as cache to skip re-build in case of no change in dependencies
docker build . -t myflaskapp:builder --cache-from=myflaskapp:builder -f Dockerfile.builder

# Building the application container with builder as cache.
docker build . -t myflaskapp:app-v1 --cache-from=myflaskapp:builder -f Dockerfile
```

## Building in Cloud Build Pipeline
**WORK_IN_PROGRESS**

### Contradiction
One might say that we can get the same performance by using main docker image as cache. I won't certainly deny that it works well in this situation, but we do have cases when the built binaries are as big like 800Mb, which whould mean that when you pull the main image instead of builder, you are pulling 800Mb of extra junk. In multi-stage we don't have an option, we will require a separate builder image for sure for a speedup.