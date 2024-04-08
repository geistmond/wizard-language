Sketches for a multi-agent battle simulator with magic system. 

* action_classes.py and wizard_language.py make a start at some natural language modeling for a domain-specified language that can communicate game events and undergo further comprehension into natural language.
* name_generator.py is code that consumes a .yml file describing a set of atoms and a mathematical distribution that together approximate a Markov model.
* resource_sim.py is a test of the resource consumption simulation library SimPy (not to be confused with the symbolic computattion library SymPy)
* disease_sim.py is reimplementing one of the major disease simulation starting points from early in the COVID-19 pandemic. This is to model game knowledge.
* wizard_genome.py is an evolutionary optimization demo because the wizards change over time and optimize.

Goals for the simulation:

* The Wizard agents communicate using a simple language.
* Wizards recognize each other's faces. Wizard faces are generated and have variations to communicate emotion.
* This means the agents are capable of sight and hearing.
* Wizards must be able to miscommunicate with each other.
* Model society- and culture-level phenomena within Wizard battles.
* For a Wizard, another Wizard has an Intent and a Statement. These do not always align.
* Wizard language must be capable of lying and deceit.

Goals for the view:

1. Initial 2D representation for visualizing and testing systems.
2. Crude 3D representation.
3. Full 3D scene with production-quality game engine.
4. Statements are sound an drop off by the square of the radius between Wizards.

Goals for the project:

1. Investors or Crowdfunding

Wizard Language Notes:

* The Wizard Language Interpreter (WLI) is also a world description interpreter. Video games have perfectly described world contents.
* Statements about the world are Wizard Beliefs by default. An Updater updates the world-state if the beliefs are world-true.
* Wizard Language can be rendered into bizarre robo-quasi-Japanese. It can also just drop in English lexemes into the Japanese frame.
* However, the goal is a language model. Language models can turn the same basis into normal-ish English or normal-ish Japanesse.
* Intent could be modeled as a queue that holds Sentences where the Wizard reads them and acts on them.
