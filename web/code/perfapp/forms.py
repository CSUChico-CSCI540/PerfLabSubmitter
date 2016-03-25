from django import forms

class perfsubmission(forms.Form):
    #username = forms.CharField(max_length=50)
    FilterMain = forms.FileField(label='FilterMain.cpp', required=True)
    Filter_c = forms.FileField(label='Filter.cpp',required=False)
    Filter_h = forms.FileField(label='Filter.h',required=False)
    Makefile = forms.FileField(label='Makefile',required=False)
    cs1300_c = forms.FileField(label='cs1300bmp.cpp',required=False)
    cs1300_h = forms.FileField(label='cs1300bmp.h',required=False)