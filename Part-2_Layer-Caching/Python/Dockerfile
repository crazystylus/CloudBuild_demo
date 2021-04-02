# Copyright (C) 2021  Kartik Sharma

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

FROM python:3.8.5-slim
COPY requirements.txt .
RUN pip3 install -r requirements.txt 
COPY . .

EXPOSE 8080

CMD ["/bin/sh","-c","gunicorn wsgi:app"]
