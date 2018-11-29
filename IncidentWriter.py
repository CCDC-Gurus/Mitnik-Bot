import time


class IncidentWriter():
        
    def __init__(self,message,incNum):
        #self.TAG_INCNUM = "<incNum>"
        self.TAG_DATE = "<date>"
        self.TAG_IMGS = "<images>"
        self.TAG_ATTINFO = "<attInfo>"
        self.TAG_TAR = "<tar>"
        self.TAG_VULN = "<vuln>"
        self.TAG_RESPONSE = "<response>"
        self.TAG_RESULT = "<result>"
        
        self.incNum = incNum
        self.imgs = ""
        self.attInfo = ""
        self.tar = ""
        self.vuln = ""
        self.response = ""
        self.result = ""
            
        # Date/Time of the Incident
        if self.TAG_DATE in message:
            data = self.msgParse(message, self.TAG_DATE)
            self.date = data
        else:
            self.date = self.setDate() # If date wasn't given, generate it
            
        # Comma Seperated list of images to be included
        if self.TAG_IMGS in message:
            data = self.msgParse(message, self.TAG_IMGS)
            self.imgs = self.secImages()
            
        # Attacker info
        if self.TAG_ATTINFO in message:
            data = self.msgParse(message, self.TAG_ATTINFO)
            self.attInfo = self.secAttackInfo(data)
            
        # Target of attacker
        if self.TAG_TAR in message:
            data = self.msgParse(message, self.TAG_TAR) # parse the data
            self.tar = self.secTarget(data) # format the data

            
        # What was the vulnerability
        if self.TAG_VULN in message:
            data = self.msgParse(message, self.TAG_VULN)
            self.VULN = self.secVulnerability(data)
            
            
        # Our response
        if self.TAG_RESPONSE in message:
            data = self.msgParse(message, self.TAG_RESPONSE)
            self.repsonse = self.secResponse(data)
            
            
        # Result of attack and actions taken
        if self.TAG_RESULT in message:
            data = self.msgParse(message, self.TAG_RESULT)
            self.result = self.secResult(data)
            
        
    
        #self.incNum = incNum
        #self.date = 20
        #self.imgs = imgs
        #self.attInfo = attInfo
        #self.tar = tar
        #self.vuln = vuln
        #self.response = response
        #self.result = result
        self.setPreamble()
        self.setEndamble()
        
    
    # Start of the LaTeX document
    def setPreamble(self):
        self.PREAMBLE = """\documentclass[11pt]{article}

\\begin{document}

\\begin{titlepage}
	\\begin{center}
		
		\\line(1,0){300} \\\\
		[0.25in]
		\\huge{\\bfseries M57} \\\\
		[2mm]
		\\line(1,0){200} \\\\
		[1.5cm]
		\\textsc{\\LARGE Incident - %s} \\\\
		[10cm]
		
	\\end{center}
	\\begin{flushright}
		\\textsc{\\large %s \\\\
			Found: %s \\\\}
	\\end{flushright}
\\end{titlepage}""" % (str(self.incNum),str(self.tar),str(self.date) )


    def setEndamble(self):
        self.ENDAMBLE = """\end{document}"""

    # Parses the discord message looking for a tag
    def msgParse(self, text, TAG):
        i = text.index(TAG) + len(TAG) # First letter of data
        j = text.index(TAG[0] + "/" + TAG[1:]) # One past last letter of data
        
        return text[i:j]
              

    # Takes a string of image filenames seperated by commas
    def secImages(self,data):
        combo = "\\section*{Images}\\label{sec:img}\n"
        images = data.split(",")
        
        for img in images:
            combo += """\\begin{figure}
  \\includegraphics[width=\\linewidth]{%s}
\\end{figure}\n
""" % (img.strip())
        
        return combo
    
    # A String representing the paragraph
    def secAttackInfo(self,data):
        combo = "\\section*{Attack Information}\\label{sec:attinfo}\n"
        combo += data + "\n"
        return combo
        
    # A String representing the paragraph
    def secTarget(self,data):
        combo = "\\section*{Target}\\label{sec:tar}\n"
        combo += data + "\n"
        return combo
        
    # A String representing the paragraph
    def secVulnerability(self,data):
        combo = "\\section*{Vulnerability}\\label{sec:vuln}\n"
        combo += data + "\n"
        return combo
        
    # A String representing the paragraph
    def secResponse(self,data):
        combo = "\\section*{Response}\\label{sec:response}\n"
        combo += data + "\n"
        return combo
        
    # A String representing the paragraph
    def secResult(self,data):
        combo = "\\section*{Result}\\label{sec:result}\n"
        combo += data + "\n"
        return combo
        
    # Write out to a tex file
    def writeToFile(self,fout):
    
        try:
            with open(fout,"w") as file:
                file.write(self.PREAMBLE)
                
                if (self.imgs != ""):
                    file.write(self.imgs)
                if (self.attInfo != ""):
                    file.write(self.attInfo)
                if (self.tar != ""):
                    file.write(self.tar)
                if (self.vuln != ""):
                    file.write(self.vuln)
                if (self.response != ""):
                    file.write(self.response)
                if (self.result != ""):
                    file.write(self.result)
                    
                file.write(self.ENDAMBLE)
        except:
            print("File opening failed")
            
if __name__ == "__main__":
    test = IncidentWriter("<date>Novemeber 11, 2018</date><attInfo>The attacker came from california</attInfo>",1)
    test.writeToFile("outfile.tex")
    print(time.localtime(time.time()))   


