// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, memo} from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';

interface CodeSnippetProps {
    language: string;
    code: string;
}

const CodeSnippet: FC<CodeSnippetProps> = memo(({
    // eslint-disable-next-line react/prop-types
    language,
    // eslint-disable-next-line react/prop-types
    code,
}): JSX.Element => (
    <SyntaxHighlighter language={language}>{code}</SyntaxHighlighter>
));

export default CodeSnippet;
