# Preventive Imprisionment  - Knowledge Technology Practical
![Initial overview](/docs/Intro.png)

[![Scc Count Badge](https://sloc.xyz/github/LauraMQuiros/Preventive-Imprisionment-Knowledge-System/)](https://github.com/LauraMQuiros/Preventive-Imprisionment-Knowledge-System/)
![GitHub last commit](https://img.shields.io/github/last-commit/LauraMQuiros/Preventive-Imprisionment-Knowledge-System)

## Instructions
Specifications about the requirements are in `Requirements.txt`. Use `pip install -r requirements.txt`to ensure all dependencies are installed.
The main command to run the code (in VS) is 
```
python3 -m streamlit run main.py
```
The knowledge system can also be accessed through [this link](https://huggingface.co/spaces/captainanna/KTP_preventive_Prison)

## Description
For the subject Knowledge Technology Practical, we are creating a knowledge system that determines whether someone will go to preventive prison for the time being before the trial. 

There are two main reasons for someone to be sent to preventive prison: 
- they are considered a danger to society
- there is an increased risk of fleeing

This knowledge system evaluates both factors through the summation and multiplication of several weights (of crimes and modifiers) and coefficients[^1].

This allows to compute the likelihood of a person to go to preventive prison in the spanish justice system according to criminal record[^2], crime commited and ease of posterior location.

## Credits
5 ECTS for the subject "Knowledge Technology Practical" taught in University of Groningen 2022-23 with code WBAI014-05. 

In the course, students design and construct a knowledge system based on expert knowledge. The course addresses rule-based representation and inference.

[^1]: More information in additional documentation folder docs, more specifically in files `report.tex` and `WeightAssignment.pdf`.
[^2]: The crimes in the criminal record are talked about as "antecedents", which is a direct translation of the spanish term for a past crime figuring in the criminal record. Other mistranslations may be found.