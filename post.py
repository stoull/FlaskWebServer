import json
class Post():
	"""docstring for Post"""
	def __init__(self, userId, id, title, body):
		self.userId = userId
		self.id = id
		self.title = title
		self.body = body

	# @classmethod
	# def from_dic(cls, infor_dic):


	@classmethod
	def get_all_posts(cls):
		with open('./static/posts.json', mode='r') as posts_file:
			data = json.load(posts_file)
			for dic in data:
				print(dic)
			return data
		