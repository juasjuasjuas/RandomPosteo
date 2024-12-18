from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
# importing messages
from django.contrib import messages
import os
import uuid
from django.conf import settings

# Model Forms.
from .forms import UserPostForm, AnswerForm
# String module
from django.template.loader import render_to_string

# Create your views here.

def home(request):
    user_posts = UserPost.objects.all()
    
    # Display latest posts.
    latest_blogs = BlogPost.objects.order_by('-timestamp')[0:3]

    latest_topics = UserPost.objects.order_by('-date_created')[0:3]
    
    context = {
        'user_posts':user_posts,
        'latest_blogs':latest_blogs,
        'latest_topics':latest_topics
    }
    return render(request, 'forum-main.html', context)

@login_required(login_url='login')
def userPost(request):
    # User Post form.
    form = UserPostForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            title = request.POST.get('title')
            description = request.POST.get('description')
            topic = UserPost.objects.create(title=title, author=request.user.author, description=description)
            topic.save()
            return redirect('home')
    else:
        form = UserPostForm()

    context = {'form':form}
    return render(request, 'user-post.html', context)

#@login_required(login_url='login')

def postTopic(request, pk):
    post_topic = get_object_or_404(UserPost, pk=pk)
    answers = Answer.objects.filter(user_post=post_topic)
    answer_form = AnswerForm()

    if request.method == "POST" and request.user.is_authenticated:
        answer_form = AnswerForm(request.POST)

        if answer_form.is_valid():
            content = answer_form.cleaned_data['content']
            image_path = None

            if request.FILES.get('image'):  # Check if 'image' is in request.FILES
                image_file = request.FILES['image']
                file_extension = os.path.splitext(image_file.name)[1]
                unique_filename = str(uuid.uuid4()) + file_extension
                image_path = os.path.join(settings.MEDIA_ROOT, 'profile_images', unique_filename)

                try:
                    with open(image_path, 'wb+') as destination:
                        for chunk in image_file.chunks():
                            destination.write(chunk)
                except OSError as e:
                    messages.error(request, f"Error saving image: {e}")
                    return redirect(request.META.get('HTTP_REFERER'))

            Answer.objects.create(user_post=post_topic, user=request.user, content=content, image_path=image_path)
            return HttpResponseRedirect(post_topic.get_absolute_url())

        else:
            for error, error_list in answer_form.errors.items():
                for message in error_list:
                    messages.error(request, f"{error}: {message}")
            return redirect(request.META.get('HTTP_REFERER'))

    elif request.method == "POST" and not request.user.is_authenticated:
        messages.error(request, "You must be logged in to post a response.")
        return redirect('login')

    context = {
        'topic': post_topic,
        'answers': answers,
        'answer_form': answer_form,
    }
    return render(request, 'topic-detail.html', context)



@login_required(login_url='login')
def userDashboard(request):
    topic_posted = request.user.author.userpost_set.all()
    ans_posted = request.user.answer_set.all()
    topic_count = topic_posted.count()
    ans_count = ans_posted.count()
    
    context = {
        'topic_posted':topic_posted,
        'ans_posted':ans_posted,
        'topic_count':topic_count,
        'ans_count':ans_count
    }
    return render(request, 'user-dashboard.html', context)

def searchView(request):
    queryset = UserPost.objects.all()
    search_query = request.GET.get('q')

    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query) 
        ).distinct()
        
        q_count = queryset.count()
    else:
        messages.error(request, f"Oops! Looks like you didn't put any keyword. Please try again.")
        return redirect('home')

    
    context = {
        'queryset':queryset,
        'search_query':search_query,
        'q_count':q_count
    }

    return render(request, 'search-result.html', context)


def upvote(request):
    answer = get_object_or_404(Answer, id=request.POST.get('answer_id'))
    
    has_upvoted = False

    if answer.upvotes.filter(id = request.user.id).exists():
        answer.upvotes.remove(request.user)
        has_upvoted = False        
    else:
        answer.upvotes.add(request.user)
        answer.downvotes.remove(request.user)
        has_upvoted = True

    return HttpResponseRedirect(answer.user_post.get_absolute_url())
    

def downvote(request):
    answer = get_object_or_404(Answer, id=request.POST.get('answer_id'))
    
    has_downvoted = False
    
    if answer.downvotes.filter(id = request.user.id).exists():
        answer.downvotes.remove(request.user)
        has_downvoted = False
    else:
        answer.downvotes.add(request.user)
        answer.upvotes.remove(request.user)
        has_downvoted = True
    
    return HttpResponseRedirect(answer.user_post.get_absolute_url())

# Blog listing page view.
def blogListView(request):
    
    # Display all blog posts.
    all_posts = BlogPost.objects.all()
    
    context = {
        'all_posts':all_posts
    }
    return render(request, 'blog-listing.html', context)

    
# Blog single post detail view.
def blogDetailView(request, slug):
    # Get specific post by slug.
    post_detail = get_object_or_404(BlogPost, slug=slug)

    context = {
        'post_detail':post_detail,
    }

    return render(request, 'blog-detail.html', context)  



