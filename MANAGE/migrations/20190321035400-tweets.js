module.exports = {
  up(db) {
    return db.createCollection('tweets');
  },

  down(db) {
    return db.collection('tweets').drop();
  }
};
