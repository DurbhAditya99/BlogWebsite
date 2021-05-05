from django.shortcuts import render
from django import forms
from tinymce.widgets import TinyMCE
from .models import BlogPost,Comments
# Create your forms here.

class PostForm(forms.ModelForm):
	content=forms.CharField(widget=TinyMCE())

	class Meta():
		model=BlogPost
		fields=('author','title','content')

		widgets={
		
			'title':forms.TextInput(attrs={'class':'textinputclass'}),
			'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
				} 


class CommentForm(forms.ModelForm):

	
	class Meta():
		model=Comments
		fields=('author','content')

		widgets={
			'author':forms.TextInput(attrs={'class':'textinputclass'}),
			'content':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})

				}