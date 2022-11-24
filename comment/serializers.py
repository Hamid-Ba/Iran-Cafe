"""
Comment Module Serializer
"""
from rest_framework import serializers
from datetime import date

from cafe.models import MenuItem
from comment.models import Comment

class CreateCommentSerializer(serializers.ModelSerializer):
    """Create Comment Serializer"""
    class Meta:
        model = Comment
        fields = ['item_id' , 'text']

    def create(self, validated_data):
        user = self.context.get('request').user
        item_id = validated_data.pop('item_id')
        
        try:
            menu_item = MenuItem.objects.filter(id=item_id).first()
            cafe = menu_item.cafe

            if user == cafe.owner :
                msg = 'برای خودتون میخواین کامنت بذارید ؟'
                raise serializers.ValidationError(msg)

            now_date = date.today()

            comment = Comment.objects.create(
                user=user, item_id=item_id,
                cafe_id=cafe.id,is_cafe=False,
                date=now_date,**validated_data)
            comment.save()
            return comment
            
        except : 
            msg = 'مشکلی ایجاد شده'
            raise serializers.ValidationError(msg)