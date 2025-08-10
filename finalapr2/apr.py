# # # """
# # # Description     : Simple Python implementation of the Apriori Algorithm (Python 3)
# # # Usage:
# # #     $ python apriori.py -f DATASET.csv -s minSupport -c minConfidence
# # #     $ python apriori.py -f DATASET.csv -s 0.15 -c 0.6
# # # """

# # # import sys
# # # from itertools import chain, combinations
# # # from collections import defaultdict
# # # from optparse import OptionParser


# # # # def subsets(arr):
# # # #     """Returns non-empty subsets of arr"""
# # # #     return chain(*[combinations(arr, i + 1) for i in range(len(arr))])
# # # def non_empty_proper_subsets(itemset):
# # #     """Return all non-empty proper subsets of itemset"""
# # #     return chain.from_iterable(combinations(itemset, r) for r in range(1, len(itemset)))

# # # def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
# # #     """Calculates support for items and returns those meeting minSupport"""
# # #     _itemSet = set()
# # #     localSet = defaultdict(int)

# # #     for item in itemSet:
# # #         for transaction in transactionList:
# # #             if item.issubset(transaction):
# # #                 freqSet[item] += 1
# # #                 localSet[item] += 1

# # #     for item, count in localSet.items():
# # #         support = float(count) / len(transactionList)
# # #         if support >= minSupport:
# # #             _itemSet.add(item)

# # #     return _itemSet


# # # def joinSet(itemSet, length):
# # #     """Join a set with itself and return n-element itemsets"""
# # #     return set([
# # #         i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length
# # #     ])


# # # def getItemSetTransactionList(data_iterator):
# # #     """Generates 1-itemsets and transaction list"""
# # #     transactionList = list()
# # #     itemSet = set()
# # #     for record in data_iterator:
# # #         transaction = frozenset(record)
# # #         transactionList.append(transaction)
# # #         for item in transaction:
# # #             itemSet.add(frozenset([item]))
# # #     return itemSet, transactionList


# # # # def runApriori(data_iter, minSupport, minConfidence):
# # # #     """Runs Apriori algorithm and returns frequent itemsets and association rules"""
# # # #     itemSet, transactionList = getItemSetTransactionList(data_iter)

# # # #     freqSet = defaultdict(int)
# # # #     largeSet = dict()
# # # #     assocRules = dict()

# # # #     oneCSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)
# # # #     currentLSet = oneCSet
# # # #     k = 2

# # # #     while currentLSet:
# # # #         largeSet[k - 1] = currentLSet
# # # #         currentLSet = joinSet(currentLSet, k)
# # # #         currentCSet = returnItemsWithMinSupport(currentLSet, transactionList, minSupport, freqSet)
# # # #         currentLSet = currentCSet
# # # #         k += 1

# # # #     def getSupport(item):
# # # #         """Returns the support of an item"""
# # # #         return float(freqSet[item]) / len(transactionList)

# # # #     toRetItems = []
# # # #     for key, value in largeSet.items():
# # # #         toRetItems.extend([(tuple(item), getSupport(item)) for item in value])

# # # #     toRetRules = []
# # # #     for k, itemsets in largeSet.items():
# # # #         if k < 2:
# # # #             continue  # Rules must come from itemsets of length 2 or more
# # # #         for itemset in itemsets:
# # # #             for antecedent in map(frozenset, subsets(itemset)):
# # # #                 consequent = itemset - antecedent
# # # #                 if len(antecedent) > 0 and len(consequent) > 0:
# # # #                     confidence = getSupport(itemset) / getSupport(antecedent)
# # # #                     if confidence >= minConfidence:
# # # #                         toRetRules.append(((tuple(antecedent), tuple(consequent)), confidence))


# # # #     return toRetItems, toRetRules

# # # def runApriori(data_iter, minSupport, minConfidence):
# # #     """Runs Apriori algorithm and returns frequent itemsets and association rules"""
# # #     itemSet, transactionList = getItemSetTransactionList(data_iter)

