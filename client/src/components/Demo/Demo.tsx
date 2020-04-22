import React, { useState } from 'react';
import { Container } from '@material-ui/core';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import { ImagePicker } from './ImagePicker';

const useStyles = makeStyles((theme: Theme) => 
  createStyles({
    root: {
      padding: `${theme.spacing(10)}px 0px`,
      width: '100%',
    }
  })
);

export const Demo: React.FC = () => {
  const classes = useStyles();

  return (
    <Container className={classes.root}>
      <ImagePicker/>
    </Container>
  );
};