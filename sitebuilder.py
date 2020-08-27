import os
import readline
from bs4 import BeautifulSoup

sitename = ""
html= None
css = None 
js = None
currentSectionDir = '' 
scriptList = []

defaultScripts = "<script src=\"https://code.jquery.com/jquery-3.5.1.min.js\" integrity=\"sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=\" crossorigin=\"anonymous\"></script><script src=\"https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js\" integrity=\"sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q\" crossorigin=\"anonymous\"></script> <script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js\" integrity=\"sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl\" crossorigin=\"anonymous\"></script><script type=\"module\" src=\"https://unpkg.com/ionicons@5.1.2/dist/ionicons/ionicons.esm.js\"></script><script nomodule=\"\" src=\"https://unpkg.com/ionicons@5.1.2/dist/ionicons/ionicons.js\"></script>"

class MyCompleter(object):  # Custom completer

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options 
                                    if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try: 
            return self.matches[state]
        except IndexError:
            return None


class Site:

    sitename = ""
    pages=[]
    css = None

    def __init__(self):
        print("Enter website name:")
        readline.parse_and_bind('tab: self-insert')
        Site.sitename = str(input())
        try:
            os.mkdir("./"+Site.sitename);
            os.mkdir(Site.sitename+"/css");
            os.mkdir(Site.sitename+"/js");
            Site.css = open(Site.sitename+"/css/styles.css", "w");
            self.initializeCss()
        except:
            print("!!! Couldn't create folder structure for the site !!!")
            exit()
        self.getCommands();


    def initializeCss(self):
        content = "*{font-family:Quicksand,sans-serif;color:#333}body{background-color:#f7f7f7}a{text-decoration:none;color:#333}a:hover{text-decoration:none;color:#7cc49c}a.highlight,a.highlight i{color:#7cc49c;margin-bottom:5px}a.highlight i:hover,a.highlight:hover{color:#89d2aa}a.cta-link{color:#fefefe;background:#7cc49c;border-radius:30px;padding:5px 10px}a.cta-link:hover{background:#89d2aa}p{font-size:1.1em;font-weight:lighter;line-height:1.6em}p a,small a{color:#7cc49c}p a:hover,small a:hover{color:#333}h5{color:#72b490}h2{margin-bottom:1em;font-size:2.3em;font-weight:lighter}.btn-primary,a.btn,button{padding:7px 19px;font-size:16px;line-height:24px;text-transform:uppercase;margin:10px 0;background-color:#89d2aa;border-radius:0;border:none;color:#fefefe}.btn-primary:hover,a.btn:hover,button:hover{background-color:#72b490;color:#fefefe}section{margin-bottom:1em}"
        content = self.beautifyCss(content)
        Site.css.write(content)

    def beautifyCss(self, content):
        content = content.replace("{", "{\n")
        content = content.replace("}", "\n}\n\n")
        content = content.replace(";", ";\n")
        return content


    def getCommands(self):
        self.listCommands()
        command = ""
        while(command !="q"):
            print()
            print("==============================================")
            print("Editing " +Site.sitename+", awaiting commands.")
            readline.parse_and_bind('tab: self-insert')
            command = str(input());
            self.executeCommand(command);

    def listCommands(self):
        print()
        print("===========================")
        print("List of available commands:")
        print("\tl:\tList pages")
        print("\tp:\tAdd Page")
        print("\tc:\tCustomize Page")
        print("\tr:\tRemove Page")
        print("\tn:\tChange Name")
        print("\tq:\tExit")
    
    def listPages(self):
        if len(Site.pages) > 0:
            print()
            print("=============")
            print("Current pages:")
            print()
            for page in Site.pages:
                print(page.name)
            print();
        else:
            print("=========")
            print("There aren't any pages yet")

    def executeCommand(self, cmd):
        if(cmd=="q"):
            self.buildSite()
            return
        elif(cmd == "p"):
            self.addPage()
        elif(cmd=="c"):
            self.customizePage()    
        elif(cmd=="r"):
            self.removePage()
        elif(cmd=="n"):
            self.renameSite()
        elif(cmd=="l"):
            self.listPages()
        elif(cmd=="h"):
            self.listCommands()
        else:
            print("!!! Unknown command, please try again !!!")
    
    def buildSite(self):
        for page in Site.pages:
            page.builder.run()

    def findPage(self, name):
        for page in Site.pages:
            if page.name == name:
                return page;
        return -1;

    def addPage(self):
        #TODO: page hierarchy
        print()
        print("===========")
        print("Adding page")
        print("Enter a name for the new page:")
        readline.parse_and_bind('tab: self-insert')
        page = Page(str(input()), self) 
        Site.pages.append(page)

    def renameSite(self):
        print()
        print("====================")
        print("Current site name is: "+ Site.sitename)
        print()
        print("Type new name:")
        readline.parse_and_bind('tab: self-insert')
        Site.sitename = str(input())

    def removePage(self):
        print()
        print("===============")
        print("Removing a page")
        print()
        print("Which page would you like to remove?")

        # Setting up autocomplete
        completer = MyCompleter((p.name for p in Site.pages))
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')

        page = self.findPage(str(input()))
        if(page == -1):
            print("!!! Page not found, please try again !!!")
        else:
            Site.pages.remove(page)

    def customizePage(self):
        print()
        print("==================")
        print("Customizing a page")
        print()
        print("Which page would you like to customize?")

        # Setting up autocomplete
        completer = MyCompleter((p.name for p in Site.pages))
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')

        selected_page = self.findPage(str(input()))
        if(selected_page == -1):
            print("!!! Page not found, please try again !!!")
        else:
            selected_page.customize()

