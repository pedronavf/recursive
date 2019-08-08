# make flipbook pages for an animated specimen
# https://codepen.io/thundernixon/pen/wVypxe?editors=1100

# TODO: eliminate reliance on 100 frames (link curve dict to t, not to frame)


from drawBot import * # requires drawbot to be installed as module
import datetime
from fontTools.misc.bezierTools import splitCubicAtT


newDrawing()
# fontFam = "Rec Mono Beta013 Var"

fontFam = "/Users/stephennixon/type-repos/recursive/src/proofs/drawbot-diagrams-etc/flipbook/fonts/Recursive-mono-full--w_ital_slnt-2019_07_25.ttf"
frames = 200
format = "gif"


frontmatter = False
debug = True

bookSize = 3.5
DPI = 150
pixels = DPI*bookSize

# pixels = 1000
W, H = pixels, pixels # size is 72 dpi * bookSize




textSize = W/30
rwSize = W/1.4


# minWeight = 300.01
# maxWeight = 899.99

# minExpression = 0.01
# maxExpression = 1

# maxSlant = 0
# minSlant = -15
    

def interp(a, b, t):
    distance = b-a
    return(a + distance * t)


# ---------------------------------------------------------
# ANIMATION -----------------------------------------------

curviness = 0.7
        
def getCurveXY(t):
    currrve = ((0,0), (pixels*curviness, 22), (pixels-(pixels*curviness),pixels), (pixels,pixels))
    split = splitCubicAtT(*currrve, t)
    x,y = split[0][-1][0], split[0][-1][1]
    return(x,y)

curveDict = {}

for frame in range(frames+1):
    # frame = frame + 1
    t = frame / frames    
    x,y = getCurveXY(t)

    curveDict[t] = (x,y)

if debug:
    import pprint
    pp = pprint.PrettyPrinter(width=80, compact=False)
    pp.pprint(curveDict)

