const rolesSeeds = require('../seeds/roles');

module.exports = {
  up(db) {
    return db.createCollection('roles')
      .then(() => db.collection('roles').insertMany(rolesSeeds));
  },

  down(db) {
    return db.collection('roles').drop();
  }
};
