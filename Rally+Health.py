
# coding: utf-8

# # Rally Health Programming Question
# 
# Your task is to transform one word into another, with four operations: add a letter, delete a letter, change a letter, and take an anagram of the existing word.  
# 
# Additionally, you have to ovey the following rules:
# * Every iterim step between the first and the last word must also be a word
# * No iterim step can be less than three letters
# * The first line of input will contain the "cost" of each operation in the order above
# * The second line of input will contain the starting word
# * The first line of input will contain the ending word
# 
# Your goal is to find the lowest possible "cost" of transforming the starting word into the ending word.  You can use any word list you like -- feel free to include your word list or a link to it as part of your solution.
# 
# You solution should detect and handle invalid input and return -1 if there is no solution.

# ### Examples
# 
# ##### Input
# 1315
# HEALTH
# HANDS
# 
# ##### Output
# 7 (HEALTH - HEATH - HEATS - HENTS - HENDS - HANDS
# 
# ##### Input
# 1913
# TEAM
# MATE
# 
# ##### Output
# 3 (TEAM - MATE)
# 
# ##### Input
# 7152
# OPHTHALMOLOGY
# GLASSES
# 
# ##### Output
# -1

# ## Solution

# ### Required framworks
# * python=3.6
# * nltk
# * jupyter notebook

# ### Word List

# In[118]:


# DO NOT RUN - Words corpus has already been downloaded
import nltk

#nltk.download()


# ### Word Functions
# Code for the 4 available operations based on the problem description with test cases to ensure the functions work appropriately.

# In[119]:


from nltk.corpus import words

word_list = words.words()


# In[120]:


# Test - First 20 words
print(word_list[:20])


# #### Add Letter

# In[121]:


def addLetter(word, index, letter):
    new_word = word[:index] + letter + word[index:]
    return new_word


# In[122]:


# Test 1 - Adding letter to end of word
# WORD -> WORDS

word = addLetter("WORD", 4, 'S')
print(word)


# In[123]:


# Test 2 - Adding letter to beginning of word
# WORD -> SWORD

word = addLetter("WORD", 0, 'S')
print(word)


# In[124]:


# Test 3 - Adding letter into middle of word
# WORD -> WORLD

word = addLetter("WORD", 3, 'L')
print(word)


# #### Delete Letter

# In[125]:


def deleteLetter(word, index):
    new_word = word[:index] + word[index+1:]
    return new_word


# In[126]:


# Test 1 - Delete first letter
# SWORD -> WORD

word = deleteLetter("SWORD", 0)
print(word)


# In[127]:


# Test 2 - Delete last letter
# WORDS -> WORD

word = deleteLetter("WORDS", 4)
print(word)


# In[128]:


# Test 3 - Delete middle letter
# WORLDS -> WORDS

word = deleteLetter("WORLDS", 3)
print(word)


# #### Change Letter

# In[129]:


def changeLetter(word, index, letter):
    new_word = word[:index] + letter + word[index+1:]
    return new_word


# In[130]:


# Test 1 - Change first letter
# WELL -> BELL

word = changeLetter("WELL", 0, 'B')
print(word)


# In[131]:


# Test 2 - Change last letter
# WELL -> WELT

word = changeLetter("WELL", 3, 'T')
print(word)


# In[132]:


# Test 3 - Change middle letter
# HUM -> HIM

word = changeLetter("HUM", 1, 'I')
print(word)


# #### Anagram

# In[133]:


import itertools

def getAnagrams(word):
    return itertools.permutations(word)


# In[134]:


# Test 1
# STEAK

words = getAnagrams("STEAK")
for word in words:
    word = "".join(word)
    print(word)


# In[135]:


# Test 2 - Only words
# STEAK

words = getAnagrams("STEAK")
for word in words:
        word = "".join(word)
        if word.lower() in word_list:
            print(word)


# #### State class

# In[136]:


explored = set()

class State: 
    def __init__(self, word, cost, distance):
        self.word = word
        self.cost = cost     
        self.distance = distance


# #### Levenshtein Distance

# In[137]:


# Taken from Wikipedia
def distance(s1, s2):
    # Base cases
    if s1 == "":
        return len(s2)
    if s2 == "":
        return len(s1)
    if s1[-1] == s2[-1]:
        cost = 0
    else:
        cost = 1
        
    res = min([distance(s1[:-1], s2)+1,
              distance(s1, s2[:-1])+1,
              distance(s1[:-1], s2[:-1])+cost])
    
    return res


# #### Get States from the addition operation

# In[138]:


def getAddStates(state, states, cost, end_word):
    for i in range(0, len(state.word)+1):
        for j in range(ord('A'), ord('Z')+1):
            new_word = addLetter(state.word, i, chr(j))  
            if new_word.lower() in word_list and new_word not in explored:
                new_state = State(new_word, state.cost + cost, distance(new_word, end_word)) 
                
                states.append(new_state)


# In[139]:


# Test
states = []
initial_state = State("WORD", 0, distance("WORD", "SWORD"))

getAddStates(initial_state, states, 1, "SWORD")

for state in states:
    print(state.word + " - " + str(state.cost) + " - " + str(state.distance))


# #### Get States from the deletion operation

