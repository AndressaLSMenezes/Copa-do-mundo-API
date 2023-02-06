from django.shortcuts import render
from datetime import datetime
from rest_framework.views import APIView, status
from rest_framework.response import Response
from django.forms.models import model_to_dict
import pdb

from .models import Team


class NegativeTitlesError(Exception):
    def __init__(self, message):
        self.message = message


class InvalidYearCupError(Exception):
    def __init__(self, message):
        self.message = message


class ImpossibleTitlesError(Exception):
    def __init__(self, message):
        self.message = message


class TeamView(APIView):
    def post(self, request):
        try:
            if request.data["titles"] < 0:
                raise NegativeTitlesError("titles cannot be negative")
        except NegativeTitlesError as err:
            return Response({"error": err.message}, 400)

        current_year = datetime.now().year
        all_cup = []
        cup_count = 0
        request_year = datetime.strptime(request.data["first_cup"], "%Y-%m-%d").year
        for year in range(1930, current_year + 1):
            if year == 1930 or year == 1934 or year == 1938:
                all_cup.append(year)
                cup_count = cup_count + 1
            elif (year - 1950) % 4 == 0 and year >= 1950:
                all_cup.append(year)
                cup_count = cup_count + 1
        try:
            if request_year < 1930:
                raise InvalidYearCupError("there was no world cup this year")
            elif request_year not in all_cup:
                raise InvalidYearCupError("there was no world cup this year")
        except InvalidYearCupError as err:
            return Response({"error": err.message}, 400)

        try:
            if request.data["titles"] > cup_count:
                raise ImpossibleTitlesError(
                    "impossible to have more titles than disputed cups"
                )
        except ImpossibleTitlesError as err:
            return Response({"error": err.message}, 400)

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
            return Response({"error": "Team not found"}, 404)

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
