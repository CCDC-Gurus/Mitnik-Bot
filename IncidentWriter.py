## IncidentWriter 
## A representation for Incidents that might occur during
## a CCDC competition.
## Gavin Lewis - 2018

from time import strftime
import os
import subprocess

        
class Incident():
    """An Incident object represents a single incident
    with the following attributes:
        1) Incident Number
        2) An array of Images
        3) Attacker information
        4) Targeted machine/service
        5) How it was found
        6) What was vulnerable
        7) Response taken to incident
        8) Result of incident
    Functions inlcude:
        1) Saving to a .tex file
        2) Saving to a .txt file
        3) Creating new incidents from user inupt.
        4) Listing current incidents.
        5) Editing incidents.
    """
    
    def __init__(self, incNum):
        
        self.incNum = incNum
        self.imgs = []
        self.attInfo = ""
        self.tar = ""
        self.found = ""
        self.vuln = ""
        self.response = ""
        self.result = ""

        self.PREAMBLE = """\\documentclass[11pt]{article}
\\usepackage{graphicx}
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
\\end{titlepage}\n""" % (str(self.incNum), str(self.tar), strftime("%A, %d %B, %Y. %H:%M"))

        self.ENDAMBLE = """\end{document}"""
   

    def fromexisting(self, num):
        """Generates an incident object from a .txt file
        
        Used to edit an incident
        """
        try:
            with open(os.path.join("./inc_raw/", str(num).strip()+".txt"), "r") as file:
                self.incNum = file.readline().strip()
                
                ## NEEDS UPDATED
                tmp_imgs = file.readline().strip().split(",")
                tmp_imgs.pop()
                self.imgs = tmp_imgs
                self.attInfo = file.readline().strip()
                self.tar = file.readline().strip()
                self.found = file.readline().strip()
                self.vuln = file.readline().strip()
                self.response = file.readline().strip()
                self.result = file.readline().strip()
                
        except Exception as e:
            print(e)
        
    def set_num(self, num):
        self.incNum = num
        
    def set_imgs(self, imgs):
        self.imgs = imgs # Instead of a string, this is a list
        
    def set_attacker(self, attacker):
        self.attInfo = attacker
        
    def set_target(self, target):
        self.tar = target
        
    def set_found(self, found):
        self.found = found
        
    def set_vulnerability(self, vuln):
        self.vuln = vuln
        
    def set_response(self, resp):
        self.response = resp
        
    def set_result(self, res):
        self.result = res
    
    def get_num(self):
        return self.incNum
        
########################################################
###
###     Saving operations
###
########################################################
    def saveall(self):
        if (self.write_to_tex() and self.write_to_raw()):
            return True
        else:
            return False
        
    def write_to_tex(self):
        """Writes the contents of the incident to a LaTeX formatted file."""

        try:
            # Generate a filename "incident_number-curr_time.tex"
            fout = os.path.join("./inc_tex/", str(self.incNum) + "-" + str(strftime("%H-%M-%S")) + ".tex")
            with open(fout, "w") as file:
                file.write(self.PREAMBLE)
                
                if (self.imgs):
                    file.write(self.secImages(self.imgs))
                if (self.attInfo):
                    file.write(self.secAttackInfo(self.attInfo))
                if (self.tar):
                    file.write(self.secTarget(self.tar))
                if (self.found):
                    file.write(self.secFound(self.found))
                if (self.vuln):
                    file.write(self.secVulnerability(self.vuln))
                if (self.response):
                    file.write(self.secResponse(self.response))
                if (self.result):
                    file.write(self.secResult(self.result))
                    
                file.write(self.ENDAMBLE)
                try:
                    #os.system("latexmk -pdf " + fout)
                    #subprocess.run(["latexmk", "-pdf", fout])
                    #os.system("latexmk -c")
                    print("[+] LaTeX compile succeeded")
                except:
                    print("[-] LaTeX compile failed")
                return True
        except Exception as e:
            print("Tex file saving failed")
            print(e)
            return False
            
    def write_to_raw(self):
        """Writes the information to a file line by line for backup, and for on-the-fly editing."""
        try:
            fout = os.path.join("./inc_raw/", str(self.incNum) + ".txt")
            with open(fout, "w") as file:
                file.write(str(self.incNum) + "\n")
                # Images are stored in a list
                for img in self.imgs:
                    file.write(img + ",")
                file.write("\n")
                file.write(self.attInfo + "\n")
                file.write(self.tar + "\n")
                file.write(self.found + "\n")
                file.write(self.vuln + "\n")
                file.write(self.response + "\n")
                file.write(self.result)
            return True
        except Exception as e:
            print("Save file opening failed")
            print(e)
            return False

########################################################
###
###     The following assist in formatting for use in
### saving to a LaTeX file format. The pdf will begin
### generated outside of the program.
###
########################################################

    # Takes list of image file names
    # Needs to return a string
    def secImages(self, data):
        combo = "\\section*{Images}\\label{sec:img}\n"
        #images = data.split(",")
        
        # img is a filename
        for img in self.imgs:
            combo += """\\begin{figure}
  \\includegraphics[width=\\linewidth]{../images/%s}
\\end{figure}\n
""" % (img.strip())
        
        return combo
    
    # A String representing the paragraph
    def secAttackInfo(self, data):
        combo = "\\section*{Attacker Information}\\label{sec:attinfo}\n"
        combo += data + "\n"
        return combo
        
    # A String representing the paragraph
    def secTarget(self, data):
        combo = "\\section*{Target}\\label{sec:tar}\n"
        combo += data + "\n"
        return combo
        
    # A String representing the paragraph
    def secFound(self, data):
        combo = "\\section*{How the Attack was Found}\\label{sec:found}\n"
        combo += data + "\n"
        return combo
        
    # A String representing the paragraph
    def secVulnerability(self, data):
        combo = "\\section*{Vulnerability}\\label{sec:vuln}\n"
        combo += data + "\n"
        return combo
        
    # A String representing the paragraph
    def secResponse(self, data):
        combo = "\\section*{Response to Attack}\\label{sec:response}\n"
        combo += data + "\n"
        return combo
        
    # A String representing the paragraph
    def secResult(self, data):
        combo = "\\section*{Result of Response}\\label{sec:result}\n"
        combo += data + "\n"
        return combo
            