# automate-Arbin-schedule-file-creation
Arbin schedule file automation from CSV

Peter Attia, 2018-2019

This code generates both "schedule files" and "batch files" for Arbin LBT battery cyclers using human-readable input.
- **"Schedule files" (.sdu)** are files that define a specific test sequence (i.e. a charging protocols, plus additional steps like discharging, rests, etc)
- **"Batch files" (.bth)** are files that map schedule files to channels (i.e. mapping experiments to batteries)

This repository has two main scripts:
- **automate_4step.py** creates 4-step (really 6-step) charging protocols based on a csv like policies_all.csv
- **automate_batchfile.py** randomly assigns charging policies from files like [these](https://github.com/petermattia/battery-parameter-spaces/tree/master/data/batch) to schedule files

Both of these scripts simply load in a template .sdu or .bth file and replace the appropriate text. The resulting schedule files are available in the "OED schedule files" directory.