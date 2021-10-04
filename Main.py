# US Demographic Map
# Made By Seby Tremblay
# Last Edited: 3/3/2020

from graphics import *
import json
import random

makeGraphicsWindow(1200,700)

# Reads a File, Looks at Specified Data, Returns Dictionary of Data According to FIPS Code
def censusData(year,ageGroup,dataIndex,censusFile):
    countyData = {}
    for line in censusFile:
        line = line.strip()
        data = line.split(",")
        # Checks Year and Age Group
        if data[5] == year and data[6] == ageGroup:
            # Combines State and County FIPS to make Key Fips
            countyData[data[1]+data[2]] = data[dataIndex]
    return countyData
    
def startWorld(world):
    # Opens and Loads State and County Borders
    statesFile = open("states.json","r")
    countiesFile = open("counties.json","r")
    world.states = json.load(statesFile)
    world.counties = json.load(countiesFile)
    
    # Opens and Loads Census File
    censusFile = open("CC-EST2012-ALLDATA.csv","r")
    
    # Analyzes Data
    world.countyData = censusData("1","4",7,censusFile)
    
    # Defines Population Ranges
    world.colorKeys = [0,50,100,250,500,1000,5000,10000,50000,100000]
    # Relates Color to Population Range
    world.colors = {}
    
    # Makes Color for Each Population Range
    colorValue = 235
    for value in world.colorKeys:
        world.colors[value] = (0,colorValue-25,colorValue)
        colorValue -= 20
    
    # Ensures County is in Both Files
    for county in world.counties:
        if county["fips"] not in world.countyData.keys():
            world.counties.remove(county)
    
    # Creates County Information Dictionary of Lists
    world.countyInformation = {}
    for county in world.countyData.keys():
        # Defines Population
        value = int(world.countyData[county])
        # Decides Color
        for color in world.colors.keys():
            if value > color:
                colorShade = world.colors[color]
        # County FIPS Corresponds to List of Population, Color and Boolean if Mouse in County
        world.countyInformation[county] = [value,colorShade]
    
    # Defines Position of Key
    world.colorX,world.colorY = 1000,460
    world.colorW,world.colorH = 50,20       

    # Relates Color to Y-Value for Key
    world.keyColorY = {}
    for color in world.colors.keys():
        world.keyColorY[color] = world.colorY
        world.colorY += 20
    
    # Fun Stuff
    world.kentuckyBool = False
    world.kentuckyStates = {"Minnesota":"gainsboro","Iowa":"cornsilk","Missouri":"gainsboro","Arkansas":"darkblue","Louisiana":"black","Tennessee":"gray","Kentucky":"goldenrod"}
    world.kentuckyDict = {}
    
    for state in world.states:
        if state["name"] in world.kentuckyStates.keys():
            world.kentuckyDict[state["name"]] = [state["polygons"],world.kentuckyStates[state["name"]]]
       
def updateWorld(world):
    # Gets User Mouse Position
    [world.mouseX,world.mouseY] = getMousePosition()
    # Gets FPS, Limits to 3 Digits
    world.FPS = "%.1f" % getActualFrameRate()
    # Kentucky Chicken Bool
    if isKeyPressed("space"):
        world.kentuckyBool = True
    else:
        world.kentuckyBool = False
    
def drawWorld(world):
    if world.kentuckyBool == False:
        # Draws Counties
        for county in world.counties:
            for coordinates in county["polygons"]:
                # Draws With Assigned Color
                fillPolygon(coordinates,world.countyInformation[county["fips"]][1])
                # Draws Borders
                drawPolygon(coordinates)
                # Fills When Mouse Inside
                if pointInPolygon(world.mouseX,world.mouseY,coordinates) == True:
                    fillPolygon(coordinates,"black")
                    # Displays Information of Highlighted County
                    drawString("State Name: "+county["state"],25,550)
                    drawString("County Name: "+county["name"],25,575)
                    drawString("Population of 15-19 Year Olds in 2010: "+str(world.countyInformation[county["fips"]][0]),25,600,)
        # Draws Map Key
        drawString("Map Key:",1020,440,25)
        for color in world.colors.keys():
            fillRectangle(world.colorX,world.keyColorY[color],world.colorW,world.colorH,world.colors[color])
            drawRectangle(world.colorX,world.keyColorY[color],world.colorW,world.colorH,)
            drawString("More than "+str(color),world.colorX + 53,world.keyColorY[color] + 3,20)
        drawRectangle(1000,435,170,225,"black",3)
        # Fun Suprise
        drawString("Press [space] for a suprise!",25,650)        
    # Draws Kentucky Man
    else:
        for state in world.kentuckyDict.values():
            for coordinates in state[0]:
                fillPolygon(coordinates,state[1])
        drawString("Displayed here is the KFC chef.",25,525)
        drawString("Minnesota is his hat, and",25,550) 
        drawString("Louisiana is his boots.",25,575)
        drawString("Tennesse is his silver platter that",25,600) 
        drawString("holds Kentucky, his fried chicken!",25,625)
    # Draws State Borders
    for state in world.states:
        for coordinates in state["polygons"]:
            drawPolygon(coordinates,"black",2)    
    # Map Title
    drawString("US Demographic Map",780,5,50)
    drawString("By: Seby Tremblay",850,45,25)
    # Displays FPS
    drawString(world.FPS,1160,0,30,(0,230,0))
    
runGraphics(startWorld,updateWorld,drawWorld)
