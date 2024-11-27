import requests

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.template import loader
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from . import serializers


# The Privacy Portal OAuth Token Endpoint
# API docs: https://privacyportal.org/developers/api-docs#oauth_token
TOKEN_ENDPOINT = 'https://api.privacyportal.org/oauth/token'

# The Privacy Portal User Info Endpoint
# API docs: https://privacyportal.org/developers/api-docs#openid_userinfo
USERINFO_ENDPOINT = 'https://api.privacyportal.org/oauth/userinfo'


User = get_user_model()


def index(request):
    template = loader.get_template("ums/login.html")
    return HttpResponse(template.render({"redirect_uri": settings.REDIRECT_URI}, request))


def redirect_uri(request):
    template = loader.get_template("ums/home.html")
    return HttpResponse(template.render({}, request))


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def fetch_token(self, code):
        payload = {
            "code": code,
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
            "redirect_uri": settings.REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        response = requests.post(TOKEN_ENDPOINT, json=payload)
        print("FETCH TOKEN>>>>>>>>>>>>>>>", response.json())
        return response.json()

    def fetch_user_info(self, access_token):
        response = requests.get(
            USERINFO_ENDPOINT,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        print("FETCH USER INFO>>>>>>>>>>>>>>>", response.json())
        return response.json()

    @action(
        methods=['POST'],
        detail=False,
        url_path='oauth/authenticate',
        serializer_class=serializers.OauthSerializer,
        permission_classes=[],
    )
    def oauth_authenticate(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = self.fetch_token(serializer.validated_data["code"])
        user_info = self.fetch_user_info(token["access_token"])

        # NOTE: User info include sub_id (unique id of the user), email (public email fo the user)
        # and name (name added by the user while logging in)
        # Other than sub_id, the name and email need to be added to the scope in the fronetend to be returned.

        # TODO: Get or create user 
        # Create access token for user
        # names = user_info["name"].split(" ")
        # first_name = names[0]
        # last_name = names[1] if len(names) > 1 else None
        # user = User.objects.get_or_create(
        #     sub_id=user_info["sub_id"],
        #     defaults={
        #         "email": user_info["email"],
        #         "first_name": first_name,
        #         "last_name": last_name,
        #     }
        # )

        return Response(
            {
                "success": True,
                "message": "User authenticated successfully",
                "token": {
                    "access": "",
                    "refresh": "",
                }
            },
            status=status.HTTP_200_OK,
        )
