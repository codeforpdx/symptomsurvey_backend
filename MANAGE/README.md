Notes on the MANAGE directory
=============================

This manages what are called "migrations" of a mongodb.  The
idea is to create repeatable processes that are applied to
mongodb collections.  A migration might be to change the
documents of a collection.

It uses NodeJS and a package named migrate-mongo
(https://www.npmjs.com/package/migrate-mongo).  Refer to that
documentation, but take a look in the ./migrations subdirectory.
They contain three migrations that were created a long time
ago (noone on the current team understands the initial goals).

The most interesting one is the *-tweets.js script which sets
up a couple of indexes for the tweets index.