class Page:

    def __init__(self, name, site):
        #Init
        self.name = name
        self.site = site
        self.sections = []
        self.builder = PageBuilder(self)

        self.footerIncludeList = []
        self.createHtml()
        # Start customizing
        self.customize()

    def createHtml(self):
        self.html = open(self.site.sitename + "/" + self.getSlug() + ".html", "w")

    def getSlug(self):
        return self.name.lower().replace(" ", "_")

    def customize(self):
        print("CUSTOMIZING PAGE: " + self.name)
        self.getCommands()

    def getCommands(self):
        self.listCommands()
        command = ""
        while(command !="q"):
            print()
            print("==============================================")
            print("Customizing " +self.name+", awaiting commands.")
            readline.parse_and_bind('tab: self-insert')
            command = str(input())
            self.handleCommand(command)

    def listCommands(self):
        print()
        print("===========================")
        print("List of available commands:")
        print("\tl:\t List current sections and modules")
        print("\ts:\t Add section")
        print("\tm:\t Add module")
        print("\trs:\t Remove section")
        print("\trm:\t Remove modules")
        print("\tr:\t Reorder sections")
        print("\tq:\t Back")

    def handleCommand(self, cmd):
        if(cmd=="q"):
            return
        elif(cmd == "s"):
            self.addSection()
        elif(cmd == "l"):
            self.list()
        elif(cmd == "rs"):
            if(self.removeSection()):
                print("!!! Section not found, please try again !!!")
        elif(cmd == "r"):
            self.reorderSections()
        elif(cmd == "h"):
            self.listCommands()
        else:
            print("!!! Unknown command, please try again !!!")

    def addSection(self):
        print()
        print("======================")
        print("Choose a section type!")

        completer = MyCompleter(self.getSections())
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')

        section = str(input())
        if(self.findSection(section)):
            print("Section " + section + " not found!");
            return 1;
        else:
            self.sections.append(Section(section, self))

    def list(self):
        print()
        print("=================")
        if(len(self.sections) == 0):
            print("There aren't any sections yet.")
        else:
            print("Current Sections:")
            numbering = 0
            for section in self.sections:
                print(str(numbering) + ".: " + section.name)
                numbering+=1

    def getSections(self):
        sections = []
        for path, subdirs, files in os.walk('./elements/'): #Traverse the current directory
            for name in files:
                if '.html' in name:  #Check for pattern in the file name
                    sections.append(os.path.basename(path))

        sections.sort();
        return sections;

    def findSection(self, section):
        for path, subdirs, files in os.walk('.'):
            for d in subdirs:
                if d == section:
                    global currentSectionDir
                    currentSectionDir = path + '/' + section
                    return 0;
        return 1;

    def removeSection(self):
        print()
        print("==============")
        print("Remove section")
        print()
        print("Which section would you like to remove?")

        # Setting up autocomplete
        completer = MyCompleter((s.name for s in self.sections))
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')

        # Finding section to delete
        selected = str(input())
        for section in self.sections:
            if(section.name == selected):
                self.sections.remove(section)
                print()
                print("Section removed")
                return 0
        return 1

    def reorderSections(self):
        self.list()
        print()
        print("Reordering Sections")
        print()

        # Setting up autocomplete
        completer = MyCompleter((s.name for s in self.sections))
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')
        
        new_order = []
        for i in range(len(self.sections)):
            print(str(i+1)+".: ", end=" ")
            name = str(input())
            while(self.getSectionByName(name) == -1):
                print("!!! Section not found, please try again !!!")
                print(str(i+1)+".: ", end=" ")
                name = str(input())

            new_order.append(self.getSectionByName(name))

        self.sections = list(new_order)

    def getSectionByName(self, name):
        for s in self.sections:
            if s.name == name:
                return s
        return -1


