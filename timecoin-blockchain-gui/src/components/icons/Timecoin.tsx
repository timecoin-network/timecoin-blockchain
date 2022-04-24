import React from 'react';
import { SvgIcon, SvgIconProps } from '@material-ui/core';
import { ReactComponent as TimecoinIcon } from './images/timecoin.svg';

export default function Keys(props: SvgIconProps) {
  return <SvgIcon component={TimecoinIcon} viewBox="0 0 58 58" {...props} />;
}
