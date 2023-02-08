from django.shortcuts import render
from rest_framework.views import APIView, status
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .models import Team
from teams.utils import EnsureData
from teams.exception import NegativeTitlesError
from teams.exception import InvalidYearCupError
from teams.exception import ImpossibleTitlesError


class TeamView(APIView):
    def post(self, request):
        try:
            EnsureData.data_processing(request.data)
        except InvalidYearCupError as error:
            return Response({"error": error.message}, 400)
        except ImpossibleTitlesError as error:
            return Response({"error": error.message}, 400)
        except NegativeTitlesError as error:
            return Response({"error": error.message}, 400)

        team = Team.objects.create(**request.data)
        team_dict = model_to_dict(team)

        return Response(team_dict, 201)

    def get(self, request):
        teams = Team.objects.all()
        team_dict = []

        for team in teams:
            t = model_to_dict(team)
            team_dict.append(t)

        return Response(team_dict)


class TeamDetailView(APIView):
    def get(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        team_dict = model_to_dict(team)
        return Response(team_dict)

    def delete(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        team.delete()
        return Response(status=204)

    def patch(self, request, team_id):
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        for key, value in request.data.items():
            setattr(team, key, value)

        team.save()
        team_dict = model_to_dict(team)

        return Response(team_dict, 200)
