# Use radom weighted choice to consume Yaml-specified language designs to generate words.

# Distributions to use for weights
from scipy.stats import poisson, zipf

from numpy.random import choice

# This will help make generating weights faster
import itertools as itr

# Language files are specified as Yaml
import yaml

#memoizer - ZT
from functools import lru_cache

@lru_cache
def poisson_weights(length: int, q=0.7)->list[float]:
    """
    Returns a list of weights according to a Poisson distribution with
    the q value for the distribution as an optional argument.

    This is fed as weights into numpy.random.choice for a weighted choice.

    The length parameter is just an integer that will come from 
    things like len(consonants)

    int, (float) -> [floats]
    """
    rv = poisson(q)

    # Use the probability mass function to get weights for weighted choice later
    weights = [rv.pmf(i) for i in range(length)]
    return weights


@lru_cache
def zipf_weights(length: int, q=0.7)->list[float]:
    """
    Alternative to the above using Zipf distribution.
    Note that this returns an array where the first element is 0,
    so we will be dropping that and adding to the index.

    int, (float) -> [floats]
    """
    length += 1 # later we drop the first value. Zipf results start with 0

    # Zipf PMF scales inversely to Poisson. This lets us switch distribution
    # without making changes, since we prevent division by zero here.
    if q == 0:
        shape = 1
    else:
        shape = 1/q 

    # Probability mass function to yield weights for weighted choice
    weights = [zipf.pmf(i, shape) for i in range(length)][1:]

    return weights


def add_weights_to_phonology(phonology: dict, distro='zipf')->dict:
    """
    This consumes a dictionary drawn from the Yaml specifying the
    langauge's phonology, and outputs a dictionary with added weights.
    """
    syls = phonology['syllables']['vals'] # Syllable struture possibilities
    syl_q = phonology['syllables']['q'] # q values for weights
    elements = phonology['elements']

    # Define a function called weight_lifter that is independent of distribtion
    if distro == 'poisson':
        weight_lifter = poisson_weights
    else:
        weight_lifter = zipf_weights # Zipf is usually more natural

    # Add weights to dictionary for the syllable structures
    phonology['syllables']['weights'] = weight_lifter(len(syls), syl_q)

    # Grab string containing only unique characters from the structures
    unique = ''.join(syls)
    unique = ''.join(k for k, g in itr.groupby(sorted(unique)))

    # Add weights for each unique element appearing in the syl structs
    for u in unique:
        el_len = len(elements[u]['vals'])
        el_q = elements[u]['q']
        weights = weight_lifter(el_len, el_q)
        elements[u]['weights'] = weights

    phonology['elements'] = elements
    return phonology


def make_syllable(phonology: dict)->str:
    """
    Builds a syllable according to a distribution of syllable structures
    taking each character in the string as a label.
    """
    # Get list of syllable structures and weights from the above
    syls = phonology['syllables']['vals'] 
    syl_weights = phonology['syllables']['weights']

    # Choose a syllable structure according to the weights
    syl_struct = choice(syls, 1, syl_weights)[0]

    # Elements: C, V, etc.
    elements = phonology['elements'] 

    # do not cache this because it uses random choice
    def get_syl(syl_struct)->str:
        # Choose an element from each list of element vals according to the weights
        syl_out = ''
        for s in syl_struct:
            vs = elements[s]['vals']
            ws = elements[s]['weights']
            phone = choice(vs, 1, ws)[0]
            syl_out += phone
        return syl_out
        
    syl_out = get_syl(syl_struct)
    return syl_out


def make_word(phonology: dict, num_syllables: int, distro='zipf')->str:
    """
    Use the make_syllable function to construct words bit by bit.

    dictionary, int, string -> string
    """
    # Construct the word
    word = ''
    for i in range(num_syllables):
        word += make_syllable(phonology)
    return word


# Try it out!
def run(words='1', syllables='1', distribution='zipf', file='', alpha='true')->str:
    output = ''
    # Create the phonology, grabbing from file if specified
    if len(file) > 0:
        phonology = yaml.load(open(file, 'r'), Loader=yaml.SafeLoader)
    else:
        phonology = yaml.load(open('wizard_names.yml', 'r'), Loader=yaml.SafeLoader)

    # Start by adding weights to the phonology we've received
    phonology = add_weights_to_phonology(phonology, distribution)

    # Create the words!
    for w in range(int(words)):
        word = make_word(phonology, int(syllables), distribution)
        output += word
        if w < int(words) - 1:
            output += '\n'

    # Alphabetize if we're asked to
    if alpha == 'true':
        output = '\n'.join(sorted(output.split('\n')))

    outstring = phonology['language'] + ' language: ' + words + ' words'
    outstring += ' of ' + syllables + ' syllable(s) each.'
    print(outstring)
    print(output)
    

run(words="100", syllables="2")
