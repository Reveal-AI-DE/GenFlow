// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

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
