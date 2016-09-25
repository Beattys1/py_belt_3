from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Quote, Favorite

def index(request):
    return render(request, 'belt_3/index.html')

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        alias = request.POST['alias']
        email = request.POST['email']
        password = request.POST['password']
        passconf = request.POST['passconf']
        dob = request.POST['dob']
        errors, user = User.userManager.register(name, alias, email, password, passconf, dob)
        if errors:
            for i in range(0, len(errors)):
                messages.warning(request, errors[i])
            return redirect('/')
        if user:
            messages.success(request, 'Wow! You did it! You really registered!')
            return redirect('/')
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        error, user = User.userManager.login(request.POST['email'], request.POST['password'])
        if error:
            for i in range(0 , len(error)):
                messages.warning(request, error[i])
            return redirect('/')
        if user:
            request.session['current_user'] = user.id
            return redirect('/quotes')
    else:
        return redirect('/')

def logout(request):
    if 'current_user' in request.session:
        del request.session['current_user']
    return redirect('/')

def quotes(request):
    user = User.objects.get(id = request.session["current_user"])
    favorites = Favorite.objects.filter(user_like = user)
    all_quotes = Quote.objects.all()
    others = Quote.objects.exclude(quote_liked__in=favorites)
    print others
    context = {
        "user":user,
        "others":others,
        "favorites": favorites,
    }
    return render(request, 'belt_3/homepage.html', context)

def add_quote(request, id):
    person = request.POST["person"]
    quote = request.POST["quote"]
    errors, quotes = Quote.quoteManager.add_quote(person, quote)
    if errors:
        for i in range(0, len(errors)):
            messages.warning(request, errors[i])
        return redirect('/quotes')
    if quotes:
        Quote.objects.create(creator = User.objects.get(id=request.session["current_user"]),person = person, quote = quote )
        return redirect('/quotes')

def favorite_quote(request, id):
    Favorite.objects.create(user_like = User.objects.get(id = request.session["current_user"]), quote_like = Quote.objects.get(id = id))
    return redirect('/quotes')

def remove_quote(request, id):
    Favorite.objects.get(user_like = User.objects.get(id = request.session["current_user"]), quote_like = Quote.objects.get(id = id)).delete()
    return redirect('/quotes')

def user(request, id):
    user = User.objects.get(id = id)
    quotes = Quote.objects.filter(creator = user)
    count = quotes.count()
    content = {
        "user":user,
        "quotes":quotes,
        "count":count
    }
    return render(request, "belt_3/quotepage.html", content)
