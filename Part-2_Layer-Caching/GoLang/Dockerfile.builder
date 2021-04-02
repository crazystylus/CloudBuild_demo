# Copyright (C) 2021  Kartik Sharma

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

FROM golang:1.15 as builder
WORKDIR /go/src/app
COPY go.mod .
RUN go mod download
#COPY . .
#RUN CGO_ENABLED=0 GOOS=linux go build -o main ./...
#
#FROM alpine:latest
#COPY --from=builder /go/src/app/main .
#CMD ["./main"]
