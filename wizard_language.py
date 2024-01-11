__syntax_readme__ = """
Wizard Language is a world description language for a video game. It describes events using the information built into Japanese grammar.

There is an additional layer of representation for verbal renderings of in-game events that includes a wizard conlang. The conlang
just uses approximately the same grammar as Japanese, with a different lexicon that describes unique in-game events. The wizard agents
induce speech events when they cast spells, which are interpreted by the game world but audible to other wizards.
 
The lexemes are defined in ways that are specific to Battle Wizard Simulator. The game world is closed, using a game tree.
So there is always a 1:1 mapping for lexemes in the constructed language.
But the surface expression can be English lexemes, Japnaese ones, or Wizard Language.

A few additional grammars are specified that should be able to handle much of the same stuff. These are intended as input to a future
machine learning based system as a layer in between game state representation and surface representation as utterance.

Flow: In-game description events or user input -> Intent is generated -> Programmatic wizard langauge text -> surface rendering as speech.
There is always a mapping between game events and how they're articulated on the surface.
The middle layer could hypothetically change out without the surface representation being different. Different game experience?

Wizard Language Engine must describe game events adequately and generate utterances that wizards use to cast spells and communicate.
The utterances must then be interpreted by other wizards for comprehension, and by the game engine to assess whether to update the world.
The same engine can then be used for other sorts of projects, but a wizard motif necessitates the use of verbal spells.

Wizard Language lexemes share a unique namespace. It is an artificial language with no homophones. 
Sentence parsing could rely on the ".wz" versions of words since they're unique, then resynthesize quasi-English and quasi-Japanese.

Once the Wizard Language has its lexicon adequately specified, and once there's a parser, chat interface conversational AIs can learn it.
Once there is a conversational AI model based on Wizard Langauge, which is specified and deterministic, the Wizards can rely on that.

Some stuff in here is annoying from a Japanese speaker POV such as:
* Conjunct -(t)te suffix is replaced by a phrase using t3 particle
* Adverbs are replaced by verbal conjuncts or particle phrases with nouns
* Adjectives are replaced by verb phrases before verbs

What language models can accept a BNF grammar specification, maybe as an adversary? 
How to use it as training data for a muti-language model given that game state is closed-world and pre-specified?

This is not a statement about Japanese linguistics, it's just so virtual sim wizards can argue.
"""

__lexicon_readme__ = """
It mostly just needs to be Wizard readable, even if that means a language model.
This means controlling Wizard Language's lexicon to homophones. 
Each English lexeme has corresopnding Wizard language phonemes. These will be mapped out in lexicon files.
Adjectives are replaced by verbs, no need for i and na adjective distinction in video game robot language. <verb> <noun> replaces <adjective> <noun>

This is not a statement about Japanese linguistics, it's just so virtual sim wizards can argue.
"""

bnf_grammar_1 = """
<topic> ::= <noun-phrase> 'w4' | <verb-phrase> 'w4' | <sentence> 'w4'
<sentence> ::= <topic> <sentence> | <noun-phrase> <particle> <sentence> | <verb-phrase> <particle> <sentence> | <sentence> <particle> <sentence>
<verb-phrase> ::= <verb> | <verb> <particle> | <verb-phrase> <particle> <verb-phrase> | <noun-phrase> <particle> <verb-phrase> | <noun-phrase> <particle> <noun-phrase> <particle> <verb-phrase> | <verb-phrase> <particle>
<noun-phrase> ::= <determiner> <noun-phrase> | <noun-phrase> <particle> <noun> | <noun-phrase> <particle> | <noun> <particle> | <noun> <noun> | <verb> <noun> | <verb-phrase> <noun> | <noun>
<particle> ::= 'w4' | 'g4' | 'w0' | 'n0' | 'n1' | 'd3' | 'h3' | 'y4' | 'm0' | 't0' | 'y4' | 'k4'
"""

bnf_grammar_2 = """
<topic-particle> ::= 'w4'
<conjunctive-particle> ::= 't3'
<particle> ::= 'g4' | 'w0' | 'n0' | 'n1' | 'd3' | 'h3' | 'y4' | 'm0' | 't0' | 'y4' | 'k4'
<topic> ::= <noun-phrase> <topic-particle> | <verb-phrase> <topic-particle> | <p-phrase> <topic-particle> | <sentence> <topic-particle>
<p-phrase> ::= <noun-phrase> <particle> | <verb-phrase> <particle> | <sentence-phrase> <particle> | <p-phrase> <particle>
<noun-phrase> ::= <noun> | <noun> <noun> | <verb-phrase> <noun-phrase> | <p-phrase> <noun-phrase>
<verb-phrase> ::= <verb> | <noun-phrase> <verb-phrase> | <p-phrase> <verb-phrase> | <verb-conjunct> <verb-phrase>
<verb-conjunct> ::= <verb-phrase> <conjunctive-particle>
<sentence> ::= <verb-phrase> | <p-phrase> | <topic> <verb-phrase>
<discourse> ::= <topic> <sentence> | <topic> <verb-phrase>
"""

