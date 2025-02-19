from accounts.models import User


def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    if backend.name == 'google-oauth2':
        if response.get('picture'):
            url = response['picture']
            user.profile.avatar = url
            user.profile.save()


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = {'email': details.get('email'), 'username': details.get('username')}

    if not fields['username']:
        fields['username'] = fields['email'].split('@')[0]

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }
