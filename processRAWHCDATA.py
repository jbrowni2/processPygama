import os

os.chdir("/home/jlb1694/processPygama/")

dspFiles = os.listdir("/home/jlb1694/data/dsp")
rawFiles = os.listdir("/home/jlb1694/data/raw")

runList = [x for x in rawFiles if x not in dspFiles]

for run in runList:
    command = "echo \'/usr/bin/python3 /home/jlb1694/pygama/experiments/coherent/processRaw.py -r \"{0}\" -c " \
              "configFiles/config.json\'| qsub -N gemini_data_proc -e /home/jlb1694/pygama/experiments/test_qsub.err " \
              "-o /home/jlb1694/pygama/experiments/coherent/test_qsub.out - ".format(
        str(
            run))

    print(command)