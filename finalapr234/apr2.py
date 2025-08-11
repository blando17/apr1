"""
Description     : Simple Python implementation of the Apriori Algorithm (Python 3)
Usage:
    $ python apriori.py -f DATASET.csv -s minSupport -c minConfidence
    $ python apriori.py -f DATASET.csv -s 0.15 -c 0.6
"""

import sys
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser


def subsets(arr):
    """Returns non-empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i in range(len(arr))])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    """Calculates support for items and returns those meeting minSupport"""
    _itemSet = set()
    localSet = defaultdict(int)

    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1

    for item, count in localSet.items():
        support = float(count) / len(transactionList)
        if support >= minSupport:
            _itemSet.add(item)

    return _itemSet


def joinSet(itemSet, length):
    """Join a set with itself and return n-element itemsets"""
    return set([
        i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length
    ])


def getItemSetTransactionList(data_iterator):
    """Generates 1-itemsets and transaction list"""
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))
    return itemSet, transactionList


def runApriori(data_iter, minSupport, minConfidence):
    """Runs Apriori algorithm and returns frequent itemsets and association rules"""
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    assocRules = dict()

    oneCSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)
    currentLSet = oneCSet
    k = 2

    while currentLSet:
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet, transactionList, minSupport, freqSet)
        currentLSet = currentCSet
        k += 1

    def getSupport(item):
        """Returns the support of an item"""
        return float(freqSet[item]) / len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item)) for item in value])

    toRetRules = []
    for key, value in list(largeSet.items())[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item) / getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)), confidence))

    return toRetItems, toRetRules


def printResults(items, rules):
    outfile = open('output.txt', 'a')
    
    # Write frequent itemsets
    outfile.write("\n------------------------ FREQUENT ITEMSETS:\n")
    for item, support in sorted(items, key=lambda x: x[1]):
        line = f"Item: {item}, Support = {round(support, 3)}\n"
        outfile.write(line)

    # Write association rules
    outfile.write("\n------------------------ RULES:\n")
    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        line = f"Rule: {pre} ==> {post}, Confidence = {round(confidence, 3)}\n"
        outfile.write(line)
    
    outfile.close()

def dataFromFile(fname):
    """Reads data from file and yields transactions"""
    with open(fname, 'r', newline='', encoding='utf-8') as file_iter:
        for line in file_iter:
            line = line.strip().rstrip(',')
            record = frozenset(line.split(','))
            yield record


if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing CSV',
                         default=None)
    optparser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support value',
                         default=0.15,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence value',
                         default=0.6,
                         type='float')

    (options, args) = optparser.parse_args()

    if options.input is None:
        print('No dataset filename specified. Use -f to provide one.')
        sys.exit('System will exit')

    minSupport = options.minS
    minConfidence = options.minC

    inFile = dataFromFile(options.input)

    items, rules = runApriori(inFile, minSupport, minConfidence)

    printResults(items, rules)