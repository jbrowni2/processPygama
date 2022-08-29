import os

os.chdir("/home/jlb1694/processPygama/")

daqFiles = os.listdir("/home/jlb1694/data/daq")
rawFiles = os.listdir("/home/jlb1694/data/raw")

runList = [x for x in daqFiles if x not in rawFiles]

for run in runList:
    command = "echo \'/usr/bin/python3 /home/jlb1694/pygama/experiments/coherent/processDaq.py -r \"{0}\" -c " \
              "configFiles/config.json\'| qsub -N gemini_data_proc -e /home/jlb1694/pygama/experiments/test_qsub.err " \
              "-o /home/jlb1694/pygama/experiments/coherent/test_qsub.out - ".format(
        str(
            run))

    print(command)
