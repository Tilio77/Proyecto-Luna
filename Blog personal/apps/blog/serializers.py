from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):

	class Meta:
		model = Post
		fields = [
			'id',
			'title',
			'slug',
			'views',
			'thumbnail',
			'description',
			'content',
			'published',
			'time_read',
			'category',
		]