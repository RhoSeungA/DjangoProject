from django.shortcuts import render ,redirect
from .models import Author,Book,Country,Genre,KeyWord,PublishingCompany,Comment,CommentOfComment
from django.views.generic import ListView,DetailView,CreateView,UpdateView ##장고에서 제공
from django.contrib.auth.mixins import  LoginRequiredMixin,UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm,CommentOfCommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q



def delete_comment(request,pk):

    comment = get_object_or_404(Comment,pk=pk)
    book = comment.book

    if request.user.is_authenticated and request.user == comment.writer:
        comment.delete()
        return redirect(book.get_absolute_url())
    else:
        PermissionDenied
def delete_coc(request,pk):
    coc = get_object_or_404(CommentOfComment, pk=pk)
    parent = coc.parent_Comment.book

    if request.user.is_authenticated and request.user == coc.writer:
        coc.delete()
        return redirect(parent.get_absolute_url())
    else:
        PermissionDenied

class CommentUpdate(LoginRequiredMixin,UpdateView):
    model = Comment
    form_class = CommentForm
    #CreateView,UpdateView 이던지,,, form을 사용하면, 템플릿이 model명_forms로 자동을 만들어짐.
    # 템플릿 모델명_forms : comment_form

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().writer:
            return super(CommentUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class CommentOfCommentUpdate(LoginRequiredMixin,UpdateView):
    model = CommentOfComment
    form_class = CommentOfCommentForm

    # CreateView,UpdateView 이던지,,, form을 사용하면, 템플릿이 model명_forms로 자동을 만들어짐.
    # 템플릿 모델명_forms : comment_form

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().writer:
            return super(CommentOfCommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied




class BookCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Book
    fields = ['title','introduction','head_image','release_date','author','price','sale'
              ,'genre','country','publisher']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):#request는 client??
        current_User=self.request.user
        if current_User.is_authenticated and (current_User.is_superuser or current_User.is_staff):
            form.instance.post_writer = current_User
            response=super(BookCreate,self).form_valid(form)
            keywords_str=self.request.POST.get('keywords_str')#여기서 POST는 (데이터 전달 방식: get 방식 혹은 post방식) ,method=post??
            if keywords_str :
                keywords_str = keywords_str.strip()#앞뒤 빈칸 없앰
                keywords_str = keywords_str.replace(',',';')
                keywords_list = keywords_str.split(';')
                for t in keywords_list:
                    t = t.strip()
                    keyword1, is_keyword_created = KeyWord.objects.get_or_create(name=t)
                    #get_or_created는 튜플 반환
                    #뒤에는 created되면 참 반환?
                    #tag에는 가져온거.
                    if is_keyword_created:
                        keyword1.slug = slugify(t, allow_unicode=True)
                        keyword1.save()
                    self.object.keyword.add(keyword1)

            return response
            #return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/shop/')

    # 템플릿 : 모델명_form.html


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookCreate, self).get_context_data()
        context['Countrys'] = Country.objects.all()
        context['Genres'] = Genre.objects.all()
        return context

class AuthorCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model=Author
    fields = ['name','author_info']
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):#request는 client??
        current_User=self.request.user
        if current_User.is_authenticated and (current_User.is_superuser or current_User.is_staff):
            form.instance.slug = form.instance.name
            response=super(AuthorCreate,self).form_valid(form)
            #return response
            return redirect('/shop/create_item/')
            #return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/shop/')



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AuthorCreate, self).get_context_data()
        context['Countrys'] = Country.objects.all()
        context['Genres'] = Genre.objects.all()
        return context

class BookUpdate(LoginRequiredMixin,UpdateView):
    model=Book
    fields = ['title', 'introduction', 'head_image',  'release_date', 'author', 'price', 'sale'
        , 'genre', 'country', 'publisher']

    template_name = 'shop/book_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().post_writer:
            return super(BookUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(BookUpdate, self).form_valid(form)
        self.object.keyword.clear()
        keywords_str = self.request.POST.get('keywords_str')
        if keywords_str:
            keywords_str = keywords_str.strip()  # 앞뒤 빈칸 없앰
            keywords_str = keywords_str.replace(',', ';')
            keywords_list = keywords_str.split(';')
            for t in keywords_list:
                t = t.strip()
                keyword, is_keyword_created = KeyWord.objects.get_or_create(name=t)
                if is_keyword_created:
                    keyword.slug = slugify(t, allow_unicode=True)
                    keyword.save()
                self.object.keyword.add(keyword)
        return response
        #return redirect('/shop/my_page/')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookUpdate, self).get_context_data()
        if self.object.keyword.exists():
            keywords_str_list = list()
            for t in self.object.keyword.all():
                keywords_str_list.append(t.name)
            context['keywords_str_default'] = ';'.join(keywords_str_list)
        context['Countrys'] = Country.objects.all()
        context['Genres'] = Genre.objects.all()
        return context

class BookList(ListView):## ListView 장고에서 제공
    model = Book
    ordering = '-pk'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookList,self).get_context_data()
        context['Countrys'] = Country.objects.all()
        context['Genres']=Genre.objects.all()

        # context['no_category_post_count']= .objects.filter(category=None).count
        return context

