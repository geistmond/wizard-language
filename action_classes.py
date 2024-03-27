"""
World Interpreter for Wizard Language

First attempt at understanding how interactions would work in the simulation.

We use 'thematic relations' from linguistics to define actions between agents.
https://en.wikipedia.org/wiki/Thematic_relation
Examples: agent, patient, undergoer

When an object is stolen, there are a thief, a person stolen from, and an item stolen.

Undergoer would be the thematic role for the person who is stolen from. That thematic role
is frequently encoded with "from" or "to" in English, such as "stolen from" or "given to".

Some goals:

* Wizard agents can form societies and hold grudges.
* Wizards evolve and reproduce. They have a genetic code (maybe as a long encoded string).
* Wizard Language can be generated from actions' thematic roles.
* Integrate with existing game engine.
* Allow agent simulation part to interface with game engine world mode.

Goals for the agent model and Wizard Language:
* Communication errors
* Identity confusion
"""

from abc import ABC, abstractmethod

from dataclasses import dataclass

import random

@dataclass
class Noun:
    """
    This class specifies Nouns within an action language interpreted by Wizard agents.
    
    Example of the type of information represented in the Wizard Language Lexicon:
    
        lexeme_example = {
        'id': 0,# corresponds to action_classes.py 
        'en': 'thing',
        'jp': 'mono',
        'wz': 'tasu',
        'class': 'noun'
    }

    lexicon_en = {
        'thing': lexeme_example
    }
    """
    name: str
    id: int
    certainty: float
    rudeness: float
    mana: float
    real: bool
    pronunciation: dict
    
    #@abstractmethod
    def do(self):
        # Create a lexeme for the Noun as our do()
        def create_lexeme(self)->dict:
            lex = {}
            lex['id'] = self.id
            lex['en'] = self.pronunciation['en']
            lex['jp'] = self.pronunciation['jp']
            lex['wz'] = self.pronunciation['wz']
            lex['class'] = 'noun'
            return lex
        # consume action
        print("Used word: ", self.name, self.id)
        print(create_lexeme(self))
        



@dataclass
class Verb:
    # Thematic roles are the frame of the verb.
    name: str
    id: int
    certainty: float
    rudeness: float
    agent: Noun
    patient: Noun
    undergoer: Noun
    experiencer: Noun
    instrument: Noun
    location: Noun
    manner: Noun
    purpose: Noun
    cause: Noun
    pronunciation: dict
    aspect: dict
        
    def set_aspect_mood(self,
                        perfective: bool, 
                        causative: bool,
                        passive: bool,
                        potential: bool,
                        volitional: bool,
                        conditional: bool,
                        imperative: bool):
        speck = {}
        speck['perfective'] = perfective
        speck['causative'] = causative
        speck['passive'] = passive
        speck['potential'] = potential
        speck['volitional'] = volitional
        speck['conditional'] = conditional
        speck['imperative'] = imperative
        self.aspect = speck
        return self.aspect
        
    def do(self):
        # Create a lexeme for the Verb as our do()
        def create_lexeme(self)->dict:
            lex = {}
            lex['id'] = self.id
            lex['en'] = self.pronunciation['en']
            lex['jp'] = self.pronunciation['jp']
            lex['wz'] = self.pronunciation['wz']
            lex['class'] = 'verb'
            return lex
        # consume action
        lex = create_lexeme()
        print("Used word: ", lex['en'], "(", lex['jp'], " , ", lex['wz'], ")", lex['class'], lex['id'])
        print(lex)
        # Run internal method when using do()
        self.set_aspect_mood()
        return lex

        
        
@dataclass
class Syntagm:
    category: str
    case: str
    def set_case(self, phrase):
        particles = ['w4', 'g4', 'w0', 'n0', 'n1', 'n3', 'q4', 'd3', 'h3', 'y4', 'm0', 't0', 'y4', 'k4']
        cases = ['neutral', 'topic', 'locative', 'subject', 'object', 'possessive', 'conjunct']
        categories = ['noun', 'verb', 'particle', 'modifier']
        words = phrase.split(' ')
        last_word = words[-1:]
        if last_word in particles:
            if last_word == 'w4':
                self.case = 'topic'
                self.category = 'noun' # verbal topics are arguably zero-derivation nominalizing for real, unlike "Verb の" or "Verb か" 
            elif last_word == 'w0':
                self.case = 'object'
                self.category = 'noun'
            elif last_word in ['n1', 'd3', 'h3']:
                self.case = 'locative'
                self.category = 'modifier' # here modifier is a concept including locative expressions, adverbs, and adjectives
            elif last_word == "g4":
                self.case = 'subject'
                self.category = 'noun'
            elif last_word in ['m0' 'y4', 't0', 'n3', 'q4']: # using 'q4' for nominal 'or [interogative]', and 'k4' for verbal question formation, todo: eventual verbal 'n3' if certainty < 0.5
                self.case = 'conjunct'
                self.category = 'modifier'
            elif last_word == 'n0':
                self.case = 'possessive'
                self.category = 'modifier'
            elif last_word == 'k4':
                self.case = 'neutral'
                self.category = 'verb' # か is still used with nouns in Japanese but for Battle Wizard world modeling statements on a computer maybe it can be verbs only
        else:
            self.case = 'neutral'
            self.category = 'noun'
        
        return self.category, self.case


