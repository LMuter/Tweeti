from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import StreamingHttpResponse
from django.db.models import Q
from rest_framework import viewsets
from rest_framework import permissions
from labeling.serializers import TweetSerializer
import json
import urlexpander
import tweepy
import csv
import codecs
import random
import requests
import datetime
from tweepy import OAuthHandler
from labeling.forms import DocumentForm
from labeling.models import Label, Tweet, Document


def get_shortcut_template(shortcut):
    return f'<span class="shortcut">{shortcut}</span>'


def get_label(name, shortcut=None):
    if shortcut:
        shortcut_template = get_shortcut_template(shortcut)
        replace_first_occurrence = 1
        name = name.replace(shortcut, shortcut_template, replace_first_occurrence)
    return name


def get_sub_label_list(sub_labels, color=None):
    sub_label_template_list = []
    for sub_label in sub_labels:
        c = color or sub_label.label_color
        sub_label_template_list.append(get_sub_label(sub_label.label_name,
                                                     sub_label.shortcut,
                                                     c))
    return sub_label_template_list


def get_sub_labels_context(sub_labels, parent):
    parent_name = parent.label_name.replace(" ", "-").lower()
    sub_labels = get_sub_label_list(sub_labels, parent.label_color)
    return {'parent_name': parent_name,
            'sub_labels': sub_labels, }


def get_sub_label(name, shortcut, color):
    label = get_label(name, shortcut)
    return {'label': label,
            'color': color,
            }


def get_buttons(name, shortcut, color=None):
    return {'label': get_label(name, shortcut),
            'name': name.replace(" ", "-").lower(),
            'color': f"{color}" if color else ""}


def get_labels():
    parent_labels = Label.objects.filter(parent_label=None)\
        .order_by('order', 'label_name')
    parent_labels_context = []
    sub_labels_context = []
    for parent_label in parent_labels:
        parent_labels_context.append(
            get_buttons(parent_label.label_name,
                        parent_label.shortcut,
                        parent_label.label_color))
    for p in parent_labels:
        sub_labels = Label.objects.filter(parent_label=p).order_by('order', 'label_name')
        if sub_labels:
            sub_labels_context.append(get_sub_labels_context(sub_labels, p))
    return {"parent_labels": parent_labels_context, "sub_labels": sub_labels_context}


def index(request):
    context = get_labels()
    if request.user.is_authenticated:
        context["user"] = request.user
    return render(request, 'labeling/index.html', context)


def update_labels(request):
    context = {}
    if request.user.is_authenticated:
        context["user"] = request.user.username
        post_data = json.loads(request.body.decode("utf-8"))
        tweet_id = post_data.get("tweet_id")
        # labels_new = post_data.get("labels")
        tweet = Tweet.objects.filter(id=tweet_id)
        label_json = get_label_json(tweet.first().labels_automatic)
        label_json.append({
            "data": post_data, "user": context["user"],
            "datetime": datetime.datetime.now().isoformat()})
        tweet.update(
            labels_automatic=json.dumps(label_json),
            labels_manual=json.dumps(post_data),
            updated_at=datetime.datetime.now(),
            status='final')
        context["status"] = "Labels Updated"
    else:
        context["error"] = "You do not have persmission for this action."
    return JsonResponse(context)


def exclude_tweet(request):
    context = {}
    if request.user.is_authenticated:
        post_data = json.loads(request.body.decode("utf-8"))
        tweet_id = post_data.get("tweet_id")
        Tweet.objects.filter(id=tweet_id).update(status="excluded")
        context["status"] = "Tweet " + str(tweet_id) + " excluded"
    else:
        context["error"] = "You do not have persmission for this action."
    return JsonResponse(context)


def discuss_tweet(request):
    context = {}
    if request.user.is_authenticated:
        post_data = json.loads(request.body.decode("utf-8"))
        tweet_id = post_data.get("tweet_id")
        Tweet.objects.filter(id=tweet_id).update(status="discuss")
        context["status"] = "Tweet " + str(tweet_id) + " is discussed"
    else:
        context["error"] = "You do not have persmission for this action."
    return JsonResponse(context)


