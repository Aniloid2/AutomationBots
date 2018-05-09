import requests
import random
import time
import datetime
import logging
import json
import atexit
import signal
import itertools


class InstaBot:
    """
    Instagram bot v 1.0
    like_per_day=1000 - How many likes set bot in one day.

    media_max_like=10 - Don't like media (photo or video) if it have more than
    media_max_like likes.

    media_min_like=0 - Don't like media (photo or video) if it have less than
    media_min_like likes.

    tag_list = ['cat', 'car', 'dog'] - Tag list to like.

    max_like_for_one_tag=5 - Like 1 to max_like_for_one_tag times by row.

    log_mod = 0 - Log mod: log_mod = 0 log to console, log_mod = 1 log to file,
    log_mod = 2 no log.

    https://github.com/LevPasha/instabot.py
    """

    url = 'https://www.instagram.com/'
    url_tag = 'https://www.instagram.com/explore/tags/'
    url_likes = 'https://www.instagram.com/web/likes/%s/like/'
    url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
    url_comment = 'https://www.instagram.com/web/comments/%s/add/'
    url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
    url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout = 'https://www.instagram.com/accounts/logout/'

    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'

    # If instagram ban you - query return 400 error.
    error_400 = 0
    # If you have 3 in row 400 error - look like you banned.
    error_400_to_ban = 3
    # If InstaBot think you have banned - going to sleep.
    ban_sleep_time = 2*60*60

    # All counter.
    like_counter = 0
    follow_counter = 0
    unfollow_counter = 0
    comments_counter = 0

    # List of user_id, that bot follow
    bot_follow_list = []

    # Log setting.
    log_file_path = '/var/www/python/log/'
    log_file = 0

    # Other.
    media_by_tag = 0
    login_status = False

    # For new_auto_mod
    next_iteration = {"Like": 0, "Follow": 0, "Unfollow": 0, "Comments": 0}

    def __init__(self, login, password,
                like_per_day=1000,
                media_max_like=10,
                media_min_like=0,
                follow_per_day=0,
                follow_time=5*60*60,
                unfollow_per_day=0,
                comments_per_day=0,
                tag_list=['cat', 'car', 'dog'],
                max_like_for_one_tag = 5,
                log_mod = 0):

        self.time_in_day = 24*60*60
        # Like
        self.like_per_day = like_per_day
        if self.like_per_day != 0:
            self.like_delay = self.time_in_day / self.like_per_day

        # Follow
        self.follow_time = follow_time
        self.follow_per_day = follow_per_day
        if self.follow_per_day != 0:
            self.follow_delay = self.time_in_day / self.follow_per_day

        # Unfollow
        self.unfollow_per_day = unfollow_per_day
        if self.unfollow_per_day != 0:
            self.unfollow_delay = self.time_in_day / self.unfollow_per_day

        # Comment
        self.comments_per_day = comments_per_day
        if self.comments_per_day != 0:
            self.comments_delay = self.time_in_day / self.comments_per_day

        # Don't like if media have more than n likes.
        self.media_max_like = media_max_like
        # Don't like if media have less than n likes.
        self.media_min_like = media_min_like
        # Auto mod seting:
        # Default list of tag.
        self.tag_list = tag_list
        # Get random tag, from tag_list, and like (1 to n) times.
        self.max_like_for_one_tag = max_like_for_one_tag
        # log_mod 0 to console, 1 to file
        self.log_mod = log_mod

        self.s = requests.Session()
        # convert login to lower
        self.user_login = login.lower()
        self.user_password = password

        self.media_by_tag = []

        now_time = datetime.datetime.now()
        log_string = 'Insta Bot v1.0 start at %s:' %\
                     (now_time.strftime("%d.%m.%Y %H:%M"))
        self.write_log(log_string)
        self.login()

        signal.signal(signal.SIGTERM, self.cleanup)
        atexit.register(self.cleanup)

    def cleanup (self):
        # Unfollow all bot follow
        if len(self.bot_follow_list)>0:
            for f in self.bot_follow_list:
                log_string = "Try to unfollow: %s" % (f[0])
                self.write_log(log_string)
                self.unfollow(f[0])
                self.bot_follow_list.remove(f)

        # Logout
        if (self.login_status):
            self.logout()

    def login(self):
        log_string = 'Try to login by %s...' % (self.user_login)
        self.write_log(log_string)
        self.s.cookies.update ({'sessionid' : '', 'mid' : '', 'ig_pr' : '1',
                               'ig_vw' : '1920', 'csrftoken' : '',
                               's_network' : '', 'ds_user_id' : ''})
        self.login_post = {'username' : self.user_login,
                           'password' : self.user_password}
        self.s.headers.update ({'Accept-Encoding' : 'gzip, deflate',
                               'Accept-Language' : self.accept_language,
                               'Connection' : 'keep-alive',
                               'Content-Length' : '0',
                               'Host' : 'www.instagram.com',
                               'Origin' : 'https://www.instagram.com',
                               'Referer' : 'https://www.instagram.com/',
                               'User-Agent' : self.user_agent,
                               'X-Instagram-AJAX' : '1',
                               'X-Requested-With' : 'XMLHttpRequest'})
        r = self.s.get(self.url)
        self.s.headers.update({'X-CSRFToken' : r.cookies['csrftoken']})
        time.sleep(5 * random.random())
        login = self.s.post(self.url_login, data=self.login_post,
                            allow_redirects=True)
        self.s.headers.update({'X-CSRFToken' : login.cookies['csrftoken']})
        self.csrftoken = login.cookies['csrftoken']
        time.sleep(5 * random.random())

        if login.status_code == 200:
            r = self.s.get('https://www.instagram.com/')
            finder = r.text.find(self.user_login)
            if finder != -1:
                self.login_status = True
                log_string = 'Look like login by %s success!' % (self.user_login)
                self.write_log(log_string)
            else:
                self.login_status = False
                self.write_log('Login error! Check your login data!')
        else:
            self.write_log('Login error! Connection error!')

    def logout(self):
        now_time = datetime.datetime.now()
        log_string = 'Logout: likes - %i, follow - %i, unfollow - %i, comments - %i.' %\
                     (self.like_counter, self.follow_counter,
                      self.unfollow_counter, self.comments_counter)
        self.write_log(log_string)

        try:
            logout_post = {'csrfmiddlewaretoken' : self.csrftoken}
            logout = self.s.post(self.url_logout, data=logout_post)
            self.write_log("Logout success!")
            self.login_status = False
        except:
            self.write_log("Logout error!")

    def get_media_id_by_tag (self, tag):
        """ Get media ID set, by your hashtag """

        if (self.login_status):
            log_string = "Get media id by tag: %s" % (tag)
            self.write_log(log_string)
            if self.login_status == 1:
                url_tag = '%s%s%s' % (self.url_tag, tag, '/')
                try:
                    r = self.s.get(url_tag)
                    text = r.text

                    finder_text_start = ('<script type="text/javascript">'
                                         'window._sharedData = ')
                    finder_text_start_len = len(finder_text_start)-1
                    finder_text_end = ';</script>'

                    all_data_start = text.find(finder_text_start)
                    all_data_end = text.find(finder_text_end, all_data_start + 1)
                    json_str = text[(all_data_start + finder_text_start_len + 1) \
                                   : all_data_end]
                    print (json_str)
                    all_data = json.loads(json_str.encode('utf-8'))
                    print (all_data)

                    self.media_by_tag = list(all_data['entry_data']['TagPage'][0]\
                                            ['tag']['media']['nodes'])

                except Exception as e:
                    print ('error code 404:', e.args)
                    self.media_by_tag = []
                    self.write_log("Exept on get_media!")
                    time.sleep(60)
            else:
                return 0

    def like_all_exist_media (self, media_size=-1, delay=True):
        """ Like all media ID that have self.media_by_tag """

        if (self.login_status):
            if self.media_by_tag != 0:
                i=0
                for d in self.media_by_tag:
                    # Media count by this tag.
                    if media_size > 0 or media_size < 0:
                        media_size -= 1
                        l_c = self.media_by_tag[i]['likes']['count']
                        if ((l_c<=self.media_max_like and l_c>=self.media_min_like)
                            or (self.media_max_like==0 and l_c>=self.media_min_like)
                            or (self.media_min_like==0 and l_c<=self.media_max_like)
                            or (self.media_min_like==0 and self.media_max_like==0)):
                            log_string = "Try to like media: %s" %\
                                         (self.media_by_tag[i]['id'])
                            self.write_log(log_string)
                            like = self.like(self.media_by_tag[i]['id'])
                            # comment = self.comment(self.media_by_tag[i]['id'], 'Cool!')
                            # follow = self.follow(self.media_by_tag[i]["owner"]["id"])
                            if like != 0:
                                if like.status_code == 200:
                                    # Like, all ok!
                                    self.error_400 = 0
                                    self.like_counter += 1
                                    log_string = "Liked: %s. Like #%i." %\
                                                 (self.media_by_tag[i]['id'],
                                                  self.like_counter)
                                    self.write_log(log_string)
                                elif like.status_code == 400:
                                    log_string = "Not liked: %i" \
                                                  % (like.status_code)
                                    self.write_log(log_string)
                                    # Some error. If repeated - can be ban!
                                    if self.error_400 >= self.error_400_to_ban:
                                        # Look like you banned!
                                        time.sleep(self.ban_sleep_time)
                                    else:
                                        self.error_400 += 1
                                else:
                                    log_string = "Not liked: %i" \
                                                  % (like.status_code)
                                    self.write_log(log_string)
                                    return False
                                    # Some error.
                                i += 1
                                if delay:
                                    time.sleep(self.like_delay*0.9 +
                                           self.like_delay*0.2*random.random())
                                else:
                                    return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
            else:
                self.write_log("No media to like!")

    def like(self, media_id):
        """ Send http request to like media by ID """
        if (self.login_status):
            url_likes = self.url_likes % (media_id)
            try:
                like = self.s.post(url_likes)
                last_liked_media_id = media_id
            except:
                self.write_log("Exept on like!")
                like = 0
            return like

    def unlike(self, media_id):
        """ Send http request to unlike media by ID """
        if (self.login_status):
            url_unlike = self.url_unlike % (media_id)
            try:
                unlike = self.s.post(url_unlike)
            except:
                self.write_log("Exept on unlike!")
                unlike = 0
            return unlike

    def comment(self, media_id, comment_text):
        """ Send http request to comment """
        if (self.login_status):
            comment_post = {'comment_text' : comment_text}
            url_comment = self.url_comment % (media_id)
            try:
                comment = self.s.post(url_comment, data=comment_post)
                if comment.status_code == 200:
                    self.comments_counter += 1
                    log_string = 'Write: "%s". #%i.' % (comment_text, self.comments_counter)
                    self.write_log(log_string)
                return comment
            except:
                self.write_log("Exept on comment!")
        return False

    def follow(self, user_id):
        """ Send http request to follow """
        if (self.login_status):
            url_follow = self.url_follow % (user_id)
            try:
                follow = self.s.post(url_follow)
                if follow.status_code == 200:
                    self.follow_counter += 1
                    log_string = "Follow: %s #%i." % (user_id, self.follow_counter)
                    self.write_log(log_string)
                return follow
            except:
                self.write_log("Exept on follow!")
        return False

    def unfollow(self, user_id):
        """ Send http request to unfollow """
        if (self.login_status):
            url_unfollow = self.url_unfollow % (user_id)
            try:
                unfollow = self.s.post(url_unfollow)
                if unfollow.status_code == 200:
                    self.unfollow_counter += 1
                    log_string = "Unfollow: %s #%i." % (user_id, self.unfollow_counter)
                    self.write_log(log_string)
                return unfollow
            except:
                self.write_log("Exept on unfollow!")
        return False

    def auto_mod(self):
        """ Star loop, that get media ID by your tag list, and like it """
        if (self.login_status):
            while True:
                random.shuffle(self.tag_list)
                self.get_media_id_by_tag(random.choice(self.tag_list))
                self.like_all_exist_media(random.randint \
                                         (1, self.max_like_for_one_tag))

    def new_auto_mod(self):
        while True:
            # ------------------- Get media_id -------------------
            if len(self.media_by_tag) == 0:
                self.get_media_id_by_tag(random.choice(self.tag_list))
                self.this_tag_like_count = 0
                self.max_tag_like_count = random.randint(1, self.max_like_for_one_tag)
            # ------------------- Like -------------------
            self.new_auto_mod_like()
            # ------------------- Follow -------------------
            self.new_auto_mod_follow()
            # ------------------- Unfollow -------------------
            self.new_auto_mod_unfollow()
            # ------------------- Comment -------------------
            self.new_auto_mod_comments()

            # Bot iteration in 1 sec
            time.sleep(3)
            # print("Tic!")

    def new_auto_mod_like(self):
        if time.time()>self.next_iteration["Like"] and self.like_per_day!=0 \
            and len(self.media_by_tag) > 0:
            # You have media_id to like:
            if self.like_all_exist_media(media_size=1, delay=False):
                # If like go to sleep:
                self.next_iteration["Like"] = time.time() +\
                                              self.add_time(self.like_delay)
                # Count this tag likes:
                self.this_tag_like_count += 1
                if self.this_tag_like_count >= self.max_tag_like_count:
                    self.media_by_tag = [0]
            # Del first media_id
            del self.media_by_tag[0]

    def new_auto_mod_follow(self):
        if time.time()>self.next_iteration["Follow"] and \
            self.follow_per_day!=0 and len(self.media_by_tag) > 0:

            log_string = "Try to follow: %s" % (self.media_by_tag[0]["owner"]["id"])
            self.write_log(log_string)

            if self.follow(self.media_by_tag[0]["owner"]["id"]) != False:
                self.bot_follow_list.append([self.media_by_tag[0]["owner"]["id"],
                                            time.time()])
                self.next_iteration["Follow"] = time.time() +\
                                                self.add_time(self.follow_delay)

    def new_auto_mod_unfollow(self):
        if time.time()>self.next_iteration["Unfollow"] and \
            self.unfollow_per_day!=0 and len(self.bot_follow_list) > 0:
            for f in self.bot_follow_list:
                if time.time() > (f[1] + self.follow_time):

                    log_string = "Try to unfollow: %s" % (f[0])
                    self.write_log(log_string)

                    if self.unfollow(f[0]) != False:
                        self.bot_follow_list.remove(f)
                        self.next_iteration["Unfollow"] = time.time() +\
                                self.add_time(self.unfollow_delay)

    def new_auto_mod_comments(self):
        if time.time()>self.next_iteration["Comments"] and self.comments_per_day!=0 \
            and len(self.media_by_tag) > 0:

            comment_text = self.generate_comment()
            log_string = "Try to comment: %s" % (self.media_by_tag[0]['id'])
            self.write_log(log_string)
            if self.comment(self.media_by_tag[0]['id'], comment_text) != False:
                self.next_iteration["Comments"] = time.time() +\
                                              self.add_time(self.comments_delay)

    def add_time(self, time):
        """ Make some random for next iteration"""
        return time*0.9 + time*0.2*random.random()

    def generate_comment(self):
        c_list = list(itertools.product(
                                    ["this", "the", "your"],
                                    ["photo", "picture", "pic", "shot", "snapshot"],
                                    ["is", "looks", "feels", "is really"],
                                    ["great", "super", "good", "very good",
                                    "good", "wow", "WOW", "cool",
                                    "GREAT", "magnificent", "magical", "very cool",
                                    "stylish", "so stylish", "beautiful",
                                    "so beautiful", "so stylish", "so professional",
                                    "lovely", "so lovely", "very lovely",
                                    "glorious", "so glorious", "very glorious",
                                    "adorable", "excellent", "amazing"],
                                    [".", "..", "...", "!", "!!", "!!!"]))

        repl = [("  ", " "), (" .", "."), (" !", "!")]
        res = " ".join(random.choice(c_list))
        for s, r in repl:
            res = res.replace(s, r)
        return res.capitalize()

    def write_log(self, log_text):
        """ Write log by print() or logger """

        if self.log_mod == 0:
            try:
                print(log_text)
            except UnicodeEncodeError:
                print("Your text has unicode problem!")
        elif self.log_mod == 1:
            # Create log_file if not exist.
            if self.log_file == 0:
                self.log_file = 1
                now_time = datetime.datetime.now()
                self.log_full_path = '%s%s_%s.log' % (self.log_file_path,
                                     self.user_login,
                                     now_time.strftime("%d.%m.%Y_%H:%M"))
                formatter = logging.Formatter('%(asctime)s - %(name)s '
                            '- %(message)s')
                self.logger = logging.getLogger(self.user_login)
                self.hdrl = logging.FileHandler(self.log_full_path, mode='w')
                self.hdrl.setFormatter(formatter)
                self.logger.setLevel(level=logging.INFO)
                self.logger.addHandler(self.hdrl)
            # Log to log file.
            try:
                self.logger.info(log_text)
            except UnicodeEncodeError:
                print("Your text has unicode problem!")



# from instabot import InstaBot
bot = InstaBot(login="", password="",
               like_per_day=800,
               max_like_for_one_tag=5,
               follow_per_day=200,
               media_max_like = 10,
               media_min_like = 0,
               follow_time=5*60*60,
               unfollow_per_day=210,
               comments_per_day=200,
               tag_list=['money','success','motivation'],
               log_mod=0)

bot.new_auto_mod()

