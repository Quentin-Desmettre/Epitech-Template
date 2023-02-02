#!/usr/bin/env python3

##
## EPITECH PROJECT, 2022
## Epitech-Template
## File description:
## c_checker.py
##

# try to launch banana
GREEN_BOLD_ON = "\033[1;32m"
RED_BOLD_ON = "\033[1;31m"
COLOR_OFF = "\033[0m"

import os

def isBananaInstalled():
    return os.system("which coding-style > /dev/null 2>&1") == 0

def installBanana():
    command = "(git clone https://github.com/Epitech/coding-style-checker.git > /dev/null"
    command +=" && cp coding-style-checker/coding-style.sh . && chmod +x coding-style.sh) > /dev/null 2>&1"
    is_installed = os.system(command) == 0
    os.system("rm -rf coding-style-checker > /dev/null 2>&1")
    return is_installed

def removeBanana():
    command = "rm -rf coding-style.sh reports_src.txt reports_include.txt > /dev/null 2>&1"
    os.system(command)

def launchBanana(currentDepth = 0):
    if not isBananaInstalled() and not installBanana():
        print("Could not install banana.")
        return False

    command = "./coding-style.sh"
    if os.system("ls ./coding-style.sh > /dev/null 2>&1") != 0:
        command = "coding-style"

    # Run for src folder
    if os.system(f"({command} src . && mv coding-style-reports.log reports_src.txt) > /dev/null 2>&1") != 0:
        print("Could not launch banana for src folder.")
        return False
    # Run for include folder
    if os.system(f"({command} include . && mv coding-style-reports.log reports_include.txt) > /dev/null 2>&1") != 0:
        print("Could not launch banana for include folder.")
        return False

    # Check if there is any error
    if os.system("(grep 'MAJOR:C-' reports_src.txt || grep 'MINOR:C-' reports_src.txt || grep 'MAJOR:C-' reports_include.txt || grep 'MINOR:C-' reports_include.txt) > /dev/null 2>&1") == 0:
        return True # Error found
    return False # No error found

if __name__ == "__main__":
    if not launchBanana():
        removeBanana()
        print(GREEN_BOLD_ON + "No style error found." + COLOR_OFF)
        exit(0)
    removeBanana()
    print(RED_BOLD_ON + "Style error(s) found." + COLOR_OFF)
    exit(1)
