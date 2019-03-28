const {pbkdf2} = require('crypto');
const uuidv4 = require('uuid/v4');
const pick = require('lodash/pick');
const {salt: {iterations, key_length, algorithm}} = require('../constants');
const userSeeds = require('../seeds/users');

/**
 * makeHash
 * @param {string} password - The user's actual password.
 * @param {string} salt - The randomly generated salt.
 * @returns {Promise<String>} A promise that resolves to a hex string of the password hash
 */
const makeHash = (password, salt) => new Promise((resolve, reject) => pbkdf2(password, salt, Number(iterations), Number(key_length), algorithm, (err, result) => {
  if (err) {
    reject(err);
    return;
  }
  resolve(result.toString('hex'));
}));

const hashUserPassword = user => {
  const salt = uuidv4();
  return makeHash(user.password, salt)
    .then(hash => {
      return Object.assign(
        {},
        pick(user, ['profile', 'role']),
        {password: {
          salt,
          hash
        }}
      )
    })
}

module.exports = {
  up(db) {
    // Generate both password hashes and create the users collection.
    return db.createCollection('users')
      .then(() => Promise.all(userSeeds.map(hashUserPassword)))
      .then(users => {
        // Insert both users with the appropriate salt/passwordHash values.
        return db.collection('users').insertMany(users);
      });
  },

  down(db) {
    // Running this down script will destroy all data in the users table.
    return db.collection('users').drop();
  }
};
