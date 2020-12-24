#!/bin/bash -e

# Copyright (C) 2020 Gunter Miegel coinboot.io
#
# This file is part of Coinboot.
#
# Coinboot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Install requirements for Coinboot server

COMPOSE_VERSION=1.27.4

if ! docker info; then
  curl -fsSL get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo usermod -aG docker $(whomami)
fi

if ! which docker-compose; then
  sudo curl -L https://github.com/docker/compose/releases/download/"${COMPOSE_VERSION}"/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
fi

if ! docker plugin ls |grep -q loki; then
  sudo docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions
  sudo docker plugin ls
fi
