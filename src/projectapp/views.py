import views as views
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, \
    RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from base.error_messages import ErrorMessage
from base.exceptions import UserDoesNotExistAPIException, DomainIsNotEligibleAPIException, DomainIsNotEligibleException
from projectapp import models
from projectapp.models import User, Treatment \
    , Reservation
from projectapp.serializers import UserSerializer, TreatmentSerializer, ReservationSerializer, DoctorSerializer


class UserAPIView(APIView):

    def get_user(self, pk):
        try:
            return User.objects.filter(pk=pk)
        except User.DoesNotExist:
            raise Http404

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


class TreatmentAPIView(APIView):

    def get_treatment(self, pk):
        try:
            return Treatment.objects.filter(pk=pk)
        except Treatment.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk:
            data = self.get_treatment(pk)
        else:
            data = Treatment.objects.all()
        serializer = TreatmentSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        serializer = TreatmentSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = Response()

        response.data = {
            'message': 'Treatment created successfully',
            'data': serializer.data
        }

        return response

    def put(self, request, pk=None, format=None):
        treatment_to_update = Treatment.objects.get(pk=pk)
        serializer = TreatmentSerializer(instance=treatment_to_update, data=request.data,
                                         partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = Response()

        response.data = {
            'message': 'Treatment updated successfully',
            'data': serializer.data
        }

        return response

    #
    def delete(self, request, pk, format=None):
        treatment_to_delete = Treatment.objects.get(pk=pk)

        treatment_to_delete.delete()

        return Response({
            'message': 'Treatment deleted successfully'
        })


class ReservationAPIView(APIView):

    def get_reservation(self, pk):
        try:
            return Reservation.objects.filter(pk=pk)
        except Reservation.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk:
            data = self.get_reservation(pk)
        else:
            data = Reservation.objects.all()
        serializer = ReservationSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
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

    def put(self, request, pk=None, format=None):
        reservation_to_update = Reservation.objects.get(pk=pk)
        serializer = ReservationSerializer(instance=reservation_to_update, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = Response()

        response.data = {
            'message': 'Reservation Updated Successfully',
            'data': serializer.data
        }

        return response

    def delete(self, request, pk, format=None):
        reservation_to_delete = Reservation.objects.get(pk=pk)

        reservation_to_delete.delete()

        return Response({
            'message': 'Reservation Deleted Successfully'
        })


class DoctorAPIView(APIView):

    def get(self, Usertype):
        data = User.objects.filter(user_type=3)
        serializer = DoctorSerializer(data, many=True)
        return Response(serializer.data)

