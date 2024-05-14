from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'email', 'phone_numbers', 'nationality', 'domicile',  'role', 'verified')

    def create(self, validated_data):
        # Assuming all fields are optional except username and email
        user = User.objects.create(
            id=validated_data['id'],
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data.get('name', ''),  # Use .get for optional fields with defaults
            phone_numbers=validated_data.get('phone_numbers', ''),
            nationality=validated_data.get('nationality', ''),
            domicile=validated_data.get('domicile', ''),
            role=validated_data.get('role', ''),
            verified=validated_data.get('verified', False)
        )
        user.save()
        return user


class OrganizerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ('id', 'name', 'username', 'password', 'email', 'phone_numbers', 
                  'nationality', 'domicile', 'role', 'created_at')
        
class OrganizerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ('id', 'name', 'username', 'email', 'phone_numbers', 
                  'nationality', 'domicile', 'role', 'created_at')
        
class CreateOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ('name', 'username', 'password', 'email', 'phone_numbers', 
                  'nationality', 'domicile', 'role')
        
class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'
        
class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'


class TripQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripQuestion
        fields = ['id', 'trip', 'question_text']

class TripAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripAnswer
        fields = ['id', 'user', 'question', 'answer_text']

class HistorySerializer(serializers.ModelSerializer):
    application_status = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = ('id', 'user', 'trip', 'application_status')

    def get_application_status(self, obj):
        status_mapping = {
            'applied': 0,
            'confirmed': 1,
            'rejected': 2,
            'cancelled': 3
        }
        return status_mapping[obj.application_status]
    
class VolunteerMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerMetrics
        fields = ['id', 'trip', 'application_rate', 'completion_rate', 'feedback_score']

class UserTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTrip
        fields = ('user', 'trip', 'application_status')
        
class UserTripCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTrip
        fields = ('user', 'trip', 'name', 'phoneNum', 'experience', 'email')
        extra_kwargs = {'user': {'required': False}}
        
class UserTripReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTrip
        fields = ('id','user', 'trip', 'name', 'phoneNum', 'experience', 'email', 'application_status')

class BlogReadSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Blog
        fields = '__all__'

class BlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'author', 'is_deleted', 'highlighted', 'post_date', 'languange')

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        
class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = '__all__'

class FundLandingPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundLandingPage
        fields = '__all__'

class FundWritingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundWriting
class MerchandiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchandise
        fields = '__all__'

class MerchandiseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchandiseSection
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = Comment
        fields = '__all__'

class CommentGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = '__all__'

class CommentReportSerializer(serializers.ModelSerializer):
    # comment = CommentSerializer()
    class Meta:
        model = CommentReport
        fields = '__all__'

class CommentReportGetSerializer(serializers.ModelSerializer):
    comment = CommentGetSerializer()
    class Meta:
        model = CommentReport
        fields = '__all__'

class HomePageSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageSection
        fields = '__all__'
class CommentReportGetSerializer(serializers.ModelSerializer):
    comment = CommentGetSerializer()
    class Meta:
        model = CommentReport
        fields = '__all__'
        
class AboutUsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        exclude = ['id']
        
class AboutUsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'
        

