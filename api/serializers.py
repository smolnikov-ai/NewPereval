from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from api.models import User, Coords, Level, Pereval, Images


class UserSerializer(WritableNestedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CoordsSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


class LevelSerializers(WritableNestedModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class ImagesSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Images
        fields = ['data', 'title', ]


class PerevalSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializers()
    images = ImagesSerializer(many=True)

    class Meta:
        model = Pereval
        fields = ['user', 'coords', 'level', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'status',
                  'images', ]
        read_only_fields = ['status', ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')

        user = User.objects.get_or_create(**user_data)
        coords = Coords.objects.create(**coords_data)
        level = Level.objects.create(**level_data)

        pereval = Pereval.objects.create(user=user, coords=coords, level=level, **validated_data)

        for image_data in images_data:
            data = image_data.get('data')
            title = image_data.get('title')
            Images.objects.create(data=data, title=title, pereval=pereval)

        return pereval