# This does not have classifiers -- not needed for a simple game discription language? 
japanese_style_grammar_3 = """
<topic-particle> ::= 'w4'
<conjunctive-particle> ::= 't3'
<particle> ::= 'g4' | 'w0' | 'n0' | 'n1' | 'd3' | 'h3' | 'y4' | 'm0' | 't0' | 'y4' | 'k4'
<honorific> ::= 'ch4n' | 'k7n' | 's4n' | 's4m4' | 's3ns31'
<name> ::= <proper-noun> <honorific>
<noun> ::= <noun> | <noun> <noun>*
<p> ::= <particle> | <topic-particle> | <conjunctive-particle>
<topic> ::= <noun-phrase> <topic-particle> | <verb-phrase> <topic-particle> | <p-phrase> <topic-particle>
<verb-conjunct> ::= <verb-phrase> <conjunctive-particle>
<p-phrase> :== <noun-phrase> <particle> | <verb-phrase> <particle>
<verb-phrase> ::= <p-phrase>* <verb> | <noun-phrase> <verb> | <verb-conjunct> <verb>
<noun-phrase> ::= <p-phrase>* <noun> | <verb-phrase>* <noun> | <pronoun>
<statement> ::= <topic> <sentence>*
<sentence> ::= <conjunct-phrase>* <verb-phrase>
<discourse> ::= <statement> <sentence>* <discourse>*
"""

# This was harder. Thankfully the Japanese structures are all 100% in my intuition and English isn't that hard.
english_style_grammar = """
<noun> ::= <noun> | <noun> <noun>*
<sentence> ::= <noun-phrase> <verb-phrase>
<verb-phrase> ::= {<noun-phrase>} {<noun-phrase>} <adverb>* <p-phrase>* 
<noun-phrase> ::= {<determiner>} <adjective>* <noun> <p-phrase>* | <noun-phrase> <conjunction> <noun-phrase> | <pronoun>
<p-phrase> ::= <preposition> <noun-phrase> | <preposition> <verb-phrase> | <noun-phrase> <postposition>
<phrase> ::= <noun-phrase> | <verb-phrase> | <p-phrase>
<topic> ::= <phrase>
"""

french_style_grammar = """
<neg-part1> ::= 'n3'
<neg-part2> ::= 'p4s' | 'r13n' | '47c7n3' | 'p37' | 'qu3' | 'qu1' | 'p3rs0nn3'
<sentence> ::= <adverb>* <noun-phrase> <neg-part1> <pronoun>* <verb-phrase>
<noun-phrase> ::= <determiner> <adjective>* <noun> <adjective>* <p-phrase>*
<p-phrase> ::= <preposition> <noun-phrase>
<adverbial> ::= <adverb> | <p-phrase>
<verb-phrase> ::= {<verb>} <adverbial>* <verb> <adverbial>* {<noun-phrase>} {<noun-phrase>} <adverbial>*
<phrase> ::= <noun-phrase> | <verb-phrase> | <p-phrase>
<topic> ::= <phrase>
"""

chinese_style_grammar = """
<noun> ::= <noun> | <noun> <noun>*
<verb> ::= <verb> | <verb> <verb>*
<sentence> ::= <noun-phrase> <verb-phrase>
<objects-phrase> ::= {<noun-phrase>} {<noun-phrase>}
<adverb-phrase> ::= <adverb>* <verb>+ {<postposition>}
<verb-phrase> ::= <adverb-phrase>+ {<objects-phrase>} <particle>* | {<objects-phrase>} <adverb-phrase>+ <particle>* 
<noun-phrase> ::= {<determiner>} <adjective>* <noun> <p-phrase>* <verb-phrase>* | <noun-phrase> <conjunction> <noun-phrase>
<p-phrase> ::= <noun-phrase> <postposition> | <verb-phrase> <postposition>
<phrase> ::= <noun-phrase> | <verb-phrase> | <p-phrase>
<topic> ::= <phrase>
"""

german_style_grammar = """
<noun> ::= <noun> | <noun>* <noun>
<sentence> ::= <phrase> <verb-phrase-main> <verb-phrase-sub>*
<noun-phrase> ::= {<determiner>} <verb-phrase-sub>* <adjective>* <noun> <p-phrase>*
<verb-phrase-sub> ::= <noun-phrase>* <p-phrase>* <adverb>* <verb>
<verb-phrase-main> ::= <verb> <noun-phrase>* <adverb>* <p-phrase>* 
<p-phrase> ::= <preposition> <noun-phrase> | <noun-phrase> <postposition>
<phrase> ::= <noun-phrase> | <verb-phrase-sub> | <p-phrase>
<topic> ::= <phrase>
"""

russian_style_grammar = """
<sentence> ::= <noun-phrase> <verb-phrase> <noun-phrase>* | <verb-phrase> <noun-phrase> <noun-phrase>* | <noun-phrase> <noun-phrase>* <verb-phrase> | <noun-phrase>* <verb-phrase> <noun-phrase>
<noun-phrase> ::= <determiner> <p-phrase>* <adjective>* <noun> <p-phrase>*
<verb-phrase> ::= <adverbial>* <verb> <adverbial>* <verb>*
<p-phrase> ::= <preposition> <noun-phrase> | <noun-phrase> <post-position>
"""


lexeme_example_noun = {
    'id': 0, # corresponds to action_classes.py 
    'en': 'thing',
    'jp': 'mono',
    'wz': 'tasu',
    'class': 'noun'
}

lexeme_example_verb = {
    'id': 1, # corresponds to action_classes.py 
    'en': 'do',
    'jp': 'suru',
    'wz': 'pekang',
    'class': 'verb'
}

lexeme_example_particle = {
    'id': 2, # corresponds to action_classes.py 
    'en': '',
    'jp': 'w4',
    'wz': 'w4',
    'class': 'particle'
}

lexeme_example_determiner = {
    'id': 3, # corresponds to action_classes.py 
    'en': 'this',
    'jp': 'kono',
    'wz': 'oc',
    'class': 'particle'
}

# This is indexed by each lexeme's English form 
lexicon_en = {
    'thing': lexeme_example_noun
}

lexicon_jp = {
    'mono': lexeme_example_noun
}

lexicon_wz = {
    'tasu': lexeme_example_noun
}

print(lexicon_en['thing'])