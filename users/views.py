from rest_framework.views import APIView
from users.models import user
from teams.models import team
from rest_framework.response import Response
from users.serializers import UserSerializer, UserPatchSerializer
from rest_framework import status

# Create your views here.

class UserBase(APIView):
    """
    Base interface implementation for API's to manage users.
    """

    # create a user
    def post(self, request, format=None):
        """
        :param request: A json string with the user details
        {
          "name" : "<user_name>",
          "display_name" : "<display name>"
        }
        :return: A json string with the response {"id" : "<user_id>"}

        Constraint:
            * user name must be unique
            * name can be max 64 characters
            * display name can be max 64 characters
        """
        serializer = UserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"id":serializer.data.get('id')}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # list all users and also describe a user
    def get(self, request, pk=None, format=None) -> str:
        """
        :return: A json list with the response
        [
          {
            "name" : "<user_name>",
            "display_name" : "<display name>",
            "creation_time" : "<some date:time format>"
          }
        ]
        
        or

        :param request: A json string with the user details
        {
          "id" : "<user_id>"
        }

        :return: A json string with the response

        {
          "name" : "<user_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>"
        }

        """
        id=pk
        if id is not None:
            uuser = user.objects.get(id=id)
            serializer = UserSerializer(uuser)
            return Response(serializer.data)
        
        usser = user.objects.all()
        serializer = UserSerializer(usser, many=True)
        return Response(serializer.data)


    # update user
    def patch(self, request, pk=None, format=None) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>",
          "user" : {
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        }

        :return:

        Constraint:
            * user name cannot be updated
            * name can be max 64 characters
            * display name can be max 128 characters
        """
        id = pk
        usser = user.objects.get(id=id)
        serializer = UserPatchSerializer(usser, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_user_teams(self, request, pk=None, format=None) -> str:
        """
        :param request:
        {
          "id" : "<user_id>"
        }

        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        pass

