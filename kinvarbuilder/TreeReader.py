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

