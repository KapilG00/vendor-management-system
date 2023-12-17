from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class CommonModel(models.Model):
	"""
	Default Common Variables In Database.
	"""
	class Meta:
		abstract = True

	created_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_created_by", null=True, blank=True, on_delete=models.SET_NULL)
	modified_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_modified_by", null=True, blank=True, on_delete=models.SET_NULL)
	deleted_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_deleted_by", null=True, blank=True, on_delete=models.SET_NULL)
	is_deleted = models.BooleanField(default=False)
	created_date = models.DateTimeField(auto_now_add=True)
	deleted_date = models.DateTimeField(null=True, blank=True)
	modified_date = models.DateTimeField(auto_now=True)
