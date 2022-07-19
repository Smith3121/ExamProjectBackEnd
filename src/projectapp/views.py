from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, \
    RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from base.error_messages import ErrorMessage
from base.exceptions import UserDoesNotExistAPIException, DomainIsNotEligibleAPIException, DomainIsNotEligibleException
from projectapp.models import User
from projectapp.serializers import UserSerializer


class UserAPIView(APIView):

    def get_user(self, pk):
        try:
            return User.objects.filter(pk=pk)
        except User.DoesNotExist:
            raise UserDoesNotExistAPIException

    def get(self, request, pk=None, format=None):
        if pk:
            data = self.get_user(pk)
        else:
            data = User.objects.all()
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        serializer = UserSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = Response()

        response.data = {
            'message': 'User Created Successfully',
            'data': serializer.data
        }
        return response

    def put(self, request, pk=None, format=None):
        user_to_update = User.objects.get(pk=pk)
        serializer = UserSerializer(instance=user_to_update, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = Response()

        response.data = {
            'message': 'User Updated Successfully',
            'data': serializer.data
        }

        return response

    def delete(self, request, pk, format=None):
        user_to_delete = User.objects.get(pk=pk)

        user_to_delete.delete()

        return Response({
            'message': 'User Deleted Successfully'
        })

# class TokenViewSet(CreateModelMixin, viewsets.GenericViewSet):
#
#     serializer_class = TokenRequestSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data.get('email', None)
#         mtoken = serializer.validated_data['mtoken']
#
#         if email is None:
#             user_id = serializer.validated_data['user_id']
#             email = UserService.get_by_id(user_id).email
#
#         token = TokenService.create_by_email_and_mtoken_with_request_params(email, mtoken, *args, **kwargs)
#         user = UserService.get_by_email(email)
#
#         # Invalidate used magic token
#         MTokenService.deactivate_by_key(mtoken)
#
#         self.serializer_class = TokenResponseSerializer
#         serializer = self.get_serializer({'user': user, 'token': token})
#         headers = self.get_success_headers(serializer.data)
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#

# class MTokenViewSet(CreateModelMixin, viewsets.GenericViewSet):
#
#     serializer_class = MTokenRequestSerializer
#
#     def create(self, request, *args, **kwargs):
#         user = MTokenHandler.handle(request, self.get_serializer, 'l', *args, **kwargs)
#
#         self.serializer_class = MTokenResponseSerializer
#         serializer = self.get_serializer({'user': user})
#         headers = self.get_success_headers(serializer.data)
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#
# class MTokenHandler:
#
#     @staticmethod
#     def handle(request, get_serializer, rtype: str, *args, **kwargs) -> User:
#         serializer = get_serializer(data=request.data)
#
#         try:
#             serializer.is_valid(raise_exception=True)
#         except User.DoesNotExist:
#             raise UserDoesNotExistAPIException(ErrorMessage.user_does_not_exist_api_exception())
#
#         email = serializer.validated_data['email']
#
#         user: User
#         try:
#             base_url = request.build_absolute_uri('/')
#             user = UserService.create_by_email_with_request_params(email, rtype, base_url, *args, **kwargs)
#         except DomainIsNotEligibleException:
#             raise DomainIsNotEligibleAPIException(ErrorMessage.domain_is_not_eligible_api_exception())
#
#         return user
