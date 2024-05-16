from django.db.models import Manager

from django.utils.timezone import now


class PostsActiveManager(Manager):
    def get_queryset(self):
        return (super().get_queryset().filter(
            pub_date__lte=now(), is_published=True,
            category__is_published=True)
            .select_related('category', 'author', 'location')
            .order_by('-pub_date')
        )


class PostTotalManager(Manager):
    def get_queryset(self):
        return (super().get_queryset()
                .select_related('category', 'author', 'location')
                .order_by('-pub_date')
                )
