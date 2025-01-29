from direct.showbase.PythonUtil import *
from pandac.PandaModules import *
import math
from enum import Enum
class Shapes(Enum):
    Default = 1
    Square = 2
    Cut = 3
    TwoCut = 4
    LongTaper = 5
    LongTaperCut = 6
    ShortTaper = 7
    ShortTaperCut = 8
ShapeCount = len(Shapes)
class Layouts(Enum):
    Square = 1
    Circle = 2
    Hex = 3
SQRT2, SQRT3 = (math.sqrt(2), math.sqrt(3))
ISQRT2 = 1 / SQRT2 / 2
LayoutOffsets = [[[0, 1], [0.5, 1], [1, 1], [0, 0.5], [0.5, 0.5], [1, 0.5], [0, 0], [0.5, 0], [1, 0]], [[0.5 - ISQRT2, 0.5 + ISQRT2], [0.5, 1], [0.5 + ISQRT2, 0.5 + ISQRT2], [0, 0.5], [0.5, 0.5], [1, 0.5], [0.5 - ISQRT2, 0.5 - ISQRT2], [0.5, 0], [0.5 + ISQRT2, 0.5 - ISQRT2]], [[0.25, 0.25 * (2 + SQRT3)], [0.75, 0.25 * (2 + SQRT3)], [0, 0.5], [0.5, 0.5], [1, 0.5], [0.25, 0.25 * (2 - SQRT3)], [0.75, 0.25 * (2 - SQRT3)]]]
LayoutCount = len(Layouts)
class Backgrounds(Enum):
    Default = 1
    VHalf = 2
    HHalf = 3
    Corners = 4
    VThird = 5
    HThird = 6
    DiagHalf = 7
    Sides = 8
    Serrated = 9
    CenterCross = 10
    OffsetCross = 11
    Texas = 12
    HNarrowBand = 13
    HWideBand = 14
    VNarrowBand = 15
    VBand = 16
    VWideBand = 17
    Slash = 18
    XCross = 19
BackgroundCount = len(Backgrounds)
class Emblems(Enum):
    Circle = 1
    Cross1 = 2
    Cross2 = 3
    Cross3 = 4
    Crescent = 5
    Star1 = 6
    Knife1 = 7
    Knife2 = 8
    Skull1 = 9
    Skull2 = 10
    Scimitar = 11
EmblemCount = len(Emblems)
MaxEmblemCount = 3
Colors = [
 Vec4(0.1, 0.1, 0.1, 1), Vec4(1), Vec4(0.4, 0.4, 0.4, 1), Vec4(0.25, 0.25, 0.25, 1), Vec4(0.25, 0, 0.07, 1), Vec4(0.39, 0, 0.1, 1), Vec4(0.5, 0.0, 0.0, 1), Vec4(0.64, 0, 0, 1), Vec4(0.75, 0, 0, 1)]
ColorCount = len(Colors)
RotationCount = 24
XPosLowCount = 0
XPosHiCount = 256
YPosLowCount = 56
YPosHiCount = 200
LayoutScaleMin = 0.125
LayoutScaleMax = 1.0
LayoutScaleResolutionFactor = 16
LayoutScales = [ LayoutScaleMin + float(x) / (LayoutScaleResolutionFactor - 1) * (LayoutScaleMax - LayoutScaleMin) for x in range(LayoutScaleResolutionFactor) ]
LayoutScaleCount = len(LayoutScales)
EmblemScales = LayoutScales
EmblemScaleCount = len(EmblemScales)
EmblemNearProximity = 0.075
EmblemFarProximity = 0.1
BgNearProximity = 0.15
BgFarProximity = 0.15