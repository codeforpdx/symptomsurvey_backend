const tweets = require('../seeds/tweets');

module.exports = {
  up(db) {
    return db
      .createCollection('tweets')
      .then(() => db.collection('tweets').insertMany(tweets))
      .then(() => db.collection('tweets').createIndex({text: 'text'}))
      .then(() => db.collection('tweets').createIndex({geo: '2dsphere'}));
  },

  down(db) {
    return db.collection('tweets').drop();
  }
};
