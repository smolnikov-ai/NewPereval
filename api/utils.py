from django.forms import model_to_dict
from rest_framework import status
from rest_framework.response import Response


def check_unique_field(model_data, model, field):
    model_data = model_data.copy()
    model_data_field = model_data.pop(field)
    filter_kwargs = {field: model_data_field}
    model_object = model.objects.filter(**filter_kwargs).first()
    if model_object:
        model_dict = model_to_dict(model_object)
        model_dict.pop('id')
        model_dict.pop(field)
        if model_dict != model_data:
            return False
    return True


def check_update_user(data_user, user_dict):
    return data_user and user_dict != data_user


def check_unique_field_response(field):
    if field == 'email':
        field_response = 'e-mail'
    elif field == 'phone':
        field_response = 'phone number'
    else:
        field_response = field

    return Response(
        {
            'status': 409,
            'message': f'This {field_response} is already occupied by another user.',
        },
        status=status.HTTP_409_CONFLICT
    )


def check_update_user_response():
    return Response(
        {
            'state': 0,
            'message': 'User data cannot be changed.'
        },
        status=status.HTTP_400_BAD_REQUEST
    )


def check_pereval_status(instance_status):
    return instance_status != 'new'


def check_pereval_status_not_new_response():
    return Response(
        {
            'state': 0,
            'message': 'Incorrect status.'
        },
        status=status.HTTP_400_BAD_REQUEST
    )
