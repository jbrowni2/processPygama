#!/bin/sh

export PYTHONPATH="${PYTHONPATH}:/home/james/analysis"

python3.9 /home/james/processPygama/influxDBScripts/writeHVGe.py

python3.9 /home/james/processPygama/influxDBScripts/writeHVMuon.py

python3.9 /home/james/processPygama/influxDBScripts/writeLeakageCurrent.py

python3.9 /home/james/processPygama/influxDBScripts/writeRMSNoise.py

python3.9 /home/james/processPygama/influxDBScripts/writeTriggerRate.py

python3.9 /home/james/processPygama/influxDBScripts/writeLN.py
