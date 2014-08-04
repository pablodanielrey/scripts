#!/bin/bash
ps -ef | grep winxp | grep -v grep | awk '{print($10)}' | xargs -I {} /usr/bin/VBoxManage controlvm {} acpipowerbutton
