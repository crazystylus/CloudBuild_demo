# Basic Cloud Build Part 1
## Folder Structure
<pre>
.
├── final                   - Example CI/CD Pipeline
│   ├── cloudbuild.yaml     - Example CloudBuild yaml
│   ├── Dockerfile          - Example Dockerfile
│   └── main.go             - Copy of Main package
├── main.go                 - Main package in Go
└── README.                 - Readme Markdown file (this file)
</pre>
## Introduction
This demo showcases deploying a simple CI/CD pipeline on Cloud Build which builds a Go Web App and pushes the container image to Google Container Registry, then deploys to cloud run. You can either test the code as below for sanity check or directly deploy the pipeline and then test the CI/CD Pipeline itself. Cloud Source Repo is utilized for creating repo because it's a part of GCP offering making things more secure, but GitHub is also supported by Cloud Build.

**NOTE** All the steps mentioned here are tested and performed in Cloud Shell so no additonal packages are required. If you are running locally, you may refer to the package dependencies in the last section.

## Requirements
Following needs to be enabled: -
1. Cloud Build API
2. Cloud Source Repository API
3. Cloud Run API
4. Cloud Run enabled in Cloud Build Settings
5. Cloud Shell
6. Google Container Registry API

## Testing the Code
```bash
# Handling multiple GOPATHs
export GOPATH=$(go env GOPATH)
export GOPATH=${GOPATH##*:}
git clone https://github.com/crazystylus/CloudBuild_demo.git
cp -r CloudBuild_demo/Part-1_Getting-Started/ $GOPATH/src/
pushd $GOPATH/src/Part-1_Getting-Started/
go mod init # Required in go 1.15 and above
go get -d -v ./...
go build -o main
popd
$GOPATH/src/Part-1_Getting-Started/main
```
Open browser on `http://127.0.0.1:8080` to visit the website

### Cleanup
```bash
# Handling multiple GOPATHs
export GOPATH=$(go env GOPATH)
export GOPATH=${GOPATH##*:}
rm -rf $GOPATH/src/Part-1_Getting-Started/
```

## Running the Cloud Build CI/CD Pipeline
```bash
# Cleanup from previous section
rm -rf CloudBuild_demo GettingStarted_Part-1

# Freshly cloning the repo
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
git push -u origin --all
git push -u origin --tags

# Get the Cloud Run url
gcloud run services list --platform managed --format json | jq '.[] | select(.metadata.name=="hello-cloudbuild")|.status.url'
```
To check the Cloud Build CI Job, open cloud console and navigate to History under CloudBuild. There we can see the status of the past and currently executed build. For triggering build again you can run `git tag RANDOM_TAG` and then run `git push -u main --tags` or simply go to triggers in the UI and manually trigger it.

### Cleanup GCP Resources
```bash
# Listing triggers
gcloud beta builds triggers list --format json | jq '.[]'

# Getting the trigger id
export TRIGGER_ID=$(gcloud beta builds triggers list --format json | jq -r '.[] | select( .triggerTemplate.repoName=="go-hello-cloudbuild") | .id')
echo $TRIGGER_ID

# Deleting the trigger
gcloud beta builds triggers delete ${TRIGGER_ID} --quiet

# Deleting Source Repostory
gcloud source repos delete  go-hello-cloudbuild --quiet

# Deleting Cloud run Service
gcloud run services delete --platform managed --region us-central1 hello-cloudbuild --quiet

# Listing Container Image
gcloud container images list --repository gcr.io/${GOOGLE_CLOUD_PROJECT}

# Deleting Container image
gcloud container images list-tags gcr.io/${GOOGLE_CLOUD_PROJECT}/hello-cloudbuild --format json| jq -r --arg GOOGLE_CLOUD_PROJECT ${GOOGLE_CLOUD_PROJECT} '[.[]| "gcr.io/"+$GOOGLE_CLOUD_PROJECT+"/hello-cloudbuild@"+.digest]| join(" ")' | xargs gcloud container images delete  -q --force-delete-tags
```
## Package Dependencies if running locally
1. Google Cloud SDK
2. Go version 1.14 minimum installed
3. jq for easy deletion of resources
4. Git for version control
5. Access to browser for testing the Cloud Run URL