class Syntagm(Noun):
    def __init__(self, case: str):
        self.category = 'noun'
        self.case = case
        return self.category, self.case

        
 
class Syntagm(Verb):
    def __init__(self, case: str):
        self.category = 'verb'
        self.case = case # Verbs can be 'possessive' in Japanese, why would it switch word class to a noun just because that's more normal in Latin
        return self.category, self.case
    


@dataclass
class Object(Noun):
    name: str
    uses: list[Verb] 
    mana: float
    #@abstractmethod
    def use():
        def object_action():
            pass
        object_action()


@dataclass
class Person(Noun):
    name: str
    face: list
    age: float
    mortal: bool
    alive: bool
    conscious: bool
    real: bool
    certainty: float # mental certainty, capacity to choose actions; statements can also carry evidential certainty
    health: float
    vitality: float
    strength: float
    agility: float
    intelligence: float
    category: str
    
    def say(self):
        print("Hey I'm", self.name)
        
    def wake_up(self)->bool:
        self.conscious = True
        return True
    
    def pass_out(self)->bool:
        self.conscious = False
        return False
    
    def birth(self)->bool:
        self.alive = True
        self.conscious = True
        return True
    
    def die(self)->bool:
        if self.mortal == False:
            return False
        else:
            self.conscious = False
            self.health = 0.0
            self.alive = False
            return True


@dataclass
class Wizard(Person):
    name: str
    power: float
    rank: int # globally unique Wizard rank stays integer
    spells: list[str]
    
    mortal = False
    alive = True
    real = True
    
    #@abstractmethod
    def say(self):
        print("A wizard spake...")
        print("Hey I'm ", self.name, self.rank, self.id)
    
        
    def kill(self, action: "Verb", target: "Wizard")->"Wizard":
        # need to write lexicon item generators that consume and genreate objects
        global nouns, verbs
        kill_action = verbs[action.name]
        target = kill_action(target)
        target.alive = False
        target.health = 0.0
        return target



@dataclass
class Zombie(Person):
    infectious: bool
    rank: int
    
    zombie = True
    mortal = True
    alive = False
    real = True
        
    def say(self):
        print("'Brains.' Infectious: ", self.infectious)
        print("Zumboid ", self.name, self.rank, self.id)
        
    def birth(self)->bool:
        self.alive = False
        self.conscious = True
        return True
    
    def die(self)->bool:
        self.conscious = False
        self.health = 0.0
        self.alive = False
        return True
    
    
@dataclass
class Apparition(Person):
    visible: bool
    rank: int
    
    apparition = True
    mortal = False
    alive = False
    real = False
    conscious = True
        
    def say(self):
        print("Apparition ", self.name, self.rank, self.id)
        
    def spawn(self)->bool:
        self.alive = False
        self.conscious = True
        return True
    
    def vanish(self)->bool:
        self.conscious = False
        self.health = 0.0
        self.visible = False
        return True
    

@dataclass
class MortalNinja(Person):
    visible: bool
    rank: int
    
    ninja = True
    
    mortal = True
    alive = True
    real = True
    conscious = True
        
    def say(self):
        print("shh (Ninja ", self.name, self.rank, self.id, ")")
        
    def spawn(self)->bool:
        self.conscious = True
        return True
    
    def vanish(self)->bool:
        self.conscious = True
        self.visible = False
        return True
    
    def die(self)->bool:
        self.alive = False
        self.health = 0.0
        return True


class Spell(Verb):
    def __init__(self, 
                 name: str,
                 damage: float, 
                 reach: float, 
                 radius: float, 
                 category: str, 
                 attributes: list[str]):
        self.name = name
        self.damage = damage
        self.reach = reach
        self.radius = radius
        self.category = category
        self.attributes = attributes
    
    #@abstractmethod
    def use(self):
        print("Used spell ", self.name, self.id)
        
        
        
# Let's try to define a Wizard named Ziploc 
wizards = []
def make_wizard():
    w = Wizard(name = "Ziploc",
               id = random.randint(0,1000),
               certainty = 1.0,
               rudeness = 1.0,
               mana = 1.0,
               real = True,
               pronunciation = {},
               face = [],
               age = 1000.0,
               mortal = False,
               alive = True,
               conscious = True,
               health = 1.0,
               vitality = 1.0,
               strength = 1.0,
               agility = 1.0,
               intelligence = 1.0,
               category = "leader",
               power = 1.0,
               rank = 1,
               spells = ['zip', 'lock'])
    return w
wizards.append(make_wizard())
[print('Name: ', w.name, 'Spells: ', w.spells, 'Mortal?', w.mortal) for w in wizards]




def get_nouns(vocab: list["Syntagm"])->list["Noun"]:
    return [vocab[n.name] for n in nouns]