from django.db import models
from django.utils.timezone import now


class PostsQuerySet(models.QuerySet):

    def posts_published(self):
        return (self.filter(
            pub_date__lte=now(), is_published=True,
            category__is_published=True)
        )

    def posts_annotate(self):
        return (self.annotate(comment_count=models.Count('comments'))
                .select_related('category', 'author', 'location')
                .order_by('-pub_date'))
