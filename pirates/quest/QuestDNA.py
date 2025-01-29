from direct.directnotify import DirectNotifyGlobal
from otp.otpbase.PythonUtil import getSetter, POD
from pirates.piratesbase import PLocalizer
from pirates.quest.QuestLadder import QuestStub
from dataclasses import dataclass, field
from dataclasses import dataclass, field
from typing import Tuple, Optional
import random

class CombineOps():
    OR = 0
    AND = 1

@dataclass
class QuestDNA:
    prereqs: Tuple = field(default_factory=tuple)
    tasks: Tuple = field(default_factory=tuple)
    combineOp: CombineOps = CombineOps.OR
    returnGiverIds: Optional = None
    chainedQuests: Tuple = field(default_factory=tuple)
    questId: Optional = None
    questInt: int = -1
    title: str = ''
    droppable: bool = True
    rewards: Tuple = field(default_factory=tuple)
    finalizeInfo: Tuple = field(default_factory=tuple)
    instanceInfo: Tuple = field(default_factory=tuple)
    completeRequiresVisit: bool = True
    playStinger: bool = True
    displayGoal: bool = True
    requiresVoyage: bool = False
    progressBlock: bool = False
    velvetRoped: bool = True
    checkPoint: int = -1
    finalQuest: bool = False
    acquireOnce: bool = False
    minLevel: int = 0
    minWeapLevel: int = 0
    weapLvlType: Optional = None
    hideButton: bool = False
    holiday: Optional = None
    timeLimit: int = 0
    obsolete: bool = False
    questLink: Optional = None
    questMod: Optional = None
    shipNPC: Optional = None
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestDNA')
    OR = CombineOps.OR
    AND = CombineOps.AND        

    def __init__(self, *args, **kwArgs):
        self.goal = 0

    def getName(self):
        return self.questId

    def makeCopy(self):
        copy = QuestDNA(self.getCurrentParams())
        taskDNAs = []
        for taskDNA in self.tasks:
            taskDNAs.append(taskDNA.makeCopy())

        copy.setTasks(tuple(taskDNAs))
        return copy

    def setTasks(self, tasks):
        self.tasks = tuple(tasks)

    def setRewards(self, rewards):
        self.rewards = tuple(rewards)

    def setFinalizeInfo(self, finalizeInfo):
        self.finalizeInfo = tuple(finalizeInfo)

    def setInstanceInfo(self, instanceInfo):
        self.instanceInfo = tuple(instanceInfo)

    def setChainedQuests(self, chainedQuests):
        self.chainedQuests = tuple(chainedQuests)

    def setPrereqs(self, prereqs):
        self.prereqs = tuple(prereqs)
        self._giverPreqs = []
        self._avPreqs = []
        self._envPreqs = []
        for preq in self.prereqs:
            return

    def vetGiver(self, giver):
        for preq in self._giverPreqs:
            if not preq.giverCanGive(giver):
                return False

        return True

    def vetAv(self, av):
        for preq in self._avPreqs:
            if not preq.avIsReady(av):
                return False

        return True

    def vetEnviron(self):
        for preq in self._envPreqs:
            if not preq.environIsValid():
                return False

        return True

    def getInitialTaskStates(self, holder):
        states = []
        for task in self.tasks:
            states.append(task.getInitialTaskState(holder))

        return states

    def _getString(self, stringName):
        if self.questId not in PLocalizer.QuestStrings:
            return
        string = PLocalizer.QuestStrings[self.questId].get(stringName)
        if string is None or len(string) == 0:
            return
        return string

    def getTitle(self):
        title = self._getString('title')
        if title is not None:
            return title
        if len(self.tasks) == 0:
            return ''
        return self.tasks[0].getTitle()

    def getStringBefore(self):
        dialog = self._getString('stringBefore')
        if dialog is not None:
            return dialog
        if len(self.tasks) == 0:
            return ''
        return self.tasks[0].getStringBefore()

    def getStringDuring(self):
        dialog = self._getString('stringDuring')
        if dialog is not None:
            return dialog
        if len(self.tasks) == 0:
            return ''
        return self.tasks[0].getStringDuring()

    def getStringAfter(self):
        dialog = self._getString('stringAfter')
        if dialog is not None:
            return dialog
        if len(self.tasks) == 0:
            return ''
        return self.tasks[0].getStringAfter()

    def getAnimSetAfter(self):
        anims = self._getString('animSetAfter')
        return anims

    def getDialogAfter(self):
        dialog = self._getString('dialogAfter')
        if dialog is not None:
            return dialog
        else:
            return ''
        return

    def getCustomTask(self):
        dialog = self._getString('customTask')
        if dialog is not None:
            return dialog
        else:
            return ''
        return

    def getTaskDNAs(self):
        return self.tasks

    def getDescriptionText(self, taskStates=[], bonus=False):
        taskDNAs = self.getTaskDNAs()
        if self._getString('customTask'):
            if bonus:
                return
            str = PLocalizer.QuestDescTaskSingle % {'task': self._getString('customTask')}
        elif len(taskDNAs) == 1:
            taskState = None
            if taskStates:
                taskState = taskStates[0]
            if bonus:
                descText = taskDNAs[0].getDescriptionTextBonus(taskState)
                if descText == None:
                    return
            else:
                descText = taskDNAs[0].getDescriptionText(taskState)
            taskStr = PLocalizer.QuestDescTaskSingle % {'task': descText}
            str = PLocalizer.QuestStrOneTask % {'task': taskStr}
        else:
            headingStr = {QuestDNA.OR: PLocalizer.QuestMultiHeadingOr,QuestDNA.AND: PLocalizer.QuestMultiHeadingAnd}[self.getCombineOp()]
            tasksStr = ''
            for taskDNA, taskState in zip(taskDNAs, taskStates):
                tasksStr += PLocalizer.QuestDescTaskMulti % {'task': taskDNA.getDescriptionText(taskState)}

            str = PLocalizer.QuestStrMultiTask % {'heading': headingStr,'tasks': tasksStr}
        return str

    def getSCSummaryText(self, taskNum, taskState=None):
        taskDNAs = self.getTasks()
        if len(taskDNAs) == 1:
            taskStr = PLocalizer.QuestDescTaskSingleNoPeriod % {'task': taskDNAs[0].getSCSummaryText(taskState)}
            str = PLocalizer.QuestStrOneTask % {'task': taskStr}
        elif len(taskDNAs) >= taskNum:
            taskStr = PLocalizer.QuestDescTaskSingleNoPeriod % {'task': taskDNAs[taskNum].getSCSummaryText(taskState)}
            str = PLocalizer.QuestStrOneTask % {'task': taskStr}
        else:
            str = ''
        return str

    def getSCWhereIsText(self, taskNum):
        taskDNAs = self.getTasks()
        if len(taskDNAs) == 1:
            taskStr = PLocalizer.QuestDescTaskSingleNoPeriod % {'task': taskDNAs[0].getSCWhereIsText([])}
            str = PLocalizer.QuestStrOneTask % {'task': taskStr}
        elif len(taskDNAs) >= taskNum:
            taskStr = PLocalizer.QuestDescTaskSingleNoPeriod % {'task': taskDNAs[taskNum].getSCWhereIsText([])}
            str = PLocalizer.QuestStrOneTask % {'task': taskStr}
        else:
            str = ''
        return str

    def getSCHowToText(self, taskNum):
        taskDNAs = self.getTasks()
        if len(taskDNAs) == 1:
            taskStr = PLocalizer.QuestDescTaskSingleNoPeriod % {'task': taskDNAs[0].getSCHowToText([])}
            str = PLocalizer.QuestStrOneTask % {'task': taskStr}
        elif len(taskDNAs) >= taskNum:
            taskStr = PLocalizer.QuestDescTaskSingleNoPeriod % {'task': taskDNAs[taskNum].getSCHowToText([])}
            str = PLocalizer.QuestStrOneTask % {'task': taskStr}
        else:
            str = ''
        return str
    
    def getQuestId(self):
        return self.questId
    def hasQuest(self, questId):
        return questId == self.getQuestId()

    def initialize(self, parentIsChoice):
        self.setDroppable(False)

    def initializeFortune(self, droppable):
        self.setDroppable(droppable)
    
    def setDroppable(self, droppable):
        self.droppable = droppable

    def getGoal(self):
        return self.goal

    def constructDynamicCopy(self, av, parent):
        questInt = self.getQuestInt()
        complete = False
        if questInt in av.getQuestHistory():
            complete = True
        rewards = self.getRewards()
        questId = self.getQuestId()
        for task in self.tasks:
            self.goal += task.getGoalNum()

        return QuestStub(name=questId, av=av, questInt=questInt, parent=parent, giverId=None, rewards=rewards, complete=complete, goal=self.getGoal())

    def getContainer(self, name):
        if self.getQuestId() == name:
            return self
        return None

    def getParentContainer(self, ctr):
        return None

    def isContainer(self):
        return False

    def compileStats(self, questStatData):
        if self.requiresVoyage:
            questStatData.incrementMisc('voyages')
        for task in self.tasks:
            task.compileStats(questStatData)

    def computeRewards(self, initialTaskStates, holder):
        rewards = []
        for taskDNA, taskState in zip(self.getTaskDNAs(), initialTaskStates):
            rewards.extend(list(taskDNA.computeRewards(taskState, holder)))

        return tuple(rewards)

    def isChoice(self):
        return False

    def isLadder(self):
        return False

    def isBranch(self):
        return False
    
    def setCombineOp(self, combineOp):
        self.combineOp = combineOp

    def setReturnGiverIds(self, returnGiverIds):
        self.returnGiverIds = returnGiverIds

    def setQuestId(self, questId):
        self.questId = questId

    if __dev__:

        def check(self):
            pass