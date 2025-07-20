from rest_framework.viewsets import ModelViewSet

from api.models import User, Images, Coords, Level, Pereval
from api.serializers import UserSerializer, ImagesSerializer, CoordsSerializer, LevelSerializer, PerevalSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CoordsViewSet(ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class LevelViewSet(ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImageViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class PerevalViewSet(ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    filterset_fields = ['user__email', ]
    http_method_names = ['get', 'post', 'patch', ]
