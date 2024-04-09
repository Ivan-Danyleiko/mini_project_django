from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import AuthorForm, QuoteForm
from .models import Quote, Author


def main(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    authors = Author.objects.all()
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page, 'authors': authors})


@login_required
def add_author(request):
    form = AuthorForm()
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            print("Form saved successfully")
            return redirect('quotes:main')
        else:
            print("Form is not valid")
    return render(request, 'quotes/add_author.html', {'form': form})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)  # Зберігаємо форму, але не зберігаємо її в базу даних поки не додамо автора
            author = form.cleaned_data['author']
            quote.author = author  # Встановлюємо автора для цитати
            quote.save()  # Зберігаємо цитату з встановленим автором
            print("Form saved successfully")
            return redirect('quotes:main')
    else:
        form = QuoteForm()
        print("Form is not valid")
    return render(request, 'quotes/add_quote.html', {'form': form})
