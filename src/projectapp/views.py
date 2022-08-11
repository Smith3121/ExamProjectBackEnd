from Tools.scripts.make_ctype import values
from django.db.models import DateTimeField, Avg
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.functional import SimpleLazyObject
from rest_framework import viewsets, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from datetime import datetime

from rest_framework.viewsets import ViewSet

from base.error_messages import ErrorMessage
from base.exceptions import UserDoesNotExistAPIException, DomainIsNotEligibleException, DomainIsNotEligibleAPIException
from projectapp.models import User, Treatment \
    , Reservation
# , Dates
from projectapp.serializers import UserSerializer, TreatmentSerializer, ReservationSerializer, DoctorSerializer, \
    TokenRequestSerializer, TokenResponseSerializer, MTokenRequestSerializer, MTokenResponseSerializer
from projectapp.services.token_service import TokenService, MTokenService
from projectapp.services.user_service import UserService


class UserViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                  viewsets.GenericViewSet, ViewSet):
    queryset = User.objects.all()

    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        user = MTokenHandler.handle(request, self.get_serializer, 'r', *args, **kwargs)

        serializer = self.get_serializer(user)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class RemoveDoctorDescriptionViewSet(UpdateModelMixin,
                                     viewsets.GenericViewSet):

    def update(self, request, pk=None, format=None):
        user_to_update = User.objects.get(pk=pk)
        serializer = UserSerializer(instance=user_to_update, data={'presentation': ""}, partial=True)
        if serializer.is_valid():
            serializer.save()

        response = Response()

        response.data = {
            'message': 'User Updated Successfully',
            'data': serializer.data
        }
        return response


class ListUserReservationViewSet(RetrieveModelMixin, ListModelMixin, viewsets.GenericViewSet):
    def list(self, request, pk=None, format=None):
        data = Reservation.objects.filter(user=pk)
        serializer = ReservationSerializer(data, many=True)
        return Response(serializer.data)


class ListDoctorReservationByNameViewSet(RetrieveModelMixin, ListModelMixin, viewsets.GenericViewSet):
    def list(self, request, pk=None, format=None):
        data = Reservation.objects.filter(doctor=pk)
        serializer = ReservationSerializer(data, many=True)
        return Response(serializer.data)


class ListDoctorReservationByDate(RetrieveModelMixin, ListModelMixin, viewsets.GenericViewSet):
    def list(self, request, pk=None, format=None):
        data = Reservation.objects.filter(doctor=pk).order_by('date')
        serializer = ReservationSerializer(data, many=True)
        return Response(serializer.data)


class TreatmentViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                       viewsets.GenericViewSet):

    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


# class TreatmentAPIView(ListCreateAPIView):
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class ReservationViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                         viewsets.GenericViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DoctorViewSet(RetrieveModelMixin, ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = User.objects.all()

    serializer_class = DoctorSerializer

    def list(self, request, *args, **kwargs):
        data = User.objects.filter(user_type=3)
        serializer = DoctorSerializer(data, many=True)
        return Response(serializer.data)


class TokenViewSet(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = TokenRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email', None)
        mtoken = serializer.validated_data['mtoken']

        if email is None:
            user_id = serializer.validated_data['user_id']
            email = UserService.get_by_id(user_id).email

        token = TokenService.create_by_email_and_mtoken_with_request_params(email, mtoken, *args, **kwargs)
        user = UserService.get_by_email(email)

        # Invalidate used magic token
        MTokenService.deactivate_by_key(mtoken)

        self.serializer_class = TokenResponseSerializer
        serializer = self.get_serializer({'user': user, 'token': token})
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MTokenViewSet(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = MTokenRequestSerializer

    def create(self, request, *args, **kwargs):
        print("Anything")
        user = MTokenHandler.handle(request, self.get_serializer, 'l', *args, **kwargs)

        self.serializer_class = MTokenResponseSerializer
        serializer = self.get_serializer({'user': user})
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MTokenHandler:

    @staticmethod
    def handle(request, get_serializer, rtype: str, *args, **kwargs) -> User:
        serializer = get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except User.DoesNotExist:
            raise UserDoesNotExistAPIException(ErrorMessage.user_does_not_exist_api_exception())

        email = serializer.validated_data['email']

        user: User
        try:
            base_url = request.build_absolute_uri('/')
            user = UserService.create_by_email_with_request_params(email, rtype, base_url, *args, **kwargs)
        except DomainIsNotEligibleException:
            raise DomainIsNotEligibleAPIException(ErrorMessage.domain_is_not_eligible_api_exception())

        return user
