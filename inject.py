import time
#time.localtime(time.time())
## TimeTuple: 3,4,5 is hour,min,sec

class Inject():

    def __init__(self,tit,num,time,assigned):
    
        self.title = tit # Title or description
        self.num = num # Inject number
        self.time_end = time # In military time
        self.assigned = [] # Who is assigned to it
    
    ## Who is a string array of who is assigned to the
    ## inject. Used for initial assign.
    def assign(self, who):
        self.assigned = who
    
    ## Adds a single person to the inject.
    def add_person(self, person):
        self.assigned.append(person)
        
    ## Returns the list of people assigned to the inject.
    def get_assigned(self):
        return self.assigned
        
    ## Used to update the title
    def set_title(self, title):
        if (title != ""):
            self.title = title
            
    
    
    

class InjectTimer():

    def __init__(self):
    
        self.inject_arr = [] # Needs to act like a queue
        
    def add_inject(self, inject):
    
        
        