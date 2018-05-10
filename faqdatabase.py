import re
import datetime
import os
import sys
import pymongo
import json
from datetime import datetime, timedelta
from bson.objectid import ObjectId
import time

client = pymongo.MongoClient('xr-nft.cisco.com', 27017)
db = client.nft.faqs


class FaqDatabase:
	"""
	Here we have written the complete code for the database in MongoDB.
	like Insert, Find , Update queries.
	"""

	def insert(self,username, title, device, feature, answer, submitter_manager_org):
		self.usernmae = username
		self.title = title
		self.device = device
		self.feature = feature
		self.answer = answer
		self.submitter_manager_org = submitter_manager_org
		self.likes = 0
		self.comments = ""
		self.views = 0


		try:
			db.insert_one(
				{
					"submitter-id":          self.usernmae,
					"title":                 self.title,
					"device":                self.device,
					"feature":               self.feature,
					"answer":                self.answer,
					"submitter-manager-org": self.submitter_manager_org,
					"likes":                 self.likes,
					"comments":              self.comments,
					"created_on":            datetime.utcnow(),
					"views":                 self.views

				}
			)
			return True
		except Exception as e:
			print(str(e))
			return False

	def findfaq(self, device,feature):
		"""Here we have writen a login to fetch the requested FAQ's from database."""

		try :
			faqs = db.find({"device": device, "feature": feature})
			return faqs
		except Exception as e:
			print(str(e))
			return False

	def updateview(self,recid):
		""""""
		try:
			views_obj = db.find({'_id': ObjectId(recid)})
			try :
				for view in views_obj :
					view_num = view["views"]
					print("before "+ str(view_num))
					view_num = 1 + int(view_num)
					print("after view_num " + str(view_num))
				db.update_one ({'_id': ObjectId (recid)}, {"$set": {"views": view_num}})
			except KeyError as e:
				print(e)
			except Exception as e:
				print(e)
			return True

		except Exception as e:
			print (str(e))
			return False

	def findrecord(self,recid):
		""""""

		try:
			record_details = db.find({'_id': ObjectId(recid)})
			return record_details
		except Exception as e:
			print(str(e))
			return False

	def updatefaq(self,recid,title, device, feature, answer):

		try :
			db.update_one(
				{
					'_id': ObjectId (recid)
				},
				{
					"$set": {
						"title": title,
						"device": device,
						"feature": feature,
						"answer": answer, "created_on": datetime.utcnow ()
					}
				}
			)
			return True

		except Exception as e:
			print(str(e))
			return False






