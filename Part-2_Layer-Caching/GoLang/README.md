# Simple Flask app with Caching
## Repo Structure
<pre>
.
├── Dockerfile          Main Dockerfile
├── Dockerfile.builder  Builder Dockerfile (Only contains steps till pulling deps)
├── go.mod              Go Module
├── go.sum              Go Dependency Checksum
├── main.go             Main Packages
└── README.md           **This file**
</pre>
## Introduction
This repo showcases speeding up a multi-stage docker build by using a separate builder image created by commenting all lines in the main Dockerfile post fetching all dependencies.

This GoLang Application simply return the number of page visits when accessed at `/`

### Building in local Docker env
```bash
# Building the builder image and using it's own image as cache to skip re-build in case of no change in dependencies
docker build . -t go-demo:builder --cache-from=go-demo:builder -f Dockerfile.builder

# Building the application container with builder as cache.
docker build . -t go-demo:app-v1 --cache-from=go-demo:builder -f Dockerfile
```
This will perform as good as a single stage stage dockerfile. But here we will have an overhead of pulling 2 base images: Alpine and Golang. We will still see a significant speedup here as we only will be compiling the code when deps don't change.

### Building in CloudBuild Pipeline
**TODO**