# # #     freqSet = defaultdict(int)
# # #     largeSet = dict()

# # #     oneCSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)
# # #     currentLSet = oneCSet
# # #     k = 2

# # #     while currentLSet:
# # #         largeSet[k - 1] = currentLSet
# # #         currentLSet = joinSet(currentLSet, k)
# # #         currentCSet = returnItemsWithMinSupport(currentLSet, transactionList, minSupport, freqSet)
# # #         currentLSet = currentCSet
# # #         k += 1

# # #     def getSupport(item):
# # #         """Returns the support of an item"""
# # #         return float(freqSet[item]) / len(transactionList)

# # #     # Frequent itemsets
# # #     toRetItems = []
# # #     for key, value in largeSet.items():
# # #         toRetItems.extend([(tuple(item), getSupport(item)) for item in value])

# # #     # Association rules
# # #     toRetRules = []
    
# # #     for k, itemsets in largeSet.items():
# # #         if k < 2:
# # #             continue  # No rule from 1-itemset
# # #         for itemset in itemsets:
# # #             for antecedent in non_empty_proper_subsets(itemset):
# # #                 antecedent = frozenset(antecedent)
# # #                 consequent = itemset - antecedent
# # #                 if len(consequent) == 0:
# # #                     continue
# # #                 confidence = getSupport(itemset) / getSupport(antecedent)
# # #                 if confidence >= minConfidence:
# # #                     toRetRules.append(((tuple(antecedent), tuple(consequent)), confidence))

# # #     return toRetItems, toRetRules

# # # def printResults(items, rules):
# # #     outfile = open('output.txt', 'a')
    
# # #     # Write frequent itemsets
# # #     outfile.write("\n------------------------ FREQUENT ITEMSETS:\n")
# # #     for item, support in sorted(items, key=lambda x: x[1]):
# # #         line = f"Item: {item}, Support = {round(support, 3)}\n"
# # #         outfile.write(line)

# # #     # Write association rules
# # #     outfile.write("\n------------------------ RULES:\n")
# # #     for rule, confidence in sorted(rules, key=lambda x: x[1]):
# # #         pre, post = rule
# # #         line = f"Rule: {pre} ==> {post}, Confidence = {round(confidence, 3)}\n"
# # #         outfile.write(line)
    
# # #     outfile.close()

# # # def dataFromFile(fname):
# # #     """Reads data from file and yields transactions"""
# # #     with open(fname, 'r', newline='', encoding='utf-8') as file_iter:
# # #         for line in file_iter:
# # #             line = line.strip().rstrip(',')
# # #             record = frozenset(line.split(','))
# # #             yield record


# # # if __name__ == "__main__":
# # #     optparser = OptionParser()
# # #     optparser.add_option('-f', '--inputFile',
# # #                          dest='input',
# # #                          help='filename containing CSV',
# # #                          default=None)
# # #     optparser.add_option('-s', '--minSupport',
# # #                          dest='minS',
# # #                          help='minimum support value',
# # #                          default=0.15,
# # #                          type='float')
# # #     optparser.add_option('-c', '--minConfidence',
# # #                          dest='minC',
# # #                          help='minimum confidence value',
# # #                          default=0.6,
# # #                          type='float')

# # #     (options, args) = optparser.parse_args()

# # #     if options.input is None:
# # #         print('No dataset filename specified. Use -f to provide one.')
# # #         sys.exit('System will exit')

# # #     minSupport = options.minS
# # #     minConfidence = options.minC

# # #     inFile = dataFromFile(options.input)

# # #     items, rules = runApriori(inFile, minSupport, minConfidence)

# # #     printResults(items, rules)
# # """
# # Description     : Simple Python implementation of the Apriori Algorithm (Python 3)
# # Usage:
# #     $ python apriori.py -f DATASET.csv -s minSupport -c minConfidence
# #     $ python apriori.py -f DATASET.csv -s 0.15 -c 0.6
# # """

