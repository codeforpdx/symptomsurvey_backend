const {database_name} = require('./constants');

const mongoHost = process.env.MONGO_HOST || 'localhost';
const mongoPort = process.env.MONGO_PORT || 27017;

module.exports = {
  mongodb: {
    // TODO: set this url in an environment variable so that it is configurable.
    url: `mongodb://${mongoHost}:${mongoPort}`,

    databaseName: database_name,

    options: {
      useNewUrlParser: true // removes a deprecation warning when connecting
    }
  },

  // The migrations dir, can be an relative or absolute path. Only edit this when really necessary.
  migrationsDir: "migrations",

  // The mongodb collection where the applied changes are stored. Only edit this when really necessary.
  changelogCollectionName: "changelog"
};
