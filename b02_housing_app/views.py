# from django.http import HttpResponseRedirect
# from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
# from django.views import generic
# from .models import Choice, Question, Deepthought
# from django.utils import timezone
from .forms import ApartmentForm


def insert_review(request):
    context = {}
    form = ApartmentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, 'apartmentform.html', {'form': form})