# # import sys
# # from itertools import chain, combinations
# # from collections import defaultdict
# # from optparse import OptionParser


# # def non_empty_proper_subsets(itemset):
# #     """Return all non-empty proper subsets of itemset"""
# #     return chain.from_iterable(combinations(itemset, r) for r in range(1, len(itemset)))


# # def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
# #     """Calculates support for items and returns those meeting minSupport"""
# #     _itemSet = set()
# #     localSet = defaultdict(int)

# #     for item in itemSet:
# #         for transaction in transactionList:
# #             if item.issubset(transaction):
# #                 freqSet[item] += 1
# #                 localSet[item] += 1

# #     for item, count in localSet.items():
# #         support = float(count) / len(transactionList)
# #         if support >= minSupport:
# #             _itemSet.add(item)

# #     return _itemSet


# # def joinSet(itemSet, length):
# #     """Join a set with itself and return n-element itemsets"""
# #     return set([
# #         i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length
# #     ])


# # def getItemSetTransactionList(data_iterator):
# #     """Generates 1-itemsets and transaction list"""
# #     transactionList = list()
# #     itemSet = set()
# #     for record in data_iterator:
# #         transaction = frozenset(record)
# #         transactionList.append(transaction)
# #         for item in transaction:
# #             itemSet.add(frozenset([item]))
# #     return itemSet, transactionList


# # def runApriori(data_iter, minSupport, minConfidence):
# #     """Runs Apriori algorithm and returns frequent itemsets and association rules"""
# #     itemSet, transactionList = getItemSetTransactionList(data_iter)

# #     freqSet = defaultdict(int)
# #     largeSet = dict()

# #     oneCSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)
# #     largeSet[1] = oneCSet  # ✅ Include 1-itemsets in largeSet
# #     currentLSet = oneCSet
# #     k = 2

# #     while currentLSet:
# #         currentLSet = joinSet(currentLSet, k)
# #         currentCSet = returnItemsWithMinSupport(currentLSet, transactionList, minSupport, freqSet)
# #         if currentCSet:
# #             largeSet[k] = currentCSet
# #         currentLSet = currentCSet
# #         k += 1

# #     def getSupport(item):
# #         """Returns the support of an item"""
# #         return float(freqSet[item]) / len(transactionList)

# #     # Frequent itemsets
# #     toRetItems = []
# #     for key, value in largeSet.items():
# #         toRetItems.extend([(tuple(item), getSupport(item)) for item in value])

# #     # Association rules
# #     toRetRules = []
# #     for k, itemsets in largeSet.items():
# #         if k < 2:
# #             continue  # No rule from 1-itemset
# #         for itemset in itemsets:
# #             for antecedent in non_empty_proper_subsets(itemset):
# #                 antecedent = frozenset(antecedent)
# #                 consequent = itemset - antecedent
# #                 if len(consequent) == 0:
# #                     continue
# #                 confidence = getSupport(itemset) / getSupport(antecedent)
# #                 if confidence >= minConfidence:
# #                     toRetRules.append(((tuple(antecedent), tuple(consequent)), confidence))

# #     return toRetItems, toRetRules


# # def printResults(items, rules):
# #     outfile = open('output.txt', 'a')

# #     # Write frequent itemsets
# #     outfile.write("\n------------------------ FREQUENT ITEMSETS:\n")
# #     for item, support in sorted(items, key=lambda x: x[1]):
# #         line = f"Item: {item}, Support = {round(support, 3)}\n"
# #         outfile.write(line)

# #     # Write association rules
# #     outfile.write("\n------------------------ RULES:\n")
# #     for rule, confidence in sorted(rules, key=lambda x: x[1]):
# #         pre, post = rule
# #         line = f"Rule: {pre} ==> {post}, Confidence = {round(confidence, 3)}\n"
# #         outfile.write(line)

