'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up (queryInterface, Sequelize) {

    await queryInterface.bulkInsert('Users', [{
      username: 'admin',
      password: '$2a$10$qgcmSwY8R4ouzPrmVCcNxeq24iRgp.461HTLXbhpMLfRAWZpWh/3m',
      createdAt: new Date(),
      updatedAt: new Date()
    }], {});
  },

  async down (queryInterface, Sequelize) {
    await queryInterface.bulkDelete('Users', null, {});
  }
};
