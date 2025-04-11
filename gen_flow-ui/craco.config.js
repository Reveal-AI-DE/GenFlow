// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

const path = require(`path`);

module.exports = {
  webpack: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    },
    configure: (config) => {
      config.plugins
        .filter((plugin) => plugin.constructor.name === 'ForkTsCheckerWebpackPlugin')
        .forEach((plugin) => {
          plugin.options.typescript = plugin.options.typescript || {};
          plugin.options.typescript.memoryLimit = 4096;
        });
      return config;
    },
  },
};