# #     outfile.close()


# # def dataFromFile(fname):
# #     """Reads data from file and yields transactions"""
# #     with open(fname, 'r', newline='', encoding='utf-8') as file_iter:
# #         for line in file_iter:
# #             line = line.strip().rstrip(',')
# #             record = frozenset(line.split(','))
# #             yield record


# # if __name__ == "__main__":
# #     optparser = OptionParser()
# #     optparser.add_option('-f', '--inputFile',
# #                          dest='input',
# #                          help='filename containing CSV',
# #                          default=None)
# #     optparser.add_option('-s', '--minSupport',
# #                          dest='minS',
# #                          help='minimum support value',
# #                          default=0.15,
# #                          type='float')
# #     optparser.add_option('-c', '--minConfidence',
# #                          dest='minC',
# #                          help='minimum confidence value',
# #                          default=0.6,
# #                          type='float')

# #     (options, args) = optparser.parse_args()

# #     if options.input is None:
# #         print('No dataset filename specified. Use -f to provide one.')
# #         sys.exit('System will exit')

# #     minSupport = options.minS
# #     minConfidence = options.minC

# #     inFile = dataFromFile(options.input)

# #     items, rules = runApriori(inFile, minSupport, minConfidence)

# #     printResults(items, rules)
# """
# Description     : Simple Python implementation of the Apriori Algorithm (Python 3)
# Usage:
#     $ python apriori.py -f DATASET.csv -s minSupport -c minConfidence
#     $ python apriori.py -f DATASET.csv -s 0.15 -c 0.6
# """

# import sys
# from itertools import chain, combinations
# from collections import defaultdict
# from optparse import OptionParser


# def subsets(arr):
#     """Returns non-empty subsets of arr"""
#     return chain(*[combinations(arr, i + 1) for i in range(len(arr))])


# def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
#     """Calculates support for items and returns those meeting minSupport"""
#     _itemSet = set()
#     localSet = defaultdict(int)

#     for item in itemSet:
#         for transaction in transactionList:
#             if item.issubset(transaction):
#                 freqSet[item] += 1
#                 localSet[item] += 1

#     for item, count in localSet.items():
#         support = float(count) / len(transactionList)
#         if support >= minSupport:
#             _itemSet.add(item)

#     return _itemSet


# def joinSet(itemSet, length):
#     """Join a set with itself and return n-element itemsets"""
#     return set([
#         i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length
#     ])


# def getItemSetTransactionList(data_iterator):
#     """Generates 1-itemsets and transaction list"""
#     transactionList = list()
#     itemSet = set()
#     for record in data_iterator:
#         transaction = frozenset(record)
#         transactionList.append(transaction)
#         for item in transaction:
#             itemSet.add(frozenset([item]))
#     return itemSet, transactionList


# def runApriori(data_iter, minSupport, minConfidence):
#     """
#     Runs the Apriori algorithm.
#     `data_iter` is a record iterator
#     `minSupport` is the minimum support
#     `minConfidence` is the minimum confidence
#     """
#     itemSet, transactionList = getItemSetTransactionList(data_iter)

#     freqSet = defaultdict(int)
#     largeSet = dict()
#     # Global dictionary which stores all frequent itemsets

#     assocRules = dict()
#     # Dictionary which stores Association Rules

#     oneCSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)

#     currentLSet = oneCSet
#     k = 2
#     while currentLSet != set([]):
#         largeSet[k - 1] = currentLSet
#         currentLSet = joinSet(currentLSet, k)
#         currentCSet = returnItemsWithMinSupport(
#             currentLSet, transactionList, minSupport, freqSet
#         )
#         currentLSet = currentCSet
#         k = k + 1

#     def getSupport(item):
#         """local function which Returns the support of an item"""
#         return float(freqSet[item]) / len(transactionList)

#     toRetItems = []
#     for key, value in largeSet.items():
#         toRetItems.extend([(tuple(item), getSupport(item)) for item in value])

