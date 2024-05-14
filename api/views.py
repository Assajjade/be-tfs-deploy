from collections import defaultdict
from datetime import timedelta, timezone
from venv import logger
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework import generics, status
from .models import User, Organizer, UserTrip, History, Blog
from .serializer import UserSerializer, OrganizerCreateSerializer, OrganizerListSerializer, CreateOrganizerSerializer, TripSerializer, TripQuestionSerializer, TripAnswerSerializer, UserTripCreateSerializer, UserTripReadSerializer, BlogReadSerializer, BlogCreateSerializer
from django.core import serializers
from .models import *
from .serializer import *
from django.urls import reverse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Trip
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os;
from django.http import Http404
from django.core.files.storage import FileSystemStorage 
from django.db.models import Count
from rest_framework.pagination import PageNumberPagination
from math import ceil
from django.db.models import Q

# Sisa Problem untuk pathing, jika iya maka semuanya udah tersolve.
# key_path = os.path.join(
#     os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
#     'privatekey',
#     'the-floating-school-firebase-adminsdk-ak5mc-35a533c35d.json'
# )

# # Initialize Firebase Admin SDK if it hasn't been already
# if not firebase_admin._apps:
#     # Load credentials from JSON file
#     cred = credentials.Certificate(key_path)
#     # Initialize the Firebase app
#     firebase_admin.initialize_app(cred)

# Sign Up for USER
class UserSignUp(generics.CreateAPIView):
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# This is for Organizer Sign Up,
# With note Organizer cannot directly signup, this is for Create Organizer
class CreateOrganizer(generics.CreateAPIView):
    serializer_class = OrganizerCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()
            return Response({'message': 'Organizer created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# This is for sign in in Main Website
# @api_view(['POST'])
# def user_signin(request):
#     email = request.data.get('email')
#     password = request.data.get('password')
#     try:
#         # Attempt to sign in with Firebase
#         user = Auth.sign_in_with_email_and_password(email, password)
#         return Response({'message': 'User signed in successfully.', 'user': user}, status=status.HTTP_200_OK)
#     except Exception as e:
#         if 'EMAIL_NOT_FOUND' in str(e):
#             return Response({'error': 'The email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
#         elif 'INVALID_PASSWORD' in str(e):
#             return Response({'error': 'Incorrect password.'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# This is for Forget Password in Main Website
# @api_view(['POST'])
# def user_forget_password(request):
#     email = request.data.get('email')
#     try:
#         # Attempt to send a password reset email
#         Auth.send_password_reset_email(email)
#         return Response({'message': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)
#     except Exception as e:
#         if 'EMAIL_NOT_FOUND' in str(e):
#             return Response({'message': 'If the email is registered, a password reset link will be sent.'}, status=status.HTTP_200_OK)
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)  
 
class UserDetailView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserView(APIView):
    serializer_class = UserSerializer

    def get_object(self, uid):
        try:
            return User.objects.get(id=uid)
        except User.DoesNotExist:
            raise get_object_or_404(User, id=uid)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid, format=None):
        user = self.get_object(uid)
        user.delete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, uid=None, format=None):
        if uid:
            user = self.get_object(uid)
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    def put(self, request, uid, format=None):
        user = self.get_object(uid)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(('GET',))
    def get_cw(self, organizer_id=None, format=None):
        users = User.objects.filter(role = "CW")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
        
    @api_view(('GET',))
    def get_io(self, organizer_id=None, format=None):
        users = User.objects.filter(role = "IO")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class OrganizerView(generics.CreateAPIView):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerCreateSerializer

class OrganizerListView(generics.ListAPIView):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerListSerializer

