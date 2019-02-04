
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
            with open(os.path.join("./inc_raw/",str(num).strip()+".txt"),"r") as file:
                self.incNum = file.readline().strip()
                self.imgs = file.readline().strip()
                self.attInfo = file.readline().strip()
                self.tar = file.readline().strip()
                self.vuln = file.readline().strip()
                self.response = file.readline().strip()
                self.result = file.readline().strip()
                
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
        
    def saveall(self):
        self.write_to_tex()
        self.write_to_raw()
        
    def write_to_tex(self):
        self.setPreamble()
        self.setEndamble()
        
        try:
            fout = os.path.join("./inc_tex/",str(self.incNum)+".tex")
            with open(fout,"w") as file:
                file.write(self.PREAMBLE)
                
                if (self.imgs != ""):
                    file.write(self.secImages(self.imgs))
                if (self.attInfo != ""):
                    file.write(self.secAttackInfo(self.attInfo))
                if (self.tar != ""):
                    file.write(self.secTarget(self.tar))
                if (self.vuln != ""):
                    file.write(self.secVulnerability(self.vuln))
                if (self.response != ""):
                    file.write(self.secResponse(self.response))
                if (self.result != ""):
                    file.write(self.secResult(self.result))
                    
                file.write(self.ENDAMBLE)
        except Exception as e:
            print("Tex file opening failed")
            print(e)
            
    def write_to_raw(self):
        try:
            fout = os.path.join("./inc_raw/",str(self.incNum)+".txt")
            with open(fout,"w") as file:
                file.write(str(self.incNum)+"\n")
                file.write(self.imgs+"\n")
                file.write(self.attInfo+"\n")
                file.write(self.tar+"\n")
                file.write(self.vuln+"\n")
                file.write(self.response+"\n")
                file.write(self.result)
        except Exception as e:
            print("Save file opening failed")
            print(e)
        
    
    def setPreamble(self):
        self.PREAMBLE = """\documentclass[11pt]{article}

\\begin{document}

\\begin{titlepage}
	\\begin{center}
		
		\\line(1,0){300} \\\\
		[0.25in]
		\\huge{\\bfseries Team 11} \\\\
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
\\end{titlepage}""" % (str(self.incNum),str(self.tar),str("02/02/19"))

    def setEndamble(self):
        self.ENDAMBLE = """\end{document}"""
        
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
            
#if __name__ == "__main__":
#    test = IncidentWriter("<date>Novemeber 11, 2018</date><attInfo>The attacker came from california</attInfo>",1)
#    test.writeToFile("outfile.tex")
#    print(time.localtime(time.time()))   


