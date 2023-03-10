from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Post, ViewCount
from apps.category.models import Category
from .serializers import PostSerializer, PostListSerializer
from .pagination import SmallSetPagination, MediumSetPagination, LargeSetPagination

# Create your views here.

class BlogListView(APIView):
	permission_classes = (permissions.AllowAny,)

	def get(self, request, format=None):
		if Post.objects.all().exists():
			
			posts = Post.objects.all()

			paginator = SmallSetPagination()
			results = paginator.paginate_queryset(posts, request)

			serializer = PostListSerializer(results, many=True)


			return paginator.get_paginated_response({ 'posts': serializer.data })
		else:
			return Response({ 'error': 'No posts found' }, status=status.HTTP_404_NOT_FOUND)


class ListPostsByCategoryView(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request, format=None):
		if Post.postobjects.all().exists():

			slug = request.query_params.get('slug')
			print(slug)
			category = Category.objects.get(slug=slug)
			
			posts = Post.postobjects.order_by('-published').all()

		# # Si la categoría tiene un padre, filtrar sólo por esta categoría y no por el padre también
		if category.parent:
			posts = posts.filter(category=category)

		# # Si la categoría no tiene una categoría padre, significa que ella misma es una categoría padre
		# else: 

			#Filtrar categoria sola
			if not Category.objects.filter(parent=category).exists():
				posts = posts.filter(category=category)
			# Si esta categoría padre tiene hijos, filtrar por la categoría padre y sus hijos
			else:
				sub_categories = Category.objects.filter(parent=category)
				
				filtered_categories = [category]

				for cat in sub_categories:
					filtered_categories.append(cat)

				filtered_categories = tuple(filtered_categories)

				posts = posts.filter(category__in=filtered_categories)
					
			paginator = SmallSetPagination()
			results = paginator.paginate_queryset(posts, request)
			serializer = PostListSerializer(results, many=True)

			return paginator.get_paginated_response({'posts': serializer.data})
		else:
			return Response({'error':'No posts found'}, status=status.HTTP_404_NOT_FOUND)