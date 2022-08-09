from Tools.scripts.make_ctype import values
from django.db.models import DateTimeField
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.functional import SimpleLazyObject
from rest_framework import viewsets, status
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
from projectapp.serializers import UserSerializer, TreatmentSerializer, ReservationSerializer, DoctorSerializer,  TokenRequestSerializer, TokenResponseSerializer, MTokenRequestSerializer, MTokenResponseSerializer
from projectapp.services.token_service import TokenService, MTokenService
from projectapp.services.user_service import UserService


class UserViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                  viewsets.GenericViewSet, ViewSet):
    queryset = User.objects.all()

    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def list(self, request, pk=None, format=None):
        user = self.request.user
        data = User.objects.all()
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data)

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class RemoveDocDescrViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
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


class ListUserResViewSet(RetrieveModelMixin, ListModelMixin, viewsets.GenericViewSet):
    def list(self, request, pk=None, format=None):
        data = Reservation.objects.filter(user=pk)
        serializer = ReservationSerializer(data, many=True)
        return Response(serializer.data)


class DocPatResViewSet(RetrieveModelMixin, ListModelMixin, viewsets.GenericViewSet):
    def list(self, request, pk=None, format=None, name=str):
        data = Reservation.objects.filter(doctor=pk, username=name)
        serializer = ReservationSerializer(data, many=True)
        return Response(serializer.data)


class DocListResByDateViewSet(RetrieveModelMixin, ListModelMixin, viewsets.GenericViewSet):
    def list(self, request, pk=None, format=None):
        data = Reservation.objects.filter(doctor=pk).order_by('date')
        serializer = ReservationSerializer(data, many=True)
        return Response(serializer.data)


class TreatmentViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer

    # def get_treatment(self, pk):
    #     try:
    #         return Treatment.objects.filter(pk=pk)
    #     except Treatment.DoesNotExist:
    #         raise Http404

    # def list(self, request, pk=None, format=None):
    #     if pk:
    #         data = self.get_treatment(pk)
    #     else:
    #         data = Treatment.objects.all()
    #     serializer = TreatmentSerializer(data, many=True)
    #     return Response(serializer.data)
    def retrieve(self, request, pk=None):
        treatment = get_object_or_404(self.queryset, pk=pk)
        serializer = TreatmentSerializer(treatment)
        return Response(serializer.data)

    def list(self, request, pk=None, format=None):
        # treatment = self.request.treatment
        data = Treatment.objects.all()
        serializer = TreatmentSerializer(data, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = TreatmentSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = Response()

        response.data = {
            'message': 'Treatement Created Successfully',
            'data': serializer.data
        }

        return response

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class ReservationViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                         viewsets.GenericViewSet):
    # def get_reservation(self, pk):
    #     try:
    #         return Reservation.objects.filter(pk=pk)
    #     except Reservation.DoesNotExist:
    #         raise Http404
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def retrieve(self, request, pk=None):
        reservation = get_object_or_404(self.queryset, pk=pk)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    def list(self, request, pk=None, format=None):
        data = Reservation.objects.all()
        serializer = ReservationSerializer(data, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = ReservationSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = Response()

        response.data = {
            'message': 'Reservation Created Successfully',
            'data': serializer.data
        }

        return response

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class DoctorViewSet(RetrieveModelMixin, ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = User.objects.all()

    serializer_class = DoctorSerializer

    def list(self, request, *args, **kwargs):
        data = User.objects.filter(user_type=3)
        serializer = DoctorSerializer(data, many=True)
        return Response(serializer.data)


# class DateViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
#                   viewsets.GenericViewSet):
#     queryset = Dates.objects.all()
#
#     def retrieve(self, request, pk=None):
#         date = get_object_or_404(self.queryset, pk=pk)
#         serializer = DateSerializer(date)
#         return Response(serializer.data)
#
#     def list(self, request, pk=None, format=None):
#         data = Dates.objects.all()
#         serializer = DateSerializer(data, many=True)
#         return Response(serializer.data)
#
#     def create(self, request, *args, **kwargs):
#         data = request.data
#         serializer = DateSerializer(data=data)
#
#         serializer.is_valid(raise_exception=True)
#
#         serializer.save()
#
#         response = Response()
#
#         response.data = {
#             'message': 'Date Created Successfully',
#             'data': serializer.data
#         }
#
#         return response
#
#     def partial_update(self, request, pk=None, format=None):
#         date_to_update = Dates.objects.get(pk=pk)
#         serializer = DateSerializer(instance=date_to_update, data=request.data, partial=True)
#
#         serializer.is_valid(raise_exception=True)
#
#         serializer.save()
#
#         response = Response()
#
#         response.data = {
#             'message': 'Date Updated Successfully',
#             'data': serializer.data
#         }
#
#         return response
#
#     def perform_destroy(self, instance):
#         date_to_delete = Dates.objects.get(pk=instance)
#
#         date_to_delete.delete()
#
#         return Response({
#             'message': 'Date Deleted Successfully'
#         })


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
