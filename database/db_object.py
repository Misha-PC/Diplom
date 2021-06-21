import psycopg2
from datetime import datetime
import re


class Site(object):
    """
        Site page abstraction.
    """

    columns = [         # columns
        'id',          'member_id',   'slug',
        'style',       'pattern',     'title',
        'head',        'body',        'side_bar',
        'photo1',      'photo2',      'create_date',
        'last_update', 'about2',      'about1',
        'phone',       'email',       'loc',
        'inst',        'vk1',         'vk2',
        'facebook',    'twitter',     'tiktok',
        'photo3'
    ]

    def __init__(self, site):
        """
        :param site: tuple with page info from database
        """
        if not site:
            return

        for elem in zip(self.columns, site):
            col, val = elem
            if isinstance(val, str):
                val = val.replace(':dol:', '$')
            self.__dict__.update({col: val})

    def __bool__(self):
        """
        :return: True if page is exist
        """
        if self.id:
            return True
        return False

    def __repr__(self):
        return f"Site object <id:{self.id} url:{self.slug} member:{self.member_id}>"


class User(object):
    """
        Site page abstraction.
    """
    id = None
    tg_id = None
    status = None
    subscription = None
    registration = None
    selected = None

    def __init__(self, user):
        """
        :param user: tuple with user info from database
        """
        if not user:
            return

        user_item = iter(user)

        self.id = next(user_item)
        self.tg_id = next(user_item)
        self.status = next(user_item)
        self.subscription = next(user_item)
        self.registration = next(user_item)
        self.selected = next(user_item)

    def __bool__(self):
        """
        :return: True if user is exist
        """
        if self.id:
            return True
        return False


def slugify(s):
    """
    # Generate slug from input string

    # replace all whitespace characters to '-'.
    :param s: Sting
    :return: Slug without whitespace characters.
    """
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s).lower()


