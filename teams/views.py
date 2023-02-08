from django.shortcuts import render
from rest_framework.views import APIView, status
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .models import Team
from datetime import datetime
from rest_framework.response import Response


class NegativeTitlesError(Exception):
    def __init__(self, message):
        self.message = message


class InvalidYearCupError(Exception):
    def __init__(self, message):
        self.message = message


class ImpossibleTitlesError(Exception):
    def __init__(self, message):
        self.message = message


class EnsureData:
    def data_processing(data):
        all_cup = []
        current_year = datetime.now().year

        for year in range(1930, current_year + 1):
            if year == 1930 or year == 1934 or year == 1938:
                all_cup.append(year)
            elif (year - 1950) % 4 == 0 and year >= 1950:
                all_cup.append(year)

        if "titles" in data:
            if data["titles"] < 0:
                raise NegativeTitlesError("titles cannot be negative")

        if "first_cup" in data:
            request_year = datetime.strptime(data["first_cup"], "%Y-%m-%d").year
            cup_count = (current_year - request_year) / 4
            if request_year < 1930:
                raise InvalidYearCupError("there was no world cup this year")
            elif request_year not in all_cup:
                raise InvalidYearCupError("there was no world cup this year")
            if "titles" in data:
                if data["titles"] > cup_count:
                    raise ImpossibleTitlesError(
                        "impossible to have more titles than disputed cups"
                    )


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