def download_tweets(request):
    """A view that streams a large CSV file."""
    if not request.user.is_staff:
        raise PermissionDenied

    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    # rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    print("download view")
    queryset = get_labeled_tweets()
    rows = []

    opts = queryset.model._meta
    # model = queryset.model
    field_names = [field.name for field in opts.fields]

    rows.append(field_names)
    for obj in queryset:
        rows.append([getattr(obj, field) for field in field_names])

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse(
        (writer.writerow(row) for row in rows),
        content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="labled_tweets.csv"'
    return response


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def get_labeled_tweets():
    return Tweet.objects.filter(~Q(labels_manual="[]"))


def manual_remove_labels(request):
    if not request.user.is_staff:
        raise PermissionDenied

    queryset = get_labeled_tweets()
    context = {"tweets_updated": []}
    start_date = datetime.datetime(2000, 1, 1)
    end_date = datetime.datetime(2021, 4, 2)

    for item in queryset.iterator():
        d = datetime.datetime.strptime(
            json.loads(item.labels_automatic)[0]["datetime"],
            "%Y-%m-%dT%H:%M:%S.%f")
        if start_date < d < end_date:
            tweet = Tweet.objects.filter(id=item.id)
            new_labels = get_label_json(tweet.first().labels_manual)
            if new_labels.get("labels"):

                s = set([
                    "Not Incident Related", "Incident Related", "Corona",
                    "Riot", "Violence"])

                new_labels["labels"] = list(set(new_labels.get("labels")).difference(s))

                for k in s:
                    new_labels["selections"].pop(k, None)

                label_json = get_label_json(tweet.first().labels_automatic)
                label_json.append({
                    "data": new_labels,
                    "user": "SYSTEM",
                    "datetime": datetime.datetime.now().isoformat()})

                tweet.update(
                    labels_automatic=json.dumps(label_json),
                    labels_manual=json.dumps(new_labels),
                    updateed_at=datetime.datetime.now())

                context["tweets_updated"].append(item.id)
    return JsonResponse(context)


def upload_tweets(request):
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()
            read_csv(doc.document)
            return render(request, 'labeling/index.html', {})
    else:
        form = DocumentForm()
    return render(request, 'labeling/upload.html', {'form': form})


def get_tweet_data(request):
    context = {}
    if request.user.is_authenticated:
        try:
            tweets_default = 1
            number_of_random_tweets = parse_int(
                request.GET.get('n', tweets_default), tweets_default)
            context["tweets"] = []
            random_tweets = get_random_tweets(number_of_random_tweets)
            for random_tweet in random_tweets:
                tweet_json = {
                    "full_text": random_tweet.full_text,
                    "id": random_tweet.id,
                    "url": random_tweet.url,
                    "tweet_group": random_tweet.tweet_group,
                    "status": random_tweet.status}
                context["tweets"].append({
                    "tweet": tweet_json,
                    "labels": random_tweet.labels_manual})
        except EmptyQueryError:
            context["error"] = "No tweets in set."
    else:
        context["error"] = "You do not have persmission for this action."
    return JsonResponse(context)


def parse_int(n, default=None):
    try:
        return int(n)
    except ValueError:
        return default


def get_random_tweets(n=10):
    tweets = Tweet.objects.filter(status="full_text, active")
    if tweets:
        return tweets.order_by("?")[:n]
    raise EmptyQueryError("No tweets in set")


def errornotifier(request):
    e = request.body.decode("utf-8")
    error_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    send_mail(
        'Tweeti error',
        'Error occured at ' + error_datetime + "\n\n" + e,
        'error@tweeti.com',
        ['laurens.muter@gmail.com'],
        fail_silently=False,
    )

    context = {"message": "notification reported"}
    return JsonResponse(context)


def send_test_email(request):
    # e = request.body.decode("utf-8")

    send_mail(
        'Tweeti test',
        'test message',
        'test@tweeti.com',
        ['laurens.muter@gmail.com'],
        fail_silently=False,
    )

    context = {"message": "send test email"}
    return JsonResponse(context)


def get_label_json(label_str):
    """
    """
    if label_str:
        try:
            return json.loads(label_str)
        except json.decoder.JSONDecodeError:
            return [{"init": label_str}]
    return {}


def read_csv(csv_file):
    """
    Save file to Document location and store reference in database.

    Parameters:
        csv_file (FileField):   fileField representing document to save.
    """
    csv_reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8'), delimiter=',')
    tweet_headers = []
    base_url = "https://twitter.com/margabult/status/"
    tweet_headers = next(csv_reader)
    line_count = 0
    for row in csv_reader:
        tweet_dict = {tweet_headers[i]: v for i, v in enumerate(row)}
        id_str = tweet_dict.get('id_str')
        save_tweet(id_str=id_str, url=base_url + id_str,
                   full_text=tweet_dict.get('full_text'),
                   content=json.dumps(tweet_dict),
                   labels_manual=tweet_dict.get('labels_manual', "[]"),
                   labels_automatic=tweet_dict.get('labels_automatic', "[]"),
                   tweet_group=tweet_dict.get('tweet_group'),
                   keywords=tweet_dict.get('keywords'),
                   status=tweet_dict.get('status', "initial"),
                   )
        line_count += 1
    return f'Processed {line_count} lines.'


def filter_tweet_url(tweet_text):
    """
    Extract URL to original tweet from tweet text.

    Parameters:
        tweet_text (str):       tweet text must include an URL

    Returns:
        url (str):              url referening to original tweet
    """
    start_index = tweet_text.rfind("https://t.co/")
    # end_index = tweet_text.rfind(" ", start_index)
    return tweet_text[start_index:]


def save_label(label_name, label_group):
    """
    Create a label and store in the database.

    Parameters:
        label_name:             Name to identify label
        label_group:            Name to group labels

    Returns:
        (Label):                label object extended from Django model
    """
    return Label.objects.create(label_name=label_name, label_group=label_group)


def save_tweet(full_text, url=None, labels_manual="[]", labels_automatic="[]",
               tweet_group=None, keywords=None, content=None, id_str=None,
               status="initial"):
    """
    Store Tweet-object in database.

    Parameters:
        url (str):                url to original tweet
        full_text (str):          text-content of the tweet
        labels_manual (str):      manually added labels
        labels_automatic (str):   calculated labels
        tweet_group (str):        additional parameter to group tweets
        keywords (str):           keywords extracted from the tweet-text
        content (str):            full content of the tweet as json

    Returns:
        (Tweet): tweet object extended from Django model
    """
    return Tweet.objects.create(url=url, full_text=full_text,
                                labels_manual=labels_manual,
                                labels_automatic=labels_automatic,
                                tweet_group=tweet_group, keywords=keywords,
                                content=content, id_str=id_str,
                                status="full_text, active")


class EmptyQueryError(Exception):
    pass


class TweetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_labeled_tweets()
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]
