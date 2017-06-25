from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils.text import slugify

from pinax.notifications.models import send as notify

from datetime import datetime, timedelta, date

from .globals import STATES, INITIATORS_COUNT, SPEED_PHASE_END
from django.db import models
import pytz

class Initiative(models.Model):

    # fallback 
    STATES = STATES 

    title = models.CharField(max_length=80)
    subtitle = models.CharField(max_length=1024, blank=True)
    state = models.CharField(max_length=1, choices=[
            (STATES.PREPARE, "preparation"),
            (STATES.INCOMING, "new arrivals"),
            (STATES.SEEKING_SUPPORT, "seeking support"),
            (STATES.DISCUSSION, "in discussion"),
            (STATES.FINAL_EDIT, "final edits"),
            (STATES.MODERATION, "with moderation team"),
            (STATES.HIDDEN, "hidden"),
            (STATES.VOTING, "is being voted on"),
            (STATES.ACCEPTED, "was accepted"),
            (STATES.REJECTED, "was rejected")
        ])

    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)


    summary = models.TextField(blank=True)
    problem = models.TextField(blank=True)
    forderung = models.TextField(blank=True)
    kosten = models.TextField(blank=True)
    fin_vorschlag = models.TextField(blank=True)
    arbeitsweise = models.TextField(blank=True)
    init_argument = models.TextField(blank=True)

    einordnung = models.CharField(max_length=50, choices=[('Einzellinitiatve','Einzelinitiative')])
    ebene = models.CharField(max_length=50, choices=[('Bund', 'Bund')])
    bereich = models.CharField(max_length=50, choices=[
                ('Mitbestimmung', 'Mitbestimmung'),
                ('Transparenz und Lobbyismus', 'Transparenz und Lobbyismus'),
                ('Demokratisches und solidarisches Europa', 'Demokratisches und solidarisches Europa'),
                ('Gerechtigkeit und Verantwortung füreinander', 'Gerechtigkeit und Verantwortung füreinander'),
                ('Vielfältige, weltoffene und inklusive Gesellschaft', 'Vielfältige, weltoffene und inklusive Gesellschaft'),
                ('Nachhaltigkeit', 'Nachhaltigkeit'),
                ('Zukunft aktiv gestalten', 'Zukunft aktiv gestalten'),
                ('(andere)', '(andere)')])

    went_public_at = models.DateField(blank=True, null=True)
    went_to_discussion_at = models.DateField(blank=True, null=True)
    went_to_voting_at = models.DateField(blank=True, null=True)
    was_closed_at = models.DateField(blank=True, null=True)

    supporters = models.ManyToManyField(User, through="Supporter")

    @property
    def slug(self):
        return slugify(self.title)


    @property
    def time_ramaining_in_phase(self):
        end_of_phase = self.end_of_this_phase

        if end_of_phase:
            return end_of_phase - datetime.today().date()

        return None

    @property
    def ready_for_next_stage(self):

        if self.state == Initiative.STATES.INCOMING:
            return self.supporting.filter(initiator=True, ack=True).count() == INITIATORS_COUNT

        if self.state == Initiative.STATES.PREPARE: #three initiators and no empty text fields
            return (self.supporting.filter(initiator=True, ack=True).count() == INITIATORS_COUNT and
                self.title and
                self.subtitle and
                self.arbeitsweise and
                self.bereich and
                self.ebene and
                self.einordnung and
                self.fin_vorschlag and
                self.forderung and
                self.init_argument and
                self.kosten and
                self.problem and
                self.summary)

        if self.state == Initiative.STATES.SEEKING_SUPPORT:
            return self.supporting.filter().count() >= self.quorum

        return False

    @property
    def end_of_this_phase(self):
        week = timedelta(days=7)
        halfyear = timedelta(days=183)

        if self.was_closed_at:
            return self.was_closed_at + halfyear # Half year later.

        if self.went_public_at:
            if self.went_public_at < SPEED_PHASE_END:
                if self.state == Initiative.STATES.SEEKING_SUPPORT:
                    if self.ready_for_next_stage:
                        return self.went_public_at + week
                    return self.went_public_at + halfyear

                elif self.state == 'd':
                    return self.went_to_discussion_at + (2 * week)

                elif self.state == 'e':
                    return self.went_to_discussion_at + (3 * week)

                elif self.state == 'v':
                    return self.went_to_voting_at + week

            else:
                if self.state == Initiative.STATES.SEEKING_SUPPORT:
                    if self.ready_for_next_stage:
                        return self.went_public_at + (2 * week)

                elif self.state == 'd':
                    return self.went_to_discussion_at + (3 * week)

                elif self.state == 'e':
                    return self.went_to_discussion_at + (5 * week)

                elif self.state == 'v':
                    return self.went_to_voting_at + (2 * week)

        return None

    @property
    def quorum(self):
        return Quorum.current_quorum()

    @property
    def show_supporters(self):
        return self.state in [self.STATES.PREPARE, self.STATES.INCOMING, self.STATES.SEEKING_SUPPORT]

    @property
    def show_debate(self):
        return self.state in [self.STATES.DISCUSSION, self.STATES.FINAL_EDIT]

    @property
    def yays(self):
        print(self.votes)
        return self.votes.filter(Vote.in_favor==True).count()

    @property
    def nays(self):
        return self.votes.filter(Vote.in_favor==False).count()

    # FIXME: cache this
    @property
    def absolute_supporters(self):
        return self.supporting.count()

    @property
    def relative_support(self):
        return self.absolute_supporters / self.quorum * 100

    @property
    def first_supporters(self):
        return self.supporting.filter(first=True)

    @property
    def public_supporters(self):
        return self.supporting.filter(public=True, first=False, initiator=False)

    @property
    def initiators(self):
        return self.supporting.filter(initiator=True)

    @property
    def custom_cls(self):
        return 'item-{} state-{} area-{}'.format(slugify(self.title),
                    slugify(self.state), slugify(self.bereich))

    def __str__(self):
        return self.title;

    def notify_moderators(self, *args, **kwargs):
        return self.notify([m.user for m in self.moderations.all()], *args, **kwargs)

    def notify_followers(self, *args, **kwargs):
        return self.notify(self.supporters.all(), *args, **kwargs)

    def notify(self, recipients, notice_type, extra_context=None, subject=None, **kwargs):
        context = extra_context or dict()
        if subject:
            kwargs['sender'] = subject
            context['target'] = self
        else:
            kwargs['sender'] = self

        notify(recipients, notice_type, context, **kwargs)