class BookSearch(BookList):#ListView 상속,post_list,post_list.html 자동 호출
    paginated_by=None
    def get_queryset(self):#listview 가 제공해주는 함수
    #queryseㅅ --> 검색 결과,검색 결과 얻는 함수
        q = self.kwargs['q']
        book_list = Book.objects.filter(
            Q(title__contains=q) |
            Q(keyword__name__contains=q)
        ).distinct()
        return book_list
    def get_context_data(self, *,object_list=None,**kwargs):
        context = super(BookSearch,self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'{q}'
        context['search_count']= f'{self.get_queryset().count()}'
        return context

class BookDetail(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookDetail,self).get_context_data()
        context['Countrys'] = Country.objects.all()
        context['Genres'] = Genre.objects.all()
        book_author = self.object.author
        context['author_other_books'] = Book.objects.filter(author=book_author)
        keyword_list = self.object.keyword.all()
        context['comment_form'] = CommentForm
        context['commentofComment_form'] =CommentOfCommentForm
        #keyword_list=list(keyword_list)

        #for i in range(0,len(keyword_list)):
        #   context[keyword_list[i]] = Book.objects.filter(keyword=keyword_list[i])



        return context

def genre_page(request ,slug1,slug2):
    country= Country.objects.get(slug=slug1)
    genre = Genre.objects.get(slug=slug2)

    book_list= Book.objects.filter(country=country , genre=genre)
    #book_list=book_list.objects.filter(genre=genre and )

    return render(request, 'shop/book_list.html', {
        'country': country,  # 따옴표 안에 있는게 변수
        'book_list': book_list,
        'Countrys': Country.objects.all(),
        'Genres': Genre.objects.all(),
        'this_page_country': slug1,
        'this_page_Genre': slug2,
    })

def keyword_page(request,slug):
    keyword = KeyWord.objects.get(slug=slug)
    book_list = keyword.book_set.all()
    return render(request, 'shop/book_list.html',{
        'keyword' : keyword,
        'book_list': book_list,
        'Countrys': Country.objects.all(),
        'Genres': Genre.objects.all(),
    })

def author_page(request,slug):
    author=Author.objects.get(slug=slug)
    return render(request,'shop/author.html',
                  {'author':author,
                   'Countrys': Country.objects.all(),
                   'Genres': Genre.objects.all(),
                   }

                  )

def publisher_page(request,slug):
    publisher=PublishingCompany.objects.get(slug=slug)
    books=Book.objects.filter(publisher=publisher)
    return render(request,'shop/publisher.html',
                  {
                      'publisher':publisher,
                      'books':books,
                  })


def my_page(request):
    current_User = request.user
    books=Book.objects.filter(post_writer= current_User)
    comments=Comment.objects.filter(writer= current_User)
    return render(request,'shop/my_page.html',
    {
        'books':books,
        'comments':comments
    })

def new_comment(request,pk):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, pk=pk)
        #포스트 모델에서 pk=pk인거 가지고 오기
        if request.method == 'POST' :
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.book = book
                comment.writer = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else: #GET으로 온 경우
            return redirect(book.get_absolute_url())
    else:
        raise PermissionDenied

def new_commentofcomment(request,pk1,pk2):
    if request.user.is_authenticated:
        book=get_object_or_404(Book,pk=pk1)
        parent = get_object_or_404(Comment, pk=pk2)
        #포스트 모델에서 pk=pk인거 가지고 오기
        if request.method == 'POST':
            commentOfComment_form = CommentOfCommentForm(request.POST)
            if commentOfComment_form.is_valid():
                comment = commentOfComment_form.save(commit=False)
                comment.parent_Comment = parent
                comment.writer = request.user
                comment.save()
                return redirect(book.get_absolute_url())
        else: #GET으로 온 경우
            return redirect(parent.get_absolute_url())
    else:
        raise PermissionDenied


def main(request):
    recent_books = Book.objects.order_by('-pk')[:4]
    return render(request, 'shop/home.html',
                  {
                      'recent_books': recent_books
                  }
                  )

def about(request):

    kor_books=Book.objects.filter(country=Country.objects.get(name="국내도서"))
    kor_books_a_count=kor_books.filter(genre=Genre.objects.get(name="소설")).count()
    kor_books_b_count=kor_books.filter(genre=Genre.objects.get(name="공학")).count()
    kor_books_c_count=kor_books.filter(genre=Genre.objects.get(name="시/에세이")).count()

    japan_books = Book.objects.filter(country=Country.objects.get(name="일본도서"))
    japan_books_a_count = japan_books.filter(genre=Genre.objects.get(name="소설")).count()
    japan_books_b_count = japan_books.filter(genre=Genre.objects.get(name="공학")).count()
    japan_books_c_count = japan_books.filter(genre=Genre.objects.get(name="시/에세이")).count()

    w_books = Book.objects.filter(country=Country.objects.get(name="서양도서"))
    w_books_a_count = w_books.filter(genre=Genre.objects.get(name="소설")).count()
    w_books_b_count = w_books.filter(genre=Genre.objects.get(name="공학")).count()
    w_books_c_count = w_books.filter(genre=Genre.objects.get(name="시/에세이")).count()

    return render(request, 'shop/about.html',
    {
        'kor_books_a_count':kor_books_a_count,
        'kor_books_b_count': kor_books_b_count,
        'kor_books_c_count': kor_books_c_count,
        'japan_books_a_count':japan_books_a_count,
        'japan_books_b_count': japan_books_b_count,
        'japan_books_c_count': japan_books_c_count,
        'w_books_a_count':w_books_a_count,
        'w_books_b_count': w_books_b_count,
        'w_books_c_count': w_books_c_count,

    }
    )  # templates에서 찾음?

