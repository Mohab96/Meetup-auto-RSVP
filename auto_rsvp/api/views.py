from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from meetup.api import Client
from .models import User, Group
from .serializers import GroupSerializer


class GroupListAPIView(APIView):
    """
    API endpoint for listing and managing groups a user is monitoring.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves a list of groups monitored by the authenticated user.
        """
        user = request.user
        groups = Group.objects.filter(user=user)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Joins a new group based on the provided Meetup group URL name.
        """
        data = request.data
        group_url_name = data.get('group_url_name')
        api_key = request.user.meetup_api_key

        if not all([group_url_name, api_key]):
            return Response({'error': 'Missing required fields: group_url_name or meetup_api_key'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = Client(api_key)
            group_info = client.GetGroup({'urlname': group_url_name})

            group, created = Group.objects.get_or_create(
                user=request.user,
                group_id=group_info.id,
                group_name=group_info.name,
            )

            if created:
                return Response({'message': f"Successfully joined group: {group.group_name}"}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': f"You are already monitoring the group: {group.group_name}"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f"Error joining group: {e}"}, status=status.HTTP_400_BAD_REQUEST)


class GroupDetailAPIView(APIView):
    """
    API endpoint for quitting a group.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, group_id):
        """
        Removes a group from the user's monitored list.
        """
        user = request.user
        try:
            group = Group.objects.get(user=user, group_id=group_id)
            group.delete()
            return Response({'message': f"Successfully quit group: {group.group_name}"}, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({'error': "Group not found in your monitored list."}, status=status.HTTP_404_NOT_FOUND)