class OrganizerViewss(APIView):
    serializer_class = OrganizerListSerializer

    def get_object(self, organizer_id):
        try:
            organizer_id = int(organizer_id)
            return Organizer.objects.get(id=organizer_id)
        except (ValueError, Trip.DoesNotExist):
            raise get_object_or_404
        
    def get(self, request, id=None, format=None):
        if id:
            organizer = self.get_object(id)
            serializer = OrganizerListSerializer(organizer)
            return Response(serializer.data)
        organizers = Organizer.objects.all()
        serializer = OrganizerListSerializer(organizers, many=True)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        comment = self.get_object(id)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id, format=None):
        comment = self.get_object(id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    @api_view(('GET',))
    def get_cw(self, organizer_id=None, format=None):
        if organizer_id is not None:
            organizer = self.get_object(organizer_id)
            serializer = self.serializer_class(organizer, many=False)
            return Response(serializer.data)
        
        organizers = Organizer.objects.filter(role = "Content Writer")
        # organizers = Organizer.objects.all()
        serializer = OrganizerListSerializer(organizers, many=True)
        return Response(serializer.data)
    
    @api_view(('GET',))
    def get_io(self, organizer_id=None, format=None):
        if organizer_id is not None:
            organizer = self.get_object(organizer_id)
            serializer = self.serializer_class(organizer, many=False)
            return Response(serializer.data)
        
        organizers = Organizer.objects.filter(role = "Island Organizer")
        # organizers = Organizer.objects.all()
        serializer = OrganizerListSerializer(organizers, many=True)
        return Response(serializer.data)

class IslandOrganizerView(APIView):
    serializer_class = TripSerializer
    
    def get_object(self, trip_id):
        try:
            trip_id = int(trip_id)
            return Trip.objects.get(id=trip_id)
        except (ValueError, Trip.DoesNotExist):
            raise get_object_or_404

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            trip_pic_file = request.FILES.get('trip_pic')
            if trip_pic_file:
                serializer.validated_data['trip_pic'] = trip_pic_file

            trip = serializer.save()
            response_data = serializer.data
            response_data['trips_id'] = trip.id 
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, trip_id, format=None):
        try:
            trip_id = int(trip_id)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        existing_trip = self.get_object(trip_id) 
        data = request.data
        serializer = self.serializer_class(existing_trip, data=data)
        if serializer.is_valid():
            # Handle file upload for trip_pic field
            trip_pic_file = request.FILES.get('trip_pic')
            if trip_pic_file:
                # Save the uploaded file
                serializer.validated_data['trip_pic'] = trip_pic_file

            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, trip_id, format=None):
        trip = self.get_object(trip_id)
        trip.delete()
        return Response({"detail": "Trip deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    def search(self, query):
        trips = Trip.objects.filter(Q(area__icontains=query) | Q(island_name__icontains=query))
        serializer = self.serializer_class(trips, many=True)
        return serializer.data
    
    def get(self, request, trip_id=None, format=None):
        if trip_id is not None:
            trip = self.get_object(trip_id)
            serializer = self.serializer_class(trip, many=False)
            return Response(serializer.data)
        
        trips = Trip.objects.all()

        search_query = request.query_params.get('search', None)
        if search_query:
            search_result = self.search(search_query)
            return Response({'results': search_result})
        
        total_count = trips.count()
        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(trips, request)
        serializer = self.serializer_class(result_page, many=True)
        total_pages = ceil(total_count / paginator.page_size)

        return Response({
            'results': serializer.data,
            'total_pages': total_pages,
            'total_count': total_count
        })
class IslandOrganizerDetail(APIView):
    serializer_class = TripSerializer
    
    def get_object(self, trip_id):
        try:
            trip_id = int(trip_id)
            return Trip.objects.get(id=trip_id)
        except (ValueError, Trip.DoesNotExist):
            raise ValueError('Trip does not exist')

    def get(self, request, trip_id, format=None):
        try:
            trip = self.get_object(trip_id)
            serializer = self.serializer_class(trip, many=False)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

class UserDetailAPIView(APIView):
    serializer_class = UserTripReadSerializer

    def get_object(self, user_id, trip_id):
        try:
            return UserTrip.objects.get(user_id=user_id, trip_id=trip_id)
        except UserTrip.DoesNotExist:
            raise Http404("UserTrip does not exist")

    def get(self, request, trip_id, user_id, format=None):
        try:
            user_trip = self.get_object(user_id, trip_id)
            serializer = self.serializer_class(user_trip)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404 as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, trip_id, user_id):
        try:
            user_trip = self.get_object(user_id, trip_id)  
            user_trip.delete()
            return Response({'message': 'User removed from the trip'}, status=status.HTTP_200_OK)
        except UserTrip.DoesNotExist:
            return Response({'message': 'UserTrip does not exist'}, status=status.HTTP_404_NOT_FOUND)

class UpdateApplicationStatus(APIView):
    serializer_class = UserTripCreateSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # print("json valid")
            userId = serializer.data.get('user')
            tripId = serializer.data.get('trip')
            user = User.objects.get(id=userId)
            trip = Trip.objects.get(id=tripId)
            name = serializer.data.get('name')
            phoneNum = serializer.data.get('phoneNum')
            experience = serializer.data.get('experience')
            email = serializer.data.get('email')
            # app_status = serializer.data.get('application_status')
            # 'user', 'trip', 'name', 'phoneNum', 'experience', 'email', 'application_status'
            
            queryset = UserTrip.objects.filter(user = user, trip = trip)
            if not queryset.exists():
                print()
                userTrip = UserTrip(user = user ,trip = trip, name = name, phoneNum = phoneNum, experience = experience, email = email, application_status = "applied")
                userTrip.save()
                return Response({'message': 'User registered for the trip', 'data' :UserTripReadSerializer(userTrip).data}, status=status.HTTP_200_OK)
            return Response({'message': 'User already registered for this trip'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Payload not match'}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, trip_id, user_id, format=None):
        try:
            user_trip = UserTrip.objects.get(user_id=user_id, trip_id=trip_id)
            new_status = request.data.get('new_status')
            if new_status in ['confirmed', 'rejected', 'cancelled']:
                user_trip.application_status = new_status
                user_trip.save()
                return Response({'message': f'Application status updated to {new_status}'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        except UserTrip.DoesNotExist:
            return Response({'message': 'UserTrip does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, trip_id, user_id, format=None):
        try:
            trip_applications = UserTrip.objects.filter(trip_id=trip_id)
            serializer = UserTripReadSerializer(trip_applications, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, trip_id, user_id, format=None):
        try:
            user_trip = UserTrip.objects.get(user_id=user_id, trip_id=trip_id)
            user_trip.delete()
            return Response({'message': 'User removed from the trip'}, status=status.HTTP_200_OK)
        except UserTrip.DoesNotExist:
            return Response({'message': 'UserTrip does not exist'}, status=status.HTTP_404_NOT_FOUND)
   
class TripQuestionAPIView(APIView):
    serializer_class = TripQuestionSerializer
    
    def get_object(self, trip_id):
        return get_object_or_404(TripQuestion, trip_id=trip_id)

    def post(self, request, trip_id, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(trip_id=trip_id)
            #             serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, trip_id, format=None):
        questions = TripQuestion.objects.filter(trip_id=trip_id)
        serializer = self.serializer_class(questions, many=True)
        return Response(serializer.data)


class TripAnswerAPIView(APIView):
    serializer_class = TripAnswerSerializer
    
    def get_trip_question(self, trip_id):
        return get_object_or_404(TripQuestion, trip_id=trip_id)

    def get_user(self, user_id):
        return get_object_or_404(User, id=user_id)

    def get(self, request, trip_id, user_id, format=None):
        trip_question = self.get_trip_question(trip_id)
        user = self.get_user(user_id)

        try:
            trip_answer = TripAnswer.objects.get(question=trip_question, user=user)
            serializer = self.serializer_class(trip_answer)
            return Response(serializer.data)
        except TripAnswer.DoesNotExist:
            return Response({'message': 'Trip answer not found for the given user and trip'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, trip_id, user_id, format=None):
        user = self.get_user(user_id)
        trip_question = self.get_trip_question(trip_id)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(question=trip_question, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ListParticipants(APIView):
    def get(self, request, trip_id=None, format=None):
        if trip_id is not None:
            participants = UserTrip.objects.filter(trip_id=trip_id)
            serializer = UserTripReadSerializer(participants, many=True)
            return Response(serializer.data)
        
        participants = Trip.objects.all()
        total_count = participants.count()

        paginator = PageNumberPagination()
        paginator.page_size = 5 
        result_page = paginator.paginate_queryset(participants, request)
        serializer = self.serializer_class(result_page, many=True)

        total_pages = ceil(total_count / paginator.page_size)

        return Response({
            'results': serializer.data,
            'total_pages': total_pages,  
            'total_count': total_count  
        })
    
    

class UserTripRegistration(APIView):
    serializer_class = UserTripCreateSerializer

    def post(self, request, trip_id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('user', None)
            name = serializer.validated_data.get('name')
            phoneNum = serializer.validated_data.get('phoneNum')
            experience = serializer.validated_data.get('experience')
            email = serializer.validated_data.get('email')

            try:
                trip = Trip.objects.get(pk=trip_id)
            except Trip.DoesNotExist:
                return Response({'message': 'Trip does not exist'}, status=status.HTTP_404_NOT_FOUND)

            if user_id is not None:
                user = get_object_or_404(User, id=user_id.id)
                user_trip, created = UserTrip.objects.get_or_create(
                    user=user,
                    trip=trip,
                    defaults={'name': name, 'phoneNum': phoneNum, 'experience': experience, 'email': email, 'application_status': 'applied'}
                )
            else:
                user_trip, created = UserTrip.objects.get_or_create(
                    user=None,
                    trip=trip,
                    defaults={'name': name, 'phoneNum': phoneNum, 'experience': experience, 'email': email, 'application_status': 'applied'}
                )

            if created:
                return Response({'message': 'User registered for the trip'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'User already registered for this trip'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, trip_id):
        user_trips = UserTrip.objects.filter(trip_id=trip_id)
        serializer = UserTripReadSerializer(user_trips, many=True)
        return Response(serializer.data)
    
class BlogListAPI(APIView):
    def get(self, request):  # This method handles requests without the 'language' parameter
        blogs = Blog.objects.all()
        serializer = BlogReadSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request, language):  # This method handles requests with the 'language' parameter
        blogs = Blog.objects.filter(languange=language)
        serializer = BlogReadSerializer(blogs, many=True)
        return Response(serializer.data)
    
class BlogAPI(APIView):
    read_serializer = BlogReadSerializer
    create_serializer = BlogCreateSerializer

    def get_object(self, blog_id):
        try:
            return Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            raise Http404("Blog does not exist")

    def get(self, request, blog_id, format=None):
        try:
            blog = self.get_object(blog_id)
            serializer = self.read_serializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404 as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = self.create_serializer(data=request.data)
        # ('title', 'content', 'author', 'is_deleted', 'highlighted')
        if serializer.is_valid():
            blog = serializer.save()
            response_data = serializer.data
            response_data['id'] = blog.id 
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, blog_id, format=None):
        try:
            blog = int(blog_id)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        existing_blog = get_object_or_404(Blog, id=blog)
        data = JSONParser().parse(request)
        print(data)

        serializer = self.create_serializer(existing_blog, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, blog_id, format=None):
        blog = self.get_object(blog_id)
        blog.delete()
        return Response({"detail": "Trip deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    @api_view(('GET',))
    def get_blogs_by_languange(self, request):
        blogs = Blog.objects.filter(languange="en")
        print(blogs)
        serializer = BlogReadSerializer(blogs)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FundApiViews(APIView):
    serializer_class = FundSerializer

    def get(self, request, fund_id=None):
        if fund_id is not None:
            try:
                fund = Fund.objects.get(pk=fund_id)
                serializer = FundSerializer(fund)
                return Response(serializer.data)
            except Fund.DoesNotExist:
                return Response({'error': 'Fund does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            funds = Fund.objects.all()
            serializer = FundSerializer(funds, many=True)
            return Response(serializer.data)
        
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, fund_id, format=None):
        try:
            fund = Fund.objects.get(pk=fund_id)
        except Fund.DoesNotExist:
            return Response({'error': 'Fund does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(fund, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, fund_id, format=None):
        try:
            fund = Fund.objects.get(pk=fund_id)
            fund.delete()
            return Response({'message': 'Fund deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Fund.DoesNotExist:
            raise Http404('Fund does not exist')

class FundLandingPageView(APIView):
    serializer_class = FundLandingPageSerializer

    def get(self, request):
        try:
            fund_landing_page = FundLandingPage.objects.first()
            serializer = self.serializer_class(fund_landing_page)
            return Response(serializer.data)
        except FundLandingPage.DoesNotExist:
            return Response({'error': 'FundLandingPage does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            existing_instance = FundLandingPage.objects.first()
            if existing_instance:
                serializer = self.serializer_class(existing_instance, data=request.data)
            else:
                serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                bg_landing = request.FILES.get('bg_landing')
                if bg_landing:
                    fs = FileSystemStorage(location='imagesdata/')
                    filename = fs.save(bg_landing.name, bg_landing)
                    serializer.validated_data['bg_landing'] = filename

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            fund_landing_page = FundLandingPage.objects.first()
            fund_landing_page.delete()
            return Response({'message': 'FundLandingPage deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except FundLandingPage.DoesNotExist:
            return Response({'error': 'FundLandingPage does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
class FundWritingView(APIView):
    serializer_class = FundWritingSerializer

    def get(self, request):
        fund_writings = FundWriting.objects.all()
        serializer = self.serializer_class(fund_writings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

    def put(self, request, pk):
        try:
            fund_writing = FundWriting.objects.get(pk=pk)
        except FundWriting.DoesNotExist:
            return Response({'error': 'FundWriting does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            fund_writing = FundWriting.objects.get(pk=pk)
            fund_writing.delete()
            return Response({'message': 'FundWriting deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except FundWriting.DoesNotExist:
            raise Http404('Fund Writing does not exist')

class MerchandiseView(APIView):
    serializer_class = MerchandiseSerializer

    def get_object(self, id):
        try:
            return Merchandise.objects.get(id=id)
        except Merchandise.DoesNotExist:
            raise Http404

    def get(self, request, id=None, format=None):
        if id:
            merchandise = self.get_object(id)
            serializer = MerchandiseSerializer(merchandise)
            return Response(serializer.data)
        merchandise = Merchandise.objects.all()
        serializer = MerchandiseSerializer(merchandise, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MerchandiseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, id, format=None):
        merchandise = self.get_object(id)
        serializer = MerchandiseSerializer(merchandise, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        merchandise = self.get_object(id)
        merchandise.is_deleted = True
        merchandise.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MerchandiseSectionView(APIView):
    serializer_class = MerchandiseSectionSerializer

    def get_object(self, id):
        try:
            return MerchandiseSection.objects.get(id=id)
        except MerchandiseSection.DoesNotExist:
            raise Http404

    def get(self, request, id=None, format=None):
        if id:
            merchandise_section = self.get_object(id)
            serializer = MerchandiseSectionSerializer(merchandise_section)
            return Response(serializer.data)
        merchandise_section = MerchandiseSection.objects.all()
        serializer = MerchandiseSectionSerializer(merchandise_section, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MerchandiseSectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):
        merchandise_section = self.get_object(id)
        serializer = MerchandiseSectionSerializer(merchandise_section, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        merchandise_section = self.get_object(id)
        merchandise_section.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentView(APIView):
    serializer_class = CommentSerializer
    def get_object(self, id):
        try:
            return Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, id=None, format=None):
        if id:
            comment = self.get_object(id)
            serializer = CommentGetSerializer(comment)
            return Response(serializer.data)
        comment = Comment.objects.all()
        serializer = CommentGetSerializer(comment, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id, format=None):
        comment = self.get_object(id)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id, format=None):
        comment = self.get_object(id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # @api_view(['GET'])
    @api_view(('GET',))
    def get_comments_by_blog_id(self, blog_id):
        comments = Comment.objects.filter(blog_id=blog_id)
        serializer = CommentGetSerializer(comments, many=True)
        return Response(serializer.data)
    
class CommentReportView(APIView):
    serializer_class = CommentReportSerializer

    def get_object(self, id):
        try:
            return CommentReport.objects.get(id=id)
        except CommentReport.DoesNotExist:
            raise Http404

    def get(self, request, id=None, format=None):
        if id:
            comment = self.get_object(id)
            serializer = CommentReportGetSerializer(comment)
            return Response(serializer.data)
        comment = CommentReport.objects.all()
        serializer = CommentReportGetSerializer(comment, many=True)
        return Response(serializer.data)

    # def get(self, request):
    #     comment_reports = CommentReport.objects.all()
    #     serializer = CommentReportSerializer(comment_reports, many=True)
    #     return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommentReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id, format=None):
        comment = self.get_object(id)
        serializer = CommentReportSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id, format=None):
        comment = self.get_object(id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# PBI-13 S2, VIEWALL List Registered Volunteers
class ListRegisteredVolunteers(APIView):
    def get(self, request):
        volunteers = User.objects.filter(verified=True)
        serializer = UserSerializer(volunteers, many=True)
        return Response(serializer.data)

class UserProfile(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class VolunteerHistoryView(APIView):
    def get(self, request, uid):
        logger.debug(f"Fetching history for UID: {uid}")
        histories = History.objects.filter(user__uid=uid)
        if not histories.exists():
            logger.info("No history found for this volunteer.")
            return Response({'message': 'No history found for this volunteer.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = HistorySerializer(histories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# PBI-13 S2, Filters Volunteers by Status
class FilterVolunteersByStatus(APIView):
    def get(self, request, status):
        user_trips = UserTrip.objects.filter(application_status=status)
        user_ids = user_trips.values_list('user', flat=True).distinct()
        volunteers = User.objects.filter(id__in=user_ids)
        serializer = UserSerializer(volunteers, many=True)
        return Response(serializer.data)

# PBI-13 S2, VIEW Organizers Contact Information. (dipikirin nanti)
class ViewOrganizerContact(APIView):
    def get(self, request, organizer_id):
        organizer = get_object_or_404(Organizer, pk=organizer_id)
        serializer = OrganizerSerializer(organizer)
        return Response(serializer.data)
    
class TotalApplicationStatusView(APIView):
    def get(self, request):
        application_status = self.count_total_application_status()
        return Response(application_status)

    def count_total_application_status(self):
        applied_count = UserTrip.objects.filter(application_status='applied').count()
        confirmed_count = UserTrip.objects.filter(application_status='confirmed').count()
        rejected_count = UserTrip.objects.filter(application_status='rejected').count()
        canceled_count = UserTrip.objects.filter(application_status='canceled').count()
        
        return {
            'applied': applied_count,
            'confirmed': confirmed_count,
            'rejected': rejected_count,
            'canceled': canceled_count,
        }
        
class TotalTripsByIslandView(APIView):
    def get(self, request):
        trips_by_island = self.count_total_trips_by_island()
        return Response(trips_by_island)

    def count_total_trips_by_island(self):
        trips_by_island = (
            Trip.objects.values('island_name')
            .annotate(total_trips=Count('id'))
            .order_by('island_name')
        )
        return trips_by_island   

class TotalParticipantsView(APIView):
    def get(self, request):
        total_participants = self.count_total_participants()
        return Response({'total_participants': total_participants})

    def count_total_participants(self):
        total_participants = 0
        trips = Trip.objects.all()
        for trip in trips:
            participants_count = UserTrip.objects.filter(trip_id=trip.id).count()
            total_participants += participants_count
        return total_participants

class TotalUserNationalitiesView(APIView):
    def get(self, request):
        user_nationalities = self.count_total_user_nationalities()
        return Response(user_nationalities)

    def count_total_user_nationalities(self):
        user_nationalities = (
            UserTrip.objects.values('user__nationality')
            .annotate(total_users=Count('user_id', distinct=True))
            .order_by('user__nationality')
        )
        return user_nationalities  

class CountParticipants(APIView):
    def get(self, request, trip_id):
        participant_count = UserTrip.objects.filter(trip_id=trip_id).count()
        return Response({'participant_count': participant_count})

    
class TotalApplicationStatusTripView(APIView):
    def get(self, request, trip_id):
        application_status = self.count_total_application_status(trip_id)
        return Response(application_status, status=status.HTTP_200_OK)

    def count_total_application_status(self, trip_id):
        applied_count = UserTrip.objects.filter(trip_id=trip_id, application_status='applied').count()
        confirmed_count = UserTrip.objects.filter(trip_id=trip_id, application_status='confirmed').count()
        rejected_count = UserTrip.objects.filter(trip_id=trip_id, application_status='rejected').count()
        canceled_count = UserTrip.objects.filter(trip_id=trip_id, application_status='canceled').count()
        
        return {
            'applied': applied_count,
            'confirmed': confirmed_count,
            'rejected': rejected_count,
            'canceled': canceled_count,
        }
        
class TotalUserNationalitiesTripView(APIView):
    def get(self, request,trip_id):
        user_nationalities = self.count_total_users(trip_id)
        return Response(user_nationalities)

    def count_total_users(self, trip_id):
        total_users = UserTrip.objects.filter(trip_id=trip_id).values('user__nationality').annotate(total_users=Count('user_id', distinct=True)).order_by('user__nationality')
        return total_users
    
class TotalCommentBlogView(APIView):
    def get(self, request, blog_id):
        total_comments = self.count_total_comment(blog_id)
        return Response(total_comments)

    def count_total_comment(self, blog_id):
        total_comments = Comment.objects.filter(blog_id=blog_id).count()
        return total_comments

class TotalCommentReportsView(APIView):
    def get(self, request, blog_id):
        total_reports = self.count_total_comment_reports(blog_id)
        return Response(total_reports)

    def count_total_comment_reports(self, blog_id):
        total_reports = CommentReport.objects.filter(comment__blog_id=blog_id).count()
        return total_reports
    
class BlogCountView(APIView):
    def get(self, request, format=None):
        today = timezone.now().date()

        start_date_daily = today
        start_date_weekly = today - timedelta(days=7)  
        start_date_monthly = today - timedelta(days=30) 
        entire_date = today - timedelta(days=30000)
        daily_count = self.get_blog_count(start_date_daily, today)
        weekly_count = self.get_blog_count(start_date_weekly, today)
        monthly_count = self.get_blog_count(start_date_monthly, today)
        entire_count = self.get_blog_count(entire_date,today)

        return Response({
            'daily_count': daily_count,
            'weekly_count': weekly_count,
            'monthly_count': monthly_count,
            'entire_count' :entire_count,
        })

    def get_blog_count(self, start_date, end_date):
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        blog_count = Blog.objects.filter(created_at__date__range=(start_date, end_date)).count()
        return blog_count
    
class TotalUserCountView(APIView):
    def get(self, request):
        total_users = User.objects.count()
        return Response({'total_users': total_users})

class TotalNationalitiesUserView(APIView):
    def get(self, request):
        user_nationalities = self.count_total_user_nationalities()
        return Response(user_nationalities)

    def count_total_user_nationalities(self):
        user_nationalities = (
            User.objects.values('nationality')
            .annotate(total_users=Count('id'))
            .order_by('nationality')
        )
        return user_nationalities

class TotalDomicileUserView(APIView):
    def get(self, request):
        user_domicile = self.count_total_user_domicile()
        return Response(user_domicile)

    def count_total_user_domicile(self):
        user_domicile = (
            User.objects.values('domicile')
            .annotate(total_users=Count('id'))
            .order_by('domicile')
        )
        return user_domicile

class TotalTripView(APIView):
    def get(self, request):
        trip_count = self.count_trip()
        return Response(trip_count)

    def count_trip(self):
        trip_count = Trip.objects.count()
        return trip_count

class AboutUsView(APIView):
    def get(self, request):
        try:
            about_us = AboutUs.objects.latest('created_at')
            serializer = AboutUsReadSerializer(about_us)
            return Response(serializer.data)
        except AboutUs.DoesNotExist:
            return Response({'error': 'No About Us Content exist'}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, format=None):
        try:
            serializer = AboutUsReadSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, id, format=None):  
        try:
            about_us = AboutUs.objects.get(pk=id)  
            serializer = AboutUsReadSerializer(about_us, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AboutUs.DoesNotExist:
            return Response({'error': 'Specified About Us content does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id, format=None):
        try:
            about_us = AboutUs.objects.get(pk=id)
            about_us.delete()
            return Response({'message': 'About Us content deleted successfully'}, status=status.HTTP_202_ACCEPTED)
        except AboutUs.DoesNotExist:
            return Response({'error': 'Specified About Us content does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
class TotalCrowdfundingView(APIView):
    def get(self, request):
        crowdFunding_count = self.count_cf()
        return Response(crowdFunding_count)

    def count_cf(self):
        crowdFunding_count =Fund.objects.count()
        return crowdFunding_count
    
class TotalMerchandiseView(APIView):
    def get(self, request):
        merchandiseCount = self.count_md()
        return Response(merchandiseCount)

    def count_md(self):
        md_count = Merchandise.objects.count()
        return md_count

class UserCreatedDateView(APIView):
    def get(self, request):
        users_with_count = User.objects.annotate(
            year=ExtractYear('created_at'),
            month=ExtractMonth('created_at'),
            day=ExtractDay('created_at'),
        ).values('year', 'month', 'day').annotate(
            total_users=Count('id')
        ).order_by('year', 'month', 'day')

        for user in users_with_count:
            user_date = datetime(user['year'], user['month'], user['day'])
            user['date'] = user_date.strftime("%d %B %Y")
            del user['year']
            del user['month']
            del user['day']

        return Response(users_with_count)

class HomePageSectionListCreateView(generics.ListCreateAPIView):
    queryset = HomePageSection.objects.all()
    serializer_class = HomePageSectionSerializer

class HomePageSectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HomePageSection.objects.all()
    serializer_class = HomePageSectionSerializer

    def delete(self, request, *args, **kwargs):
        section = self.get_object()
        if HomePageSection.objects.count() <= 1:
            return Response({'error': 'At least one section must remain.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().delete(request, *args, **kwargs)

class HomePageSections(APIView):
    def get(self, request):
        published = request.query_params.get('published')
        if published:
            sections = HomePageSection.objects.filter(is_published=True)
        else:
            sections = HomePageSection.objects.all()
        serializer = HomePageSectionSerializer(sections, many=True)
        return Response(serializer.data)
    
class TripQuestionAnswerListAPIView(APIView):
    def get_trip_questions_answers(self, trip_id):
        trip_questions = TripQuestion.objects.filter(trip_id=trip_id)
        trip_question_answers = []

        for question in trip_questions:
            try:
                answer = TripAnswer.objects.get(question=question)
                trip_question_answers.append({'question': TripQuestionSerializer(question).data, 'answer': TripAnswerSerializer(answer).data})
            except TripAnswer.DoesNotExist:
                trip_question_answers.append({'question': TripQuestionSerializer(question).data, 'answer': None})

        return trip_question_answers

    def get(self, request, trip_id, format=None):
        trip_question_answers = self.get_trip_questions_answers(trip_id)
        return Response(trip_question_answers)
    
class IslandSearchView(APIView):
    serializer_class = TripSerializer

    def get(self, request):
        search_query = request.query_params.get('q', None)
        if search_query:
            trips = Trip.objects.filter(area__icontains=search_query) | Trip.objects.filter(island_name__icontains=search_query)
            serializer = self.serializer_class(trips, many=True)
            return Response(serializer.data)
        else:
            return Response("No search query provided", status=status.HTTP_400_BAD_REQUEST)
# class UpdateApplicationStatus(APIView):

#     def send_email(subject, recipient_email, content):
#     message = Mail(
#         from_email='from_your_email@example.com',
#         to_emails=recipient_email,
#         subject=subject,
#         html_content=content
#     )
#     try:
#         sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
#         response = sg.send(message)
#         print(response.status_code)
#         print(response.body)
#         print(response.headers)
#     except Exception as e:
#         print(e.message)

#     def put(self, request, trip_id, user_id, format=None):
#         user_trip = UserTrip.objects.get(user_id=user_id, trip_id=trip_id)
#         new_status = request.data.get('new_status')
#         if new_status in ['confirmed', 'rejected', 'cancelled'] and user_trip.application_status != new_status:
#             user_trip.application_status = new_status
#             user_trip.save()
#             send_email(
#                 subject="Application Status Updated",
#                 recipient_email=user_trip.user.email,
#                 content=f"Your application status has been updated to {new_status}."
#             )
#             return Response({'message': f'Application status updated to {new_status}'}, status=200)
#         return Response({'message': 'Invalid status or no change required'}, status=400)