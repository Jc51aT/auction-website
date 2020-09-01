from django import forms

class CreateListingForm(forms.Form):

    CHOICES = [('1','Home'),('2','Garden'),('3','Clothing'),('4','Books'),('5','Other')]

    listing_title = forms.CharField(max_length=64, label='Listing Title', min_length=2)
    listing_price = forms.IntegerField(min_value=0)
    listing_categories = forms.ChoiceField(choices=CHOICES)
    listing_description = forms.CharField(widget=forms.Textarea, max_length=256, min_length=1)
    listing_image = forms.ImageField(allow_empty_file=True, required=False)