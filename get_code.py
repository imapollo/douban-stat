from douban_client import DoubanClient

KEY = '022e300c79c18fc7068a90256d44af55'
SECRET = '11c8bcbac80e8085'
CALLBACK = 'http://www.douban.com'
SCOPE = 'douban_basic_common,movie_basic,movie_basic_r,community_basic_note,community_basic_user,community_basic_photo,book_basic_r,music_basic_r,shuo_basic_r'
client = DoubanClient(KEY, SECRET, CALLBACK, SCOPE)

print client.authorize_url
