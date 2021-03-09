import itertools
from tkinter import Tk
from tkinter.filedialog import askopenfilename


# Define a function to parse the Export Data
def parseExport(filePath):
    # Open the selected File and read its contents
    with open(filePath, 'r') as file:
        string = file.read()

    # List of things not to parse out of the data
    exceptions = [" ", "\n", ":", ".", "[", "]"]

    # Define a new string for all the data and remove all the strange characters from it.
    newStr = ""
    for i in string:
        if i == "Â":
            continue
        elif i.isalnum() or i in exceptions:
            newStr += i
        else:
            continue

    # Compile the string into a list to parse it more easily.
    dataList = newStr.split('\n')

    # Return the list of parsed data
    return dataList


# Find the final total of a given stat from the export data
def findStat(stat, exportData):
    for val in exportData:
        if val.split(" ")[0] == stat:
            # For some reason other stats such as HP, PRR, MRR, Fort, AC, Hamp etc... are on the same line...
            # Parse the data into a list seperated at the numbers so we can grab the value we need later.
            data = ["".join(x) for _, x in itertools.groupby(val, key=str.isdigit)]
            # Grab the 3rd value (3rd value is always the final total of the given stat)
            data = [i for i in data if i.isalpha() or i.isdigit()]

            finalStat = data[2]

            return finalStat

        else:
            continue

    # If matching data isn't found return None.
    return None


def findWeaponDice(exportData):
    # Define a list to store weapon data incase user is TWF
    weapons = []
    for val in exportData:
        # Parse the data for the On Hit section (weapon dice is stored on this line)
        if val.split(" ")[0] == "On":
            # Create a list of each seperate dice roll
            data = [i for i in val.split(" ") if i]
            # Remove the first 2 sections of created list (On, and Hit)
            del data[:2]
            # Parse out the damage types (Acid, Untyped, Fire etc...)
            data = [i for i in data if any(c.isdigit() for c in i)]

            weapons.append(data)

    return weapons


def calculateAverage(weaponDice, meleePower):
    for weapon in weaponDice:
        bonusDamage = []
        for val in weapon:
            if '[' in val:
                # Parse the string so you can grab the weapon dice
                parsedVal = val.split('[')
                wepDice = parsedVal[0]

                # Parse the string so you can grab the bonus damage
                parsedVal = parsedVal[1].split(']')
                bonus = parsedVal[1]

                # Parse out the inner roll of the dice so it can be calculated.
                inner = parsedVal[0].split('D')
                innerDice = inner[0]
                innerRoll = inner[1][:-1]
                innerBonus = inner[1][-1]

                # Calculate the average roll for the inner dice
                innerAverage = float(innerDice) * (float(innerRoll)/2) + int(innerBonus)
                # Calculate the total average damage
                averageTotal = float(wepDice) * float(innerAverage) + float(bonus)

                # Melee Power calculations (need to parse melee power)
                meleePowerCalc = ((100 + meleePower))/100 * averageTotal

            else:
                dice = val.split('D')
                averageDamage = float(dice[0]) * (float(dice[1])/2)
                bonusDamage.append(averageDamage)

        print(sum(bonusDamage))


# -------------------------------------------------------------
# -------------------- < Begin Execution > --------------------
# -------------------------------------------------------------

# Prevent the root window for tkinter from appearing.
Tk().withdraw()
filePath = askopenfilename()

parsedExport = parseExport(filePath)
weaponDice = findWeaponDice(parsedExport)
calculateAverage(weaponDice, 304)