#     toRetRules = []
#     for key, value in list(largeSet.items())[1:]:
#         for item in value:
#             _subsets = map(frozenset, [x for x in subsets(item)])
#             for element in _subsets:
#                 remain = item.difference(element)
#                 if len(remain) > 0:
#                     confidence = getSupport(item) / getSupport(element)
#                     if confidence >= minConfidence:
#                         toRetRules.append(((tuple(element), tuple(remain)), confidence))
#     return toRetItems, toRetRules


# def printResults(items, rules, minSupport, minConfidence):
#     """Prints the frequent itemsets and association rules to a file 'output.txt'."""
    
#     # Using 'w' to overwrite the file for each run.
#     with open('output.txt', 'w', encoding='utf-8') as outfile:
#         outfile.write("="*60 + "\n")
#         outfile.write(" Apriori Algorithm Results\n")
#         outfile.write("="*60 + "\n")
#         outfile.write(f"Parameters:\n")
#         outfile.write(f"  - Minimum Support: {minSupport}\n")
#         outfile.write(f"  - Minimum Confidence: {minConfidence}\n")
#         outfile.write("-"*60 + "\n\n")

#         if not items:
#             outfile.write("No frequent itemsets found.\n")
#             outfile.write("Consider lowering the minimum support value (-s).\n")
#             return

#         # Sort items by support for readability
#         items.sort(key=lambda x: x[1], reverse=True)
#         outfile.write(f"--- Frequent Itemsets ({len(items)} found) ---\n")
#         for item, support in items:
#             # Format for better alignment and readability
#             outfile.write(f"Item: {str(sorted(list(item))):<40} Support: {support:.4f}\n")

#         outfile.write("\n" + "-"*60 + "\n\n")

#         if not rules:
#             outfile.write("--- Association Rules ---\n")
#             outfile.write("No rules found that meet the minimum confidence.\n")
#             # Provide guidance to the user
#             if any(len(item[0]) > 1 for item in items):
#                  outfile.write("Frequent itemsets with >1 item exist. Try lowering the minimum confidence (-c).\n")
#             else:
#                  outfile.write("No frequent itemsets with >1 item were found, so no rules could be made.\n")
#                  outfile.write("Try lowering the minimum support (-s) to find larger itemsets.\n")
#             return

#         # Sort rules by confidence for readability
#         rules.sort(key=lambda x: x[1], reverse=True)
#         outfile.write(f"--- Association Rules ({len(rules)} found) ---\n")
#         for rule, confidence in rules:
#             pre, post = rule
#             # Sort items in the rule for consistent output
#             pre_list = sorted(list(pre))
#             post_list = sorted(list(post))
#             outfile.write(f"Rule: {str(pre_list)} ==> {str(post_list)}\n")
#             outfile.write(f"  Confidence: {confidence:.4f}\n\n")

#     print("✅ Success! Results have been written to output.txt")


# def dataFromFile(fname):
#     """Reads data from a CSV file and yields transactions."""
#     with open(fname, 'r', encoding='utf-8') as file_iter:
#         for line in file_iter:
#             # Clean up the line: remove whitespace, trailing commas
#             line = line.strip()
#             if line.endswith(','):
#                 line = line[:-1]
#             # Clean up each item: remove whitespace and quotes, then filter out empty strings
#             cleaned_record = [item.strip().strip('"\'') for item in line.split(',')]
#             record = frozenset(item for item in cleaned_record if item)
            
#             if record:  # Do not yield empty transactions
#                 yield record


# if __name__ == "__main__":
#     optparser = OptionParser()
#     optparser.add_option('-f', '--inputFile',
#                          dest='input',
#                          help='filename containing CSV',
#                          default=None)
#     optparser.add_option('-s', '--minSupport',
#                          dest='minS',
#                          help='minimum support value',
#                          default=0.15,
#                          type='float')
#     optparser.add_option('-c', '--minConfidence',
#                          dest='minC',
#                          help='minimum confidence value',
#                          default=0.6,
#                          type='float')