# In[190]:


def getDeleteStates(state, states, cost, end_word):
    for i in range(0, len(state.word)):
        new_word = deleteLetter(state.word, i)  
        if len(new_word) >= 3:
            if new_word.lower() in word_list and new_word not in explored:
                new_state = State(new_word, state.cost + cost, distance(new_word, end_word))             
                states.append(new_state)


# In[141]:


# Test
states = []
initial_state = State("NORMAL", 0, distance("NORMAL", "NORM"))

getDeleteStates(initial_state, states, 1, "NORM")

for state in states:
    print(state.word + " - " + str(state.cost) + " - " + str(state.distance))


# #### Get States from the change operation

# In[142]:


def getChangeStates(state, states, cost, end_word):
    for i in range(0, len(state.word)):
        for j in range(ord('A'), ord('Z')+1):
            if state.word[i] != chr(j):
                new_word = changeLetter(state.word, i, chr(j))  
                if new_word.lower() in word_list and new_word not in explored:
                    new_state = State(new_word, state.cost + cost, distance(new_word, end_word))                    
                    states.append(new_state)


# In[143]:


# Test
states = []
initial_state = State("WORN", 0, distance("WORN", "BORN"))

getChangeStates(initial_state, states, 1, "BORN")

for state in states:
    print(state.word + " - " + str(state.cost) + " - " + str(state.distance))


# #### Get States from anagram operation

# In[144]:


def getAnagramStates(state, states, cost, end_word):
    new_words = getAnagrams(state.word)
    for new_word in new_words:
        new_word = "".join(new_word)
        if new_word != state.word and new_word.lower() in word_list and new_word not in explored:
            new_state = State(new_word, state.cost + cost, distance(new_word, end_word)) 
            states.append(new_state)           


# In[145]:


# Test
states = []
initial_state = State("STEAK", 0, distance("STEAK", "STAKE"))

getAnagramStates(initial_state, states, 1, "STAKE")

for state in states:
    print(state.word + " - " + str(state.cost) + " - " + str(state.distance))


# #### Solution function - main loop

# In[211]:


def solution(costs, begin_word, end_word):
    
    # Beginning word or ending word is not a word
    if begin_word.lower() not in word_list or end_word.lower() not in word_list:
        return -1
    
    # Beginning word or ending word smaller than 3 characters
    if len(begin_word) < 3 or len(end_word) < 3:
        return -1
    
    # Costs is not a valid input
    if len(costs) != 4:
        return -1
    if not costs.isdigit():
        return -1
    
    
    # Define function costs
    add_cost = int(costs[0])
    delete_cost = int(costs[1])
    change_cost = int(costs[2])
    anagram_cost = int(costs[3])
    
    # Initial State
    init_state = State(begin_word, 0, distance(begin_word, end_word))
    
    # Define possible states
    states = []
    getAddStates(init_state, states, add_cost, end_word)
    getDeleteStates(init_state, states, delete_cost, end_word)
    getChangeStates(init_state, states, change_cost, end_word)
    getAnagramStates(init_state, states, anagram_cost, end_word)
    
    # Explored states
    explored.add(init_state.word)
    
    # Loop until goal or states = []
    while states != []:
    
        # Find lowest cost state
        states = sorted(states, key=lambda state: state.distance, reverse=True)
        states = sorted(states, key=lambda state: state.cost+state.distance, reverse=True)
        
        # DEBUG
        #for state in states:
            #print(state.word + " - " + str(state.cost) + " - " + str(state.distance))     
        
        # Pop lowest state
        while True:
            new_state = states.pop()
            
            if new_state.word not in explored:
                explored.add(new_state.word)
                break
        
        # DEBUG
        #print("")
        print(new_state.word + " - " + str(new_state.cost) + " - " + str(new_state.distance))
        #input()

        # Check is state is goal state
        if new_state.word == end_word:
            return new_state.cost
        
        # Expand new_state
        #print("Start Add")
        getAddStates(new_state, states, add_cost, end_word)
        #print("Start Delete")
        getDeleteStates(new_state, states, delete_cost, end_word)
        #print("Start Change")
        getChangeStates(new_state, states, change_cost, end_word)
        #print("Start Anagram")
        getAnagramStates(new_state, states, anagram_cost, end_word)
    
    return -1


# In[198]:


# Reset explored
explored = set()


# In[199]:


# Test
# 1315
# HEALTH
# HANDS

print(solution("1315", "HEALTH", "HANDS"))


# In[200]:


"hands" in word_list


# In[218]:


# Reset explored
explored = set()


# In[219]:


# Test
# 1313
# HEALTH
# HANDS

print(solution("1913", "TEAM", "MATE"))


# In[216]:


# Reset explored
explored = set()


# In[217]:


# Test
# 1234
# GAME
# GRADE

print(solution("1234", "GAME", "GRADE"))


# In[214]:


# Reset explored
explored = set()


# In[215]:


# Test
# 7152
# ZIP
# ME

print(solution("7152", "ZIP", "ME"))


# In[212]:


# Reset explored
explored = set()


# In[213]:


# Test
# 7152
# GAME
# GRADE

print(solution("7152", "GAME", "GRADE"))


# In[ ]:




