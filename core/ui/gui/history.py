'''
history.py

Copyright 2007 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''
import cPickle
import operator
import os


class HistorySuggestion(object):
    '''Handles the history of any text, providing suggestions.

    :param filename: Name of the file where the info is stored

    It's also responsible of loading and saving the info in a file.
    '''
    def __init__(self, filename):
        self.filename = filename
        self.history = {}

        if os.access(filename, os.R_OK):
            # dict: {text:points}
            fileh = open(filename)
            #
            # Added this try/except because of this bug:
            # https://sourceforge.net/tracker/?func=detail&atid=853652&aid=2830825&group_id=170274
            #
            try:
                self.history = cPickle.load(fileh)
            except:
                self.history = {}
            fileh.close()

    def get_texts(self):
        '''Provides the texts, ordered by relevance.

        :return: a generator with the texts
        '''
        info = sorted(self.history.items(),
                      key=operator.itemgetter(1),
                      reverse=True)
        
        return [k for k, v in info]

    def insert(self, newtext):
        '''Inserts new text to the history.'''
        self.history[newtext] = self.history.get(newtext, 0) + 1

    def save(self):
        '''Saves the history information.'''
        try:
            fileh = open(self.filename, "w")
        except IOError:
            pass
        else:
            cPickle.dump(self.history, fileh)
            fileh.close()
