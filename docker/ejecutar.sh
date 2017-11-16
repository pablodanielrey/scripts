#!/bin/bash
sudo docker run -ti --name scripts --env-file /home/pablo/gitlab/produccion/scripts -v $(pwd)/src:/src scripts bash

