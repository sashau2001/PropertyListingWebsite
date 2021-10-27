# from django.http import HttpResponseRedirect
# from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
# from django.views import generic
from .models import Review
# from django.utils import timezone
from .forms import ReviewForm


def insert_review(request):
    context = {}
    form = ReviewForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, 'reviewform.html', {'form': form})


def reviews(request):
    review_list = Review.objects.all()
    context = {'review_list': review_list}
    return render(request, 'reviews.html', context)