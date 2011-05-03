from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import View, TemplateView
from django.http import HttpResponse, Http404
from models import Advise, Happy, Voter
import datetime


class Index(TemplateView):
    template_name = 'happyapp/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['yes'] = Happy.objects.filter(happy=True).count()
        day = datetime.datetime.now()
        day = datetime.datetime(day.year, day.month, day.day)
        context['yes_today'] = Happy.objects.filter(happy=True, day__gt=day).count()
        context['no'] = Happy.objects.filter(happy=False).count()
        context['no_today'] = Happy.objects.filter(happy=False, day__gt=day).count()
        return context

    def post(self, request):
        data = request.POST
        happy = Happy(happy=('yes' in data))
        happy.done = happy.happy
        happy.save()

        nxt = redirect(why, happy.id)
        if happy.happy:
            nxt = redirect(good_for_you)

        return nxt


class AdviseView(TemplateView):
    template_name = 'happyapp/advise.html'

    def get(self, request):
        return super(AdviseView, self).get(request)


    def get_context_data(self, **kwargs):
        context = super(AdviseView, self).get_context_data(**kwargs)
        day = datetime.datetime.now()
        day = day - datetime.timedelta(1)
        problems = Happy.objects.filter(happy=False, done=True, day__gt=day)
        context['problems'] = problems
        return context


class GoodForYou(TemplateView):
    template_name = 'happyapp/good_for_you.html'


class Why(TemplateView):
    template_name = 'happyapp/why.html'
    happy = None

    def get(self, request, happy):
        self.happy = get_object_or_404(Happy, id=happy)
        request.session['hassession'] = True
        self.sid = request.session.session_key
        return super(Why, self).get(request)

    def post(self, request, happy):
        self.happy = get_object_or_404(Happy, id=happy)
        request.session['hassession'] = True
        self.sid = request.session.session_key
        data = request.POST

        if 'reason' in data and self.happy.done:
            return Http404()

        if 'reason' in data:
            reason = data['reason']
            self.happy.reason = reason
            self.happy.done = True
            self.happy.save()

        elif 'advise' in data:
            advise = Advise(ad=data['advise'], happy=self.happy, votes=0)
            advise.save()

        return redirect(why, happy)

    def get_context_data(self, **kwargs):
        context = super(Why, self).get_context_data(**kwargs)
        context['happy'] = self.happy
        context['ads'] = ((i, i.voter_set.filter(sid=self.sid)) for i in\
                            Advise.objects.filter(happy=self.happy))
        return context


class Vote(View):

    def post(self, request, advise):
        ad = get_object_or_404(Advise, id=advise)
        sid = request.session.session_key
        v = Voter.objects.filter(ad=ad, sid=sid)
        if not v.count():
            if 'p1' in request.POST:
                ad.votes += 1
            elif 'm1' in request.POST:
                ad.votes -= 1
            ad.save()
        v = Voter(ad=ad, sid=sid)
        v.save()
        return redirect(why, ad.happy.id)


index = Index.as_view()
advise = AdviseView.as_view()
why = Why.as_view()
good_for_you = GoodForYou.as_view()
vote  = Vote.as_view()
