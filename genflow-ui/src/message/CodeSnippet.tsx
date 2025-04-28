// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

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
