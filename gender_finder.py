import random
import csv,re
import nltk

male_file = open("Indian-Male-Names.csv",'r')
female_file = open("Indian-Female-Names.csv",'r')

male_names = []
female_names = []


def extract_names(file_obj):
    names = []    
    reader = csv.reader(file_obj, delimiter= ",")
    for line in reader:
        name = line[0].lower()                    
        if(re.match(r"\w+",name)!=None):
            names.append(remove_unwanted_stuff(name))
    return names


def remove_unwanted_stuff(name):
    temp_name = re.split(r"[\.\,\s\@]",name)
   
    if (len(temp_name)>1):
        if (len(temp_name[0])<=4 and re.match(r"smt|mr|ms|mrs|miss|km|ku|mohd",temp_name[0]) != None):
        	value = [nm for nm in temp_name[1:] if len(nm)>=3][0]        	
    		return value
        else:
        	value = [nm for nm in temp_name if len(nm)>=3][0]
        	return value
    else:
    	return temp_name[0]
        
        
        
male_names = extract_names(male_file)
female_names = extract_names(female_file) 
    

def male_prob(name):
    prob = 0.0
    name_count = float(male_names.count(name))
    total_male = float(len(male_names))    
    try:
        prob =  name_count/total_male
    except ZeroDivisionError:
        print("DIvision by Zero is bad!! :(")
    return prob   
    
def female_prob(name):
    prob = 0.0
    name_count = float(female_names.count(name))
    total_female = float(len(female_names))    
    try:
        prob =  name_count/total_female
    except ZeroDivisionError:
        print("DIvision by Zero is bad!! :(")
    return prob   



def extract_features(name):	
	features={}
	features["last_two"]=name[-2:]
	features["first_two"]=name[:2]
	features["male_prob"]=male_prob(name)
	features["female_prob"]=female_prob(name)
	return features




female_features = [(extract_features(name),'f') for name in female_names]
male_features = [(extract_features(name),'m') for name in male_names]
total_features = female_features + male_features
random.shuffle(total_features)



train_len = len(total_features)/2
train_set = total_features[:train_len]
test_set = total_features[train_len+1:]

classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))



