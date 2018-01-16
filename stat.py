##
# Get following information for a period of time
# x Following
# x Follower
# - Dairy count
# - Dairy comments
# - Dairy liked
# - Dairy recommended
# - Post count
# - Post comments
# - Post repost
# - Post liked
# x Post in #topic#
# - Photo count
# - Photo comments
# - Photo liked

# TODO movie share not included

from six.moves import input
from douban_client import DoubanClient
from datetime import datetime, timedelta
import sys
import time

KEY = '022e300c79c18fc7068a90256d44af55'
SECRET = '11c8bcbac80e8085'
CALLBACK = 'http://www.douban.com'

SCOPE = 'douban_basic_common,movie_basic,movie_basic_r,community_basic_note,community_basic_user,community_basic_photo,community_basic_online,book_basic_r,music_basic_r,shuo_basic_r'
client = DoubanClient(KEY, SECRET, CALLBACK, SCOPE)

BEFORE_DAY = datetime.now() + timedelta(days=-15)
AFTER_DAY = BEFORE_DAY + timedelta(days=-15)

print client.authorize_url
code = input('Enter the verification code: ')
client.auth_with_code(code)


def get_current_user():
    return client.user.me


def get_note_list(user_id):
    return client.note.list(user_id, 0, 100)

def _get_earliest_postid(posts):
    return int(posts[len(posts)-1]['id'])


def get_posts_list(user_id, times=10):
    all_posts = []
    prev_posts = client.miniblog.user_timeline(user_id)
    all_posts.extend(prev_posts)
    for i in range(1,times):
        posts = client.miniblog.user_timeline(user_id, until_id=_get_earliest_postid(prev_posts))
        all_posts.extend(posts)
        prev_posts = posts
        time.sleep(5000)
        print "......"
    return all_posts


def get_album_list():
    return [1655677751, 1653768160, 1647100525, 1646303977, 1628760203, 1657250677]


def get_album(id):
    return client.album.get(id)


def get_photo_list():
    albums = get_album_list()
    all_photos = []
    for album in albums:
        photos = client.album.photos(album, 0, 500)
        all_photos.extend(photos['photos'])
    return all_photos


def within_15days(date_str):
    timestamp = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    if (timestamp > AFTER_DAY and timestamp <= BEFORE_DAY):
        return True
    else:
        return False


me = get_current_user()

posts = get_posts_list(me['id'], times=30)
posts_count = 0
posts_reposts_sum = 0
posts_liked_sum = 0
posts_comments_sum = 0
# print "posts len: %s" % str(len(posts))
for post in posts:
    if (within_15days(post['created_at'])):
        posts_count += 1
        posts_reposts_sum += int(post['reshared_count'])
        posts_liked_sum += int(post['like_count'])
        posts_comments_sum += int(post['comments_count'])

notes = get_note_list(me['id'])['notes']
dairy_comment_sum = 0
dairy_liked_sum = 0
dairy_recs_sum = 0
dairy_count = 0
for note in notes:
    if (within_15days(note['publish_time'])):
        dairy_comment_sum += int(note['comments_count'])
        dairy_liked_sum += int(note['liked_count'])
        dairy_recs_sum += int(note['recs_count'])
        dairy_count += 1

album_liked_sum = 0
album_recommended_sum = 0
for album_id in get_album_list():
    album = get_album(album_id)
    album_liked_sum += int(album['liked_count'])
    album_recommended_sum += int(album['recs_count'])

photos = get_photo_list()
photos_count = 0
photos_liked_sum = 0
photos_comments_sum = 0
photos_recommended_sum = 0
for photo in photos:
    if (within_15days(photo['created'])):
        photos_count += 1
        photos_liked_sum += int(photo['liked_count'])
        photos_comments_sum += int(photo['comments_count'])
        photos_recommended_sum += int(photo['recs_count'])


print "Dairy: count %s, comments %s, liked %s, recommended %s" \
      % (dairy_count, dairy_comment_sum, dairy_liked_sum, dairy_recs_sum)

print "Post: count %s, comments %s, liked %s, repost %s" \
      % (posts_count, posts_comments_sum, posts_liked_sum, posts_reposts_sum)

print "Photo: count %s, comments %s, liked %s, recommended %s" \
      % (photos_count, photos_comments_sum, photos_liked_sum, photos_recommended_sum)

print "Album: liked %s, recommended %s" % (album_liked_sum, album_recommended_sum)

print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" \
      % (dairy_count, dairy_comment_sum, dairy_liked_sum, dairy_recs_sum,
         posts_count, posts_comments_sum, posts_liked_sum, posts_reposts_sum,
         photos_count, photos_comments_sum, photos_comments_sum, photos_recommended_sum,
         album_liked_sum, album_recommended_sum)
