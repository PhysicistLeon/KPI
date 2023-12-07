from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, ResearcherForm, ArticleForm
from django.contrib.auth.decorators import login_required
from .models import Article
from django.http import JsonResponse


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")  # Redirect to a home page or profile page
    else:
        form = CustomUserCreationForm()
    return render(request, "achievements/register.html", {"form": form})


def index(request):
    return render(request, "achievements/index.html")


from django.contrib.auth.decorators import login_required
from .models import Researcher


@login_required
def profile(request):
    researcher = request.user.researcher
    # Calculate the number of articles
    num_articles = Article.objects.filter(researchers=researcher).count()
    return render(
        request,
        "achievements/profile.html",
        {
            "researcher": researcher,
            "num_articles": num_articles,  # Pass the number of articles to the template
        },
    )


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ResearcherForm(request.POST, instance=request.user.researcher)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ResearcherForm(instance=request.user.researcher)
    return render(request, "achievements/edit_profile.html", {"form": form})


from .utils import get_article_data_from_doi


@login_required
def submit_article(request):
    print("SUBMITT!!!")
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            article.researchers.add(request.user.researcher)
            # You can handle many-to-many fields (like researchers) after saving the form
            form.save_m2m()
            return redirect(
                "articles_list"
            )  # Redirect to the list of articles or some other appropriate page
    elif (
        request.method == "GET"
        and request.headers.get("X-Requested-With") == "XMLHttpRequest"
    ):
        print("GET!!!")
        doi = request.GET.get("doi")
        print("doi")
        article_data = get_article_data_from_doi(doi)
        if article_data:
            return JsonResponse(article_data)
        else:
            return JsonResponse({"error": "Data not found"}, status=404)
    else:
        print("NO!!!")
        form = ArticleForm()
    return render(request, "achievements/submit_article.html", {"form": form})


@login_required
def articles_list(request):
    # Filter articles where the current user is a researcher # Article.objects.all()
    articles = Article.objects.filter(researchers__user=request.user)
    return render(request, "achievements/articles_list.html", {"articles": articles})
