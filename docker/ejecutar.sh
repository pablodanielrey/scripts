#!/bin/bash
sudo docker run -ti --rm --name scripts -v $(pwd)/src:/src scripts bash

