// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { ResourceProps } from 'react-admin';
import SchemaIcon from '@mui/icons-material/Schema';

import WorkflowList from '@/workflow/WorkflowList';

const WorkflowResourceProps: ResourceProps = {
    name: 'workflows',
    list: WorkflowList,
    icon: SchemaIcon,
};

export {
    WorkflowResourceProps,
};