class Vote(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    initiative = models.ForeignKey(Initiative, related_name="votes")
    in_favor = models.BooleanField(default=True)

    class Meta:
        unique_together = (("user", "initiative"),)



class Quorum(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    quorum = models.IntegerField(null=0)

    @classmethod
    def current_quorum(cls):
        return cls.objects.order_by("-created_at").values("quorum").first()["quorum"]


class Supporter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    initiative = models.ForeignKey(Initiative, related_name="supporting")
    # whether this initiator has acknowledged they are
    ack = models.BooleanField(default=False)
    initiator = models.BooleanField(default=False)
    public = models.BooleanField(default=True)
    first = models.BooleanField(default=False)

    class Meta:
        unique_together = (("user", "initiative"),)



# Debating Models

class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)

    target_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_id = models.IntegerField()
    target = GenericForeignKey('target_type', 'target_id')

    text = models.CharField(max_length=500)


class Like(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    target_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_id = models.IntegerField()
    target = GenericForeignKey('target_type', 'target_id')

    class Meta:
        unique_together = (("user", "target_type", "target_id"),)


### Abstracts

class Likeable(models.Model):
    class Meta:
        abstract = True

    likes_count = models.IntegerField(default=0) # FIXME: should be updated per DB-trigger
    likes = GenericRelation(Like,
                            content_type_field='target_type',
                            object_id_field='target_id')


class Commentable(models.Model):
    class Meta:
        abstract = True

    comments_count = models.IntegerField(default=0) # FIXME: should be updated per DB-trigger
    comments = GenericRelation(Comment,
                               content_type_field='target_type',
                               object_id_field='target_id')


class Response(Likeable, Commentable):
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="%(class)ss")
    initiative = models.ForeignKey(Initiative, related_name="%(class)ss")

    class Meta:
        abstract = True

    @property
    def unique_id(self):
        return "{}-{}".format(self.type, self.id)


class Argument(Response):
    title = models.CharField(max_length=80)
    text = models.CharField(max_length=500)

    class Meta:
        abstract = True

### End of Abstract

class Proposal(Response):
    type = "proposal"
    text = models.CharField(max_length=1024)

class Pro(Argument):
    type = "pro"
    css_class = "success"
    icon = "thumb_up"

class Contra(Argument):
    type = "contra"
    css_class = "danger"
    icon = "thumb_down"


class Moderation(Response):
    type = "moderation"
    stale = models.BooleanField(default=False)
    vote = models.CharField(max_length=1, choices=[
            ('y', 'okay'),
            ('a', 'abstain'),
            ('r', 'request'),
            ('n', 'no!')
        ])
    text = models.CharField(max_length=500, blank=True)

    
    class Meta:
        unique_together = (("user", "initiative"),)