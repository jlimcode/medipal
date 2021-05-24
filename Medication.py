TimeList = list[str]


# might want to make restrictions a list of str?
class Medication:
    def __init__(self, name: str, times: TimeList, chronic: bool, withFood: bool, doses: int, restrictions: str, anonymous: bool, *unused, **unusedkw) -> None:
        self.name = name
        self.times = times
        self.chronic = chronic
        self.withFood = withFood
        self.doses = doses
        self.restrictions = restrictions
        self.anonymous = anonymous

    def addUID(self, uid: str) -> None:
        self.uid = uid

    def addMessage(self, mes: str) -> None:
        self.message = mes

    def getDBFormat(self) -> dict:
        myDict = vars(self)
        myDict["food"] = myDict.pop("withFood")
        myDict["remDoses"] = myDict.pop("doses")
        return myDict


MedicationList = list[Medication]


class Entry:
    def __init__(self, number: str, meds: MedicationList) -> None:
        self.number = number
        self.meds = meds
