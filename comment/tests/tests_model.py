"""
Test Comment Module Models
"""
from django.test import TestCase

from comment.models import Comment
from django.contrib.auth import get_user_model
from datetime import time, date


def create_user(phone, password):
    """Helper Function for creating a user"""
    return get_user_model().objects.create_user(phone=phone, password=password)


class CommentModel(TestCase):
    """Test Comment Model"""

    def test_create_comment(self):
        """Test Create Comment Model"""
        user = create_user("09151498722", "123456")
        payload = {
            "text": "this is a test",
            "date": date.today(),
            "is_cafe": False,
            "cafe_id": 2,
            "item_id": 4,
        }

        comment = Comment.objects.create(user=user, **payload)

        self.assertEqual(comment.user, user)
        for key, value in payload.items():
            self.assertEqual(getattr(comment, key), value)
