# SkillFormatter.py
# poop
#
# Legend:
#   x = Finished
#   / = In Progress
#   _ = Not Started
#
# REQUIREMENTS/TODO:
#   For each mode:
#       x Read a file in a set path
#       / Convert each file into an html formatted output
#       x Write to a set file path
#   LONG TERM GOALS
#       _ Clone/Update from set github repository
#           https://github.com/enhinnen/ResumeWeb
#       _ After conversion, push to repository and clean up local files
#   KNKOWN ISSUES:
#       _ Need to add newlines to HTML output ('\\n') after each newline in an item

import os

PATH = './'
inPATH = './'
outPATH = './'

# modes
S = 'skills'
T = 'technologies'
F = 'full'

def getInPath(mode):
    return inPATH + mode + '.txt'

def getOutPath(mode):
    return outPATH + mode + '.html'

def writeToFile(HTML, mode):
    path = getOutPath(mode)
    file = open(path, 'w')
    file.write(HTML)
    file.close()

def getTXT(mode):
    path = getInPath(mode)
    file = open(path)
    TXT = file.read()
    file.close()
    return TXT

def readFile(filename):
    file = open(PATH + filename)
    HTML = file.read()
    file.close()
    return HTML

def getHTML(itemHTML):
    HTML = ''
    for itemHTMLIndex in range(len(itemHTML)):
        HTML += itemHTML[itemHTMLIndex] + '\n'
    return HTML

def getLinesPerItem(mode):
    if mode == S or mode == T:
        return 5

def getNumberOfItems(TXT, mode):
    n = 0
    for c in TXT:
        if c == '\n':
            n += 1
    return int((n+2) / getLinesPerItem(mode))

def getItemTXT(TXT, numberOfItems, mode):
    itemTXT = [''] * numberOfItems
    startIndex = 0
    endIndex = 0
    for itemIndex in range(numberOfItems):
        newlines = 0
        for TXTIndex in range(startIndex, len(TXT)):
            if TXT[TXTIndex] == '\n':
                newlines += 1
                if newlines == getLinesPerItem(mode) - 1:
                    endIndex = TXTIndex
                    itemTXT[itemIndex] = TXT[startIndex:endIndex]
                    startIndex = endIndex + 2
                    TXTIndex = len(TXT) + 1
        itemTXT[itemIndex] += '\n'
    return itemTXT

def getItemListTXT(itemTXT):
    itemListTXT = [''] * len(itemTXT)
    for itemIndex in range(len(itemTXT)):
        newlines = 0
        for itemCharIndex in range(len(itemTXT[itemIndex])):
            if itemTXT[itemIndex][itemCharIndex] == '\n':
                newlines += 1
                if newlines == 1:
                    itemListTXT[itemIndex] = itemTXT[itemIndex][:itemCharIndex]
                    itemCharIndex = len(itemTXT[itemIndex]) + 1
    return itemListTXT

def getItemAccordionTXT(itemTXT, mode):
    itemAccordionTXT = [''] * len(itemTXT)
    for itemIndex in range(len(itemTXT)):
        itemStringIndex = 0
        endIndex = 0
        newlines = 0
        while endIndex < len(itemTXT[itemIndex]):
            if itemTXT[itemIndex][itemStringIndex] == '\n':
                newlines += 1
                startIndex = itemStringIndex + 1
                endIndex = startIndex + 1
                try:
                    while itemTXT[itemIndex][endIndex] != '\n':
                        endIndex += 1
                except:
                    iDontKnowWhatImDoing=True
                for n in range(2, getLinesPerItem(mode) - 1):
                    if newlines == n:
                        itemAccordionTXT[itemIndex] += '<br/>'
                if newlines == getLinesPerItem(mode) - 2:
                    itemAccordionTXT[itemIndex] += '<br/>'
                itemAccordionTXT[itemIndex] +=itemTXT[itemIndex][startIndex:endIndex + 1]
                if endIndex < len(itemTXT[itemIndex]) - 1:
                    itemAccordionTXT[itemIndex] += '\t\t'
            itemStringIndex += 1
    return itemAccordionTXT

def getItemListHTML(itemListTXT, mode):
    itemListHTML = [''] * len(itemListTXT)
    for itemIndex in range(len(itemListTXT)):
        buttonID = mode.upper() + '_' + str(itemIndex)
        itemListHTML[itemIndex] = '<li><a href="#' + buttonID + '">' + itemListTXT[itemIndex] + '</a></li>'
    return itemListHTML

def getItemAccordionHTML(itemListTXT, itemAccordionTXT, mode):
    itemAccordionHTML = [''] * len(itemAccordionTXT)
    for itemIndex in range(len(itemAccordionTXT)):
        buttonID = mode.upper() + '_' + str(itemIndex)
        itemAccordionHTML[itemIndex] = '<button id="' + buttonID + '" class="accordion">\n\t' + itemListTXT[itemIndex] + '\n</button>\n<div class="panel">\n\t<p>\n\t\t' + itemAccordionTXT[itemIndex] + '\t</p>\n\t<a href="#' + mode.upper() + '_LIST">Return to ' + mode + ' list</a>\n</div>\n'
    return itemAccordionHTML                

def main():
    return 0
    
# END MAIN

if __name__ == '__main__':
    main()

#-----------------TESTING AREA BELOW THIS LINE - DELETE EVERYTHING BEFORE FINAL USE-----------------
br = '\n</br>\n'
    
def run():
    sTXT = getTXT(S)
    numberOfSkills = getNumberOfItems(sTXT, S)
    skillsTXT = getItemTXT(sTXT, numberOfSkills, S)
    skillsListTXT = getItemListTXT(skillsTXT)
    skillsListHTML = getItemListHTML(skillsListTXT, S)
    skillsAccordionHTML = getItemAccordionHTML(skillsListTXT, getItemAccordionTXT(skillsTXT, S), S)

    tTXT = getTXT(T)
    numberOfTechnologies = getNumberOfItems(tTXT, T)
    technologiesTXT = getItemTXT(tTXT, numberOfTechnologies, T)
    technologiesListTXT = getItemListTXT(technologiesTXT)
    technologiesListHTML = getItemListHTML(technologiesListTXT, T)
    technologiesAccordionHTML = getItemAccordionHTML(technologiesListTXT, getItemAccordionTXT(technologiesTXT, T), T)

    listHTML = '<h3 id="SKILLS_LIST">SKILLS</h3>\n' + getHTML(skillsListHTML)+ br + '<h3 id=TECHNOLOGIES_LIST">TECHNOLOGIES</h3>\n' + getHTML(technologiesListHTML)
    accordionHTML = '<h3 id="SKILLS_ACCORDION">SKILLS</h3>\n' + getHTML(skillsAccordionHTML) + br + br + '<h3 id=TECHNOLOGIES_ACCORDION">TECHNOLOGIES</h3>\n' + getHTML(technologiesAccordionHTML)

    bodyHTML = '<body>\n' + listHTML + br + '\n' + accordionHTML + '\n' + readFile('script.html') + '\n</body>'

    HTML = readFile('head.html') + '\n' + bodyHTML
    
    writeToFile(HTML, F)
