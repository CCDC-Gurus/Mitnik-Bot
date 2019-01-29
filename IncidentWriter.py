import time
import os

        
class Incident():
    
    def __init__(self,incNum):
        
        self.incNum = incNum
        self.imgs = ""
        self.attInfo = ""
        self.tar = ""
        self.vuln = ""
        self.response = ""
        self.result = ""
        
    def fromexisting(self, num):
        
        try:
            with open(os.oath.join("./inc_raw/",str(num)+".txt"),"r") as file:
                self.incNum = num
                self.imgs = file[1]
                self.attInfo = file[2]
                self.tar = file[3]
                self.vuln = file[4]
                self.response = file[5]
                self.result = file[6]
                
        except Exception as e:
            print(e)
        
    def set_num(self, num):
        self.incNum = num
        
    def set_imgs(self, imgs):
        self.imgs = imgs
        
    def set_attacker(self, attacker):
        self.attInfo = attacker
        
    def set_target(self, target):
        self.tar = target
        
    def set_vulnerability(self, vuln):
        self.vuln = vuln
        
    def set_response(self, resp):
        self.response = resp
        
    def set_result(self, res):
        self.result = res
    
    def get_num(self):
        return self.incNum





class IncidentWriter():
        
    ## Creates incident writer object from a given incident
    def __init__(self,incident):
        self.incident = incident
        
        # Format from incident
        self.incNum = incident.incNum
        self.imgs = self.secImages(incident.imgs)
        self.attInfo = self.secAttackInfo(incident.attInfo)
        
        # Im sorry...
        self.tar = incident.tar
        self.setPreamble()
        self.tar = self.secTarget(incident.tar)
        
        self.vuln = self.secVulnerability(incident.vuln)
        self.response = self.secResponse(incident.response)
        self.result = self.secResult(incident.result)
        
        
        # Date/Time of the Incident
        #self.date = self.setDate() # If date wasn't given, generate it
            
        self.setPreamble()
        self.setEndamble()
        
        self.writeToTexFile()
        self.writeToSaveFile()
        

    
    
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
\\end{titlepage}""" % (str(self.incNum),str(self.tar),str("01/24/19") )


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
    def writeToTexFile(self):
    
        try:
            fout = os.path.join("./inc_tex/",str(self.incNum)+".tex")
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
        except Exception as e:
            print("Tex file opening failed")
            print(e)
            
    def writeToSaveFile(self):
        try:
            fout = os.path.join("./inc_raw/",str(self.incident.incNum)+".txt")
            with open(fout,"w") as file:
                file.write(str(self.incident.incNum)+"\n")
                file.write(self.incident.imgs+"\n")
                file.write(self.incident.attInfo+"\n")
                file.write(self.incident.tar+"\n")
                file.write(self.incident.vuln+"\n")
                file.write(self.incident.response+"\n")
                file.write(self.incident.result)
        except Exception as e:
            print("Save file opening failed")
            print(e)
            
if __name__ == "__main__":
    test = IncidentWriter("<date>Novemeber 11, 2018</date><attInfo>The attacker came from california</attInfo>",1)
    test.writeToFile("outfile.tex")
    print(time.localtime(time.time()))   


