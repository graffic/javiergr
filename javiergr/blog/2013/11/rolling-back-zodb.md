title: Rolling back a transaction in ZODB
date: 2013-11-21
category: technical
slug: rolling-back-zodb
published: true
summary: Different ways to roll back a transaction in ZODB using file
    storage.


In my case I needed this after a “bad upgrade”. I had run some model
migrations in the wrong environment and I only needed to remove those
changes from the database file (Data.fs) after rolling back the code.

I found two ways of doing it:

-   Cut the file: no python code needed but it only works if you want to
    remove the last transaction/s.
-   Create a rollback transaction: this will revert the effects of the
    transaction you want.

In any case:

-   Keep a backup of your database.
-   Shut down your web application and your ZEO server if any.

Cut the file
------------

Locate the `Data.fs` file and use `fstail` or `fsdump` to get the
location of the last transaction. Let's see this with an example of a
file with two transactions:

    :::console
    $ fsdump Data.fs
    Trans #00000 tid=03a298991c976744 time=2013-11-07 11:05:06.701114 offset=52
        status=' ' user='' description='initial database creation'
      data #00000 oid=0000000000000000 size=60 class=persistent.mapping.PersistentMapping
    Trans #00001 tid=03a298caaa5ae600 time=2013-11-07 11:54:39.926970 offset=185
        status=' ' user='' description=''
      data #00000 oid=0000000000000000 size=94 class=persistent.mapping.PersistentMapping
      data #00001 oid=0000000000000001 size=42 class=__main__.Fruit
    $ fstail Data.fs
    2013-11-07 11:54:39.926970: hash=0f95c4915219251e73bc66ccdd6bb0376ecae064
    user='' description='' length=243 offset=185

    2013-11-07 11:05:06.701114: hash=5c3a287923922c3540eb32ca95d926d52a7843da
    user='' description='initial database creation' length=150 offset=52

The important part here is the *offset*. It tells us where the
transaction data starts. There is a header that usually is *23 bytes*
but it can be longer if there is meta-data like: description, user or status.
ZODB will clean that extra header for us. Let's cut the `Data.fs` file:

    :::console
    $ head -c 185 Data.fs > NewData.fs
    $ ls -l NewData*
    -rw-r--r-- 1  hey jude 185 Nov 21 10:06 NewData.fs

Now you can rename the `NewData.fs` as `Data.fs`, delete the `Data.fs.index` to
make sure it is regenerated on restart and start your application.
Another alternative is to use python code to load the storage and make
ZODB fix the file for you. In both cases you will get the following files

    :::console
    $ ls -l NewData*
    -rw-r--r--  1 hey  jude  162 Nov 21 10:08 Data.fs
    -rw-r--r--  1 hey  jude   30 Nov 21 10:08 Data.fs.index
    -rw-r--r--  1 hey  jude    6 Nov 21 10:08 Data.fs.lock
    -rw-r--r--  1 hey  jude    0 Nov 21 10:08 Data.fs.tmp
    -rw-r--r--  1 hey  jude   23 Nov 21 10:08 Data.fs.tr0

The `tr0` file is the transaction header for the transaction we've
removed. The new file size has been adjusted from 185 bytes to 162 bytes
and the index has been generated. Now `fsdump` and `fstail` show
only one transaction:

    :::console
    $ fsdump Data.fs
    Trans #00000 tid=03a298991c976744 time=2013-11-07 11:05:06.701114 offset=52
        status=' ' user='' description='initial database creation'
      data #00000 oid=0000000000000000 size=60 class=persistent.mapping.PersistentMapping
    $ fstail NewData.fs
    2013-11-07 11:05:06.701114: hash=5c3a287923922c3540eb32ca95d926d52a7843da
    user='' description='initial database creation' length=150 offset=52

That's it but check your application just in case.

Create a rollback transaction
-----------------------------

To rollback a transaction we need to find the transaction id. But not
just the id, but the id encoded in *base64*.

If you use `fsdump` or `fstail` to locate your transaction you have
that transaction id in front of you. Using the `Data.fs` file of the
previous example. In this case I want to roll back the last transaction
that has this id `03a298caaa5ae600`:

    :::pycon
    >>> import base64
    >>> base64.b64encode('03a298caaa5ae600'.decode('hex'))
    'A6KYyqpa5gA='

If you only know that a specific object has been changed, we can get
the id from the database. We need some python here. I will be using the
previous `Data.fs` and let's say that the object changed is the root:

    :::pycon
    >>> from ZODB.FileStorage import FileStorage
    >>> from ZODB.DB import DB
    >>> storage = FileStorage('Data.fs')
    >>> db = DB(storage)
    >>> con = db.open()
    >>> db.history(con.root()._p_oid)
    [{'tid': '\x03\xa2\x98\x9b\x1f\x19e\xbb', 'time': 1383822427.288877,
      'user_name': '', 'description': '', 'size': 94}]

With this information I can get the transaction id from the `undoLog`
using the `undoInfo` method and the *time* when the object was
updated:

    :::pycon
    >>> info = db.undoInfo(specification={'time': 1383822427.288877})
    >>> info
    [{'description': '', 'size': 243, 'user_name': '', 'id': 'A6KYmx8ZZbs=',
      'time': 1383822427.288877}]
    >>> db.undo(info[0]['id'])
    >>> import transaction
    >>> transaction.get().note('Rolling back!')
    >>> transaction.commit()
    >>> db.close()
    >>> storage.close()

After committing these changes we can check the `Data.fs` file with
`fsdump` to see a new transaction that reverses the one we wanted to
rollback:

    :::console
    $ fsdump Data.fs
    Trans #00000 tid=03a298991c976744 time=2013-11-07 11:05:06.701114 offset=52
        status=' ' user='' description='initial database creation'
      data #00000 oid=0000000000000000 size=60 class=persistent.mapping.PersistentMapping
    Trans #00001 tid=03a2989b1f1965bb time=2013-11-07 11:07:07.288877 offset=185
        status=' ' user='' description=''
      data #00000 oid=0000000000000000 size=94 class=persistent.mapping.PersistentMapping
      data #00001 oid=0000000000000001 size=42 class=__main__.Fruit
    Trans #00002 tid=03a2e724b1b6af99 time=2013-11-21 10:12:41.651629 offset=449
        status=' ' user='' description='Rolling back!'
      data #00000 oid=0000000000000000 size=60 class=persistent.mapping.PersistentMapping bp=03a298991c976744
      data #00001 oid=0000000000000001 class=undo or abort of object creation

And that's all, again. If you know any other way, or you find something
wrong with this, let me know about it.

References
----------

-   The ZODB guide.
    ([link](http://www.zodb.org/en/latest/documentation/guide/transactions.html))
-   ZODB `undoInfo` method
    ([link](https://github.com/zopefoundation/ZODB/blob/6b484f8a2ce6cd627139cd6a2c8e9219ecf0ecf2/src/ZODB/UndoLogCompatible.py))
-   Wolfgang Schnerring post about undoing transactions in ZODB
    ([link](http://blog.gocept.com/2011/05/04/how-to-undo-a-transaction-with-the-zodb/))

