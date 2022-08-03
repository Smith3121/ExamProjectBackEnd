from Tools.scripts.make_ctype import values
from django.db.models import DateTimeField
from django.http import Http404
from django.utils.functional import SimpleLazyObject
from rest_framework.response import Response
from rest_framework.views import APIView

from projectapp.models import User, Treatment \
    , Reservation, Date, Hour
from projectapp.serializers import UserSerializer, TreatmentSerializer, ReservationSerializer, DoctorSerializer, \
    DateSerializer, HourSerializer


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


class RemoveDocDescrAPIView(APIView):

    def put(self, request, pk=None, format=None):
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


class ListUserResAPIView(APIView):
    def get(self, request, pk=None, format=None):
        data = Reservation.objects.filter(user=pk)
        serializer = ReservationSerializer(data, many=True)
        return Response(serializer.data)


class DocPatResAPIView(APIView):
    def get(self, request, pk=None, format=None):
        data = Reservation.objects.filter(doctor=pk).order_by()
        serializer = ReservationSerializer(data, many=True)
        return Response(serializer.data)


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

    def get(self, usertype):
        data = User.objects.filter(user_type=3)
        serializer = DoctorSerializer(data, many=True)
        return Response(serializer.data)


class DateAPIView(APIView):

    def get_date(self, pk):
        try:
            return Date.objects.filter(pk=pk)
        except Date.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk:
            data = self.get_date(pk)
        else:
            data = Date.objects.all()
        serializer = DateSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        serializer = DateSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = Response()

        response.data = {
            'message': 'Date Created Successfully',
            'data': serializer.data
        }
        return response

    def put(self, request, pk=None, format=None):
        date_to_update = Date.objects.get(pk=pk)
        serializer = DateSerializer(instance=date_to_update, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = Response()

        response.data = {
            'message': 'Date Updated Successfully',
            'data': serializer.data
        }

        return response

    def delete(self, request, pk, format=None):
        date_to_delete = Date.objects.get(pk=pk)

        date_to_delete.delete()

        return Response({
            'message': 'Date Deleted Successfully'
        })


class HourAPIView(APIView):

    def get_hour(self, pk):
        try:
            return Hour.objects.filter(pk=pk)
        except Hour.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk:
            data = self.get_hour(pk)
        else:
            data = Hour.objects.all()
        serializer = HourSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        serializer = HourSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = Response()

        response.data = {
            'message': 'Hour Created Successfully',
            'data': serializer.data
        }
        return response

    def put(self, request, pk=None, format=None):
        hour_to_update = Hour.objects.get(pk=pk)
        serializer = HourSerializer(instance=hour_to_update, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = Response()

        response.data = {
            'message': 'Hour Updated Successfully',
            'data': serializer.data
        }

        return response

    def delete(self, request, pk, format=None):
        hour_to_delete = Hour.objects.get(pk=pk)

        hour_to_delete.delete()

        return Response({
            'message': 'Hour Deleted Successfully'
        })

# class DoctorsOfTheTreatmentAPIView(APIView):
#     data = User.objects.filter(user_type=3)
#
