"""
Comment Module Serializer
"""
from rest_framework import serializers
from datetime import date

from cafe.models import Bartender, Cafe, MenuItem
from comment.models import Comment


class CreateCommentSerializer(serializers.ModelSerializer):
    """Create Comment Serializer"""

    class Meta:
        model = Comment
        fields = ["item_id", "text"]

    def validate(self, attrs):
        item_id = attrs.get("item_id")

        user = self.context.get("request").user
        menu_item = MenuItem.objects.filter(id=item_id).first()

        if not menu_item:
            msg = "این آیتم وجود ندارد"
            raise serializers.ValidationError(msg)
        cafe = menu_item.cafe

        is_bartender = Bartender.objects.filter(
            cafe=cafe, user=user, is_active=True
        ).exists()

        if user == cafe.owner or is_bartender:
            msg = "برای خودتون میخواین کامنت بذارید ؟"
            raise serializers.ValidationError(msg)

        return attrs

    def create(self, validated_data):
        user = self.context.get("request").user
        item_id = validated_data.get("item_id")

        try:
            menu_item = MenuItem.objects.filter(id=item_id).first()
            cafe = menu_item.cafe

            now_date = date.today()

            comment = Comment.objects.create(
                user=user,
                cafe_id=cafe.id,
                is_cafe=False,
                date=now_date,
                **validated_data
            )
            comment.save()
            return comment

        except:
            msg = "مشکلی ایجاد شده"
            raise serializers.ValidationError(msg)


class ResponseCommentSerializer(serializers.ModelSerializer):
    """Response Comment Serializer"""

    id = serializers.IntegerField(required=True)
    # text = serializers.CharField(max_length=500, required=True)

    class Meta:
        model = Comment
        fields = ["id", "text"]

    def validate(self, attrs):
        comment_id = attrs.get("id")
        user = self.context.get("request").user
        try:
            comment = Comment.objects.get(id=comment_id)
            cafe = Cafe.objects.get(id=comment.cafe_id)
            is_bartender = Bartender.objects.filter(
                cafe=cafe, user=user, is_active=True
            ).exists()

            if not (user == cafe.owner or is_bartender):
                msg = "جواب کامنت بقیه را نمیتوانید بدهید"
                raise serializers.ValidationError(msg)
        except:
            msg = "همچین کامنتی وجود ندارد"
            raise serializers.ValidationError(msg)
        return attrs

    def create(self, validated_data):
        user = self.context.get("request").user
        comment_id = validated_data.get("id")
        text = validated_data.get("text")

        try:
            comment = Comment.objects.get(id=comment_id)
            now_date = date.today()

            response = Comment.objects.create(
                user=user,
                cafe_id=comment.cafe_id,
                is_cafe=True,
                date=now_date,
                text=text,
                item_id=comment.item_id,
            )

            response.save()

            comment.response = response
            comment.save()

            return response

        except:
            msg = "مشکلی ایجاد شده"
            raise serializers.ValidationError(msg)


class CommentSerializer(serializers.ModelSerializer):
    """Comment Serializer"""

    class Meta:
        model = Comment
        fields = "__all__"
        # read_only_fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["name"] = instance.user.fullName
        try:
            item = MenuItem.objects.filter(id=instance.item_id).first()
            response["item"] = item.title

            if instance.response:
                response["response"] = {
                    "name": instance.response.user.fullName,
                    "date": instance.response.date,
                    "text": instance.response.text,
                }

        except:
            None
        return response
