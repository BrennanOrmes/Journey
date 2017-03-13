from ..models import CustomUser, Event, Vote
from django.db.models import F

def recommend_by_interest(user):
    recommendations = []
    events = Event.objects.all()
    for event in events:
        for tag in event.eventTags.all():
            if tag in user.userInterests.all() and event not in recommendations:
                recommendations.append(event)
                Vote.objects.filter(user=user).filter(event=event).update(interestScore = 1)
            elif tag in user.userInterests.all() and event in recommendations:
                Vote.objects.filter(user=user).filter(event=event).update(interestScore=F('interestScore') + 1)
    #return recommendations
    
def recommend_by_other_users(user):
    recommendations = []
    events = user.schedule.events.all()
    otherUsers = CustomUser.objects.all()
    for event in events:
        for otherUser in otherUsers:
            if event in otherUser.schedule.events.all():
                for otherEvent in otherUser.schedule.events.all():
                    if otherEvent not in user.schedule.events.all() and otherEvent not in recommendations:
                        recommendations.append(otherEvent)
                        # v = Vote(user=user, event=otherEvent, interestScore=0, othersScore=1)
                        # v.save()
                        Vote.objects.filter(user=user).filter(event=otherEvent).update(othersScore = 1)
                        # vote = 1
                        # vote.save()
                    elif otherEvent not in user.schedule.events.all() and otherEvent in recommendations:
                        Vote.objects.filter(user=user).filter(event=otherEvent).update(othersScore=F('othersScore') + 1)
                        # vote += 1
                        # vote.save()
    #return recommendations

# from django.contrib.auth.models import User
# from recommends.providers import RecommendationProvider
# from recommends.providers import recommendation_registry

# from .models import Product, Vote

# class ProductRecommendationProvider(RecommendationProvider):
#     def get_users(self):
#         return User.objects.filter(is_active=True, votes__isnull=False).distinct()

#     def get_items(self):
#         return Product.objects.all()

#     def get_ratings(self, obj):
#         return Vote.objects.filter(product=obj)

#     def get_rating_score(self, rating):
#         return rating.score

#     def get_rating_site(self, rating):
#         return rating.site

#     def get_rating_user(self, rating):
#         return rating.user

#     def get_rating_item(self, rating):
#         return rating.product

# recommendation_registry.register(Vote, [Product], ProductRecommendationProvider)

