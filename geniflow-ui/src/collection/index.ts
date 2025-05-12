// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { ResourceProps } from 'react-admin';
import LocalLibraryIcon from '@mui/icons-material/LocalLibrary';

import CollectionList from '@/collection/CollectionList';

const CollectionResourceProps: ResourceProps = {
    name: 'collections',
    list: CollectionList,
    icon: LocalLibraryIcon,
};

export {
    CollectionResourceProps,
};