#     (options, args) = optparser.parse_args()

#     if options.input is None:
#         print('No dataset filename specified. Use -f to provide one.')
#         sys.exit('System will exit')

#     minSupport = options.minS
#     minConfidence = options.minC

#     inFile = dataFromFile(options.input)

#     items, rules = runApriori(inFile, minSupport, minConfidence)

#     printResults(items, rules, minSupport, minConfidence)

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
    """
    Runs the Apriori algorithm.
    `data_iter` is a record iterator
    `minSupport` is the minimum support
    `minConfidence` is the minimum confidence
    """
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores all frequent itemsets

    oneCSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)

    currentLSet = oneCSet
    k = 2
    while currentLSet != set([]):
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(
            currentLSet, transactionList, minSupport, freqSet
        )
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
        """local function which Returns the support of an item"""
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


def printResults(items, rules, minSupport, minConfidence):
    """Prints the frequent itemsets and association rules to a file 'output.txt'."""
    
    # Using 'w' to overwrite the file for each run.
    with open('output.txt', 'w', encoding='utf-8') as outfile:
        outfile.write("="*60 + "\n")
        outfile.write(" Apriori Algorithm Results\n")
        outfile.write("="*60 + "\n")
        outfile.write(f"Parameters:\n")
        outfile.write(f"  - Minimum Support: {minSupport}\n")
        outfile.write(f"  - Minimum Confidence: {minConfidence}\n")
        outfile.write("-"*60 + "\n\n")

        if not items:
            outfile.write("No frequent itemsets found.\n")
            outfile.write("Consider lowering the minimum support value (-s).\n")
            return

        # Sort items by support for readability
        items.sort(key=lambda x: x[1], reverse=True)
        outfile.write(f"--- Frequent Itemsets ({len(items)} found) ---\n")
        for item, support in items:
            # Format for better alignment and readability
            outfile.write(f"Item: {str(sorted(list(item))):<40} Support: {support:.4f}\n")

        outfile.write("\n" + "-"*60 + "\n\n")

        if not rules:
            outfile.write("--- Association Rules ---\n")
            outfile.write("No rules found that meet the minimum confidence.\n")
            # Provide guidance to the user
            if any(len(item[0]) > 1 for item in items):
                 outfile.write("Frequent itemsets with >1 item exist. Try lowering the minimum confidence (-c).\n")
            else:
                 outfile.write("No frequent itemsets with >1 item were found, so no rules could be made.\n")
                 outfile.write("Try lowering the minimum support (-s) to find larger itemsets.\n")
            return

        # Sort rules by confidence for readability
        rules.sort(key=lambda x: x[1], reverse=True)
        outfile.write(f"--- Association Rules ({len(rules)} found) ---\n")
        for rule, confidence in rules:
            pre, post = rule
            # Sort items in the rule for consistent output
            pre_list = sorted(list(pre))
            post_list = sorted(list(post))
            outfile.write(f"Rule: {str(pre_list)} ==> {str(post_list)}\n")
            outfile.write(f"  Confidence: {confidence:.4f}\n\n")

    print("✅ Success! Results have been written to output.txt")


def dataFromFile(fname):
    """Reads data from a CSV file and yields transactions."""
    with open(fname, 'r', encoding='utf-8') as file_iter:
        for line in file_iter:
            # Clean up the line: remove whitespace, trailing commas
            line = line.strip()
            if line.endswith(','):
                line = line[:-1]
            # Clean up each item: remove whitespace and quotes, then filter out empty strings
            cleaned_record = [item.strip().strip('"\'') for item in line.split(',')]
            record = frozenset(item for item in cleaned_record if item)
            
            if record:  # Do not yield empty transactions
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

    printResults(items, rules, minSupport, minConfidence)