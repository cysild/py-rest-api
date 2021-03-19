from django.conf.urls import url, include
from django.urls import  path

from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt import views as jwt_views
from rest_framework.permissions import IsAuthenticated

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email','password','url',)
        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
 

    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.



urlpatterns = [ 
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('tutorials.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]