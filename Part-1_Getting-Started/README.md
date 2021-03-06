# Basic Cloud Build Part 1
## Folder Structure
<pre>
.
├── final                   - Example CI Pipeline
│   ├── cloudbuild.yaml     - Example CloudBuild yaml
│   ├── Dockerfile          - Example Dockerfile
│   └── main.go             - Copy of Main package
├── main.go                 - Main package in Go
└── README.                 - Readme Markdown file (this file)
</pre>
## Introduction
This demo showcases deploying a simple CI pipeline on Cloud Build which builds a Go Web App and pushes the container image to Google Container Registry. You can either test the code as below for sanity check or directly deploy the pipeline and then test the CI Pipeline itself. Cloud Source Repo is utilized for creating repo because it's a part of GCP offering making things more secure.

## Testing the Code
```bash
export GOPATH=$(go env GOPATH)
export GOPATH=${GOPATH##*:}
git clone https://github.com/crazystylus/CloudBuild_demo.git
cp -r CloudBuild_demo/Part-1_Getting-Started/ $GOPATH/src/
cd $GOPATH/src/Part-1_Getting-Started/
go mod init
go get -d -v ./...
go run main.go
```
Open browser on `http://127.0.0.1:8080` to visit the website

## Running the Cloud Build CI Pipeline
```bash
git clone https://github.com/crazystylus/CloudBuild_demo.git
cp -r CloudBuild_demo/Part-1_Getting-Started/final GettingStarted_Part-1
cd GettingStarted_Part-1

# Creating Git Repo with the code
git init
git add .
git commit -m "First Commit"

# Creating Cloud Source Repo
gcloud source repos create go-hello-cloudbuild

# Creating Cloud Build Trigger
gcloud beta builds triggers create cloud-source-repositories \
--repo=go-hello-cloudbuild \
--tag-pattern='.*' \
--build-config='cloudbuild.yaml'

# Adding Remote to git repo
git config --global credential.'https://source.developers.google.com'.helper gcloud.sh
git remote add origin https://source.developers.google.com/p/${GOOGLE_CLOUD_PROJECT}/r/go-hello-cloudbuild

# Tagging and pushing to git repo
git tag v1
git push -u origin master --tags
```
To check the Cloud Build CI Job, open cloud console and navigate to History under CloudBuild. There we can see the status of the past and currently executed build.

### Cleanup GCP Resources
```bash


```
## References

## Link to article