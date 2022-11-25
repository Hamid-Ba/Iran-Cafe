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

    def validate(self, attrs):
        item_id = attrs.get('item_id')
        
        user = self.context.get('request').user
        menu_item = MenuItem.objects.filter(id=item_id).first()

        if not menu_item :
            msg = 'این آیتم وجود ندارد'
            raise serializers.ValidationError(msg)
        cafe = menu_item.cafe
        
        if user == cafe.owner :
            msg = 'برای خودتون میخواین کامنت بذارید ؟'
            raise serializers.ValidationError(msg)

        return attrs
   
    def create(self, validated_data):
        user = self.context.get('request').user
        item_id = validated_data.get('item_id')
        
        try:
            menu_item = MenuItem.objects.filter(id=item_id).first()
            cafe = menu_item.cafe
            
            now_date = date.today()
            
            comment = Comment.objects.create(
                user=user,cafe_id=cafe.id
                ,is_cafe=False,date=now_date
                ,**validated_data)
            comment.save()
            return comment
            
        except : 
            msg = 'مشکلی ایجاد شده'
            raise serializers.ValidationError(msg)

class CommentSerializer(serializers.ModelSerializer):
    """Comment Serializer"""
    class Meta:
        model = Comment
        fields = '__all__'
        # read_only_fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = instance.user.fullName
        try:
            item = MenuItem.objects.filter(id=instance.item_id).first()
            response['item'] = item.title
        except : None
        return response