# core django imports
from django.views.generic import DetailView
# third-party imports
from braces.views import LoginRequiredMixin
# imports from your apps
from .models import Student
from lookouts.models import Lookout
from trades.models import Listing, Bid, Rating


class DetailStudent(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'profile.html'
    context_object_name = 'student'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(DetailStudent, self).get_context_data(**kwargs)

        # can be done with sum & filter only solds
        def total_sales(listings):
            sales = 0
            for listing in listings:
                if listing.sold:
                    sales = sales + 1
            return sales

        # can be done with sum & filter only solds
        def total_proceeds(listings):
            proceeds = 0
            for listing in listings:
                if listing.sold:
                    try:
                        proceeds = proceeds + listing.final_price()
                    except:
                        pass
            return proceeds

        student_listings = Listing.objects.filter(seller=self.get_object().pk)

        student_ratings = Rating.objects.filter(listing__seller__user=self.get_object())
        if student_ratings:
            student_stars = [int(rating.stars) for rating in student_ratings]
            print student_stars
            average_stars = sum(student_stars)/float((len(student_stars)))
        else:
            average_stars = None
       
        context['avg_stars'] = average_stars
        context['listings'] = student_listings
        context['me'] = self.get_object().pk
        context['lookouts'] = Lookout.objects.filter(owner=self.get_object())

        context['proceeds'] = total_proceeds(student_listings)
        context['sales'] = total_sales(student_listings)

        context['bids'] = Bid.objects.filter(bidder=self.get_object())

        return context

class StudentRatings(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'ratings.html'
    context_object_name = 'student'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(StudentRatings, self).get_context_data(**kwargs)

        student_ratings = Rating.objects.filter(listing__seller__user=self.get_object())

        # copied code!
        if student_ratings:
            student_stars = [int(rating.stars) for rating in student_ratings]
            print student_stars
            average_stars = sum(student_stars)/float((len(student_stars)))
        else:
            average_stars = None
       
        context['avg_stars'] = average_stars

        context['student_ratings'] = student_ratings
        context['student_ratings_num'] = student_ratings.count()

        return context
