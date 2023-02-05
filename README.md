# Preventive Imprisionment  - Knowledge Technology Practical
![Initial overview](/img/Intro.png)
https://img.shields.io/tokei/lines/github/LauraMQuiros/Preventive-Imprisionment-Knowledge-System

## Environment
Some specifications about the requirements are in the file `Requirements.txt`. 

The main command to run the code (in VS) is 
```
python3 -m streamlit run main.py
```

The knowledge system can also be accessed through [this link](https://huggingface.co/spaces/captainanna/KTP_preventive_Prison)

## Description
For the subject Knowledge Technology Practical, we are creating a knowledge system that determines whether someone will go to preventive prison for the time being before the trial. 
There are two main reasons for someone to be sent to preventive prison: either they are considered a danger to society or there is an increased risk of fleeing. 
This knowledge system evaluates both factors through the summation and multiplication of several weights (of crimes and modifiers) and coefficients. 
This allows to compute the likelihood of a person to go to preventive prison in the spanish justice system according to criminal record[^1], crime commited and ease of posterior location.

## Credits

[^1]: The crimes in the criminal record are talked about as "antecedents", which is a direct translation of the spanish term for a past crime figuring in the criminal record. Other mistranslations may be found.