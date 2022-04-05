from rest_framework.views import APIView
from teams.models import team
from teams.serializers import TeamSerializer, TeamGETSerializer, TeamPOSTSerializer, TeamUserSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class TeamBase(APIView):
    """
    Base interface implementation for API's to manage teams.
    For simplicity a single team manages a single project. And there is a separate team per project.
    Users can be
    """ 

    # create a team
    def post(self, request, format=None):
        """
        :param request: A json string with the team details
        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "admin": "<id of a user>"
        }
        :return: A json string with the response {"id" : "<team_id>"}

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        serializer = TeamPOSTSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"id":serializer.data.get('id')}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # list all teams and also describe specific team
    def get(self, request, pk=None, format=None) -> str:
        """
        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>",
            "admin": "<id of a user>"
          }
        ]

        or

        :param request: A json string with the team details
        {
          "id" : "<team_id>"
        }

        :return: A json string with the response

        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>",
          "admin": "<id of a user>"
        }
        """
        id=pk
        if id is not None:
            uuser = team.objects.get(id=id)
            serializer = TeamGETSerializer(uuser)
            return Response(serializer.data)
        
        usser = team.objects.all()
        serializer = TeamGETSerializer(usser, many=True)
        return Response(serializer.data)

    # update team
    def patch(self, request, pk=None, format=None):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """

        id = pk
        if 'members' in request.data.keys():
          new_members = request.data.get('members')
          existing_members = team.objects.get('id').values_list('members', flat=True)
          print(new_members)
          print(existing_members)
          all_memebers = new_members + existing_members
          request.data.update({'members': set(all_memebers)})
          serializer = TeamUserSerializer(usser, data=request.data, partial=True)
          if serializer.is_valid():
              serializer.save()
              return Response({"MSG":"Team Updated Successfully"})
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
          """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "team" : {
            "name" : "<team_name>",
            "description" : "<team_description>",
            "admin": "<id of a user>"
          }
        }
        
        :return:

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
          usser = team.objects.get(id=id)
          serializer = TeamSerializer(usser, data=request.data, partial=True)
          if serializer.is_valid():
              serializer.save()
              return Response({"MSG":"Team Updated Successfully"})
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # add users to team
    def add_users_to_team(self, request: str):
        
        pass

    # add users to team
    def remove_users_from_team(self, request: str):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        pass

    # list users of a team
    def list_team_users(self, request: str):
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<user_id>",
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        ]
        """
        pass

