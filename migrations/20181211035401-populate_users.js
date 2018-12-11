const {pbkdf2} = require('crypto');
const constants = require('../constants');
const {salt_iterations, salt_key_length, salt_algorithm} = constants;

const USER_PASSWORD = 'pw';
const USER_SALT = '209880c8-df7d-4792-8eb1-08092d03f1b0';

const ADMINISTRATOR_PASSWORD = 'superC0Mp13x';
const ADMINISTRATOR_SALT = '0f3e8d68-13a0-4cef-b9f1-359862d7566a';

const makeHash = (password, salt) => new Promise((resolve, reject) => pbkdf2(password, salt, Number(salt_iterations), Number(salt_key_length), salt_algorithm, (err, result) => {
  if (err) {
    reject(err);
    return;
  }
  resolve(result.toString('hex'));
}));

module.exports = {
  up(db) {
    return Promise.all([
      makeHash(USER_PASSWORD, USER_SALT),
      makeHash(ADMINISTRATOR_PASSWORD, ADMINISTRATOR_SALT),
      db.createCollection('users')
    ]).then(([userHash, administratorHash]) => {
      db.collection('users').insertMany([
        {
          profile: {
            username: 'bob',
            firstName: 'Robert',
            lastName: 'Smith'
          },
          password: {
            salt: USER_SALT,
            hash: userHash
          },
          role: 'user'
        },
        {
         profile: {
          username: 'grand_magus',
          firstName: 'Reginald',
          lastName: 'McFancypants'
         },
         password: {
           salt: ADMINISTRATOR_SALT,
           hash: administratorHash
         },
         role: 'administrator'
        }
      ]);
    });
  },

  down(db) {
    return db.collection('users').drop();
  }
};
