from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import License
from .serializers import LicenseSerializer
from datetime import date
from rest_framework.decorators import permission_classes, authentication_classes

@permission_classes([permissions.AllowAny])
@authentication_classes([])
class LicenseDetailView(generics.RetrieveAPIView):
    """
    API endpoint that allows retrieval and validation of a specific license.
    """
    queryset = License.objects.all()
    serializer_class = LicenseSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve details of a specific license and determine its validity status.

        Parameters:
        - license_id (path): The unique identifier of the license

        Returns:
        - 200 OK: License details retrieved successfully
            {
                'licenseId': 'string',
                'issue_date': 'date',
                'expiry_date': 'date',
                'status': 'string',
                'details': 'string'
            }
        - 404 Not Found: License does not exist
            {
                'licenseId': 'string',
                'status': 'invalid',
                'details': 'License does not exist'
            }
        """
        license_id = self.kwargs.get('license_id')
        print(f"Retrieving license with ID: {license_id}")
        
        try:
            instance = License.objects.get(licenseId=license_id)
        except License.DoesNotExist:
            print("License does not exist")
            return Response(
                {
                    'licenseId': license_id,
                    'status': 'invalid',
                    'details': 'License does not exist'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        today = date.today()  # Get the current date
        print(f"Today's date: {today}")
        print(f"Issue date: {instance.issue_date}")
        print(f"Expiry date: {instance.expiry_date}")

        # Determine license status
        if instance.expiry_date < today:
            status_text = 'expired'
            details = 'License has expired'
        elif instance.issue_date > today:
            status_text = 'invalid'
            details = 'License is not yet valid (future issue date)'
        else:
            status_text = 'valid'
            details = 'License is currently valid'

        response_data = {
            'licenseId': instance.licenseId,
            'issue_date': instance.issue_date,
            'expiry_date': instance.expiry_date,
            'status': status_text,
            'details': details,
        }
        print(f"Response data: {response_data}")
        return Response(response_data, status=status.HTTP_200_OK)
