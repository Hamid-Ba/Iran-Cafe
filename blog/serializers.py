"""
Blog Module Serializer
"""
from rest_framework import serializers
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

from blog import models
from cafe.models import Bartender,Cafe

class CreateBlogSerializer(TaggitSerializer,serializers.ModelSerializer):
    """Create Blog Serializer"""
    tags = TagListSerializerField()
    class Meta:
        model = models.Blog
        fields = ['cafe_id','title','slug','short_desc','desc','image','image_alt','image_title',
        'publish_date','tags']

    def validate(self, attrs):
        cafe_id = attrs.get('cafe_id')
        user = self.context.get('request').user
        
        try :
            if user.cafe.id != cafe_id :
                print(user.cafe.id)
                msg = 'شناسه کافه اشتباه هست'
                raise serializers.ValidationError(msg)
        except :
            cafe = Cafe.objects.filter(id = cafe_id).first()
            is_bartender = Bartender.objects.filter(user=user , cafe=cafe , is_active=True).exists()
            if not is_bartender :
                    msg = 'شما قادر به ثبت بلاگ نمی باشید'
                    raise serializers.ValidationError(msg)
        
        attrs['is_cafe'] = True

        return attrs

class UpdateBlogSerializer(TaggitSerializer,serializers.ModelSerializer):
    """Update Blog Serializer"""
    tags = TagListSerializerField()
    class Meta:
        model = models.Blog
        fields = ['title','slug','short_desc','desc','image','image_alt','image_title',
        'publish_date','tags']

class BlogSerializer(CreateBlogSerializer):
    """Blog Serializer"""
    class Meta(CreateBlogSerializer.Meta):
        fields = '__all__'

    def to_representation(self, instance):
        datas =  super().to_representation(instance)
        try :
            cafe = Cafe.objects.filter(id=instance.cafe_id).first()
            datas['cafe'] = {
                'title' : cafe.persian_title,
                'code' : cafe.code,
                'owner' : cafe.owner.fullName
            }
        except : None
        return datas

class BlogListSerializer(UpdateBlogSerializer):
    """Blog List Serializer"""
    class Meta(UpdateBlogSerializer.Meta):
        """Meta Class"""