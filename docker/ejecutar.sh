#!/bin/bash
sudo docker run -ti --name scripts --env-file $HOME/gitlab/fce/produccion/scripts -p 9090:5000 -v $(pwd)/src:/src scripts bash

