from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = (
            'title',
            'movie_title',
            'rank',
            'content',
        )
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'create_review_title',
                }
            ),
            'movie_title': forms.TextInput(
                attrs={
                    'class': 'create_review_movie_title',
                }
            ),
            # 'rank': forms.IntegerField(
            #     attrs={
            #         'class': 'create_review_rank',
            #     }
            # ),
            'content': forms.Textarea(
                attrs={
                    'class': 'create_review_content',
                    'style': 'resize: none;',
                }
            ),
        }


class CommentForm(forms.ModelForm):
    
    content = forms.CharField(
        label='',
        widget = forms.TextInput(
            attrs={
                'class': 'comment_content',
                'style': 'width:80%',
            }
        )
    )

    class Meta:
        model = Comment
        exclude = (
            'review',
            'user',
        )


