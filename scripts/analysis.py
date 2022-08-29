import json
import os

print("Welcome to the analysis for Gemini")
cont = True
while(True):
    print("The analysis that we have code for is: Energy resolution, Noise, and Drift Time")
    val = input("What Analysis would you like to do?")
    with open("analysis.json", "r") as read_file:
        data = json.load(read_file)
    if str(val).lower() == "energy resolution":
        skip = False
        eu = [121, 244.70, 344.28, 411.12, 778.90, 867.37, 964.08, 1085.9, 1112.1, 1408.0]
        ba = [276.40, 302.85, 356.02]
        co = [1172, 1333, 1460]
        sor = input("Which source did you use, eu152, ba133, or co60?")
        if str(sor).lower() == "eu152":
            data["Energy Resolution"]['peaks'] = eu
        elif str(sor).lower() == "ba133":
            data["Energy Resolution"]['peaks'] = ba
        elif str(sor).lower() == "co60":
            data["Energy Resolution"]['peaks'] = co
        else:
            print("we do not have that source")
            skip = True
        with open("analysis.json", "w") as write_file:
            data = json.dump(data, write_file)

        if skip is False:
            os.system("python3 -W ignore energy_resolution.py")
    elif str(val).lower() == "noise":
        print("There are a lot of variables needed to run this analysis")

        flatmin = input("What is the minimum flat time?")
        flatmax = input("what is the maximum flat time?")
        flatstep = input("What is the step size for the flat time?")
        risemin = input("What is the minimum rise time?")
        risemax = input("what is the maximum rise time?")
        risestep = input("What is the step size for the rise time?")
        que = input("what is the query number for the files?")

        data['Noise']['flat'] = [float(flatmin), float(flatmax), float(flatstep)]
        data['Noise']['rise'] = [float(risemin), float(risemax), float(risestep)]
        data['Noise']['query'] = str(que)

        with open("analysis.json", "w") as write_file:
            data = json.dump(data, write_file)

        os.system("python3 -W ignore NoiseMinimize.py")
    elif str(val).lower() == "drift time":
        chan = input("what channel is the germanium detector in?")
        data['Drift Time']['Ge channel'] = int(chan)
        with open("analysis.json", "w") as write_file:
            data = json.dump(data, write_file)

        os.system("python3 -W ignore drift_dist.py")
    else:
        print("sorry we dont have " + str(val))

    var = input("Would you like to run another code? y/n")
    if str(var).lower() == "y":
        cont = True
    elif str(var).lower() == "yes":
        cont = True
    elif str(var).lower() == "n":
        cont = False
    elif str(var).lower() == "no":
        cont = False
    else:
        print("We only take yes or no")
        var = input("Would you like to run another code? y/n")

    if cont is False:
        break
