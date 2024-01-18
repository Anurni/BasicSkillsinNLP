from math import log

class AbstrCondPr():                #parent class
    
    def __init__(self,obs):
        self.obs = obs
    
class CondPr(AbstrCondPr):         #subclass of AbstrCondPr, inherits all the attributes and methods

    """Takes a dictionary of raw counts of observed combinations
    and creates the probability distributions for Pr(b|a)"""

    def __init__(self, obs, k=0):
        super().__init__(obs)
        self.k = k
        self.probabilities = self.transform(k)

    def transform(self,k=0):   

        '''Transforms a dictionary of raw counts into a dictionary of probabilities'''
        probabilities = {}
        self.brands = {}
        for (brand,colour),values in self.obs.items():           #Creating a new dictionary where we can add our car 'instances' as keys
            if brand not in self.brands:
                self.brands[brand] = values
            else:
                self.brands[brand] = self.brands[brand] + values
        for (brand,colour),value in self.obs.items():      
            if k == 0:      
                prob = value / self.brands[brand] 
            elif k>0:
                prob = (value + k) / (self.brands[brand] + k * len(self.brands))
            probabilities[f"Pr('{colour}'|'{brand}')"] = prob
            probabilities[f"Pr('unseen'|'{brand}')"] = 0        #adding the special combinations in the distribution?
        probabilities[f"Pr('unseen'|'unseen')"] = "undefined"

        return probabilities


    def show(self): 

        """Prints out the conditional probabilities in a loop."""      

        self.transform()            #calling the transform-method inside this method
        for prob,value in self.probabilities.items():
            if value != 0 and value != "undefined":
                print(prob,value)

    def __getitem__(self, index):

        """Allows the use of standard Python indexing."""

        car = index[0]          
        colour = index[1]
        try:
            return self.probabilities[f"Pr('{colour}'|'{car}')"]
        except:                                                 #   executes if error raised with an unseen combination                                        
            if car in self.brands.keys():     #   if a seen (the car type is in the dictionary) but not together with b
                if self.k == 0:              
                    unseen_colour = self.probabilities[f"Pr('unseen'|'{car}')"]
                    return unseen_colour
                elif self.k > 0:
                    unseen_colour = self.k  / (self.brands[car] + self.k * len(self.brands))
                    return unseen_colour
            else:                               # if neither the car type or the colour are in the dictionary                                 
                if self.k == 0: 
                    both_unseen = self.probabilities["Pr('unseen'|'unseen')"]
                    return both_unseen
                if self.k > 0:
                    both_unseen = self.k / (self.k * len(self.brands))
                    return both_unseen

            


class LogCondPr(AbstrCondPr):       #subclass of AbstrCondPr
    def __init__(self, obs, k=0):
        super().__init__(obs)
        self.k = k
        self.log_probabilities = self.log_transform(k)

    def log_transform(self,k=0):   

        '''Transforms a dictionary of raw counts into a dictionary of log probabilities'''
        log_probabilities = {}
        self.brands = {}
        for (brand,colour),values in self.obs.items():           #Creating a new dictionary where we can add our car 'instances' as keys
            if brand not in self.brands:        
                self.brands[brand] = values
            else:
                self.brands[brand] = self.brands[brand] + values
        for (brand,colour),value in self.obs.items():      
            if k == 0:      
                prob = value / self.brands[brand] 
                log_prob = log(prob)
                if prob <=0:
                    log_prob = float("-inf")
            elif k>0:
                prob = (value + k) / (self.brands[brand] + k * len(self.brands))
                log_prob = log(prob)
                if prob <=0:
                    log_prob = float("-inf")
            log_probabilities[f"Pr('{colour}'|'{brand}')"] = log_prob
            log_probabilities[f"Pr('unseen'|'{brand}')"] = float("-inf")        #adding the special combinations in the distribution?
        log_probabilities[f"Pr('unseen'|'unseen')"] = "undefined"

        return log_probabilities
    

    def show(self): 

        """Prints out the conditional probabilities in a loop."""      

        self.log_transform()            #calling the transform-method inside this method
        for prob,value in self.log_probabilities.items():
            if "unseen" not in prob:
                print(prob,value)

    def __getitem__(self, index):

        """Allows the use of standard Python indexing."""

        car = index[0]         
        colour = index[1]
        
        try:
            return self.log_probabilities[f"Pr('{colour}'|'{car}')"]
        except:                                                 #   executes if error raised with an unseen combination                                        
            if car in self.brands.keys():     #   if a seen (the car type is in the dictionary) but not together with b
                if self.k == 0:              
                    unseen_colour = self.log_probabilities[f"Pr('unseen'|'{car}')"]
                    return unseen_colour
                elif self.k > 0:
                    unseen_colour = self.k  / (self.brands[car] + self.k * len(self.brands))
                    return unseen_colour
            else:                               # if neither the car type or the colour are in the dictionary                                 
                if self.k == 0: 
                    both_unseen = self.log_probabilities["Pr('unseen'|'unseen')"]
                    return both_unseen
                if self.k > 0:
                    both_unseen = self.k / (self.k * len(self.brands))
                    return both_unseen

observations = {('Maserati','green'):2, 
       ('Ferrari','red'):3, 
       ('Maserati','blue'): 4, 
       ('Ferrari','black'): 1, 
       ('Jaguar', 'green'): 10}

col_given_brand = CondPr(observations)    #no smoothing used
#col_given_brand.show()
log_col_given_brand = LogCondPr(observations) #no smoothing used
#log_col_given_brand.show()
test = log_col_given_brand[('Maserati','blue')] #what is the log probability of blue given Maserati (notice the inversed order!)
#print(test)