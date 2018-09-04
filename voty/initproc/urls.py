# ==============================================================================
# Voty initproc urls
# ==============================================================================
#
# parameters (*default)
# ------------------------------------------------------------------------------
from django.conf.urls import url
from django.views import generic
from django.utils.translation import ugettext as _
from . import views

urlpatterns = [
  url(r'^(?P<filename>(robots.txt)|(humans.txt))$', views.crawler, name='crawler'),

  # home/i18n
  url(r"^$", views.index, name="home"),

  # about (ueber) is not static
  url(r"^about/$", views.about, name="about"),
  url(r"^account/language/$", views.account_language, name="account_language"),

  # autocomplete for mass invitations  
  url(r"^user_autocomplete$", views.UserAutocomplete.as_view(), name="user_autocomplete"),

  # policies
  url(r"^policy/new$", views.policy_new, name="policy_new"),
  url(r"^policy/(?P<policy_id>\d+)(?:-(?P<slug>.*))?/$", views.policy_item, name="policy_item"),
  url(r"^policy/(?P<policy_id>\d+)(?:-(?P<slug>.*))?/edit$", views.policy_edit, name="policy_edit"),
  url(r"^policy/(?P<policy_id>\d+)(?:-(?P<slug>.*))?/ack_support$", views.policy_acknowledge_support, name="policy_acknowledge_support"),
  url(r"^policy/(?P<policy_id>\d+)(?:-(?P<slug>.*))?/rm_support$", views.policy_remove_support, name="policy_remove_support"),
  url(r"^policy/(?P<policy_id>\d+)(?:-(?P<slug>.*))?/invite/(?P<invite_type>.*)$", views.policy_invite, name="policy_invite"),
  url(r"^policy/(?P<policy_id>\d+)(?:-(?P<slug>.*))?/stage$", views.policy_stage, name="policy_stage"),
  url(r"^policy/(?P<policy_id>\d+)(?:-(?P<slug>.*))?/delete$", views.policy_delete, name="policy_delete"),
  url(r"^policy/(?P<policy_id>\d+)(?:-(?P<slug>.*))?/undelete$", views.policy_undelete, name="policy_undelete"),
  url(r"^policy/(?P<policy_id>\d+)(?:-(?P<slug>.*))?/unhide$", views.policy_unhide, name="policy_unhide"),

  # undo
  url(r'^policy/(?P<policy_id>\d+)(?:-(?P<slug>.*))?/undo/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.policy_undo, name="policy_undo"),

  # notification forward to initiative, careful, this autotranslates unfortunately
  #url(r"^initiative/(?P<init_id>\d+)/?$", views.item, name=_("initiative")),
  url(r"^initiative/(?P<init_id>\d+)/$", views.item, name=_("initiative")),

  url(r"^initiative/new$", views.new, name="initiative_new"),
  url(r"^initiative/(?P<init_id>\d+)(?:-(?P<slug>.*))?/support$", views.support, name="support"),
  url(r"^initiative/(?P<init_id>\d+)(?:-(?P<slug>.*))?/ack_support$", views.ack_support, name="ack_support"),
  url(r"^initiative/(?P<init_id>\d+)(?:-(?P<slug>.*))?/rm_support$", views.rm_support, name="rm_support"),
  url(r"^initiative/(?P<init_id>\d+)(?:-(?P<slug>.*))?/edit$", views.edit, name="edit_initiative"),
  url(r"^initiative/(?P<init_id>\d+)(?:-(?P<slug>.*))?/submit_to_committee$", views.submit_to_committee, name="submit_to_committee"),
  url(r"^initiative/(?P<init_id>\d+)(?:-(?P<slug>.*))?/new_argument$", views.new_argument, name="new_argument"),
  url(r"^initiative/(?P<init_id>\d+)(?:-(?P<slug>.*))?/new_proposal$", views.new_proposal, name="new_proposal"),
  url(r"^initiative/(?P<init_id>\d+)(?:-(?P<slug>.*))?/new_moderation$", views.moderate, name="moderate"),
  url(r"^initiative/(?P<init_id>\d+)(?:-(?P<slug>.*))?/vote$", views.vote, name="vote"),
  url(r"^initiative/(?P<init_id>\d+)(?:-(?P<slug>.*))?/reset_vote$", views.reset_vote, name="reset_vote"),
  url(r"^initiative/(?P<init_id>\d+)(?:-(?P<slug>.*))?/compare/(?P<version_id>\d+)$", views.compare, name="compare"),
  url(r"^initiative/(?P<init_id>\d+)(?:-(?P<slug>.*))?/invite/(?P<invite_type>.*)$", views.invite, name="invite"),
  url(r"^initiative/(?P<init_id>\d+)(?:-(?P<slug>.*))?/moderation/(?P<target_id>\d+)$", views.show_moderation, name="show_moderation"),
  url(r"^initiative/(?P<init_id>\d+)(?:-(?P<slug>.*))?/(?P<target_type>.*)/(?P<target_id>\d+)$", views.show_resp, name="show_resp"),
  url(r"^initiative/(?P<init_id>\d+)(?:-(?P<slug>.*))?$", views.item, name="initiative_item"),
  url(r"^comment/(?P<target_type>.*)/(?P<target_id>\d+)$", views.comment, name="comment"),
  url(r"^like/(?P<target_type>.*)/(?P<target_id>\d+)$", views.like, name="like"),
  url(r"^unlike/(?P<target_type>.*)/(?P<target_id>\d+)$", views.unlike, name="unlike")
]
