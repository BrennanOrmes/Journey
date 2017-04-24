'''
    social.py - Social Authentication Utilities.

    Author: Team Alpha

    Tested?: Yes
    Functional?: Yes
    Merged?: Yes
    Copyright: (c) 2017 Team Alpha, University of Aberdeen.
'''
from social_django.models import UserSocialAuth


def get_social_context(user):
    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    }
