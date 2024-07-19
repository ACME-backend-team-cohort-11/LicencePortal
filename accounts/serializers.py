from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from application.models import LicenseApplication
from licence.models import License

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'confirm_password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        user = authenticate(**credentials)

        if user is None or not user.is_active:
            raise serializers.ValidationError(
                'No active account found with the given credentials'
            )

        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        application = LicenseApplication.objects.filter(applicant=user).first()
        if application:
            data['user'] = {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': application.first_name,
                'last_name': application.last_name,
                'nin': application.nin,
                'phone_no': application.phone_number,
                'sex': application.gender,
            }
        else:
            data['user'] = {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': '',
                'last_name': '',
                'nin': '',
                'sex': '',
            }

        try:
            license = License.objects.get(IdNo=application.nin)
            data['license'] = {
                'licenseId': license.licenseId,
                'license_class': application.vehicle_type,
                'country_of_issue': license.country_of_issue,
                'issue_date': license.issue_date,
                'expiry_date': license.expiry_date,

            }
        except License.DoesNotExist:
            data['license'] = {
                'licenseId': '',
                'license_class': '',
                'country_of_issue': '',
                'issue_date': '',
                'expiry_date': '',
            }

        return data