class Section:
    def __init__(self, section_type, page):
        self.type = section_type
        print(self.type)
        self.page = page
        self.directory = ""
        if(self.getDirectory()):
            print("===================================")
            print("!!! Section directory not found !!!")
            return
        print() 
        print("=============================")
        print("Enter a name for the section:")
        readline.parse_and_bind('tab: self-insert')
        self.name = str(input())

        print(self.type + " section named " + self.name + " has been created")



    def getDirectory(self):
        for path, subdirs, files in os.walk('.'):
            for d in subdirs:
                if d == self.type:
                    self.directory = path + '/' + self.type
                    return 0;
        return 1;
    

class PageBuilder:
    def __init__(self, page):
        self.page = page
        self.cssList = []

    def run(self):
        # Compiling head and head includes
        self.startPage()

        # Copying sections
        for s in self.page.sections:
            self.copySection(s)

        # Copying js files and adding footer includes
        self.footerIncludes()
        self.closePage()
    
    def startPage(self):
        content="<!doctype html><html lang=\"en\"> <head> <meta charset=\"utf-8\"> <meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\"> <link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css\" integrity=\"sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm\" crossorigin=\"anonymous\"> <link rel=\"stylesheet\" href=\"css/styles.css\"><title>"+self.page.name+"</title> </head> <body>"
        content = beautifyHtml(content)
        self.page.html.write(content)

    def copySection(self, s):
        error = 0
        htmlPath = s.directory + "/" + s.type + ".html"
        cssPath = s.directory + "/" + s.type + ".css"
        if(os.path.isfile(htmlPath)):
            if(self.copyHtml(htmlPath)):
                print("Error while copying html of "+ s.type)
                error = 1
        else:
            print("HTML file not found for "+ s.type)

        if(os.path.isfile(cssPath)):
            if(self.copyCss(cssPath, s.type)):
                print("Error while copying css of " + s.type)
                error = 1
                return error
        else:
            print("CSS file not found for " + s.type)

        return error

    def copyHtml(self, path):
        try:
            with open(path, 'r') as f:
                lines = f.readlines()
                self.page.html.writelines(lines) 
            return 0
        except:
            return 1
    
    def copyCss(self, path, sectype):
        try:
            if sectype not in self.cssList:
                self.cssList.append(sectype)
                with open(path, 'r') as f:
                    lines = f.readlines()
                    Site.css.writelines(lines)
            return 0
        except:
            return 1

    def footerIncludes(self):
        global defaultScripts
        self.page.html.write(defaultScripts)
        for s in self.page.sections:
            jsPath = s.directory + "/" + s.type + ".js"
            if(os.path.isfile(jsPath)):
                if(copyJs(jsPath)):
                    print("Copying js file for " + s.name + "failed")
                else:
                    # TODO write only once
                    self.page.html.write("<script src=\"js/" + s.type  + ".js\"></script>")

    def closePage(self):
        self.page.html.write("</body></html>")
        self.page.html.close()

    def copyJs(self, path):
        try:
            with open(path, "r") as f:
                lines = f.readlines()
                self.page.html.writelines(lines)
            return 0
        except:
            return 1;

def builder(): 
    if(createFiles()):
        print("Error while creating files")
    else:
        print("Enter sections to include (in order!)")
        print("(Write q to exit)")

        section = ""
        while(section!="q"):
            if(section=="q"): 
                closeHtml()
                return

            if(addSection(section)):
                print("Adding section " + section + " failed")
        closeHtml()

def addSection(section):
    return 0;



def createFiles():
    try:
        os.mkdir("./"+sitename);
        os.mkdir(sitename+"/css");
        os.mkdir(sitename+"/js");

        global html, css, js

        html = open(sitename + "/index.html", "w")
        css = open(sitename + "/css/styles.css", "w")
        js = open(sitename + "/js/scripts.js", "w")

        initializeHtml(html)
        initializeCss(css)
        return 0
    except:
        return 1




def beautifyHtml(htmlstring):
    return BeautifulSoup(htmlstring, 'html.parser').prettify()



def copyJs(path):
    global scriptList
    scriptList.append(os.path.basename(path))
    with open(path, "r") as f:
        lines = f.readlines()
        with open(Site.sitename + "/js/"+os.path.basename(path), "w") as n:
            n.writelines(lines)

def copyCss(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        css.writelines(lines) 

def closeHtml():
    includeScripts()
    html.write("</body></html>")

def includeScripts():
    print(scriptList)
    html.write("<!-- script includes -->")
    html.write(defaultScripts)
    for script in scriptList:
       html.write("<script src=\"js/" + script  + ".js\"></script>") 
    html.write("<!-- end of script includes -->")

def main():
    site = Site()

if __name__ == "__main__":
    main()

