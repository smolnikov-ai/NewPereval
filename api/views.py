from django.db import DatabaseError
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import User, Images, Coords, Level, Pereval
from api.serializers import UserSerializer, ImagesSerializer, CoordsSerializer, LevelSerializer, PerevalSerializer
from api.utils import (check_unique_field, check_update_user, check_unique_field_response, check_update_user_response,
                       check_pereval_status, check_pereval_status_not_new_response, )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CoordsViewSet(ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class LevelViewSet(ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImagesViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class PerevalViewSet(ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    filterset_fields = ['user__email', ]
    http_method_names = ['get', 'post', 'patch', 'put', 'delete', 'head', 'options', ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data_user = request.data.get('user')
        if not check_unique_field(data_user, User, 'email'):
            return check_unique_field_response('email')
        if not check_unique_field(data_user, User, 'phone'):
            return check_unique_field_response('phone')
        try:
            if not serializer.is_valid():
                return Response(
                    {
                        'status': 400,
                        'message': serializer.errors,
                        'pk': None
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(
                {
                    'status': 200,
                    'message': None,
                    'pk': serializer.instance.pk,
                },
                status=status.HTTP_200_OK,
            )
        except DatabaseError as e:
            return Response(
                {
                    'status': 500,
                    'message': f'Database connection error {str(e)}',
                    'pk': None,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


    def update(self, request, *args, **kwargs):
        pereval = self.get_object()
        user_dict = model_to_dict(pereval.user)
        user_dict.pop('id')
        serializer = self.get_serializer(pereval, data=request.data, partial=True)
        if check_pereval_status(pereval.status):
            return check_pereval_status_not_new_response()
        if check_update_user(request.data.get('user'), user_dict):
            return check_update_user_response()
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'state': 1,
                'message': 'The record was successfully updated.',
            },
            status=status.HTTP_200_OK,
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