for frame in range(frames):
    # frame = frame + 1
    
    newPage(W, H)
    font(fontFam)
    # font("fonts/Recursive-mono-full--w_ital_slnt-2019_07_24.ttf")
    
    frameDuration(1/60)
    fill(0)
    rect(0,0,W,H)
    
    t = frame / frames 
    x,y = getCurveXY(t)
    
    fill(1)
    
    factor = y / pixels
    

    if frame >= frames*0 and frame <= frames*0.25:

        xprn = (0.001,  0.5)
        wght = (300.01, 800 - 0.01)
        slnt = (0.01,   -7.5)
        currentItal = 0

        startPos = curveDict[0.0][1]
        endPos = curveDict[0.25][1]

        stepRange = endPos - startPos

        factor = (y - startPos ) / stepRange

    if frame > frames*0.25 and frame <= frames*0.5:
        xprn = (0.5, 1)
        wght = (800.01, 900 - 0.01)
        slnt = (-7.5, -15)
        currentItal = 0

        startPos = curveDict[0.25][1]
        endPos = curveDict[0.5][1]

        stepRange = endPos - startPos

        factor = (y - startPos ) / stepRange
        
        
    if frame > frames*0.5 and frame <= frames * 0.75:
        xprn = (1, 0.5)
        wght = (900 - .01, 800 + 0.01)
        slnt = (-15, -7.5)
        currentItal = 1

        startPos = curveDict[0.5][1]
        endPos = curveDict[0.75][1]

        stepRange = endPos - startPos

        factor = (y - startPos ) / stepRange
        
    if frame > frames*0.75 and frame <= frames * 1.0:
        xprn = (0.5, 0)
        wght = (800 - .01, 300 + 0.01)
        slnt = (-7.5, 0)
        currentItal = 1

        startPos = curveDict[0.75][1]
        endPos = curveDict[1.0][1]

        stepRange = endPos - startPos

        factor = (y - startPos ) / stepRange
    
    currentXprn = interp(xprn[0], xprn[1], factor)
    currentWght = interp(wght[0], wght[1], factor)
    currentSlnt = interp(slnt[0], slnt[1], factor)
    
    fontVariations(
        wght=currentWght,
        XPRN=currentXprn,
        slnt=currentSlnt,
        ital=currentItal
        )
    
    
    padding = W*0.025
    
    fontSize(W/1.4)
    text("rw", (W/15, padding*2)) # H/12
    
    fontSize(W/30)
    
    # padding = 0.1
    # text(str(round(currentWght)), (((W*0.1)+(W*completionOnCurve * 0.7)), H *0.7))

    currentProp = 0
    
    x = str('{:4.2f}'.format(currentXprn))
    w = str('{:3.2f}'.format(currentWght))
    s = str('{:05.2f}'.format(abs(currentSlnt)))
    i = str('{:4.2f}'.format(currentItal))
    p = str('{:4.2f}'.format(currentProp))
    # text(f"prop {str(0)}   xprn {x}   wght {w}   slnt -{s}   ital {i}   {frame+1}", (((W*0.025)), H *0.025))

    # ----------------------------------------------------------------------
    # BAR CHARTS / SLIDERS FOR AXES ----------------------------------------

    # minVal, maxVal, currentVal

    xprnVal = currentXprn
    minWght, maxWght = 300, 900
    wghtVal = (currentWght - minWght) / (maxWght - minWght)
    minSlnt, maxSlnt = 0, -15
    slntVal = abs(((currentSlnt - minSlnt) / (minSlnt - maxSlnt)))
    minItal, maxItal = 0, 1
    italVal = currentItal

    infoSpacing = H * 0.075

    infoHeight = H * 0.5

    # print(f"slntVal: {slntVal}")

    trackSize = padding*0.125
    ovalSize = padding*0.675

    fill(0.5,0.5,0.5,1)
    rect(padding, infoHeight, (W- (padding*2)), trackSize)
    fill(1)
    oval(((W - (padding*2)) * italVal) -(ovalSize/2) + padding, infoHeight-(ovalSize/2)+(trackSize/2), ovalSize, ovalSize)
    textBox(f"ital", (padding, infoHeight + padding*0.25, (W- (padding*2)), textSize*1.5))
    textBox(f"{i}", (padding, infoHeight + padding*0.25, (W- (padding*2)), textSize*1.5), align="right")

    infoHeight += infoSpacing
    fill(0.5,0.5,0.5,1)
    rect(padding, infoHeight, (W- (padding*2)), trackSize)
    fill(1)
    oval(((W - (padding*2)) * slntVal) -(ovalSize/2) + padding, infoHeight-(ovalSize/2)+(trackSize/2), ovalSize, ovalSize)
    textBox(f"slnt", (padding, infoHeight + padding*0.25, (W- (padding*2)), textSize*1.5))
    textBox(f"-{s}", (padding, infoHeight + padding*0.25, (W- (padding*2)), textSize*1.5), align="right")

    infoHeight += infoSpacing
    fill(0.5,0.5,0.5,1)
    rect(padding, infoHeight, (W- (padding*2)), trackSize)
    fill(1)
    oval(((W - (padding*2)) * wghtVal) -(ovalSize/2) + padding, infoHeight-(ovalSize/2)+(trackSize/2), ovalSize, ovalSize)
    textBox(f"wght", (padding, infoHeight + padding*0.25, (W- (padding*2)), textSize*1.5))
    textBox(f"{w}", (padding, infoHeight + padding*0.25, (W- (padding*2)), textSize*1.5), align="right")

    infoHeight += infoSpacing
    fill(0.5,0.5,0.5,1)
    rect(padding, infoHeight, (W- (padding*2)), trackSize)
    fill(1)
    oval(((W - (padding*2)) * xprnVal) -(ovalSize/2) + padding, infoHeight-(ovalSize/2)+(trackSize/2), ovalSize, ovalSize)
    textBox(f"XPRN", (padding, infoHeight + padding*0.25, (W- (padding*2)), textSize*1.5))
    textBox(f"{x}", (padding, infoHeight + padding*0.25, (W- (padding*2)), textSize*1.5), align="right")

    currentProp = 0
    infoHeight += infoSpacing
    fill(0.5,0.5,0.5,1)
    rect(padding, infoHeight, (W- (padding*2)), trackSize)
    fill(1)
    oval(((W - (padding*2)) * currentProp) -(ovalSize/2) + padding, infoHeight-(ovalSize/2)+(trackSize/2), ovalSize, ovalSize)
    textBox(f"PROP", (padding, infoHeight + padding*0.25, (W- (padding*2)), textSize*1.5))
    textBox(f"{p}", (padding, infoHeight + padding*0.25, (W- (padding*2)), textSize*1.5), align="right")

    # page number

    textBox(str(frame + 1), (padding, padding*0.5, (W- (padding*2)), textSize*1.5), align="right")

    if debug:

        print(str(frame).ljust(3), " | factor: ", str(round(factor, 3)).ljust(5)," | t: ", str(round(t, 3)).ljust(5), " | wght: ", str(round(currentWght, 0)).ljust(5),\
        " | y: ", str(round(y, 3)))

        size = padding * 0.15

        # visual of each stage along curve
        fill(0,1,1,0.25)
        quarter = curveDict[0.25][0]
        rect(quarter, 0, size, H)
        half = curveDict[0.5][0]
        rect(half, 0, size, H)
        threequarters = curveDict[0.75][0]
        rect(threequarters, 0, size, H)

        
        fill(0,1,1,1)
        fontSize(textSize*0.625)
        text("t 0.25", quarter + padding*0.5, H - padding)
        text("t 0.50", half + padding*0.5, H - padding)
        text("t 0.75", threequarters + padding*0.5, H - padding)

        # overall y value progress bar
        fill(1,0,1,1)
        
        rect(W-size,0, size, H*y/H )      # y - curved
        rect(0,0, size, H*y/H )      # y - curved


        

        for i in range(frames):
            
            fill(0.6,0.6,0.6,0.375)
            t = i / frames

            x,y = getCurveXY(t)
            
            size = padding * 0.375
            # oval(x-size/2, (y*0.375)+(H/12)-(size/2), size, size) # covering letters
            oval(x-size/2, (y)-(size/2), size, size)
            
        fill(1,0,1,1)
        t = frame / frames
        
        x,y = getCurveXY(t)
                
        size = padding * 0.5
        # oval(x-size/2, (y*0.375)+(H/12)-(size/2), size, size) # covering letters
        oval(x-size/2, (y)-(size/2), size, size)


now = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M") # -%H_%M_%S

saveImage("/Users/stephennixon/type-repos/recursive/src/proofs/drawbot-diagrams-etc/flipbook/exports/recursive-flipbook-axes-" + now + "." + format)

endDrawing()