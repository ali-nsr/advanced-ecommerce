from django import forms
from .models import *


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ('content',)


class CourseCommentReplyForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ('content',)
