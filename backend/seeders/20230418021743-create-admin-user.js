'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up (queryInterface, Sequelize) {

    await queryInterface.bulkInsert('Users', [{
      username: 'admin',
      password: '$2y$10$JtriV.NgSfGfXRX3NouROeoPhqG2lCEHMC5M4xuWmJOj3tsJsTfry',
      createdAt: new Date(),
      updatedAt: new Date()
    }], {});
  },

  async down (queryInterface, Sequelize) {
    await queryInterface.bulkDelete('Users', null, {});
  }
};
