import datetime

from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact='o').order_by('due_back')

def index(req):
    # view fn for the home page of this site

    # generate counts of some main objects
    numOfBooks = Book.objects.all().count()
    numOfInstances = BookInstance.objects.all().count()

    numofInstancesAvailable = BookInstance.objects.filter(status__exact='a').count()

    numOfAuthors = Author.objects.count()

    # session implementation
    numVisits = req.session.get('numVisits', 0)
    req.session['numVisits'] = numVisits + 1
    context = {
        'numBooks': numOfBooks,
        'numInstances': numOfInstances,
        'numInstancesAvailable': numofInstancesAvailable,
        'numAuthors': numOfAuthors,
        'numVisits': numVisits,
    }
    return render(req, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

# CRUD operations for authors and books on user side
class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'dateOfDeath': '05/01/2018'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = [
        'firstName',
        'lastName',
        'dateOfBirth',
        'dateOfDeath'
    ]

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

