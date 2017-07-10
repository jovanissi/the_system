from manager.models import user_profile

class CustomUserAuth(object):

	def authenticate(self, username=None, password=None):
		try:
			user = user_profile.objects.get(Username=username)
			if user.check_password(password):
				return user
		except user_profile.DoesNotExist:
			return None


	def get_user(self, user_id):
		try:
			user = user_profile.objects.get(pk=user_id)
			if user.is_active:
				return user
			return None
		except user_profile.DoesNotExist:
			return None