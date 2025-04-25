// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

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
