# Use radom weighted choice to consume Yaml-specified language designs to generate words.

from scipy.stats import poisson, zipf

from numpy.random import choice

import itertools as itr 

import yaml

from functools import lru_cache # memoizer to save memory


@lru_cache
def poisson_weights(length: int, q=0.7)->list[float]:
    rv = poisson(q)
    weights = [rv.pmf(i) for i in range(length)]
    return weights


@lru_cache
def zipf_weights(length: int, q=0.7)->list[float]:
    # have to add 1 to an index for this distribution vs Poisson
    length += 1 
    if q == 0:
        shape = 1
    else:
        shape = 1/q
    weights = [zipf.pmf(i, shape) for i in range(length)][1:]
    return weights


def add_weights_to_phonology(phonology, distro='zipf')->dict:
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

    # Choose an element from each list of element vals according to the weights
    syl_out = ''
    @lru_cache
    def choose_phones(struct):
        syl_out = ''
        for s in struct:
            vs = elements[s]['vals']
            ws = elements[s]['weights']
            phone = choice(vs, 1, ws)[0]
            syl_out += phone
        if syl_out != '':
            return syl_out
        else:
            assert False
    syl_out = choose_phones(syl_struct)
    return syl_out



def make_word(phonology: dict, num_syllables: int, distro='zipf')->str:
    """
    Use the make_syllable function to construct words bit by bit.

    dictionary, int, string -> string
    """
    # Construct the word
    @lru_cache
    def choose_syls(num_syllables)->str:
        word = ''
        i = 0
        while i < num_syllables:
            s = make_syllable(phonology)
            word += s
            i += 1
        return word
    word = choose_syls(num_syllables)
    if word != '':
        return word



def run(words='1', syllables='1', distribution='zipf', file='wizard_names.yml', alpha='true')->str:
    output = ''
    # Create the phonology, grabbing from file if specified
    if len(file) > 0:
        phonology = yaml.load(open(file, 'r'), Loader=yaml.FullLoader)
    else:
        phonology = yaml.load(open('wizard_names.yml', 'r'), Loader=yaml.FullLoader)

    # Start by adding weights to the phonology we've received
    print(phonology)
    phonology = add_weights_to_phonology(phonology, distribution)

    # Create the words!
    i = 0
    while i < int(words):
        word = make_word(phonology, int(syllables), distribution)
        if word not in output.split('\n'):
            output += word
            i += 1
        if i < int(words) - 1:
            output += '\n'

    # Alphabetize if we're asked to
    if alpha == 'true':
        output = '\n'.join(sorted(output.split('\n')))

    outstring = phonology['language'] + ' language: ' + words + ' words'
    outstring += ' of ' + syllables + ' syllable(s) each.'
    print(output)
    
    
run(words="100", syllables="1")