class Database(object):
    connection: None
    last_response = []

    user_table = 'public.users'
    site_table = 'public.site'

    def __init__(self, **kwargs):
        self.connection = psycopg2.connect(**kwargs)

    def do_query(self, query, get_result=False):
        """

        # This function execute SQL request from database and save response if it's necessary

        :param query: SQL request from string format
        :param get_result: bool; set True if you want write response
        :return: Nothing
        """
        print("do query", query, " get_result: ", get_result)
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        if get_result:
            self.last_response = cursor.fetchall()
        cursor.close()

    @staticmethod
    def prepare_condition(json=None, **kwargs):
        """

        # This function need to transformate condition from python(dict) format to part of SQL request

        :param json:    [ { 'p1': v1, 'p2': v2, ..., 'pn': vn } ]
        :param kwargs:  [ p1= v1, p2= v2, ..., pn=vn ]
        :return: str: " WHERE p1='v1' and p2='v2' and ... and pn='vn'"
        """

        if not kwargs.items() and not json:
            return ''

        out = ''

        def add_cond(cond):
            key, val = cond
            return f" AND {key} = '{val}'"

        if kwargs.items():
            for item in kwargs.items():
                out += add_cond(item)

        if json:
            for item in json.items():
                out += add_cond(item)

        return " WHERE " + out[4:]

    def select(self, table, cond=None, **kwargs):
        """

        #   Get all matching rows from database

        :param table: database table name
        :param cond:    [ { 'p1': v1, 'p2': v2, ..., 'pn': vn } ]
        :param kwargs:  [ p1= v1, p2= v2, ..., pn=vn ]

        :return: List with all matching entries
        """
        cond = self.prepare_condition(cond, **kwargs)

        query = f'SELECT * from {table} {cond}'
        self.do_query(query, get_result=True)
        return self.last_response

    def insert(self, table, data):
        """

        #   Add new row to database

        :param table: database table name
        :param data:  { 'p1': v1, 'p2': v2, ..., 'pn': vn }
        :return: Nothing
        """
        names = ''
        values = ''
        for i in data.items():
            n, v = i
            names += f"{n}, "
            values += f"$${v}$$, "
        names = names[:-2]
        values = values[:-2]
        query = f'INSERT INTO {table} ({names}) VALUES ({values})'
        self.do_query(query)

    def delete(self, table, cond=None, **kwargs):
        """

        #   Remove row from database

        :param table: database table name
        :param cond:    [ { 'p1': v1, 'p2': v2, ..., 'pn': vn } ]
        :param kwargs:  [ p1= v1, p2= v2, ..., pn=vn ]

        :return: Nothing
        """
        query = f"DELETE FROM {table} {self.prepare_condition(cond, **kwargs)}"
        self.do_query(query)

    def update(self, table, data, cond=None, **kwargs):
        set_values = ''

        for item in data.items():
            key, val = item
            set_values += f"{key} = $${val}$$, "

        set_values = set_values[:-2]

        query = f"UPDATE {table} SET {set_values} {self.prepare_condition(cond, **kwargs)}"
        self.do_query(query)

    def get_user(self, cond=None, r=False, **kwargs):
        """

        #   Get all matching users

        :param r: row user or refactored
        :param cond:    [ { 'p1': v1, 'p2': v2, ..., 'pn': vn } ]
        :param kwargs:  [ p1= v1, p2= v2, ..., pn=vn ]

        :return: List of tuples
        """
        user = self.select(self.user_table, cond=cond, **kwargs)
        if r:
            if not user:
                return User([])

            return User(user[0])
        return user

    def create_user(self, tg_id):
        """

        #   Create new user from database.

        :param tg_id: User id from telegram
        :return: Nothing
        """

        self.insert(self.user_table, {
            "tg_id": tg_id,
            "registration": datetime.now(),
            "subscription": 0,
            "status": 0
        })

    def remove_user(self, u_id=None, tg_id=None):
        """

        #   Remove user(and his sites) from database

        :param u_id:    [id from database]
        :param tg_id:   [id from telegram]

        :return: Nothing
        """
        if not u_id:
            if not tg_id:
                return
            try:
                u_id = self.get_user(tg_id=tg_id)[0][0]
            except IndexError:
                print("user dose not exist")

        self.delete(self.user_table, id=u_id)

    def set_user_status(self, status, u_id=None, tg_id=None):
        """

        #   Set new chat status

        #   Need to parsing text message from user

        :param status: new status
        :param u_id:   [id from database]
        :param tg_id:  [id from telegram]

        :return: Nothing
        """
        if not u_id:
            if not tg_id:
                return
            try:
                u_id = self.get_user(tg_id=tg_id)[0][0]
            except IndexError:
                print("user dose not exist")
        self.update(self.user_table, {'status': status}, id=u_id)

    def user(self, f):
        """

        #   This decorator need to telegram message handlers

        #   def handler(message) ---> def handler(message, user)

        """
        def decorator(message=None):
            user = self.get_user(tg_id=message.chat.id, r=True)
            if not user:
                self.create_user(message.chat.id)
                user = self.get_user(tg_id=message.chat.id, r=True)

            if user:
                return f(message, user)
            else:
                print(f"{message.chat.id} is not exist!")
                return f(message, tuple())
        return decorator

    def user_is_not_exist(self, f):
        """

        #   This decorator check user from database

        #   def handler(message) ---> def handler(message, exist)

        """

        def decorator(message=None):
            user = self.get_user(tg_id=message.chat.id)
            if not user:
                f(message, True)
            else:
                f(message, False)
                print(f"{message.chat.id} is exist!")
        return decorator

    def get_user_status_code(self, f):
        """

        #   This decorator add user status code to handler

        #   def handler(message) ---> def handler(message, status_code)

        """
        def decorator(message=None):
            user = self.get_user(tg_id=message.chat.id)
            f(message, user[2])
        return decorator

    def get_site(self, url=None, u_id=None, site_id=None, **kwargs):
        """

        #   Get raw data from database

        :param url:     [str(url)]
        :param u_id:    [str(member_id)]
        :param site_id: [str(site_id)]
        :param kwargs:  [ p1= v1, p2= v2, ..., pn=vn ]

        :return:    List of tuple
        """
        cond = {}
        if url:
            cond.update({'slug': url})
        if u_id:
            cond.update({'member_id': u_id})
        if site_id:
            cond.update({'id': site_id})

        try:
            return Site(self.select(self.site_table, cond=cond, **kwargs)[0])
        except IndexError:
            return Site([])

    def select_site(self, u_id, s_id):
        """

        #   Update row from user table, set new selected site id

        :param u_id: user id from database
        :param s_id: site id from database

        :return: Nothing
        """
        self.update(self.user_table, {'selected': s_id}, id=u_id)

    @staticmethod
    def refactor_site_object(site):
        """
        #   deprecated
        """
        if not site:
            return {}

        s_iter = iter(site)

        return {
            'id': next(s_iter),
            'member': next(s_iter),
            'url': next(s_iter),
            'style': next(s_iter),
            'pattern': next(s_iter),
            'title': next(s_iter),
            'head': next(s_iter),
            'body': next(s_iter),
            'side_bar': next(s_iter),
            'photo1': next(s_iter),
            'photo2': next(s_iter),
            'create': next(s_iter),
            'last_update': next(s_iter)
        }

    def site(self, f):
        """

        #   This decorator need to get site from slug

        :param f:
        :return: function
        """
        def decorator(url=None):
            print("decorator url:", url)
            if not url:
                return f(False)
            site = self.get_site(url=url)
            return f(site)
        return decorator

    def get_all_sites(self, u_id):
        """

        #   Get all user sites

        :param u_id: user id from database
        :return: list of Site object
        """
        sites = self.select(self.site_table, member_id=u_id)
        # sites = self.get_site(u_id=u_id)
        out = []
        for site in sites:
            out.append(Site(site))
        return out

    def new_site(self, member, title):
        """

        #   create new site and save to database

        :param member: user id from database
        :param title:   site title
        :return:    Site object
        """

        slug = slugify(title)
        slug_count = len(self.select(self.site_table, slug=slug))

        while slug_count > 0:
            slug += '-'
            slug_count = len(self.select(self.site_table, slug=slug))

        data = {
            'member_id': member,
            'title': title,
            'slug': slug,
            # 'create': datetime.now(),
            'last_update': datetime.now()
        }

        self.insert(self.site_table, data)

        return self.get_site(member_id=member, title=title, slug=slug, last_update=data['last_update'])

    def update_site_data(self, site_id, **kwargs):
        self.update(self.site_table, kwargs, id=site_id)

    def remove_site(self, site_id):
        self.delete(self.site_table, id=site_id)