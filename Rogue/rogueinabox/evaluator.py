#Copyright (C) 2017 Andrea Asperti, Carlo De Pieri, Gianmaria Pedrini, Francesco Sovrano
#
#This file is part of Rogueinabox.
#
#Rogueinabox is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Rogueinabox is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections

class Episode:
	def __init__(self, info, reward, has_won, step):
		self.info = info
		self.reward = reward
		self.has_won = has_won
		self.step = step
	
class RogueEvaluator:

	def __init__(self, match_count_for_evaluation):
		self.reset()
		self.match_count_for_evaluation = match_count_for_evaluation
		
	def reset(self):
		self.episodes = collections.deque()
		self.min_reward = 0
		self.max_reward = 0
		
	def add(self, info, reward, has_won, step): # O(1)
		self.episodes.append( Episode(info, reward, has_won, step) )
		if len(self.episodes) > self.match_count_for_evaluation:
			self.episodes.popleft()
	
	def statistics(self): # O(self.match_count_for_evaluation)
		result = {}
		result["success_rate"] = 0
		result["avg_reward"] = 0
		result["avg_tiles"] = 0
		result["avg_success_steps"] = 0
		
		count = len(self.episodes)
		if count>0:
			for e in self.episodes:
				if e.has_won:
					result["success_rate"] += 1
					result["avg_success_steps"] += e.step
				result["avg_reward"] += e.reward
				result["avg_tiles"] += e.info.get_known_tiles_count()
			if result["success_rate"] > 0:
				result["avg_success_steps"] /= result["success_rate"] # do it BEFORE averaging the success_rate
				result["success_rate"] /= count # do it AFTER averaging the success_steps
			result["avg_reward"] /= count
			result["avg_tiles"] /= count
		return result
		