# Formats text into an HTML page featuring lists, buttons and an accordion
# Takes .txt files from ../../TXT/, converts to HTML and outputs to ../../HTML/skills-technologies.html
# Requires ./head.html and ./script.html

import os, string

PATH = './'
ROOT = '../../'
inPATH = ROOT + 'TXT/'
outPATH = ROOT + 'HTML/skills-technologies.html'

S = 'skills'
T = 'technologies'

# LPI = Lines Per Item
LPI = 5

class Item:    
    def __init__(self, title, experience, companies, description):
        self.Title = title
        self.Experience = experience
        self.Companies = companies
        self.Description = description     

def writeToFile(HTML):
    file = open(outPATH, 'w')
    file.write(HTML)
    file.close()

def readFile(filename, path):
    file = open(path + filename)
    TXT = file.read()
    file.close()
    return TXT

# returns list of Item class objects
def getItem(TXT):
    def getNumberOfItems(TXT):
        n=0
        for c in TXT:
            if c == '\n':
                n += 1
        return int((n+2)/LPI)
    
    def getItemBlock(TXT, nItems):
        itemBlock = [''] * nItems
        startIndex=0
        endIndex=0
        for itemIndex in range(nItems):
            newlines = 0
            for charIndex in range(startIndex, len(TXT)):
                if TXT[charIndex] == '\n':
                    newlines += 1
                    if newlines == LPI - 1:
                        endIndex = charIndex
                        itemBlock[itemIndex] = TXT[startIndex:endIndex]
                        startIndex = endIndex + 2
                        charIndex = len(TXT) + 1
        return itemBlock
    
    nItems = getNumberOfItems(TXT)
    itemBlock = getItemBlock(TXT, nItems)
    
    item = [Item('','','','')] * nItems
    for itemIndex in range(nItems):
        block = itemBlock[itemIndex] + '\n'
        i = Item('','','','')
        startIndex=0
        endIndex=0
        it=0 # iterator
        for charIndex in range(len(block)):
            if block[charIndex] == '\n':
                endIndex = charIndex
                if it == 0: i.Title=block[startIndex:endIndex]
                if it == 1: i.Experience=block[startIndex:endIndex]
                if it == 2: i.Companies=block[startIndex:endIndex]
                if it == 3: i.Description=block[startIndex:endIndex]
                startIndex = endIndex + 1
                it += 1
        item[itemIndex] = i
    return item

def getListHTML(skills, tech):
    def getList(item):
        title = [''] * len(item)
        for index in range(len(item)):
            title[index] = item[index].Title
        return title
    
    def formatList(title, mode):
        HTML = title
        for index in range(len(title)):
            HTML[index] = '<li><a href="#%s_%s">%s</a></li>\n' % (mode.upper(), index, title[index])
        return HTML

    skillsList = getList(skills)
    techList = getList(tech)
    skillsHTML = formatList(skillsList, S)
    techHTML = formatList(techList, T)

    HTML = '<h3 id="SKILLS_LIST">SKILLS</h3>\n'
    for i in range(len(skillsHTML)):
        HTML += skillsHTML[i]
    HTML += '</br>\n'
    HTML += '<h3 id="TECHNOLOGIES_LIST">TECHNOLOGIES</h3>\n'
    for i in range(len(techHTML)):
        HTML += techHTML[i]
    return HTML
    
def getAccordionHTML(skills, tech):
    def bold(line):
        bolded = '<b>'
        for i in range(len(line)):
            if line[i] == ':':
                bolded += line[0:i+1]
                bolded += '</b> '
                bolded += line[i+2:]
                return bolded
            
    def formatButton(title, index, mode):
        button = '<button id="%s_%s" class="accordion">\n' % (mode.upper(), index)
        button += '\t' + title + '\n'
        button += '</button>'
        return button
    
    def formatPanel(item, mode):
        panel = '<div class="panel">\n'
        panel += '\t<p>\n'
        panel += '\t\t' + bold(item.Experience) + '<br/>\n'
        panel += '\t\t' + bold(item.Companies) + '<br/><br/>\n'
        panel += '\t\t' + item.Description + '\n'
        panel += '\t</p>\n'
        panel += '\t<a href="#%s_LIST">Return to %s list</a>\n' % (mode.upper(), mode)
        panel += '</div>'
        return panel

    HTML = '<h3 id="SKILLS_ACCORDION">SKILLS</h3>\n'
    for i in range(len(skills)):
        sButton = formatButton(skills[i].Title, i, S)
        sPanel = formatPanel(skills[i], S) + '\n\n'
        HTML += sButton + '\n' + sPanel
    HTML += '<h3 id="TECHNOLOGIES_ACCORDION">TECHNOLOGIES</h3>\n'
    for i in range(len(tech)):
        tButton = formatButton(tech[i].Title, i, T)
        tPanel = formatPanel(tech[i], T) + '\n\n'
        HTML += tButton + '\n' + tPanel

    return HTML

def formatBodyHTML(listHTML, accordionHTML):
    bodyHTML = '<body>\n'
    bodyHTML += listHTML
    bodyHTML += '\n<br>\n'
    bodyHTML += accordionHTML
    bodyHTML += '\n' + readFile('script.html', PATH)
    bodyHTML += '</body>'
    return bodyHTML

# MAIN FUNCTION
def main():
    # Get text
    STXT = readFile(S+'.txt',inPATH)
    TTXT = readFile(T+'.txt',inPATH)
    # Get Item objects
    skills = getItem(STXT)
    tech = getItem(TTXT)
    # Format into HTML
    listHTML = getListHTML(skills, tech)
    accordionHTML = getAccordionHTML(skills, tech)
    # Get header, format body and concatenate
    headHTML = readFile('head.html', PATH) + '\n'
    bodyHTML = formatBodyHTML(listHTML, accordionHTML)
    HTML = headHTML + bodyHTML
    # WRITE IT OUT
    writeToFile(HTML)
    print 'successfully wrote to ' + str(os.path.abspath(outPATH))

if __name__ == '__main__':
    main()
