#!/usr/bin/env python

# kinvarbuilder - A library for searching kinematic variables in a systematic way
#
# Copyright 2014 University of California, San Diego
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


#----------------------------------------------------------------------

def CachingFunction(wrappedClass):
    # a decorator function which caches the calculated quantity of the
    # current event
    #
    # note that this is a function (with a class inside), NOT a class itself
    #
    # see e.g. https://www.inkling.com/read/learning-python-mark-lutz-4th/chapter-38/coding-class-decorators

    class Wrapper(object):

        def __init__(self, *args, **kwargs):

            self.wrappedObj = wrappedClass(*args, **kwargs)
            self.cachedValue = None

        def newEvent(self):
            # this is called when a new event is read from the tree
            # invalidate the cache
            self.cachedValue = None

            #if hasattr(self.wrappedObj, "newEvent"):
            #    self.wrappedObj.newEvent()

            # also propagate this to the parents
            for parent in self.getParents():
                parent.newEvent()

        def getValue(self):
            if self.cachedValue == None:
                # recalculate
                self.cachedValue = self.wrappedObj.getValue()

            return self.cachedValue

        def __getattr__(self, item):
            # this is for calling the methods on the wrapped function
            return getattr(self.wrappedObj, item)

        def getParents(self):
            if hasattr(self.wrappedObj,"getParents"):
                return self.wrappedObj.getParents()
            else:
                return []

        def __str__(self):
            if hasattr(self.wrappedObj, '__str__'):
                return self.wrappedObj.__str__()
            return object.__str__(self.wrappedObj)

        def __repr__(self):
            if hasattr(self.wrappedObj, '__repr__'):
                return self.wrappedObj.__repr__()
            return object.__repr__(self.wrappedObj)

    # create a dynamic subclass to decorate the static/class methods
    retval = type('Wrapped' + wrappedClass.__name__, (Wrapper,), {})

    setattr(retval, 'getNumArguments', staticmethod(lambda maxNumArguments: wrappedClass.getNumArguments(maxNumArguments)))

    # return Wrapper
    return retval


#----------------------------------------------------------------------

class IllegalArgumentTypes(Exception):
    """ is thrown if a function does not accept the arguments given """
    pass

#----------------------------------------------------------------------

class TreeReader:
    # class for reading multiple expressions from a ROOT tree in batches of multiple events

    #----------------------------------------

    def __init__(self, tree, readBatchSize = 10000):
        # @param readBatchSize is the number of events which
        #        are read in a batch

        self.tree = tree
        self.readBatchSize = int(readBatchSize)

        self.numEvents = tree.GetEntries()

        # the expressions we want to read from a tree
        self.expressions = []

        # the float buffers (lists) corresponding to the expressions
        self.buffers = []

        # arrays to read from the tree
        self.cache = []
        
        # the first and last + 1 event in the cache
        self.cacheBegin = None
        self.cacheEnd = None

        # the currently loaded event
        self.currentEvent = None


    #----------------------------------------

    def getVar(self, expression):

        # @return a variable which will hold the given expression
        # whenever a new event is read
        # 
        # this will return a list with one float variable which will
        # be updated by this class (there are no references for
        # floats in python)
        #
        try:
            index = self.expressions.index(expression)

            # if we come here, the expression exists already
            return self.buffers[index]

        except ValueError:
            # expression is not yet there, reserve a new buffer

            # TODO: check that this is not happening after we
            #       have read events (or we would have to
            #       invalidate the buffers we read already)

            self.expressions.append(expression)
            self.buffers.append([ 0. ])

            # add a buffer for reading from the tree
            self.cache.append([ 0. ] * self.readBatchSize)

            return self.buffers[-1]

    #----------------------------------------

    def __fillCache(self, begin, end):
        numEvents = end - begin
        assert numEvents >= 0

        for index, expr in enumerate(self.expressions):
            self.tree.Draw(expr, "", "goff",
                           numEvents,
                           begin)
            
            vec = self.tree.GetV1()
            for i in range(numEvents):
                self.cache[index][i] = vec[i]

        self.cacheBegin = begin
        self.cacheEnd = end

    #----------------------------------------

    def getEvent(self, eventIndex):
        # fills the buffers with the event given by 'index'

        # avoid getting the same event multiple times
        if self.currentEvent == eventIndex:
            return 

        # check if we have the event in the cache
        if self.cacheBegin == None or not (eventIndex >= self.cacheBegin and eventIndex < self.cacheEnd):
            # must fill the cache
            start = (eventIndex // self.readBatchSize) * self.readBatchSize
            end = (eventIndex // self.readBatchSize + 1) * self.readBatchSize
            end = min(end, self.numEvents)
            
            self.__fillCache(start, end)

        # fill the event
        relIndex = eventIndex - self.cacheBegin

        # copy a line of our internal buffer 
        # to 
        for index in range(len(self.buffers)):
            self.buffers[index][0] = self.cache[index][relIndex]

        self.currentEvent = eventIndex


    #----------------------------------------

#----------------------------------------------------------------------

def makePartitions(items, numsubsets):
    # generates all possible 'numsubsets' tuples of non-overlapping
    # subsets of the given items

    assert numsubsets >= 1

    # generate a 'power set': a set and the rest
    # then recursively generate partitions with numsubsets - 1 groups
    # and join them 

    numItems = len(items)

    retval = []

    for i in range(1 << numItems):

        thisGroup = []

        otherGroup = []

        for j in range(numItems):
            if i & (1 << j):
                thisGroup.append(items[j])
            else:
                otherGroup.append(items[j])

        # skip empty sets
        if not thisGroup:
            continue

        if numsubsets == 1:
            retval.append([thisGroup])
        else:
            if not otherGroup:
                continue

            for subs in makePartitions(otherGroup, numsubsets - 1):
                retval.append(sorted([ thisGroup ] + subs))


    # end of loop over powers

    #----------
    # eliminate dupliactes
    #----------

    # this is probably not the most efficient way
    # but it works for small sets
    
    retval2 = []

    seen = set()
     
    for line in retval:
        # line is a list of lists
        #
        # sort the groups such that we avoid duplicates
        line2 = tuple([tuple(x) for x in line])

        if not line2 in seen:
            seen.add(line2)
            retval2.append(line)

    return sorted(retval2)

#----------------------------------------------------------------------