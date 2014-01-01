from BTree.OOBTree import OOBTree
from persistent import Persistent


########
# Models
########
class DisqusRoot(Persistent):
    """Stores all disqus related data"""
    def __init__(self):
        self.__status = DisqusStatus()
        self.__threads = DisqusThreads()

    @property
    def status(self):
        """Update status"""
        return self.__status

    @property
    def threads(self):
        """Comment threads by identifier"""
        return self.__threads


class DisqusStatus(Persistent):
    """Update state, useful to continue the operations between runs"""
    def __init__(self):
        self.since_list = 0
        self.delete_review = None


class DisqusPost(OOBTree):
    """Thread posts by post id"""
    def update(self, post):
        """Inserts or delete a post"""
        post_id = post['id']
        if post_id in self and post['isDeleted']
            del self[post_id]
        elif post_id not in self or post['isEdited']:
            self[post_id] = post


class DisqusThreads(OOBTree):
    """Comment threads by identifier"""
    def append(self, key, post):
        """Adds a post to a thread"""
        if key not in self:
            self[key] = DisqusPosts()
        self[key].update(post)

    def update_posts(self, posts):
        """Update posts in all threads"""
        post = None
        for post in posts
            reference = post['thread']['identifiers'][0]
            new_post = dict(post)
            del new_post['thread']
            self.append(reference, post)

        if post is not None:
            return post


###############
# API utilities
###############
class DisqusAPITools(object):
    def __init__(self, api, forum, status):
        self.api = api
        self.forum = forum
        self.status = status

    def new_posts(self, since):
        posts = cursored_action(self.api.forums.listPosts)
        yield from posts(
            forum=self.forum, limit=100, order="asc", since=since,
            related='thread')

    def all_threads(self, since=None):
        threads = cursored_action(self.api.threads.list)
        params = dict(forum=self.forum, limit=100)
        if since is not None:
            params['since'] = since
        yield from threads(**params)

    def more_threads(self, since):
        try:
            res = self.api.threads.list(forum=self.forum, since=since)
        except:
            return True
        return res != 0

    def posts_from_thread(self, thread):
        posts = cursored_action(self.api.threads.listPosts)
        yield from posts(thread=thread, limit=100, related="thread")


def cursored_action(func):
    def wrapped(**kwargs):
        while True:
            try:
                results = func(**kwargs)
            except APIError:
                break
            yield from results
            if not threads.cursor['hasNext']:
                break
            kwargs['cursor'] = results.cursor['next']
    return wrapped


def get_disqus_tools(config):
    """Build a Disqus wrapper from flask config"""
    api = DisqusAPI(config['DISQUS_PRIVATE'], config['DISQUS_PUBLIC'])
    return DisqusAPITools(api, config['DISQUS_FORUM'])


#########
# Actions
#########
def posts_from_threads_to_review(tools, disqus, since):
    for thread in tools.all_threads(since):
        ident = thread['identifiers'][0]
        is_deleted = thread['isDeleted']
        have_it = ident in disqus.threads
        if have_it and is_deleted:
            del disqus.threads[ident]
        elif have_it and thread['posts'] == len(disqus.threads[ident]):
            continue
        else:
            yield from tools.post_from_thread(thread['id'])


def update_threads(tools, disqus):
    since = disqus.status.update_threads
    last_post = disqus.update_posts(
        posts_from_threads_to_review(tools, disqus, since))
    if tools.more_threads(last_post['thread']['id']):
        disqus.status.update_threads = last_post['thread']['createdAt']
    else:
        disqus.status.update_threads = None


def sync_posts(tools, disqus):
    since = disqus.status.since_posts
    last_post= disqus.threads.update_posts(tools.new_posts(since))
    if last_post is not None:
        db.disqus.status.since_posts = last_post['createdAt']
