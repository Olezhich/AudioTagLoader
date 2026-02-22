# AudioTagLoader

[![License](https://img.shields.io/github/license/Olezhich/AudioTagLoader )](https://github.com/Olezhich/AudioTagLoader/blob/main/LICENSE )
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://python.org)  
[![Tests](https://github.com/Olezhich/AudioTagLoader/workflows/Tests/badge.svg )](https://github.com/Olezhich/AudioTagLoader/actions )

> **Cli auduio tags toolkit** \
 Loading audio tags from the Discogs API and assigning them to tracks

 ## Features
 - Fast `Redis` cache
 - A user-friendly interface for selecting the desired artist and then the desired album
 - Working on Linux/MacOS

 ## QuickStart
 ```bash
git clone https://github.com/Olezhich/AudioTagLoader.git

cd AudioTagLoader

# install the dependencies from pyprodject.toml
poetry install

# run docker redis container

docker-compose -f cache/docker-compose.yml up -d   
 ```