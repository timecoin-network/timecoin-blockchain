import React from 'react';
import styled from 'styled-components';
import { Box, BoxProps } from '@material-ui/core';
import { Timecoin } from '@timecoin/icons';

const StyledTimecoin = styled(Timecoin)`
  max-width: 100%;
  width: auto;
  height: auto;
`;

export default function Logo(props: BoxProps) {
  return (
    <Box {...props}>
      <StyledTimecoin />
    </Box>
  );
}
