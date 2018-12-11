module.exports = {
  up(db) {
    return db
    .createCollection('users')
    .then(() => {
      db.collection('users').insertMany([
        {
          profile: {
            username: 'bob',
            firstName: 'Robert',
            lastName: 'Smith'
          },
          password: 'pw',
          role: 'user'
        },
        {
         profile: {
          username: 'grand_magus',
          firstName: 'Reginald',
          lastName: 'McFancypants'
         },
         password: 'superC0Mp13x',
         role: 'administrator'
        }
      ]);
    });
  },

  down(db) {
    return db.collection('users').drop();
  }
};
