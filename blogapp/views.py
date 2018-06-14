from django.shortcuts import render
from .models import Banner, Post, BlogCategory, Comment, FriendlyLink, Tags
from django.views.generic.base import View
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
# 首页
def index(request):
    banner_list = Banner.objects.all()
    # 去数据库里面取出所有　推荐的文章
    recomment_list = Post.objects.filter(is_recomment=True)
    for recoment in recomment_list:
        recoment.content = recoment.content[:100] + '......'

    # 倒序
    post_list = Post.objects.order_by('-pub_date')
    for post in post_list:
        post.content = post.content[:160] + '......'

    # 博客分类
    blogcategory_list = BlogCategory.objects.all()

    # 最新评论博客列表
    comment_list = Comment.objects.order_by('-pub_date')
    new_comment_list = []
    for test in comment_list:
        if test.post not in new_comment_list:
            new_comment_list.append(test.post)
    # 友情链接
    friendlylink_list = FriendlyLink.objects.all()
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        pagea = 1

    p = Paginator(post_list, per_page=2, request=request)
    post_list = p.page(page)
    ctx = {
        'banner_list': banner_list,
        'recomment_list': recomment_list,
        'post_list': post_list,
        'blogcategory_list': blogcategory_list,
        'new_comment_list': new_comment_list,
        'friendlylink_list': friendlylink_list

    }
    return render(request, 'index.html', ctx)


# 列表页
def lista1(request, tcv=-1, cat=-1):
    #点击标签云出现到列表页面
    tcv = int(tcv)
    cat = int(cat)
    post_list = None
    if tcv != -1:
        post_list = Post.objects.filter(tags=tcv)
    elif cat != -1:
        post_list = Post.objects.filter(category=cat)
    else:
        post_list = Post.objects.order_by('-pub_date')

    #点击分类出现到列表

    # else:
    #     post_list = Post.objects.order_by('-pub_date')

    for post in post_list:
        post.content = post.content[:160] + '......'
    try:
        pagea = request.GET.get('page', 1)
    except PageNotAnInteger:
        pagea = 1

    p = Paginator(post_list, per_page=2, request=request)
    post_list = p.page(pagea)

    banner_list = Banner.objects.all()
    # 去数据库里面取出所有　推荐的文章
    recomment_list = Post.objects.filter(is_recomment=True)
    for recoment in recomment_list:
        recoment.content = recoment.content[:100] + '......'

    # 博客分类
    blogcategory_list = BlogCategory.objects.all()

    # 最新评论博客列表
    comment_list = Comment.objects.order_by('-pub_date')
    new_comment_list = []
    for test in comment_list:
        if test.post not in new_comment_list:
            new_comment_list.append(test.post)

    # 友情链接
    friendlylink_list = FriendlyLink.objects.all()
    # 标签云
    tags_list = Tags.objects.all()
    now_tags_list = []
    for t in tags_list:
        count = len(t.post_set.all())
        now_tags_list.append({'name': t.name, 'id': t.id, 'count': count})

    ctx = {
        'banner_list': banner_list,
        'recomment_list': recomment_list,
        'post_list': post_list,
        'blogcategory_list': blogcategory_list,
        'new_comment_list': new_comment_list,
        'friendlylink_list': friendlylink_list,
        'tags_list': now_tags_list,
    }
    return render(request, 'list.html', ctx)


# 搜索
class SearchView(View):
    def get(self, request):
        pass

    def post(self, request):
        kw = request.POST.get('keyword')
        post_list = Post.objects.filter(Q(title__icontains=kw) | Q(content__icontains=kw))
        for post in post_list:
            post.content = post.content[:160] + '......'
        banner_list = Banner.objects.all()
        # 去数据库里面取出所有　推荐的文章
        recomment_list = Post.objects.filter(is_recomment=True)
        for recoment in recomment_list:
            recoment.content = recoment.content[:100] + '......'

        # 倒叙
        # post_list = Post.objects.order_by('-pub_date')
        # for post in post_list:
        #     post.content = post.content[:160] + '......'

        # 博客分类
        blogcategory_list = BlogCategory.objects.all()

        # 最新评论博客列表
        comment_list = Comment.objects.order_by('-pub_date')
        new_comment_list = []
        for test in comment_list:
            if test.post not in new_comment_list:
                new_comment_list.append(test.post)

        # 友情链接
        friendlylink_list = FriendlyLink.objects.all()
        # 标签
        tags_list = Tags.objects.all()

        ccx = {
            'banner_list': banner_list,
            'recomment_list': recomment_list,
            'post_list': post_list,
            'blogcategory_list': blogcategory_list,
            'new_comment_list': new_comment_list,
            'friendlylink_list': friendlylink_list,
            'tags_list': tags_list,
        }

        return render(request, 'search.html', ccx)

#详情
def show(request, sh=-1):

    cht = int(sh)
    if cht != -1:
        post_list = Post.objects.get(id=cht)
    else:
        post_list = Post.objects.filter(is_recomment=True).order_by('-views')
        post_list = post_list[0]
    #最新评论 去重
    comment_list = Comment.objects.order_by('-pub_date')
    new_comment_list = []
    for test in comment_list:
        if test.post not in new_comment_list:
            new_comment_list.append(test.post)
    #标签
    tag_list = post_list.tags.all()

    #相关推荐 除了本身 推荐这个分类其他的
    category_list = Post.objects.filter(category=post_list.id)
    new_comment_lists = []
    for i in category_list:
        if i.title != post_list.title:
            new_comment_lists.append(i.title)

    ctx = {
        'post': post_list,
        'new_comment_list': new_comment_list,
        'tag_list': tag_list,
        'category_list' : new_comment_lists,

    }

    return render(request, 'show.html', ctx)
