// lint-staged.config.js

const micromatch = require('micromatch');

function containsInPath(pattern, list) {
    return list.filter((item) => micromatch.contains(item, pattern));
}

function makePattern(extension) {
    return `**/*.${extension}`;
}

module.exports = (stagedFiles) => {
    const eslintExtensions = ['ts', 'tsx', 'js'].map(makePattern);
    const scssExtensions = ['scss'].map(makePattern);
    const eslintFiles = micromatch(stagedFiles, eslintExtensions);
    const scssFiles = micromatch(stagedFiles, scssExtensions);

    const genFowUI = containsInPath('/gen_flow-ui/', eslintFiles);

    const mapping = {};
    const commands = [];
    mapping['npx stylelint --fix '] = scssFiles.join(' ');
    mapping['yarn run precommit:gen_flow-ui '] = genFowUI.join(' ');

    for (const command of Object.keys(mapping)) {
        const files = mapping[command];
        if (files.length) {
            commands.push(`${command} ${files}`);
        }
    }

    return commands;
};